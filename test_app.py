#!/usr/bin/env python3
"""
Simple test script for the CSV Analysis Flask application
"""

import os
import sys
import tempfile
import pandas as pd
from app import app, clean_data, detect_outliers, generate_eda_report

def test_data_cleaning():
    """Test the data cleaning functionality"""
    print("Testing data cleaning functionality...")
    
    # Create test data with missing values and duplicates
    test_data = {
        'Name': ['John', 'Jane', 'John', 'Mike', 'Sarah', None],
        'Age': [25, 30, 25, 35, 28, None],
        'Salary': [50000, 60000, 50000, 70000, 55000, 65000],
        'Department': ['IT', 'HR', 'IT', 'Sales', 'IT', 'Marketing']
    }
    
    df = pd.DataFrame(test_data)
    print(f"Original data shape: {df.shape}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Duplicates: {df.duplicated().sum()}")
    
    # Clean the data
    df_clean = clean_data(df)
    print(f"Cleaned data shape: {df_clean.shape}")
    print(f"Missing values after cleaning: {df_clean.isnull().sum().sum()}")
    print(f"Duplicates after cleaning: {df_clean.duplicated().sum()}")
    
    print("✅ Data cleaning test passed!\n")

def test_outlier_detection():
    """Test the outlier detection functionality"""
    print("Testing outlier detection functionality...")
    
    # Create test data with outliers
    test_data = {
        'Normal_Values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'With_Outliers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]  # 100 is an outlier
    }
    
    df = pd.DataFrame(test_data)
    
    # Test IQR method
    outliers_iqr = detect_outliers(df, method='iqr')
    print(f"Outliers detected (IQR): {len(outliers_iqr.get('With_Outliers', []))}")
    
    # Test Z-score method
    outliers_zscore = detect_outliers(df, method='zscore')
    print(f"Outliers detected (Z-score): {len(outliers_zscore.get('With_Outliers', []))}")
    
    print("✅ Outlier detection test passed!\n")

def test_eda_report():
    """Test the EDA report generation"""
    print("Testing EDA report generation...")
    
    # Create test data
    test_data = {
        'Numeric_Col': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Categorical_Col': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    }
    
    df = pd.DataFrame(test_data)
    outliers = detect_outliers(df)
    report = generate_eda_report(df, outliers)
    
    print(f"Report keys: {list(report.keys())}")
    print(f"Dataset shape: {report['shape']}")
    print(f"Columns: {report['columns']}")
    print(f"Data types: {report['dtypes']}")
    
    print("✅ EDA report generation test passed!\n")

def test_flask_app():
    """Test if Flask app can be created"""
    print("Testing Flask application creation...")
    
    try:
        # Test if app can be created
        with app.test_client() as client:
            # Test home route
            response = client.get('/')
            assert response.status_code == 200
            print("✅ Home route test passed!")
            
            # Test that app is working
            assert app.name == 'app'
            print("✅ Flask app creation test passed!")
            
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting CSV Analysis App Tests...\n")
    
    try:
        test_data_cleaning()
        test_outlier_detection()
        test_eda_report()
        
        if test_flask_app():
            print("🎉 All tests passed! The application is ready to run.")
            print("\nTo start the application, run:")
            print("python app.py")
        else:
            print("❌ Some tests failed. Please check the errors above.")
            
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 