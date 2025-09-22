#!/usr/bin/env python3
"""
Demo script for the AI-Powered CSV Analysis App
This script demonstrates the core functionality without running the web server
"""

import pandas as pd
import numpy as np
from app import clean_data, detect_outliers, generate_eda_report, create_plots

def main():
    """Demonstrate the core functionality of the CSV analysis app"""
    
    print("🚀 AI-Powered CSV Analysis App - Demo Mode")
    print("=" * 50)
    
    # Create sample data with various data quality issues
    print("\n📊 Creating sample dataset with data quality issues...")
    
    # Generate sample data
    np.random.seed(42)
    n_samples = 100
    
    data = {
        'Employee_ID': range(1, n_samples + 1),
        'Name': [f"Employee_{i}" for i in range(1, n_samples + 1)],
        'Age': np.random.normal(35, 10, n_samples).astype(int),
        'Salary': np.random.normal(60000, 15000, n_samples).astype(int),
        'Department': np.random.choice(['Engineering', 'Marketing', 'Sales', 'HR'], n_samples),
        'Experience_Years': np.random.poisson(5, n_samples),
        'Performance_Score': np.random.normal(80, 10, n_samples),
        'Projects_Completed': np.random.poisson(8, n_samples)
    }
    
    # Add some data quality issues
    df = pd.DataFrame(data)
    
    # Add missing values
    df.loc[10:15, 'Age'] = np.nan
    df.loc[20:25, 'Salary'] = np.nan
    df.loc[30:35, 'Department'] = np.nan
    
    # Add duplicates
    df = pd.concat([df, df.iloc[0:3]], ignore_index=True)
    
    # Add outliers
    df.loc[95, 'Salary'] = 200000  # Very high salary
    df.loc[96, 'Age'] = 18  # Very young
    df.loc[97, 'Performance_Score'] = 120  # Very high score
    
    print(f"✅ Created dataset with {df.shape[0]} rows and {df.shape[1]} columns")
    print(f"📈 Missing values: {df.isnull().sum().sum()}")
    print(f"🔄 Duplicates: {df.duplicated().sum()}")
    
    # Step 1: Data Cleaning
    print("\n🧹 Step 1: Data Cleaning")
    print("-" * 30)
    
    df_clean = clean_data(df)
    
    print(f"✅ Data cleaned successfully!")
    print(f"📊 Original shape: {df.shape}")
    print(f"✨ Cleaned shape: {df_clean.shape}")
    print(f"🧹 Missing values after cleaning: {df_clean.isnull().sum().sum()}")
    print(f"🔄 Duplicates after cleaning: {df_clean.duplicated().sum()}")
    
    # Step 2: Outlier Detection
    print("\n🔍 Step 2: Outlier Detection")
    print("-" * 30)
    
    outliers = detect_outliers(df_clean, method='iqr')
    
    print(f"✅ Outliers detected using IQR method:")
    for col, outlier_data in outliers.items():
        if len(outlier_data) > 0:
            print(f"   📊 {col}: {len(outlier_data)} outliers ({len(outlier_data)/len(df_clean)*100:.1f}%)")
    
    # Step 3: EDA Report Generation
    print("\n📋 Step 3: EDA Report Generation")
    print("-" * 30)
    
    report = generate_eda_report(df_clean, outliers)
    
    print(f"✅ EDA report generated successfully!")
    print(f"📊 Dataset shape: {report['shape']}")
    print(f"📝 Columns: {', '.join(report['columns'])}")
    print(f"🔢 Data types: {len(report['dtypes'])} columns")
    print(f"📈 Descriptive stats: {len(report['descriptive_stats'])} numerical columns")
    print(f"🔥 Correlation matrix: {'Yes' if report['correlation'] else 'No'}")
    
    # Step 4: Visualization Creation
    print("\n📊 Step 4: Visualization Creation")
    print("-" * 30)
    
    plots = create_plots(df_clean, outliers)
    
    print(f"✅ Visualizations created successfully!")
    print(f"🔥 Correlation heatmap: {'Yes' if plots.get('correlation_heatmap') else 'No'}")
    print(f"📊 Histograms: {len(plots.get('histograms', {}))} charts")
    print(f"📦 Box plots: {len(plots.get('boxplots', {}))} charts")
    
    # Summary
    print("\n🎉 Demo Completed Successfully!")
    print("=" * 50)
    print("✅ Data cleaning: Working")
    print("✅ Outlier detection: Working")
    print("✅ EDA report generation: Working")
    print("✅ Visualization creation: Working")
    print("\n🚀 The application is ready to use!")
    print("💡 Run 'python app.py' to start the web server")
    print("🌐 Open http://localhost:5000 in your browser")

if __name__ == "__main__":
    main() 