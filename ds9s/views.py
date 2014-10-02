#-*- coding: utf-8 -*-
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from ds9s.forms import ConnectForm, CreateUserForm
from django.db import IntegrityError
from django.views.generic import TemplateView, ListView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# Create your views here.

"""def home(request):
	users = Users.objects.all()
	#return HttpResponse(text);
	return render(request, 'home.html', {'users': users})
"""
@login_required
def focus(request, id):
	save = request.GET
	if save:
		user = get_object_or_404(User, id=id)
		return render(request, 'focus.html', {'user': user, 'save':save['save']})
	else:
		user = get_object_or_404(User, id=id)
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
			user = User()
			user.username = form.cleaned_data['username']
			user.email = form.cleaned_data['email']
			user.password = make_password(form.cleaned_data['password'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			try:
				user.save()
				save = True
				u = User.objects.latest('id') #get the id of the user
				return redirect("/ds9s/view/"+str(u.id)+"?save=1") #redirect to the userpage
			except IntegrityError as e:
				error = "Email already in our database."
				return render(request, 'newUser.html',locals())
	else:
		form = CreateUserForm()

	return render(request, 'newUser.html',locals())



def connect(request):
	error = False
	if request.method == 'POST':
		to = request.POST.get('next')
		form = ConnectForm(request.POST)
		if form.is_valid():			
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return render(request,'test.html',locals())
			else:
				error = True
	else:
		form = ConnectForm()

	return render(request,'connect.html',locals())

def deconnect(request):
	logout(request)
	return redirect('/ds9s/')




class ViewHome(ListView):
	model = User
	context_object_name = "users"
	template_name = "home.html"
	paginate_by = 1
	#queryset = Users.objects.filter(role_id=1) #{can add some filter with queryset}
"""
class FocusUser(DetailView):
	model = Users
	context_object_name = "u"
	template_name = "focus.html


class CreateUser(CreateView):
	model = Users
	template_name = "newUser.html"
	form_class = CreateUserModForm
	#success_url = ""


class UpdateUser(UpdateView):
	model = Users
	template_name = "newUser.html"
	form_class = CreateUserModForm
	#success_url = ""
"""

class DeleteUser(DeleteView):
	model = User
	context_object_name = "u"
	template_name = "delete.html"
	success_url = "/ds9s/"

