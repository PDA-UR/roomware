from django.conf.urls import url, include
from django.http import HttpResponse
from django.template import engines
from django.template.loader import render_to_string
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
import os

import dj_database_url



DEBUG = True
SECRET_KEY = '$092qo$uxn=1&08mp4=*$+oxryg6ot$9!l-=_33e6ptsn2poq0'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = [
	'132.199.131.227',
    'localhost',
    'lab.mi.ur.de',	
]
ROOT_PATH = os.path.dirname(__file__)

AUTH_LDAP_SERVER_URI = "ldaps://ldap3.ur.de:636"

AUTH_LDAP_BIND_DN = "" 
AUTH_LDAP_BIND_PASSWORD = "" 
AUTH_LDAP_USER_SEARCH = LDAPSearch("o=uni-regensburg,c=de", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT:False,
}

AUTH_LDAP_CACHE_TIMEOUT = 3600

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=mi,ou=sprachlit,o=uni-regensburg,c=de",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

AUTH_LDAP_REQUIRE_GROUP = "cn=mi-lab,ou=mi,ou=sprachlit,o=uni-regensburg,c=de"

AUTH_LDAP_USER_ATTR_MAP = {
	"first_name": "givenName", "last_name": "sn"
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=mi-lab,ou=mi,ou=sprachlit,o=uni-regensburg,c=de",
    "is_staff": "cn=mi-labadmin,ou=mi,ou=sprachlit,o=uni-regensburg,c=de",
}

LOGIN_REDIRECT_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#DATABASES['default'] =  dj_database_url.config()

INSTALLED_APPS = [
	'django.contrib.staticfiles',
	'django.contrib.contenttypes',
	'django.contrib.auth',
	'django.contrib.sessions',
	'django.contrib.messages',
	'rest_framework',
	'api',
	'bin',
	'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'cache_headers.middleware.CacheHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

SESSION_COOKIE_HTTPONLY = True

CACHE_HEADERS = {'browser-cache-seconds': 2}

AUTHENTICATION_BACKENDS = [
	'django_auth_ldap.backend.LDAPBackend',
	'django.contrib.auth.backends.ModelBackend',
]
ROOT_URLCONF = __name__
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			'/home/roomuser/Roomware/roomware/templates/'
		],
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

STATICFILES_DIRS = [
	'/home/roomuser/Roomware/roomware/static',
]

urlpatterns = [
	url(r'', include('urls')),
]

STATIC_URL = '/static/'


REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'rest_framework.authentication.SessionAuthentication'
	],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ],
}
