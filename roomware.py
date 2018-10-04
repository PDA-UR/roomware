from django.conf.urls import url, include
from django.http import HttpResponse
from django.template import engines
from django.template.loader import render_to_string
import os

DEBUG = True
SECRET_KEY = '$092qo$uxn=1&08mp4=*$+oxryg6ot$9!l-=_33e6ptsn2poq0'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = [
	'132.199.131.227',
	'localhost',	
]
ROOT_PATH = os.path.dirname(__file__)

INSTALLED_APPS = [
	'django.contrib.staticfiles',
	'django.contrib.contenttypes',
	'django.contrib.auth',
	'django.contrib.sessions',
	'django.contrib.messages',
	'sqlite3',
	'rest_framework',
	'api',
	'bin',
	'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


ROOT_URLCONF = __name__
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			'/home/roomuser/Roomware/roomware/templates/'
		],
	},
]

SESSION_COOKIE_HTTPONLY = True

STATICFILES_DIRS = [
	'/home/roomuser/Roomware/roomware/static',
]

	

urlpatterns = [
	url(r'', include('urls')),
]

STATIC_URL = '/static/'
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

'''
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	],
	'UNAUTHENTICATED_USER': None,
	'DEFAULT_AUTHENTICATION_CLASSES': [],
}
