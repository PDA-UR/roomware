from django.conf.urls import url, include
from django.http import HttpResponse
from django.template import engines
from django.template.loader import render_to_string

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
	'rest_framework',
	'api',
	'bin',
]

	
STATIC_URL = '/static/'		

urlpatterns = [
	url(r'', include('urls')),
] 
