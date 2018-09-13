from django.db import models

class Snippet(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	device = models.CharField(default="powerstrip", max_length=100)
	code = models.TextField()
	language = models.CharField(default="python", max_length=100)
	
	objects = models.Manager()
	
	class Meta:
		ordering = ('created',)
		
		
		
