# AI-Powered CSV Data Cleaning & EDA Report Generation

A comprehensive Flask web application that automatically cleans CSV data, performs Exploratory Data Analysis (EDA), and generates AI-powered insights using OpenAI's GPT API.

## 🚀 Features

### Core Functionality
- **Smart Data Cleaning**: Automatically handles missing values, removes duplicates, and cleans column names
- **Outlier Detection**: Uses IQR and Z-score methods to identify and flag outliers
- **Comprehensive EDA**: Generates detailed reports including data types, missing values, and descriptive statistics
- **Interactive Visualizations**: Creates beautiful charts using Plotly (correlation heatmaps, histograms, box plots)
- **AI-Powered Insights**: GPT API provides narrative analysis and recommendations
- **Data Download**: Cleaned CSV available for download

### Technical Features
- **Large File Support**: Handles CSV files up to 50MB
- **Responsive Design**: Modern Bootstrap-based UI with drag-and-drop file upload
- **Real-time Processing**: Efficient data processing with progress indicators
- **Modular Architecture**: Clean, maintainable code structure

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Data Processing**: Pandas 2.1.1, NumPy 1.24.3, SciPy 1.11.3
- **Visualization**: Plotly 5.17.0
- **AI Integration**: OpenAI GPT API
- **Frontend**: HTML5, Bootstrap 5.3.0, JavaScript
- **Styling**: Custom CSS with modern gradients and animations

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (for AI insights feature)
- Modern web browser with JavaScript enabled

## 🚀 Installation

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd csv-analysis-app

# Or simply download and extract the ZIP file
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set OpenAI API Key
```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# macOS/Linux
export OPENAI_API_KEY=your_api_key_here

# Or create a .env file in the project root:
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 5. Run the Application
```bash
python app.py
```

The application will start at `http://localhost:5000`

## 📖 Usage Guide

### 1. Upload CSV File
- Navigate to the application in your browser
- Drag and drop a CSV file or click to browse
- Supported format: CSV files only
- Maximum size: 50MB

### 2. Automatic Analysis
The application will automatically:
- Clean your data (handle missing values, remove duplicates)
- Detect outliers using statistical methods
- Generate comprehensive EDA reports
- Create interactive visualizations
- Provide AI-powered insights

### 3. Review Results
- **Overview Tab**: Dataset summary and data quality issues
- **Data Preview Tab**: Compare original vs. cleaned data
- **Visualizations Tab**: Interactive charts and graphs
- **Statistics Tab**: Detailed numerical analysis

### 4. Download Cleaned Data
- Click the "Download Cleaned Data" button
- Get your processed CSV file ready for further analysis

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for AI insights
- `FLASK_ENV`: Set to 'production' for production deployment
- `FLASK_DEBUG`: Set to 'False' for production

### Customization Options
- Modify `MAX_FILE_SIZE` in `app.py` to change file size limit
- Adjust outlier detection methods in the `detect_outliers()` function
- Customize data cleaning logic in the `clean_data()` function

## 📊 Data Processing Details

### Data Cleaning
- **Column Names**: Removes spaces and special characters
- **Missing Values**: 
  - Numerical columns: Filled with median
  - Categorical columns: Filled with mode
- **Duplicates**: Automatically removed
- **Data Types**: Preserved and optimized

### Outlier Detection
- **IQR Method**: Q1 - 1.5×IQR to Q3 + 1.5×IQR
- **Z-Score Method**: Values beyond ±3 standard deviations
- **Configurable**: Easy to modify detection thresholds

### EDA Report Generation
- Dataset shape and memory usage
- Column data types and missing value counts
- Descriptive statistics (mean, median, std, min, max, quartiles)
- Correlation analysis for numerical columns
- Outlier summary with counts and percentages

## 🎨 UI Features

### Modern Design
- Gradient backgrounds and smooth animations
- Responsive layout for all device sizes
- Interactive elements with hover effects
- Professional color scheme and typography

### User Experience
- Drag-and-drop file upload
- Real-time progress indicators
- Tabbed interface for organized results
- Mobile-friendly responsive design

## 🔒 Security Features

- File type validation (CSV only)
- File size limits (50MB max)
- Secure file handling with temporary storage
- Input sanitization and error handling

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📁 Project Structure

```
csv-analysis-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html       # Main upload page
│   └── results.html     # Analysis results page
├── static/              # Static assets
│   └── style.css        # Custom styles
└── uploads/             # Upload directory (auto-created)
```

## 🐛 Troubleshooting

### Common Issues

**1. OpenAI API Key Error**
```
Error generating AI insights: No API key provided
```
**Solution**: Set your `OPENAI_API_KEY` environment variable

**2. File Upload Errors**
```
Error reading CSV file: [Errno 2] No such file or directory
```
**Solution**: Ensure the file is a valid CSV and not corrupted

**3. Memory Issues with Large Files**
```
MemoryError: Unable to allocate array
```
**Solution**: Reduce file size or increase system memory

**4. Plotly Charts Not Rendering**
```
Plotly is not defined
```
**Solution**: Check internet connection for CDN access

### Performance Tips
- For very large files (>10MB), consider chunked processing
- Use SSD storage for better I/O performance
- Monitor memory usage during processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask team for the excellent web framework
- Pandas team for powerful data manipulation tools
- Plotly team for beautiful interactive visualizations
- OpenAI for GPT API integration
- Bootstrap team for responsive UI components

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the code comments for implementation details

---

**Happy Data Analysis! 🎉📊** 