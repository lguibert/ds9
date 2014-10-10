from django.db import models
from django.contrib.auth.models import User

class ParFolder(models.Model):
	name_par = models.CharField(max_length=254,null=True)
	fieldId_par = models.IntegerField(default=0)
	date_upload = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return self.name_par

class Galaxy(models.Model):
	uniq_id = models.IntegerField(default=0)
	last_update = models.DateTimeField(auto_now=True)

	parfolder = models.ForeignKey('ParFolder')	
	users = models.ManyToManyField(User, through='Analysis')
	galaxyfields = models.ManyToManyField('GalaxyFields', through='GalaxyFeatures')

	def __unicode__(self):
		return self.name

class GalaxyFields(models.Model):
	name = models.CharField(max_length=254)
	shortname = models.CharField(max_length=254)

	def __unicode__(self):
		return self.name + ' (' +self.shortname +')'

class GalaxyFeatures(models.Model):
	galaxy = models.ForeignKey('Galaxy')
	galaxyfields = models.ForeignKey('GalaxyFields')
	value = models.DecimalField(max_digits=19, decimal_places=10, default=None) 


class EmissionLine(models.Model):
	name = models.CharField(max_length=254)
	shortname = models.CharField(max_length=254)
	emissionlinefields = models.ManyToManyField('EmissionLineFields', through='EmissionFeatures')
	
	galaxys = models.ManyToManyField(Galaxy, through='Analysis')

	def __unicode__(self):
		return self.name + ' (' +self.shortname +')'

class EmissionLineFields(models.Model):
	name = models.CharField(max_length=254)
	shortname = models.CharField(max_length=254)

	def __unicode__(self):
		return self.name + ' (' +self.shortname +')'

class EmissionFeatures(models.Model):
	emissionlinefields = models.ForeignKey('EmissionLineFields')
	emissionline = models.ForeignKey('EmissionLine')

class Analysis(models.Model):
	user = models.ForeignKey(User)
	galaxy = models.ForeignKey('Galaxy')
	emissionline = models.ForeignKey('EmissionLine')
	#approximately one billion with a resolution of 10 decimal
	value = models.DecimalField(max_digits=19, decimal_places=10)
	#many more are comming

	def __unicode__(self): 	
		return "Done by {0} on galaxy number {1}",format(self.user.username, self.galaxy.uniq_id)
