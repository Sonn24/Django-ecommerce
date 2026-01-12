from .base import *
import os
from decouple import config

# ------------------------------------------------------------------
# CORE SETTINGS
# ------------------------------------------------------------------

DEBUG = False

ALLOWED_HOSTS = [
    '.onrender.com',
]

# ------------------------------------------------------------------
# INSTALLED APPS
# ------------------------------------------------------------------

# ❌ Do NOT load debug_toolbar on Render
# Keep development.py clean for deployment

# INSTALLED_APPS += []


# ------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------

# ❌ Do NOT enable debug toolbar middleware
# MIDDLEWARE += []


# ------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------
# SQLite is OK for initial deployment
# (We will move to Postgres later)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------------------------------
# STRIPE (keep test keys for now)
# ------------------------------------------------------------------

STRIPE_PUBLIC_KEY = config('STRIPE_TEST_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY', default='')
