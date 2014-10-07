#-*- coding: utf-8 -*-
import matplotlib
import matplotlib.cm as cm
matplotlib.use('Agg')
matplotlib.rc_file("/etc/matplotlibrc")
import matplotlib.pyplot as plt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
#from django.contrib.auth.models import User
from ds9s.models import Fits
from ds9s.forms import UploadFitsForm
from django.db import IntegrityError
#from django.views.generic import TemplateView, ListView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator

from astropy.io import fits

import numpy as np
import uuid

import pyfits





def homeFits(request):
	fits = Fits.objects.all()
	return render(request,'homeFits.html',locals())


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