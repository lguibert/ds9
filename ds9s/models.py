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

	def __unicode__(self):
		return self.name

class Analysis(models.Model):
	user = models.ForeignKey(User)
	galaxy = models.ForeignKey('Galaxy')
	date_done = models.DateTimeField(auto_now_add=True, auto_now=False)
	#approximately one billion with a resolution of 10 decimal
	redshift = models.DecimalField(max_digits=19, decimal_places=10)
	#many more are comming

	def __unicode__(self): 	
		return "Done by {0} on galaxy number {1}",format(self.user.username, self.galaxy.uniq_id)
