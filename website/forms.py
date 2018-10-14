from django import forms
from website.models import RoomReservation, DevicesReservation, Login

# show password unreadable
# https://simpleisbetterthancomplex.com/tutorial/2016/08/15/how-to-create-a-password-confirmation-view.html last access: 26.09.2018

# form for room reservation
class RoomReservationForm(forms.ModelForm):

	class Meta:
		model = RoomReservation
		fields = ('Vorname', 'Nachname', 'Email', 'Reservierung_Labor', 'Reservierung_Studio', 'Reservierung_Werkstatt', 'Datum_von', 'Datum_bis', 'Uhrzeit_Start', 'Uhrzeit_Ende', 'Zweck', 'Kommentar',)
		
# form for devices reservation		
class DevicesReservationForm(forms.ModelForm):

	class Meta:
		model = DevicesReservation
		fields = ('Vorname', 'Nachname', 'Email', 'Datum_von', 'Datum_bis', 'Gerät', 'Zweck', 'Kommentar',)

# form for login
class LoginForm(forms.ModelForm):
	Passwort = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Login
		fields = ('Benutzername', 'Passwort',)
