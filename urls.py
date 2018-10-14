from django.contrib import admin
from website import views
from api import views as view
from api import models
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from bin import powerstrip
from django.contrib.auth import views as auth_views

# all urls of the project
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
	url(r'media/$', views.post_media, name='media'),
	url(r'room/$', views.post_room, name='room'),
	url(r'devices/$', views.post_devices, name='devices'),
	url(r'media/hdmi/$', views.hdmi_post, name='hdmi'),
    url(r'media/light/$', views.light_post, name='light'),
    url(r'media/powerstrip/$', views.powerstrip_post, name='powerstrip'),
    url(r'media/usb_switch/$', views.usb_switch, name='usb_switch'),
    url(r'media/beamer/$', views.beamer_post, name='beamer'),
	url(r'room/new_room_reservation/$', views.new_room_reservation, name='new_room_reservation'),
	url(r'devices/new_devices_reservation/$', views.new_devices_reservation, name='new_devices_reservation'),
	url(r'^api/', include('api.urls')),
	url(r'stream_start/$', views.stream, name='stream_start'),
    url(r'stream/$', views.video_stream, name='stream'),
    url(r'video_start/$', views.video_start, name='video_start'),
    url(r'video_stop/$', views.video_stop, name='video_stop'),
    url(r'stream_stop/$', views.stream_stop, name='stream_stop'),
	url(r'media/link/$', views.stream_file, name='link'),
	url(r'link/(?P<file>[\w.-]+)/$', views.stream_file, name='link'),
	url(r'delete/$', views.delete_file, name='delete'),
	url(r'delete/(?P<file>[\w.-]+)/$', views.delete_file, name='delete'),
	url(r'deleteAll/$', views.delete_all_files, name='deleteAll'),
]
