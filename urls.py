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
from website import views
from api import views as view
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets


urlpatterns = [
    url(r'^$', views.login, name='home'),
	url(r'^media/$', views.post_media, name='media'),
	url(r'^room/$', views.post_room, name='room'),
	url(r'^devices/$', views.post_devices, name='devices'),
	url(r'^media/hdmi/$', views.hdmi_post, name='hdmi'),
	url(r'^room/new_room_reservation/$', views.new_room_reservation, name='new_room_reservation'),
	url(r'^devices/new_devices_reservation/$', views.new_devices_reservation, name='new_devices_reservation'),
	url(r'^', include('api.urls')),
	url(r'^stream/$', views.stream, name='stream'),
	url(r'^login/$', views.login, name='login')
]
