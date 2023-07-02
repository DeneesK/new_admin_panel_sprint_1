import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

include(
    'components/database.py',
    'components/middleware.py',
    'components/templates.py',
    'components/validators.py',
    'components/locales.py',
    'components/installed_apps.py',
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
