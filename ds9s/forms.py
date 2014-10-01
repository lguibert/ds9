from django import forms

class LoginForm(forms.Form):
	login = forms.EmailField(label=u'Your mail')
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_login(self):
		cleaned_data = super(LoginForm, self).clean()
		login = cleaned_data.get('login')

		if login:
			if "bob" in login:
				msg = u"No Bob allowed here!"
				self._errors['login'] = self.error_class([msg])
				del cleaned_data['login']

		return cleaned_data


class CreateUserForm(forms.Form):
	email = forms.EmailField(label=u'Your mail (will be your login)')
	password = forms.CharField(widget=forms.PasswordInput)
	passwordCheck = forms.CharField(widget=forms.PasswordInput, label=u"Password confirmation")
	fName = forms.CharField(label=u"First name")
	lName = forms.CharField(label=u"Last name")
	photo = forms.ImageField()

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

		



