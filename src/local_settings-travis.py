
DEBUG = True
COMPRESS_ENABLED = True
THUMBNAIL_DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "1234"
NEVERCACHE_KEY = "1234"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db"
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

PICASA_USER = 'user'
PICASA_PASSWORD = 'password'

INTERNAL_IPS = ('192.168.33.1')
