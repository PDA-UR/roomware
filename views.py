from django.shortcuts import render
from bin import beamer as beamer

def post_home(request):
	return render(request, 'index.html', {})
	
def post_media(request):
	return render(request, 'media.html', {})
	
def post_room(request):
	return render(request, 'room.html', {})
	
def post_devices(request):
	return render(request, 'devices.html', {})
	
def beamer_on_post(request):
	beamer.Beamer().on()
	return render(request, 'media.html', {})
	
def beamer_off_post(request):
	beamer.Beamer().off()
	return render(request, 'media.html', {})
	
