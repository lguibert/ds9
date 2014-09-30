from django.db import models

class Users(models.Model):
	ID_USER = models.AutoField(primary_key=True)
	EMAIL_USER = models.EmailField(max_length=254,unique=True)
	PASSWORD_USER = models.CharField(max_length=100)
	FIRSTNAME_USER = models.CharField(max_length=75)
	LASTNAME_USER = models.CharField(max_length=75)
	REGISTRATIONDATE_USER = models.DateTimeField(auto_now_add=True, auto_now=False)
