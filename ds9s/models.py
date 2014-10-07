from django.db import models
class Fits(models.Model):
	name = models.CharField(max_length=254)
	date_upload = models.DateTimeField(auto_now_add=True, auto_now=False)
	file_field = models.FileField(upload_to='fits/', null=True)
	uniqname = models.CharField(max_length=254,null=True)
	generated = models.BooleanField(default=False) 
	active = models.BooleanField(default=True) 

	def __unicode__(self):
		return self.name