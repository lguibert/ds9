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

@login_required
def focus(request, id):
	save = request.GET
	if save:
		user = get_object_or_404(User, id=id)
		return render(request, 'focus.html', {'user': user, 'save':save['save']})
	else:
		user = get_object_or_404(User, id=id)
		return render(request, 'focus.html', {'user': user})

def newUser(request):
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = User()
			user.username = form.cleaned_data['username']
			user.email = form.cleaned_data['email']
			user.password = make_password(form.cleaned_data['password'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			try:
				user.save()				
				u = User.objects.latest('id') #get the id of the user
				messages.success(request, u"User saved.")
				return redirect("/ds9s/view/"+str(u.id)+"?save=1") #redirect to the userpage
			except IntegrityError as e:
				messages.error(request, u"Email already in our database.")
				return render(request, 'newUser.html',locals())
	else:
		form = CreateUserForm()

	return render(request, 'newUser.html',locals())

@login_required
@permission_required('ds9s.update_user')
def updateUser(request, pk):
	formType = True #change the <form> in the template
	data = User.objects.get(id=pk)
	if request.method == 'POST':
		form = UpdateUserForm(request.POST, instance=data)
		if form.is_valid():
			user = User(pk)	
			user.username = form.cleaned_data['username']
			user.email = form.cleaned_data['email']
			user.password = make_password(form.cleaned_data['password'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.is_superuser = data.is_superuser
			user.is_staff = data.is_staff
			#user.is_active = data.is_active
			try:
				user.save()
				messages.success(request, u"User updated.")
				return redirect('/ds9s/view/'+pk)
			except IntegrityError as e:
				messages.error(request, u"Username already in use")
				return render(request, 'newUser.html',locals())
	else:
		form = UpdateUserForm(instance=data)		
	
	return render(request, 'newUser.html',locals())


def connect(request):
	next = ''

	if request.GET:
		next = request.GET['next']

	if request.method == 'POST':
		to = request.POST.get('next')
		form = ConnectForm(request.POST)
		if form.is_valid():	
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
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

def deconnect(request):
	logout(request)
	return redirect('/ds9s/')




class ViewHome(ListView):
	model = User
	context_object_name = "users"
	template_name = "home.html"
	#paginate_by = 3
	#queryset = Users.objects.filter(role_id=1) #{can add some filter with queryset}


class DeleteUser(DeleteView):
	model = User
	context_object_name = "u"
	template_name = "delete.html"
	success_url = "/ds9s/"

	@method_decorator(login_required)
	@method_decorator(permission_required('ds9s.user_delete',login_url='/ds9s/'))
	def dispatch(self, *args, **kwargs):
		return super(DeleteUser, self).dispatch(*args, **kwargs)

