#!/usr/bin/python3
# -*- coding: utf-8 -*-
# source to import django.
# https://stackoverflow.com/questions/34114427/django-upgrading-to-1-9-error-appregistrynotready-apps-arent-loaded-yet last access 05.09.2018

# source to request.POST,
# https://stackoverflow.com/questions/42327004/django-form-is-valid-fails last access 06.09.2018

# sending an email
# https://www.tutorialspoint.com/python3/python_sending_email.htm last access 06.09.2018

# creating an email subject
# https://stackoverflow.com/questions/7232088/python-subject-not-shown-when-sending-email-using-smtplib-module last access 06.09.2018

# get name of html button
# https://stackoverflow.com/questions/20448911/get-id-of-one-of-multiple-buttons-in-html-form-in-django last access 19.09.2018

import django
django.setup()

import smtplib
from bin import hdmi_controller
from bin import beamer

from django.shortcuts import render, redirect
from website.models import RoomReservation, DevicesReservation
from website.forms import RoomReservationForm, DevicesReservationForm

hdmiController = hdmi_controller.HdmiController()

def post_home(request):
	return render(request, 'index.html', {})
	
def post_media(request):
	return render(request, 'media.html', {})
	
def post_room(request):
	return render(request, 'room.html', {})
	
def post_devices(request):
	return render(request, 'devices.html', {})

def hdmi_post(request):
	action = None
	output = '0'
	input = '0'
	for key in request.POST.keys():
		if key.startswith('output'):
			action = key[6:]
			break
	if action != None:
		input = action[0]
		output = action[1]
		hdmiController.setInput = input
		hdmiController.setOutput = output
		hdmiController.toggleConnection()
	return redirect('media')
	
def new_room_reservation(request):
	if request.method == "POST":
		form = RoomReservationForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			print(post.user_firstName, post.reservation_labor, post.reservation_studio, post.reservation_workshop)
			sender = post.user_email 
			receiver = ['katharina.lichtner@stud.uni-regensburg.de']
			roomsIndex = 0
			rooms = ""
			if post.reservation_labor:
				rooms += "Labor"
				roomsIndex = 1
			if post.reservation_studio:
				if roomsIndex > 0:
					rooms += ", "
				rooms += "Studio"
				roomsIndex +=1
			if post.reservation_workshop:
				if roomsIndex > 0:
					rooms += ", "
				rooms += "Werkstatt"
			SUBJECT = "Reservierungsanfrage " + rooms
			TEXT =  """Neue Reservierung von """ + post.user_firstName + """ """ + post.user_secondName + """ für """ + rooms +  """.\n Reservierung von """ + str(post.date_start) + """ bis """ + str(post.date_end) + """ jeweils zwischen """ + str(post.time_start) + """ und """ + str(post.time_end) + """ Uhr.\n Reservierungsgrund: """ + post.purpose
			if len(post.comments) > 0:
				TEXT += """\n Kommentar: """ + post.comments
			message ='Subject: {}\n\n{}'.format(SUBJECT, TEXT.encode('utf-8'))
			
			try:
				smtpObj = smtplib.SMTP('mail.uni-regensburg.de')
				smtpObj.sendmail(sender, receiver, message)
				print("Successfully send email")
			except smtplib.SMTPException:
				print("Error: unable to send email")
			return redirect('room')
	else: 
		form = RoomReservationForm()
	return render(request, 'room_reservation_inquiry.html', {'form': form})
	
def new_devices_reservation(request):
	if request.method == "POST":
		form = DevicesReservationForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			sender = post.user_email 
			receiver = ['katharina.lichtner@stud.uni-regensburg.de']
			TEXT =  """Neue Reservierung von """ + post.user_firstName + """ """ + post.user_secondName + """ für """ + post.device +  """.\n Reservierung von """ + str(post.date_start) + """ bis """ + str(post.date_end) + """.\n Reservierungsgrund: """ + post.purpose
			if len(post.comments) > 0:
				TEXT += """\n Kommentar: """ + post.comments			
			SUBJECT = "Reservierungsanfrage " + post.device
			message ='Subject: {}\n\n{}'.format(SUBJECT, TEXT.encode('utf-8'))
			try:
				smtpObj = smtplib.SMTP('mail.uni-regensburg.de')
				smtpObj.sendmail(sender, receiver, message)
				print("Successfully send email")
			except smtplib.SMTPException:
				print("Error: unable to send email")
			return redirect('devices')
	else: 
		form = DevicesReservationForm()
	return render(request, 'devices_reservation_inquiry.html', {'form': form})	
