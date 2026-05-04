import os
from pathlib import Path

# Loyiha yo'li
BASE_DIR = Path(__file__).resolve().parent.parent

# Xavfsizlik kaliti (Ochiq qoldirishingiz mumkin, lekin loyihada maxfiy bo'lishi kerak)
SECRET_KEY = 'django-insecure-zvty3(oo*6fwwl!9akskv%7j7x3j&^o2@-h*8r4_07p*(0cqxl'

# Render-da ishlashi uchun DEBUG False bo'lishi tavsiya etiladi
DEBUG = True

# RENDER VA LOCAL HOSTLAR
ALLOWED_HOSTS = ['://onrender.com', 'localhost', '127.0.0.1', '.onrender.com']

# ILOVALAR
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # CSS uchun qo'shildi
    'django.contrib.staticfiles',
    'app', 
]

# MIDDLEWARE (WhiteNoise qo'shildi)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # SHU QATOR MUHIM!
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# MA'LUMOTLAR BAZASI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# TIL VA VAQT
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# --- STATIC VA MEDIA SOZLAMALARI ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Render uchun static fayllarni siqish va keshdan foydalanish
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- LOGIN/LOGOUT ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'

# --- GMAIL SMTP SOZLAMALARI ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '://gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'shastik595@gmail.com'
EMAIL_HOST_PASSWORD = 'brjldehchcoketxn' 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Avtomatik ID turi
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
