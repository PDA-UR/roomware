from django import forms

from website.models import RoomReservation, DevicesReservation

class RoomReservationForm(forms.ModelForm):

	class Meta:
		model = RoomReservation
		fields = ('user_firstName', 'user_secondName', 'user_email', 'reservation_labor', 'reservation_studio', 'reservation_workshop', 'date_start', 'date_end', 'time_start', 'time_end', 'purpose', 'comments',)
		
		
class DevicesReservationForm(forms.ModelForm):

	class Meta:
		model = DevicesReservation
		fields = ('user_firstName', 'user_secondName', 'user_email', 'date_start', 'date_end', 'device', 'purpose', 'comments',)
