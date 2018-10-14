from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# model for room reservation form
class RoomReservation(models.Model):
	Vorname =  models.CharField(max_length=100, blank=False)
	Nachname = models.CharField(max_length=100)
	Email = models.EmailField()
	Reservierung_Labor = models.BooleanField()
	Reservierung_Studio = models.BooleanField()
	Reservierung_Werkstatt = models.BooleanField()
	Datum_von = models.CharField(max_length=100)
	Datum_bis = models.CharField(max_length=100)
	Uhrzeit_Start = models.CharField(max_length=100)
	Uhrzeit_Ende = models.CharField(max_length=100)
	Zweck = models.TextField(max_length=100)
	Kommentar = models.TextField(blank=True)
	
# model for devices reservation form
class DevicesReservation(models.Model):
	Vorname =  models.CharField(max_length=100)
	Nachname = models.CharField(max_length=100)
	Email = models.EmailField()
	Datum_von = models.CharField(max_length=100)
	Datum_bis = models.CharField(max_length=100)
	Gerät = models.CharField(max_length=100)
	Zweck = models.TextField()
	Kommentar = models.TextField(blank=True)

# model for login	
class Login(models.Model):
	Benutzername = models.CharField(max_length=8)
	Passwort = models.CharField(max_length=32)
