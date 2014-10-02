from django.db import models
"""
class Users(models.Model):
	EMAIL_USER = models.EmailField(max_length=254,unique=True)
	PASSWORD_USER = models.CharField(max_length=100)
	FIRSTNAME_USER = models.CharField(max_length=76)
	LASTNAME_USER = models.CharField(max_length=75)
	REGISTRATIONDATE_USER = models.DateTimeField(auto_now_add=True, auto_now=False)
	PHOTO_USER = models.ImageField(upload_to="user/", null=True)
	active = models.BooleanField(default=True)
	role = models.ForeignKey('Roles', null=True)

	def __unicode__(self):
		return self.EMAIL_USER


class Roles(models.Model):
	NAME_ROLE = models.CharField(max_length=75)

	def __unicode__(self):
		return self.NAME_ROLE
"""