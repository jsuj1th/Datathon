import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    
    # Application Settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 50000000))
    
    # Dual-LLM Verification
    ENABLE_DUAL_LLM = os.getenv('ENABLE_DUAL_LLM', 'false').lower() == 'true'
    VERIFICATION_MODEL = os.getenv('VERIFICATION_MODEL', 'openai/gpt-4o-mini')  # Faster/cheaper for verification
    
    # Classification Categories
    CATEGORIES = {
        'highly_sensitive': 'Highly Sensitive',
        'confidential': 'Confidential',
        'public': 'Public',
        'unsafe': 'Unsafe'
    }
    
    # Allowed Extensions
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}
    
    # Pre-processing Thresholds
    MIN_IMAGE_QUALITY = 0.3
    MAX_PAGES = 1000
    MAX_IMAGES = 500
