from django import forms
from website.models import RoomReservation, DevicesReservation, Login

# show password unreadable
# https://simpleisbetterthancomplex.com/tutorial/2016/08/15/how-to-create-a-password-confirmation-view.html last access: 26.09.2018

class RoomReservationForm(forms.ModelForm):

	class Meta:
		model = RoomReservation
		fields = ('user_firstName', 'user_secondName', 'user_email', 'reservation_labor', 'reservation_studio', 'reservation_workshop', 'date_start', 'date_end', 'time_start', 'time_end', 'purpose', 'comments',)
		
		
class DevicesReservationForm(forms.ModelForm):

	class Meta:
		model = DevicesReservation
		fields = ('user_firstName', 'user_secondName', 'user_email', 'date_start', 'date_end', 'device', 'purpose', 'comments',)

class LoginForm(forms.ModelForm):
	Passwort = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Login
		fields = ('Benutzername', 'Passwort',)
