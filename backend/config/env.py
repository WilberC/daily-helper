"""
Environment configuration module.
Loads environment variables from .env file and provides typed access.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')


def get_bool(key: str, default: str = 'False') -> bool:
    """Get boolean environment variable."""
    return os.getenv(key, default).lower() in ('true', '1', 'yes', 'on')


def get_int(key: str) -> int:
    """Get integer environment variable."""
    return int(os.getenv(key))


def get_list(key: str, default: str = 'val-not-found-at-env', separator: str = ',') -> list[str]:
    """Get list environment variable (comma-separated by default)."""
    value = os.getenv(key, default)
    return [item.strip() for item in value.split(separator) if item.strip()]


# ==============================================
# Django Core Settings
# ==============================================

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = get_bool('DEBUG', 'True')

ALLOWED_HOSTS = get_list('ALLOWED_HOSTS')

# ==============================================
# Database Configuration
# ==============================================

DATABASE_URL = os.getenv('DATABASE_URL')

# ==============================================
# Session Configuration
# ==============================================

SESSION_COOKIE_AGE = get_int('SESSION_COOKIE_AGE')

SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE')

SESSION_COOKIE_SECURE = get_bool('SESSION_COOKIE_SECURE')

# ==============================================
# CORS Configuration
# ==============================================

CORS_ALLOWED_ORIGINS = get_list('CORS_ALLOWED_ORIGINS')

FRONTEND_URL = os.getenv('FRONTEND_URL')
