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
	uniq_name = models.CharField(max_length=254,null=True)

	parfolder = models.ForeignKey('ParFolder')	
	users = models.ManyToManyField(User, through='Analysis')
	galaxyfields = models.ManyToManyField('GalaxyFields', through='GalaxyFeatures')
	galaxytype = models.ManyToManyField('GalaxyType', through='Identifications')

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
	
	galaxys = models.ManyToManyField('Galaxy', through='Analysis')

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

class GalaxyType(models.Model):
	name = models.CharField(max_length=254)

	galaxys = models.ManyToManyField('Galaxy', through='Identifications', related_name="galaxytype_galaxys_iden")

	def __unicode__(self):
		return self.name

class Analysis(models.Model):
	user = models.ForeignKey(User)
	galaxy = models.ForeignKey('Galaxy')
	emissionline = models.ForeignKey('EmissionLine')
	#approximately one billion with a resolution of 10 decimal
	value = models.DecimalField(max_digits=19, decimal_places=10)

	def __unicode__(self): 	
		return "Done by {0} on galaxy number {1}",format(self.user.username, self.galaxy.uniq_id)

class Identifications(models.Model):
	user = models.ForeignKey(User)
	galaxy = models.ForeignKey('Galaxy')
	galaxytype = models.ForeignKey('GalaxyType')
	redshift = models.DecimalField(max_digits=19, decimal_places=10)
	contaminated = models.BooleanField(default=False)

	def __unicode__(self): 	
		return "{0} is a {1} for {2}",format(self.galaxy.uniq_id, self.galaxytype.name, self.user.username)