DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'iom_db',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '172.21.0.2',
        'PORT': '5432',
    }
}

LOGIN_REDIRECT_URL = 'dashboard/home/'

