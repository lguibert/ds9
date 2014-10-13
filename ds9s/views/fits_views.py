#-*- coding: utf-8 -*-
import matplotlib
import matplotlib.cm as cm
matplotlib.use('Agg')
matplotlib.rc_file("/etc/matplotlibrc")
import matplotlib.pyplot as plt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
#from django.contrib.auth.models import User
from ds9s.models import Galaxy, ParFolder, Analysis, GalaxyFeatures
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
from os import listdir, makedirs
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
	queryset = Galaxy.objects.values('uniq_id').order_by('uniq_id')
	paginate_by = 5

def makePng(request, file, gal, short_name):
	"""try:
		data = fits.getdata(file)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.plot(data)

		directory = "ds9s/upload/fits_png/"+gal.parfolder.name_par+"/"+str(gal.uniq_id)

		if not exists(directory):
			makedirs(directory)

		fig.savefig(directory+'/'+short_name+'_'+gal.uniq_name+'.png')
		messages.success(request, u"PNG created.")
		return True
	except:
		messages.error(request, u"PNG unable.")
		return False"""
	try:
		inFits=pyfits.open(file)
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

		#plt.ion() # Necessary for interactive Python (ipython) environment
		fig = plt.figure(1,figsize=(xDispSize*1.3,yDispSize*2.5))
		plt.imshow(iData,cmap=cm.Greys_r,origin="lower",aspect=dl/da, extent=(l1,l2,y1,y2)) # Call imshow
		plt.axhline(y=0.0,c='cyan',linestyle=':') # Plot a blue dotted line at distance = 0
		plt.xlabel(r'Wavelength ($\AA$)')
		plt.ylabel('Distance (arcsec)')
		directory = "ds9s/upload/fits_png/"+gal.parfolder.name_par+"/"+str(gal.uniq_id)

		if not exists(directory):
			makedirs(directory)

		fig.savefig(directory+'/'+short_name+'_'+gal.uniq_name+".svg",bbox_inches='tight',pad_inches=0.3)
		inFits.close()
		messages.success(request, u"PNG created.")
		return True
	except:
		messages.error(request, u"PNG unable.")
		return False

def viewGalaxy(request, id):
	gal = get_object_or_404(Galaxy, uniq_id=id)

	try:
		n = int(id) + 1
		next = Galaxy.objects.get(uniq_id=n)
	except:
		next = None
	try:
		p = int(id) -1
		previous = Galaxy.objects.get(uniq_id=p)
	except:
		previous = None

	features = GalaxyFeatures.objects.filter(galaxy_id = gal.id)

	try:
		analysis = Analysis.objects.get(user_id=request.user, galaxy_id=gal.id)
	except ObjectDoesNotExist:
		messages.info(request,'No analysis yet.')

	if not gal.generated:
		gen = []
		checked, checked_short = checkAllFiles(gal.id, gal.parfolder.name_par)
		for index, c in enumerate(checked):
			png = makePng(request, c, gal, checked_short[index])
			#gen.append(png)
		#if not False in gen:
			gal.generated = True
			gal.save()	

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
	checked_short = []
	for f in filesToCheck:
		if exists(f):
			checked.append(f)
			f = split(f,'/')
			f = f[-1]
			f = split(f,'_')
			if len(f[0]) > 5 :
				f = f[1]
			else:
				f = f[0]
			checked_short.append(f)

	return checked, checked_short

#def readCatFile():
	#catdat=np.genfromtxt(p,dtype=np.str)
	#p = file

#only for g102 & g141

def newParFile(request):
	if request.method == 'POST':
		form = NewParFileForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data['name']
			#try:
			if(int(data)): 
#if data is not int (name of the folder), we'll have a exception. So, in except we have the code for the name.
				if(exists(basePath+"Par"+str(data)+"_final")):
					uploaded = uploadParFile(request, "Par"+str(data)+"_final")
					if uploaded:
						return redirect("/ds9s/fits/")
				else:
					messages.error(request, 'No file with this number.')
					return render(request, 'newParFits.html',locals())
			"""except ValueError:
				messages.error(request, 'The value is not a number.')
				return render(request, 'newParFits.html',locals())"""
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

				try:
					addFileDatabase(ids_final, par.id, getTypeSecondFiles())
				except:
					messages.error(request, u"Error during the saveing.")
					par.delete()
					return False;

				messages.success(request, u"File saved in database.")
				return True;
		else:
			messages.error(request, u"File already in database.")
			return False;	

def getTypeSecondFiles():
	toCheck = basePath + grismFolder + f140w
	toCheck2 = basePath + grismFolder + f160w

	if exists(toCheck):
		return True
	elif exists(toCheck2):
		return False

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
	tab = getDataFromCat(par, type)
	for id in ids:	
		#add bdd		
		gal = Galaxy()
		gal.parfolder_id = par
		gal.uniq_id = id
		gal.uniq_name = str(id) + '_' + str(uuid.uuid1()) 
		gal.save()

		#data for each galaxy
		index = getIndexPerId(id, tab[0])
		for x in range(0, 9):
			feat = GalaxyFeatures()
			feat.galaxy_id = gal.id
			feat.galaxyfields_id = x+1
			feat.value = tab[x][index]
			feat.save()
		

def getDataFromCat(par_id, type):	
	parfile = get_object_or_404(ParFolder,id=par_id)		
	cat_file_f = basePath + parfile.name_par + grismFolder + "fin_F110.cat"

	catdat=np.genfromtxt(cat_file_f,dtype=np.str)

	catid=np.array(catdat[0:,1],dtype=np.int)

	catra = np.array(catdat[0:,7],dtype=np.float)
	catdec = np.array(catdat[0:,8],dtype=np.float)
	catmajaxe = np.array(catdat[0:,9],dtype=np.float)
	catminaxe = np.array(catdat[0:,10],dtype=np.float)
	catmagf110 = np.array(catdat[0:,12],dtype=np.float)
	catmagautof110 = np.array(catdat[0:,13],dtype=np.float)


	cat_file = defineNumberCatFile(type)
	cat_file_f = basePath + parfile.name_par + grismFolder + cat_file
	catdat=np.genfromtxt(cat_file_f,dtype=np.str)

	catmagf0 = np.array(catdat[0:,12],dtype=np.float)
	catmagautof0 = np.array(catdat[0:,13],dtype=np.float)

	tab = []
	tab.append(catid)
	tab.append(catra)
	tab.append(catdec)
	tab.append(catmajaxe)
	tab.append(catminaxe)
	tab.append(catmagf110)
	tab.append(catmagautof110)
	tab.append(catmagf0)
	tab.append(catmagautof0)

	return tab

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