from django.shortcuts import render, redirect
from bin import beamer as beamer
from website.models import Reservation
def post_home(request):
	return render(request, 'index.html', {})
	
def post_media(request):
	return render(request, 'media.html', {})
	
def post_room(request):
	return render(request, 'room.html', {})
	
def post_devices(request):
	return render(request, 'devices.html', {})

def beamer_post(request):
	beamer.Beamer().changeState()
	return redirect('media')
	

	
	
		
	
