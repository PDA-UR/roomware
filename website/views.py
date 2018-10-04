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

# making files downloadable
# https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files last access 03.10.2018

# showing files on website
# https://stackoverflow.com/questions/7042031/django-auto-generating-a-list-of-files-in-a-directory last access 03.10.2018
import os
import django
django.setup()

import smtplib

from bin import hdmi_controller
from bin import beamer
from bin import stream as stm
from bin import login as lgn

from django.shortcuts import render, redirect
from website.models import RoomReservation, DevicesReservation, Login
from website.forms import RoomReservationForm, DevicesReservationForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.static import serve
from django.urls import reverse
hdmiController = hdmi_controller.HdmiController()
session_connected = []

def post_home(request):
	return render(request, 'login.html', {})
	
def post_media(request):
	if len(request.session.items()) > 0:	
		return render(request, 'media.html', {})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form': form})
	
def post_room(request):
	if len(request.session.items()) > 0:
		return render(request, 'room.html', {})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form': form})
	
def post_devices(request):
	if len(request.session.items()) > 0:
		return render(request, 'devices.html', {})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form': form})

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
			except smtplib.SMTPException:
				print("Error: unable to send email")
			return redirect('devices')
	else: 
		form = DevicesReservationForm()
	return render(request, 'devices_reservation_inquiry.html', {'form': form})	

def stream(request):
	username = request.session['Benutzername']
	audio_recorder = stm.AudioRecorder()
	audio_recorder.start()
	video_recorder = stm.VideoRecorder(audio_recorder, username)
	video_recorder.start()
	stm.stop_recording(audio_recorder, video_recorder)
	path = '/home/roomuser/Roomware/'+username+'/'
	files = os.listdir(path)
	return render(request, 'stream_files.html', {'files': files})
	
def login(request):
	global account
	username = 'not logged in'
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			try:
				account = lgn.LDAPConnection()
				conn = account.TestConnection(post.Benutzername, post.Passwort)
				if conn[0] is True:
					username = post.Benutzername
					request.session['Benutzername'] = username
					user_conn = (username, conn[1], conn[0])
					session_connected.append(user_conn) 
					return redirect('media')
				else:
					form = LoginForm()
					return render(request, 'login.html', {'form': form})
			except:
				form = LoginForm()
				return render(request, 'login.html', {'form': form})
	else:
		form = LoginForm()
		
	return render(request, 'login.html', {'form': form})
	
	
def logout(request):
	try:
		connection = None
		user = request.session['Benutzername']
		for i in range(len(session_connected)):
			if user == session_connected[i][0]:
				connection = session_connected[i][1]
				index = i
		if connection is not None: 
			session_connected.pop(index)
			account.logout(connection)
			request.session.flush()
	except Exception as e:
	    print("Logout error", e)
	form = LoginForm()
	return HttpResponseRedirect('/login/')


def stream_file(request, file=None):
	username = request.session['Benutzername']
	path = '/home/roomuser/Roomware/'+username+'/'
	if file is not None:
		filepath= path + file
		return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
	else:
		return redirect('link')
		
		
def delete_file(request, file=None):
	if file is not None:
		username = request.session['Benutzername']
		path = '/home/roomuser/Roomware/'+username
		filepath= path + '/' + file
		os.remove(filepath)
		if len(os.listdir(path)) == 0:
			os.chdir('/home/roomuser/Roomware')
			os.rmdir(path)
			return render(request, 'media.html', {})
		else:
			files = os.listdir(path)
			return render(request, 'stream_files.html', {'files': files})
	else:
		return redirect('link')
		
def delete_all_files(request):
	username = request.session['Benutzername']
	os.chdir('/home/roomuser/Roomware/'+username)
	path = '/home/roomuser/Roomware/'+username
	files = os.listdir(path)
	for i in range(len(files)):
		filepath = path + '/' + files[i]
		os.remove(filepath)
	os.chdir('/home/roomuser/Roomware')
	os.rmdir(path)
	return render(request, 'media.html', {})
