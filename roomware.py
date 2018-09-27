from django.conf.urls import url, include
from django.http import HttpResponse
from django.template import engines
from django.template.loader import render_to_string
import os

DEBUG = True
SECRET_KEY = '$092qo$uxn=1&08mp4=*$+oxryg6ot$9!l-=_33e6ptsn2poq0'
ROOT_URLCONF = __name__
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			'/home/roomuser/Roomware/roomware/templates/'
		],
	},
]

STATICFILES_DIRS = [
	"/home/roomuser/Roomware/roomware/static/",
]
'''
MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
SESSION_ENGINE = [
	'django.contrib.sessions.backends.signed_cookies',
]

SESSION_COOKIE_HTTPONLY = [
	'False',
]'''

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

	
STATIC_URL = '/static/'		

urlpatterns = [
	url(r'', include('urls')),
]

#DATABASE_ENGINE = {
#	}


REST_FRAMEWORK = {
'DEFAULT_PERMISSION_CLASSES': [
	'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	],
'UNAUTHENTICATED_USER': None,
'DEFAULT_AUTHENTICATION_CLASSES': [],
}
