#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from ds9s.forms import ConnectForm, CreateUserForm, UpdateUserForm
from django.db import IntegrityError
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator

import pdb



@login_required
def myAccount(request):
	user = User.objects.get(id=request.user.id)
	return render(request, 'myaccount.html',locals())

def information(request):
	return render(request, 'information.html',locals())

def gettingStarted(request):
	return render(request, 'gettingStarted.html',locals())

def newUser(request):
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = User()
			user.username = None
			user.email = form.cleaned_data['emailUser']
			user.password = make_password(form.cleaned_data['password'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			
			user.save()	
			try:			
				u = User.objects.latest('id') #get the id of the user
				messages.success(request, u"User saved.")
				return redirect("/ds9s/account/") #redirect to the userpage
			except:
				messages.error(request, u"Error during the saving.")
				return render(request, 'newUser.html',locals())
	else:
		form = CreateUserForm()

	return render(request, 'newUser.html',locals())

@login_required
def updateUser(request):
	formType = True #change the <form> in the template
	data = User.objects.get(id=request.user.id)
	if request.method == 'POST':
		form = UpdateUserForm(request.POST, instance=data)
		if form.is_valid():
			user = User(pk)	
			user.username = None
			user.email = form.cleaned_data['email']

			if form.cleaned_data['password'] != '':
				user.password = make_password(form.cleaned_data['password'])
			else:
				user.password = request.user.password

			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.is_superuser = data.is_superuser
			user.is_staff = data.is_staff
			#user.is_active = data.is_active
			try:
				user.save()
				messages.success(request, u"User updated.")
				return redirect('/ds9s/account/')
			except IntegrityError as e:
				messages.error(request, u"Username already in use")
				return render(request, 'newUser.html',locals())
	else:
		form = UpdateUserForm(instance=data)		
		
	return render(request, 'newUser.html',locals())


def connect(request):
	if not request.user.is_authenticated():
		next = ''

		if request.GET:
			next = request.GET['next']

		if request.method == 'POST':
			to = request.POST.get('next')
			form = ConnectForm(request.POST)
			if form.is_valid():	
				#username = form.cleaned_data['username']
				email = form.cleaned_data['email']
				password = form.cleaned_data['password']
				user = authenticate(username=email, password=password)
				if user:
					login(request, user)
					if next == '':
						return HttpResponseRedirect("/ds9s/")
					else:
						return HttpResponseRedirect(next)		
				else:
					messages.error(request, u"Bad password or the user doesn't exist")				
		else:
			form = ConnectForm()

		return render(request,'connect.html',locals())
	else:
		return redirect('/ds9s/account/')

def deconnect(request):
	logout(request)
	return redirect('/ds9s/')