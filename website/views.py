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

# no store=True in cache_control
# https://stackoverflow.com/questions/9625046/django-login-required-views-still-show-when-users-are-logged-out-by-going-back last access 10.10.2018

# send request from javascript to django view and get its data
# https://stackoverflow.com/questions/3889769/how-can-i-get-all-the-request-headers-in-django last access 12.10.2018

import os
import django
django.setup()

import smtplib

from bin import hdmi_controller
from bin import beamer
from bin import ffmpeg_stream as ffstr
from bin import powerstrip
from bin import controller
from bin import media_template
from bin import usb_switch
import time

from django.shortcuts import render, redirect
from website.models import RoomReservation, DevicesReservation, Login
from website.forms import RoomReservationForm, DevicesReservationForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.static import serve
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

import ldap
from django.contrib.auth.models import Group, Permission, User
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from django.utils import timezone
from configparser import ConfigParser

os.chdir('/home/roomuser/Roomware/roomware')
config = ConfigParser()
config.read('config.ini')
controller = controller.Controller()
hdmi_controller = hdmi_controller.HdmiController()
powerstrip_studio = powerstrip.Powerstrip(1)
powerstrip_labor = powerstrip.Powerstrip(2)
session_connected = []
media_template = media_template.PropertiesTemplate()


# render login page
@login_required
@cache_control(no_cache=True, must_revalidate=True)
def post_home(request):
    return render(request, 'login.html', {})

#render media page 
@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def post_media(request):
    if request.user.is_authenticated:
        return render(request, 'media.html', media_template.get_template())
    else:
        return redirect('login')

# render room reservation page
@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True)	
def post_room(request):
    if request.user.is_authenticated:
        return render(request, 'room.html', {})
    else:
        return redirect('login')

# render device reservation page
@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True)
def post_devices(request):
    if request.user.is_authenticated:
        return render(request, 'devices.html', {})
    else:
        return redirect('login')

# get request to control hdmi 
@cache_control(no_cache=True, must_revalidate=True)
def hdmi_post(request):
    action = None
    output = '0'
    inputs = '0'
    for key in request.POST.keys():
        if key.startswith('output'):
            action = key[6:]
            break
    if action != None:
        inputs = action[1]
        output = action[0]
        outputint = int(output)
        status_labor = controller.status_powerstrip_labor()
        status_studio = controller.status_powerstrip_studio()

        status = media_template.get_template()
        if status['beamer_'+output+inputs] == "output_on":
            media_template.change_template('beamer_headline_'+output, 'off')
            media_template.change_template('beamer_onoff_'+output, 'beamer_off')
            media_template.change_template('beamer_'+output+inputs, 'output_off')
        else:
            media_template.change_template('beamer_headline_'+output, 'on')
            media_template.change_template('beamer_onoff_'+output, 'beamer_on')
            media_template.change_template('beamer_'+output+inputs, 'output_on')
            for i in range(1,5):
                if str(i) != inputs:
                    media_template.change_template('beamer_'+output+str(i), 'output_off')
              
        controller.control_hdmi_switch(inputs, output)
    return render(request, 'media.html', media_template.get_template())

# get request to control light
@cache_control(no_cache=True, must_revalidate=True)
def light_post(request):
    change = controller.control_light()
    if change == "on":
        media_template.change_template('light_1', 'on')
        media_template.change_template('lamp_1', 'light_on')
    else:
        media_template.change_template('light_1', 'off')
        media_template.change_template('lamp_1', 'light_off')
    return render(request, 'media.html', media_template.get_template())

