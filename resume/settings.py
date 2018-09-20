
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zp5a6f3m0mn+7n0)xd8hwpl3h%o)p#+*bf#q3#*$cc=uwtq-6-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# This is required because we have extended the user model in accounts app
AUTH_USER_MODEL = 'accounts.User'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_USER_MODEL = 'accounts.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    # my apps
    'job',
    'accounts',

    'datetimewidget',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    'social_django.middleware.SocialAuthExceptionMiddleware',

]

ROOT_URLCONF = 'resume.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            
            ],
        },
    },
]

WSGI_APPLICATION = 'resume.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'resume',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': ''
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = (
 'social_core.backends.open_id.OpenIdAuth',
 
 'social_core.backends.linkedin.LinkedinOAuth2',

 'django.contrib.auth.backends.ModelBackend',


)

SOCIAL_AUTH_PIPELINE = (
   'social_core.pipeline.social_auth.social_details',
   'social_core.pipeline.social_auth.social_uid',
   'social_core.pipeline.social_auth.social_user',
   'social_core.pipeline.user.get_username',
   'social_core.pipeline.user.create_user',
   'social_core.pipeline.social_auth.associate_user',
   'social_core.pipeline.social_auth.load_extra_data',
   'social_core.pipeline.user.user_details',
   'social_core.pipeline.social_auth.associate_by_email',
)

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '869ale4pgv5tww'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'gI2szIzK19hhPN4u'
SOCIAL_AUTH_LINKEDIN_SCOPE = [ 'r_basicprofile', 'r_emailaddress' ]

SOCIAL_AUTH_FIELD_SELECTORS = ['email-address',]

# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_local'),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'static_root')

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'media_root')


ACCOUNT_EMAIL_VERIFICATION = "none"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'daking.infodev@gmail.com'
EMAIL_HOST_PASSWORD = 'entertheinfodev'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
