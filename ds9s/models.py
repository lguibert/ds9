from django.db import models

class ParFileFits(models.Model):
	name_par = models.CharField(max_length=254,null=True)
	fieldId_par = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name_par

class Fits(models.Model):
	name = models.CharField(max_length=254)
	date_upload = models.DateTimeField(auto_now_add=True, auto_now=False)
	uniqname = models.CharField(max_length=254,null=True)
	uniq_id = models.IntegerField(default=0)
	generated = models.BooleanField(default=False) 
	active = models.BooleanField(default=True) 
	parfilefits = models.ForeignKey('ParFileFits',null=True)

	def __unicode__(self):
		return self.name