# control direct beamer request
def beamer_post(request):
    output = 0
    for key in request.POST.keys():
        if key.startswith('beamer'):
            output = key[6]
            break
    if output is not None:
        status_labor = controller.status_powerstrip_labor()
        status_studio = controller.status_powerstrip_studio()

        if int(output) > 2:
            if status_labor['beamer_'+output] == 1:
                media_template.change_template('beamer_headline_'+output, 'off')
                media_template.change_template('beamer_onoff_'+output, 'beamer_off')
                feedback = controller.hdmi_status(output)
                try:
                    media_template.change_template('beamer_'+output+feedback, 'output_off')
                except:
                    pass
            else:
                media_template.change_template('beamer_headline_'+output, 'on')
                media_template.change_template('beamer_onoff_'+output, 'beamer_on')
                feedback = controller.hdmi_status(output)
                try:
                    media_template.change_template('beamer_'+output+feedback, 'output_on')
                except:
                    pass
        else:
            if status_studio['beamer_'+output] == 1:
                media_template.change_template('beamer_headline_'+output, 'off')
                media_template.change_template('beamer_onoff_'+output, 'beamer_off')
                feedback = controller.hdmi_status(output)
                try:
                    media_template.change_template('beamer_'+output+feedback, 'output_off')
                except:
                    pass
            else:
                media_template.change_template('beamer_headline_'+output, 'on')
                media_template.change_template('beamer_onoff_'+output, 'beamer_on')
                feedback = controller.hdmi_status(output)
                try:
                    media_template.change_template('beamer_'+output+feedback, 'output_on')
                except:
                    pass
        controller.control_beamer(output)
            
    return render(request, 'media.html', media_template.get_template())

# control powerstrips
@cache_control(no_cache=True, must_revalidate=True)
def powerstrip_post(request):
    room = 0
    socket = 0
    action = ""
    for key in request.POST.keys():
        if key.startswith('socket'):
            action = key[6:]
            break
    if action is not None:
        room = action[0]
        socket = action[1]
    control = controller.control_powerstrip(room, socket)
    if control == 'on':
        media_template.change_template('powerstrip_'+room, 'on')
        media_template.change_template('socket_'+room+socket, 'output_on')
    else:
        if room == '2':
            status = controller.status_powerstrip_labor()
            if status['2'] == 0:
                if status['3'] == 0:
                    media_template.change_template('powerstrip_'+room, 'off')
        else:
            media_template.change_template('powerstrip_'+room, 'off')
        media_template.change_template('socket_'+room+socket, 'output_off')
    
    return render(request, 'media.html', media_template.get_template())

# get, create and send new reservation for rooms
@cache_control(no_cache=True, must_revalidate=True)
def new_room_reservation(request):
    if request.method == "POST":
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            sender = post.Email 
            receiver = [config.get("reservation_email", "email_address")]
            roomsIndex = 0
            rooms = ""
            if post.Reservierung_Labor:
                rooms += "Labor"
                roomsIndex = 1
            if post.Reservierung_Studio:
                if roomsIndex > 0:
                    rooms += ", "
                rooms += "Studio"
                roomsIndex +=1
            if post.Reservierung_Werkstatt:
                if roomsIndex > 0:
                    rooms += ", "
                rooms += "Werkstatt"
            SUBJECT = "Reservierungsanfrage " + rooms
            TEXT =  """Neue Reservierung von """ + post.Vorname + """ """ + post.Nachname + """ für """ + rooms +  """.\n Reservierung von """ + str(post.Datum_von) + """ bis """ + str(post.Datum_bis) + """ jeweils zwischen """ + str(post.Uhrzeit_Start) + """ und """ + str(post.Uhrzeit_Ende) + """ Uhr.\n Reservierungsgrund: """ + post.Zweck
            if len(post.Kommentar) > 0:
                TEXT += """\n Kommentar: """ + post.Kommentar
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
    else: 
        form = RoomReservationForm()
    return render(request, 'room_reservation_inquiry.html', {'form': form})

# get, create and send new device reservation
@cache_control(no_cache=True, must_revalidate=True)
def new_devices_reservation(request):
    if request.method == "POST":
        form = DevicesReservationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            sender = post.Email 
            receiver = [config.get("reservation_email", "email_address")]
            TEXT =  """Neue Reservierung von """ + post.Vorname + """ """ + post.Nachname + """ für """ + post.Gerät +  """.\n Reservierung von """ + str(post.Datum_von) + """ bis """ + str(post.Datum_bis) + """.\n Reservierungsgrund: """ + post.Zweck
            if len(post.Kommentar) > 0:
                TEXT += """\n Kommentar: """ + post.Kommentar			
            SUBJECT = "Reservierungsanfrage " + post.Gerät
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

# starts stream
@cache_control(no_cache=True, must_revalidate=True)
def stream(request):
    new_stream.start_live(request.session['Benutzername'])
    return render(request, 'stream.html', {})

