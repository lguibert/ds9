#-*- coding: utf-8 -*-
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
# Create your views here.

def home(request):
	text = "<h1>Test résusis!</h1>"
	return HttpResponse(text)

def tpl(request):
	return render(request, 'tpl.html', {'current_date': datetime.now()})

def addition(request, num1, num2):
	total = int(num1) + int(num2)
	return render(request, 'add.html', {'total': total})
