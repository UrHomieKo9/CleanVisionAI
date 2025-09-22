import os
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.utils
import json
import numpy as np
from scipy import stats
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
import openai
from io import StringIO
import tempfile

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# OpenAI API configuration (set your API key in environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY')

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_data(df):
    """Clean the dataset by handling missing values, duplicates, and column names"""
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Clean column names (remove spaces, special characters)
    df_clean.columns = df_clean.columns.str.strip().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '')
    
    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    for col in df_clean.columns:
        if df_clean[col].dtype in ['int64', 'float64']:
            # For numerical columns, fill with median
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
        else:
            # For categorical columns, fill with mode
            mode_val = df_clean[col].mode()
            if len(mode_val) > 0:
                df_clean[col] = df_clean[col].fillna(mode_val[0])
            else:
                df_clean[col] = df_clean[col].fillna('Unknown')
    
    return df_clean

def detect_outliers(df, method='iqr'):
    """Detect outliers using IQR or Z-score method"""
    outliers = {}
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numerical_cols:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers[col] = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            outliers[col] = df[col][z_scores > 3]
    
    return outliers

def generate_eda_report(df, outliers):
    """Generate comprehensive EDA report"""
    report = {}
    
    # Basic info
    report['shape'] = df.shape
    report['columns'] = list(df.columns)
    report['dtypes'] = df.dtypes.to_dict()
    
    # Missing values
    report['missing_values'] = df.isnull().sum().to_dict()
    
    # Descriptive statistics
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 0:
        report['descriptive_stats'] = df[numerical_cols].describe().to_dict()
    else:
        report['descriptive_stats'] = {}
    
    # Outlier summary
    report['outlier_summary'] = {}
    for col, outlier_data in outliers.items():
        report['outlier_summary'][col] = {
            'count': len(outlier_data),
            'percentage': (len(outlier_data) / len(df)) * 100
        }
    
    # Correlation matrix (only for numerical columns)
    if len(numerical_cols) > 1:
        correlation_matrix = df[numerical_cols].corr()
        report['correlation'] = correlation_matrix.to_dict()
    else:
        report['correlation'] = {}
    
    return report

def create_plots(df, outliers):
    """Create interactive Plotly visualizations"""
    plots = {}
    
    # Correlation heatmap
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 1:
        correlation_matrix = df[numerical_cols].corr()
        fig_heatmap = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap"
        )
        plots['correlation_heatmap'] = json.dumps(fig_heatmap, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Histograms for numerical columns
    histograms = {}
    for col in numerical_cols:
        fig_hist = px.histogram(
            df, 
            x=col, 
            title=f"Distribution of {col}",
            nbins=30
        )
        histograms[col] = json.dumps(fig_hist, cls=plotly.utils.PlotlyJSONEncoder)
    plots['histograms'] = histograms
    
    # Box plots for outlier visualization
    boxplots = {}
    for col in numerical_cols:
        fig_box = px.box(
            df, 
            y=col, 
            title=f"Box Plot of {col} (with outliers)"
        )
        boxplots[col] = json.dumps(fig_box, cls=plotly.utils.PlotlyJSONEncoder)
    plots['boxplots'] = boxplots
    
    return plots

def generate_ai_insights(df, report, outliers):
    """Generate AI-powered insights using OpenAI GPT API"""
    try:
        if not openai.api_key:
            return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        # Prepare context for GPT
        context = f"""
        Dataset Summary:
        - Shape: {report['shape']}
        - Columns: {', '.join(report['columns'])}
        - Missing values: {sum(report['missing_values'].values())} total
        - Outliers detected: {sum(len(outliers.get(col, [])) for col in outliers)}
        
        Key Statistics:
        {json.dumps(report['descriptive_stats'], indent=2)}
        
        Please provide a brief, insightful analysis of this dataset highlighting:
        1. Key patterns or trends
        2. Potential data quality issues
        3. Notable outliers or anomalies
        4. Recommendations for further analysis
        Keep the response under 200 words and focus on actionable insights.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data analyst expert. Provide clear, concise insights about datasets."},
                {"role": "user", "content": context}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error generating AI insights: {str(e)}"

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process uploaded CSV file and generate analysis"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        
        # Check if file name is empty
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        # Check file extension
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload a CSV file.', 'error')
            return redirect(url_for('index'))
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            flash('File too large. Maximum size is 50MB.', 'error')
            return redirect(url_for('index'))
        
        # Read CSV file
        try:
            df = pd.read_csv(file)
        except Exception as e:
            flash(f'Error reading CSV file: {str(e)}', 'error')
            return redirect(url_for('index'))
        
        # Check if dataframe is empty
        if df.empty:
            flash('The uploaded file is empty.', 'error')
            return redirect(url_for('index'))
        
        # Clean the data
        df_clean = clean_data(df)
        
        # Detect outliers
        outliers = detect_outliers(df_clean)
        
        # Generate EDA report
        report = generate_eda_report(df_clean, outliers)
        
        # Create plots
        plots = create_plots(df_clean, outliers)
        
        # Generate AI insights
        ai_insights = generate_ai_insights(df_clean, report, outliers)
        
        # Save cleaned data to temporary file for download
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        df_clean.to_csv(temp_file.name, index=False)
        temp_file.close()
        
        return render_template('results.html',
                             original_data=df.head(10).to_html(classes='table table-striped', index=False),
                             cleaned_data=df_clean.head(10).to_html(classes='table table-striped', index=False),
                             report=report,
                             plots=plots,
                             outliers=outliers,
                             ai_insights=ai_insights,
                             download_path=temp_file.name,
                             original_shape=df.shape,
                             cleaned_shape=df_clean.shape)
    
    except Exception as e:
        flash(f'An error occurred during analysis: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download the cleaned CSV file"""
    try:
        return send_file(filename, as_attachment=True, download_name='cleaned_data.csv')
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File too large. Maximum size is 50MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 