# controls stream access
@cache_control(no_cache=True, must_revalidate=True)
def video_stream(request):
    global new_stream
    new_stream = ffstr.Stream()
    all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    is_online = False
    for session in all_sessions:
        session_data = session.get_decoded()
        if session_data['stream'] == True:
            if session_data['Benutzername'] == request.session['Benutzername']:
                response = render(request, 'stream.html', {})
                response['stream'] = 'true'
                return response
            else:
                is_online = True
    if is_online is False:
        usb_switch.USBSwitch().find_usb_switch()
        new_stream.start_live(session_data['Benutzername'])
        request.session['stream'] = True
        media_template.change_template('stream', 'output_on stream_disable')
        response = render(request, 'stream.html', {})
        response['stream'] = 'true'
        return response

    else:
        return render(request, 'media.html', media_template.get_template()) 

# starts video stream
@cache_control(no_cache=True, must_revalidate=True)
def video_start(request):
    new_stream.start()
    return HttpResponse(status=204)

# stops recording stream
@cache_control(no_cache=True, must_revalidate=True)
def video_stop(request):
    if request.META['HTTP_FILENAME'] == '':
        new_stream.deleteFiles()
    else:
        new_stream.stop(request.META['HTTP_FILENAME'])
        return HttpResponse(status=204)

# stops live stream
@cache_control(no_cache=True, must_revalidate=True)
def stream_stop(request):
    new_stream.stop_stream()
    request.session['stream'] = False
    media_template.change_template('stream', 'output_off')
    return render(request, 'media.html', media_template.get_template()) 

# controls usb switch
@cache_control(no_cache=True, must_revalidate=True)
def usb_switch(request):
    output = 0
    for key in request.POST.keys():
        if key.startswith('usb_output'):
            output = key[10]
            break
    if output is not None:
        controller.control_usb_switch(output)
    if output != "1":
        media_template.change_template('usb', 'on')
        for i in range(1,5):
            if str(i) != output:
                media_template.change_template('usb_output_'+str(i), 'output_off')
            else:
                media_template.change_template('usb_output_'+str(i), 'output_on')
    else:
        media_template.change_template('usb', 'off')
        media_template.change_template('usb_output_2', 'output_off')
        media_template.change_template('usb_output_3', 'output_off')
        media_template.change_template('usb_output_4', 'output_off')
    return render(request, 'media.html', media_template.get_template())


# handles login with nds accounts, ip address and necessary access groups
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    global account
    if request.META['REMOTE_ADDR'][0:8] == "132.199.":
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                username = post.Benutzername
                try:
                    auth = LDAPBackend()
                    user = auth.authenticate(request, username, post.Passwort)
                    if user is not None:
                        request.session['Benutzername'] = username
                        request.session['stream'] = False
                        django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        return render(request, 'media.html', media_template.get_template())
                    else:
                        form = LoginForm()
                        return redirect('login')
                except:
                    print('exceptLDAP')
                    form = LoginForm()
                    return redirect('login')
            else:
                form = LoginForm()
                return render(request, 'login.html', {'form': form})
        else:
            form = LoginForm()
	    
            return render(request, 'login.html', {'form': form})

# logout user
@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')

# render view for recorded streams
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def stream_file(request, file=None):
    username = request.session['Benutzername']
    try:
        path = '/home/roomuser/Roomware/'+username+'/'
        files = os.listdir(path)    
        if files is not None:
            if file is not None:
                filepath= path + file
                return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
            else:
                return render(request,'stream_files.html', {'files':files})
    except:
        return render(request, 'media.html', media_template.get_template())

# delete one video		
@cache_control(no_cache=True, must_revalidate=True, no_store=True)	
def delete_file(request, file=None):
    if file is not None:
        username = request.session['Benutzername']
        path = '/home/roomuser/Roomware/'+username
        filepath= path + '/' + file
        os.remove(filepath)
        if len(os.listdir(path)) == 0:
            os.chdir('/home/roomuser/Roomware')
            os.rmdir(path)
            return render(request, 'media.html', media_template.get_template())
        else:
            files = os.listdir(path)
            return render(request, 'stream_files.html', {'files': files})
    else:
        return redirect('link')

# delete all files in own directory
@cache_control(no_cache=True, must_revalidate=True, no_store=True)	
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
    return render(request, 'media.html', media_template.get_template())
