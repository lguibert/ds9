#-*- coding: utf-8 -*-
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from ds9s.models import Users
from ds9s.forms import LoginForm, CreateUserForm
import hashlib
from django.db import IntegrityError
# Create your views here.

def home(request):
	users = Users.objects.all()
	#return HttpResponse(text);
	return render(request, 'home.html', {'users': users})

def focus(request, id):
	save = request.GET
	if save:
		user = get_object_or_404(Users, id=id)
		return render(request, 'focus.html', {'user': user, 'save':save['save']})
	else:
		user = get_object_or_404(Users, id=id)
		return render(request, 'focus.html', {'user': user})

def tpl(request):
	return render(request, 'tpl.html', {'current_date': datetime.now()})

def addition(request, num1, num2):
	total = int(num1) + int(num2)
	return render(request, 'add.html', {'total': total})

def newUser(request):
	save = False

	if request.method == "POST":
		form = CreateUserForm(request.POST, request.FILES)
		if form.is_valid():
			user = Users()
			user.EMAIL_USER = form.cleaned_data['email']
			user.PASSWORD_USER = form.cleaned_data['password']
			user.PASSWORD_USER = hashlib.md5(str(user.PASSWORD_USER)).hexdigest()
			user.FIRSTNAME_USER = form.cleaned_data['fName']
			user.LASTNAME_USER = form.cleaned_data['lName']
			user.PHOTO_USER = form.cleaned_data['photo']

			try:
				user.save()
				save = True
				u = Users.objects.latest('id') #get the id of the user
				return redirect("/ds9s/view/"+str(u.id)+"?save=1") #redirect to the userpage
			except IntegrityError as e:
				error = "Email already in our database."
				return render(request, 'newUser.html',locals())
	else:
		form = CreateUserForm()

	return render(request, 'newUser.html',locals())



def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data['login']
			password = form.cleaned_data['password']
	else:
		form = LoginForm()

	return render(request,'login.html',locals())