from django.conf.urls import url
from api import views

urlpatterns = [
	url(r'^api/$', views.view_api),
	url(r'^api/beamer/$', views.view_beamer),
	url(r'^api/powerstrip/$', views.view_powerstrip),
]
