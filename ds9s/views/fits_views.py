#-*- coding: utf-8 -*-
import matplotlib
import matplotlib.cm as cm
matplotlib.use('Agg')
matplotlib.rc_file("/etc/matplotlibrc")
import matplotlib.pyplot as plt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
#from django.contrib.auth.models import User
from ds9s.models import Fits, ParFileFits
from ds9s.forms import UploadFitsForm
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

from astropy.io import fits

import numpy as np
import uuid

import pyfits

from string import split
import re
from os import listdir





class ViewHomeFits(ListView):
	model = Fits
	context_object_name = "fits"
	template_name = "homeFits.html"
	paginate_by = 5


def makePng(request, id):
	fit = get_object_or_404(Fits, id=id)
	if fit:
		try:
			file = "/opt/lampp/projects/ds9/ds9s/upload/" + str(fit.file_field)
			data = fits.getdata(file)
			fig = plt.figure()
			ax = fig.add_subplot(111)
			ax.plot(data)
			fig.savefig('ds9s/upload/fits_png/'+fit.uniqname+'.png')
			messages.success(request, u"PNG created.")
			fit.generated = 1
			fit.save()
			return redirect("/ds9s/fits/view/"+id)
		except:
			messages.error(request, u"PNG unable .")
			return redirect("/ds9s/fits/view/"+id)

def viewFits(request,id):
	fit = get_object_or_404(Fits, id=id)
	try:
		file = "/opt/lampp/projects/ds9/ds9s/upload/" + str(fit.file_field)
		data = fits.getdata(file)
	except:
		data = None
	return render(request, 'viewFits.html',locals())



def showFits(request,id,zmin=None,zmax=None): # pathToFits is the pathway to one of the stamps in either the G102_DRIZZLE or G141_DRIZZLE directories
	fit = get_object_or_404(Fits, id=id)
	try :
		pathToFits = "/opt/lampp/projects/ds9/ds9s/upload/" + str(fit.file_field)
		inFits=pyfits.open(pathToFits)
		#inFits.info() # shows contents of the FITS image
		iHdr=inFits[1].header # We will use data from this later
		iData=inFits[1].data # This is the image data

		#print iHdr['CRPIX1'],iHdr['CRVAL1'],iHdr['CDELT1']
		x0,l0,dl=iHdr['CRPIX1'],iHdr['CRVAL1'],iHdr['CDELT1'] # Get the x-pixel coordinate - to - wavelength mapping
		y0,a0,da=iHdr['CRPIX2'],iHdr['CRVAL2'],iHdr['CDELT2'] # Get the y-pixel coordinate - to - distance in arcsec map
		npixx,npixy=iData.shape[1],iData.shape[0] # get the number of pixels in each direction
		l1,l2,y1,y2 = l0-x0*dl, l0+(float(npixx)-x0)*dl, a0-y0*da, a0+(float(npixy)-y0)*da # set the min wavelength, max wavelength, min distance, max distance
	    #print l1,l2,y1,y2

		xDispSize=6.0
		yDispSize=xDispSize*float(npixy)/float(npixx) # Size the image to scale with the image dimensions

		plt.ion() # Necessary for interactive Python (ipython) environment
		plt.figure(1,figsize=(xDispSize*1.3,yDispSize*2.5))
		plt.imshow(iData,cmap=cm.Greys_r,origin="lower",aspect=dl/da, extent=(l1,l2,y1,y2)) # Call imshow
		plt.axhline(y=0.0,c='cyan',linestyle=':') # Plot a blue dotted line at distance = 0
		plt.xlabel(r'Wavelength ($\AA$)')
		plt.ylabel('Distance (arcsec)')
		plt.draw() 
		inFits.close()
		return redirect("/ds9s/fits/view/"+id)
	except:
		messages.error(request, u"Error.")
		return redirect("/ds9s/fits/view/"+id)



def uploadFits(request):
	if request.method == "POST":
		form = UploadFitsForm(request.POST, request.FILES)
		if form.is_valid():
			file = Fits()
			file.name = form.cleaned_data['name']
			file.file_field = form.cleaned_data['upload']
			file.uniqname = uuid.uuid1()
			try:
				file.save()
				f = Fits.objects.latest('id')
				messages.success(request, u"File uploaded & saved.")
				return redirect("/ds9s/fits/view/"+str(f.id))
			except:
				messages.error(request, u"Error during file upload.")
				return render(request, 'uploadFits.html',locals())
	else:
		form = UploadFitsForm()

	return render(request, 'uploadFits.html',locals())


def newParFile(request, name='Par321_final'):
	basePath = "/home/lguibert/test/"
	findIn = "/G102_DRIZZLE"
	findIn2 = "/G141_DRIZZLE"

	fileExist = ParFileFits.objects.filter(name_par=name)
	if not fileExist:
		#get fieldNum
		state = split(name,"_")
		state = state[0]
		fieldNum = state[3:len(state)] #OK

		par = saveParFile(fieldNum, name)
		if par != False :
			#get ID
			expression = r"^aXeWFC3_G102_mef_ID([0-9]+).fits$"
			expression2 = r"^aXeWFC3_G141_mef_ID([0-9]+).fits$"
			
			try:
				addFileDatabase(basePath, name, findIn, expression, par.id)
				addFileDatabase(basePath, name, findIn2, expression2, par.id)
			except:
				messages.error(request, u"Error during the saveing.")
				return redirect("/ds9s/fits/")

			messages.success(request, u"File saved in database.")
			return redirect("/ds9s/fits/")
	else:
		messages.error(request, u"File already in database.")
		return redirect("/ds9s/fits/")

def saveParFile(fieldNum, name):
	try:
		par = ParFileFits()
		par.fieldId_par = fieldNum
		par.name_par = name
		par.save()
		return par
	except:
		return False

def addFileDatabase(basePath, name, findIn, expression, par):
	directory = listdir(basePath + name + findIn)
	for file in directory:
		if re.match(expression, file) is not None:
			state = split(file,"_")
			state = split(state[-1],".")
			state = state[0]
			id = state[2:len(state)]			
			#add bdd
			fit = Fits()
			fit.name = file
			fit.parfilefits_id = par
			fit.uniqname = uuid.uuid1()
			fit.uniq_id = id
			fit.save()