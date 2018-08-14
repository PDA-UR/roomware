"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.post_home, name='home'),
	url(r'^media/$', views.post_media, name='media'),
	url(r'^room/$', views.post_room, name='room'),
	url(r'^devices/$', views.post_devices, name='devices'),
	url(r'^media/beamer_on/$',views.beamer_on_post, name='beamer_on'),
	url(r'^media/beamer_off/$',views.beamer_off_post, name='beamer_off'),
]