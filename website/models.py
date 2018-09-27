from django.db import models
from django import forms

class RoomReservation(models.Model):
	user_firstName =  models.CharField(max_length=100, blank=False)
	user_secondName = models.CharField(max_length=100)
	user_email = models.EmailField()
	reservation_labor = models.BooleanField()
	reservation_studio = models.BooleanField()
	reservation_workshop = models.BooleanField()
	date_start = models.DateField()
	date_end = models.DateField()
	time_start = models.TimeField()
	time_end = models.TimeField()
	purpose = models.TextField()
	comments = models.TextField(blank=True)
	

class DevicesReservation(models.Model):
	user_firstName =  models.CharField(max_length=100)
	user_secondName = models.CharField(max_length=100)
	user_email = models.EmailField()
	date_start = models.DateField()
	date_end = models.DateField()
	device = models.CharField(max_length=100)
	purpose = models.TextField()
	comments = models.TextField(blank=True)
	
class Login(models.Model):
	Benutzername = models.CharField(max_length=8)
	Passwort = models.CharField(max_length=32)
	#,widget=forms.PasswordInput
