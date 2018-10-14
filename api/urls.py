from django.conf.urls import url
from api import views
from bin import powerstrip

# api urls
urlpatterns = [
	url(r'^$', views.view_api),
	url(r'beamer/$', views.view_beamer),
    url(r'beamer/on/$', views.view_beamer_on),
    url(r'beamer/off/$', views.view_beamer_off),
    url(r'beamer/change_state/$', views.view_beamer_change_state),
	url(r'powerstrip/$', views.view_powerstrip),
    url(r'powerstrip/on/$', views.view_powerstrip_on),
    url(r'powerstrip/off/$', views.view_powerstrip_off),
    url(r'powerstrip/switch_all_on/$', views.view_powerstrip_switch_all_on),
    url(r'powerstrip/switch_all_off/$', views.view_powerstrip_switch_all_off),
    url(r'powerstrip/status/$', views.view_powerstrip_status),
    url(r'powerstrip/status_all/$', views.view_powerstrip_status_all),
    url(r'hdmiswitch/$', views.view_hdmi_switch),
    url(r'hdmiswitch/status/$', views.view_hdmi_switch_status),
    url(r'hdmiswitch/outputconnections/$', views.view_hdmi_switch_output_connections),
    url(r'hdmiswitch/getconnection/$', views.view_hdmi_switch_get_connection),
    url(r'hdmiswitch/statusin/$', views.view_hdmi_switch_status_in),
    url(r'hdmiswitch/statusout/$', views.view_hdmi_switch_status_out),
    url(r'hdmiswitch/getinoutdevices/$', views.view_hdmi_switch_get_in_out_devices),
    url(r'hdmiswitch/connect/$', views.view_hdmi_switch_connect),
    url(r'hdmiswitch/off/$', views.view_hdmi_switch_off),
    url(r'hdmiswitch/on/$', views.view_hdmi_switch_on),
    url(r'usbswitch/$', views.view_usb_switch),
    url(r'usbswitch/change_hub/$', views.view_usb_switch_change_hub),
    url(r'usbswitch/change_to_previous_hub/$', views.view_usb_switch_change_to_previous_hub),
    url(r'usbswitch/change_to_number/$', views.view_usb_switch_change_to_number),
    url(r'usbswitch/set_number_switch/$', views.view_usb_switch_set_number_switch),
    url(r'usbswitch/check_usb/$', views.view_usb_switch_check_usb),
    url(r'usbswitch/find_usb_switch/$', views.view_usb_switch_find_usb_switch),
]
