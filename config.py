import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration class for the Flask application"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # File Upload Configuration
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 50 * 1024 * 1024))  # 50MB default
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Server Configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Data Processing Configuration
    OUTLIER_DETECTION_METHOD = os.environ.get('OUTLIER_METHOD', 'iqr')  # 'iqr' or 'zscore'
    Z_SCORE_THRESHOLD = float(os.environ.get('Z_SCORE_THRESHOLD', 3.0))
    IQR_MULTIPLIER = float(os.environ.get('IQR_MULTIPLIER', 1.5))
    
    # Chart Configuration
    HISTOGRAM_BINS = int(os.environ.get('HISTOGRAM_BINS', 30))
    CHART_HEIGHT = int(os.environ.get('CHART_HEIGHT', 500))
    
    @staticmethod
    def init_app(app):
        """Initialize configuration with Flask app"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 