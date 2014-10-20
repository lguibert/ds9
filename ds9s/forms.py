from django import forms
from django.contrib.auth.models import User
from ds9s.models import Galaxy
from string import split
from django.utils.safestring import mark_safe

class ConnectForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
	username = forms.CharField(label="Your username")
	password = forms.CharField(widget=forms.PasswordInput)
	passwordCheck = forms.CharField(widget=forms.PasswordInput, label=u"Password confirmation")
	email = forms.EmailField(label=u'Your mail')	
	first_name = forms.CharField(label=u"First name")
	last_name = forms.CharField(label=u"Last name")

	def clean_passwordCheck(self):
		cleaned_data = super(CreateUserForm, self).clean()
		password = cleaned_data.get('password')
		passwordCheck = cleaned_data.get('passwordCheck')
		if password and passwordCheck :
			if password != passwordCheck:
				msg = u"Passwords aren't the same."
				self._errors['password'] = self.error_class([msg])
				del cleaned_data['passwordCheck']
				del cleaned_data['password']

		return cleaned_data

class UpdateUserForm(forms.ModelForm):
	username = forms.CharField(label="Your username")
	password = forms.CharField(widget=forms.PasswordInput)
	passwordCheck = forms.CharField(widget=forms.PasswordInput, label=u"Password confirmation")
	email = forms.EmailField(label=u'Your email')	
	first_name = forms.CharField(label=u"First name")
	last_name = forms.CharField(label=u"Last name")

	class Meta:
		model = User
		fields = ()

	def clean_passwordCheck(self):
		cleaned_data = super(UpdateUserForm, self).clean()
		password = cleaned_data.get('password')
		passwordCheck = cleaned_data.get('passwordCheck')
		if password and passwordCheck :
			if password != passwordCheck:
				msg = u"Passwords aren't the same."
				self._errors['password'] = self.error_class([msg])
				del cleaned_data['passwordCheck']
				del cleaned_data['password']


class NewParFileForm(forms.Form):
	name = forms.CharField(label=mark_safe("Number of the Par<span class='precision'>XXX</span>"))

class UploadFitsForm(forms.Form):
	name = forms.CharField(label="File's name")
	upload = forms.FileField(label="File (only .fits)")

	def clean_uploadFile(self):
		cleaned_data = super(UploadFitsForm, self).clean()
		file = cleaned_data.get('upload')
		if file:
			ext = str(file).split(".")
			if ext[-1] != "fits":
				msg = u"File much be at .fits format."
				self._errors['upload'] = self.error_class([msg])
				del cleaned_data['upload']