#-*- coding: utf-8 -*-
import matplotlib
import matplotlib.cm as cm
matplotlib.use('Agg')
matplotlib.rc_file("/etc/matplotlibrc")
import matplotlib.pyplot as plt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
#from django.contrib.auth.models import User
from ds9s.models import Galaxy, ParFolder, Analysis
from ds9s.forms import UploadFitsForm, NewParFileForm
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.db.models import Count

from astropy.io import fits

import numpy as np
import uuid

import pyfits

from string import split
import re
from os import listdir
from os.path import exists

import pdb
from django.db.models import Q

#------------------ GLOBAL VARIABLES --------------------------------
basePath = "/home/lguibert/test/"

findIn = "/G102_DRIZZLE/"
findIn2 = "/G141_DRIZZLE/"

grismFolder = '/DATA/DIRECT_GRISM/'

expression = r"^aXeWFC3_G102_mef_ID([0-9]+).fits$"
expression2 = r"^aXeWFC3_G141_mef_ID([0-9]+).fits$"

f110w = "F110W_rot_drz.fits"
f160w = "F160W_rot_drz.fits"
f140w = "F140W_rot_drz.fits"
#--------------------------------------------------------------------


class ViewHomeFits(ListView):
	model = Galaxy
	context_object_name = "galaxys"
	template_name = "homeFits.html"
	queryset = Galaxy.objects.values('uniq_id').order_by('uniq_id').annotate(Count('uniq_id'))
	paginate_by = 5

def makePng(request, id):
	fit = get_object_or_404(Galaxy, id=id)
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

def viewGalaxy(request, id):
	gal = get_object_or_404(Galaxy, uniq_id=id)

	try:
		analysis = Analysis.objects.get(user_id=request.user, galaxy_id=gal.id)
	except ObjectDoesNotExist:
		messages.info(request,'No analysis yet.')

	checked = checkAllFiles(gal.id, gal.parfolder.name_par)


	return render(request, 'viewGalaxy.html',locals())

def checkAllFiles(gal_id, par_name):
	base = basePath + par_name 
	g102 =  base + findIn + "aXeWFC3_G102_mef_ID"+str(gal_id)+".fits"
	g141 = base + findIn2 + "aXeWFC3_G141_mef_ID"+str(gal_id)+".fits"

	base_grism = base + grismFolder
	f110w_f = base_grism + f110w
	f160w_f = base_grism + f160w
	f140w_f = base_grism + f140w


	filesToCheck = [g102,g141,f110w_f,f140w_f,f160w_f]
	#filesToCheck = {'g102':g102,'g141':g141,'f110w':f110w_f,'f140':f140w_f,'f160w':f160w_f}
	checked = []
	for f in filesToCheck:
		if exists(f):
			checked.append(f)

	return checked

#def readCatFile():
	#catdat=np.genfromtxt(p,dtype=np.str)
	#p = file

#only for g102 & g141
def showFits(request, id, pathToFits, zmin=None, zmax=None): # pathToFits is the pathway to one of the stamps in either the G102_DRIZZLE or G141_DRIZZLE directories
	try : 
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
		return redirect("/ds9s/fits/view/"+str(id))
	except:
		messages.error(request, u"Error.")
		return redirect("/ds9s/fits/view/"+str(id))

def newParFile(request):
	if request.method == 'POST':
		form = NewParFileForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data['name']
			try:
				if(int(data)): 
#if data is not int (name of the folder), we'll have a exception. So, in except we have the code for the name.
					if(exists(basePath+"Par"+data+"_final")):
						uploaded = uploadParFile(request, "Par"+data+"_final")
						if uploaded:
							return redirect("/ds9s/fits/")
					else:
						messages.error(request, 'No file with this number.')
						return render(request, 'newParFits.html',locals())
			except ValueError:
				messages.error(request, 'The value is not a number.')
				return render(request, 'newParFits.html',locals())
		else:
			messages.error(request, 'Error in the file.')
			return render(request, 'newParFits.html',locals())
	else:
		form = NewParFileForm()

	return render(request, 'newParFits.html',locals())


def uploadParFile(request, name=None):
	if name is None:
		messages.error('Error in the folder\'s name')
		return redirect("/ds9s/fits/newParFile/")
	else:
		fileExist = ParFolder.objects.filter(name_par=name)
		if not fileExist:
			#get fieldNum
			state = split(name,"_")
			state = state[0]
			fieldNum = state[3:len(state)]

			par = saveParFile(fieldNum, name)
			if par != False :
				#process of check and add
				#get ID
				ids1 = getUniqIdFromFile(name, findIn, expression)
				ids2 = getUniqIdFromFile(name,findIn2,expression2)

				ids_final = checkFilesGtype(ids1,ids2)

				try :
					addFileDatabase(ids_final, par.id)
				except:
					messages.error(request, u"Error during the saveing.")
					par.delete()
					return False;

				messages.success(request, u"File saved in database.")
				return True;
		else:
			messages.error(request, u"File already in database.")
			return False;			

def saveParFile(fieldNum, name):
	try:
		par = ParFolder()
		par.fieldId_par = fieldNum
		par.name_par = name
		par.save()
		return par
	except:
		return False


def getUniqIdFromFile(name, fIn, exp):
	ids = []
	directory = listdir(basePath + name + fIn)
	for file in directory:
		if re.match(exp, file) is not None:
			state = split(file,"_")
			state = split(state[-1],".")
			state = state[0]
			id = state[2:len(state)]
			ids.append(id)
	return ids	

def checkFilesGtype(ids1, ids2):
	ids_final = []
	#ids_wrong = []?
	for i in ids1:
		if i in ids2:
			ids_final.append(i)
		#else:
			#ids_wrong.append(i)
	return ids_final#,ids_wrong

def addFileDatabase(ids, par, type):
	catid, catra, catdec, catmajaxe, catminaxe, catmagf110, catmagautof110, catmagf0, catmagautof0 = getDataFromCat(par, type)
	for id in ids:	
		#add bdd
		index = getIndexPerId(id, catid)
		gal = Galaxy()
		gal.parfolder_id = par
		gal.uniq_id = id
		gal.save()

		feat = GalaxyFeatures()
		feat.ga

def getDataFromCat(parfile, type):			
	cat_file_f = basePath + parfile + grismFolder + "fin_F110.cat"

	catdat=np.genfromtxt(cat_file_f,dtype=np.str)

	catid=np.array(catdat[0:,1],dtype=np.int)

	catra = np.array(catdat[0:,7],dtype=np.float)
	catdec = np.array(catdat[0:,8],dtype=np.float)
	catmajaxe = np.array(catdat[0:,9],dtype=np.float)
	catminaxe = np.array(catdat[0:,10],dtype=np.float)
	catmagf110 = np.array(catdat[0:,12],dtype=np.float)
	catmagautof110 = np.array(catdat[0:,13],dtype=np.float)


	cat_file = defineNumberCatFile(type)
	cat_file_f = basePath + parfile + grismFolder + cat_file
	catdat=np.genfromtxt(cat_file_f,dtype=np.str)

	catmagf0 = np.array(catdat[0:,12],dtype=np.float)
	catmagautof0 = np.array(catdat[0:,13],dtype=np.float)

	return catid, catra, catdec, catmajaxe, catminaxe, catmagf110, catmagautof110, catmagf0, catmagautof0

def getIndexPerId(id, ids):
	ids_normal = []
	for i in ids:
		ids_normal.append(i)

	return ids_normal.index(int(id))

def defineNumberCatFile(type):
	if type:
		return "fin_F140.cat"
	else:
		return "fin_F160.cat"