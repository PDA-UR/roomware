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

#DATABASES = {
#	'default': {
#		'ENGINE': 'django.db.backends.dummy',
#		'NAME': 'base.py',
#	}
#}

REST_FRAMEWORK = {
'DEFAULT_PERMISSION_CLASSES': [
	'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	],
'UNAUTHENTICATED_USER': None,
'DEFAULT_AUTHENTICATION_CLASSES': [],
}
