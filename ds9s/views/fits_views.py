#-*- coding: utf-8 -*-
import time
from django.conf import settings
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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils.html import escape

from astropy.io import fits

from math import cos, pi, sin

import numpy as np
import matplotlib.image as mpimg
import uuid

import pyfits

from string import split
import re
from os import listdir, makedirs, remove
from os.path import exists

from six.moves import zip

import pdb

from itertools import repeat

from django.utils.safestring import mark_safe

from bokeh.plotting import *
from bokeh.embed import components
from bokeh.resources import Resources
from bokeh.templates import RESOURCES
from bokeh.utils import encode_utf8
from bokeh.objects import HoverTool
from collections import OrderedDict

import stsci.imagestats as imagestats

import json


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
	template_name = "homeGalaxy.html"
	queryset = Galaxy.objects.values('uniq_id').order_by('uniq_id')
	paginate_by = 15

def viewHomeGalaxy(request):
	galaxy_list = Galaxy.objects.values('uniq_id','id').order_by('uniq_id')
	analysis = Analysis.objects.raw('SELECT COUNT(DISTINCT user_id) as count, galaxy_id, id FROM ds9s_analysis group by galaxy_id')

	aly = {}
	for g in galaxy_list:
		aly[g['id']] = 0
	for a in analysis:
		aly[a.galaxy_id] = a.count

	paginator = Paginator(galaxy_list, 15)
	page = request.GET.get('page')
	try:
		galaxys = paginator.page(page)
	except PageNotAnInteger:
		galaxys = paginator.page(1)
	except EmptyPage:
		galaxys = paginator.page(paginator.num_pages)

	return render(request, 'homeGalaxy.html',locals())

def test(request):
	return render(request, 'test.html',locals())

def wavelenghing(request, id, redshift):
	gal = Galaxy.objects.get(uniq_id=id)

	checked, checked_short = checkAllFiles(gal.uniq_id, gal.parfolder.name_par)

	g1script, g1div = displayGImage(request, checked[0],checked_short[0],redshift)
	g2script, g2div = displayGImage(request, checked[1],checked_short[1],redshift)

	#return f110script, f110div, f160script, f160div
	data = g1script, g1div, g2script, g2div
	return HttpResponse(json.dumps(data))

@login_required
def scaling(request, id, val, color):
	#pdb.set_trace()
	gal = Galaxy.objects.get(uniq_id=id)

	checked, checked_short = checkAllFiles(gal.uniq_id, gal.parfolder.name_par)

	f110script, f110div = displayFImage(request, checked[2], gal, checked_short[2], val, color)
	f160script, f160div = displayFImage(request, checked[3], gal, checked_short[3], val, color)

	#return f110script, f110div, f160script, f160div
	data = f110script, f110div, f160script, f160div
	return HttpResponse(json.dumps(data))

def displayFImage(request, file, gal, short_name, val, color="Greys-9"):
	val = int(val)
	features = GalaxyFeatures.objects.filter(galaxy_id=gal.id).order_by('galaxyfields_id')
	raCenter = float(features[0].value)
	decCenter = float(features[1].value)

	inFits=pyfits.open(file)
	iHdr=inFits[1].header
	iData=inFits[1].data


	# Get parameters for converting Pixel Coordinates to Celestial Coordinates: Right ascension (RA) and Declination (Dec)
	x0,y0,ra0,dec0,drdx,drdy,dddx,dddy,fieldRotation=iHdr["CRPIX1"],iHdr["CRPIX2"],iHdr["CRVAL1"],iHdr["CRVAL2"],iHdr["CD1_1"],iHdr["CD1_2"],iHdr["CD2_1"],iHdr["CD2_2"],iHdr["ORIENTAT"]
	    
	fieldRotation=-1.*fieldRotation 
	pixScaleR,pixScaleD=(drdy**2+drdx**2)**0.5 * 3600., (dddy**2+dddx**2)**0.5 * 3600. 
	xcen = (raCenter-ra0)*cos(dec0*pi/180.)*3600./pixScaleR*-1.*cos(pi*fieldRotation/180.)+(decCenter-dec0)*3600./pixScaleD*-1.*sin(pi*fieldRotation/180.)+x0 # OK, this transformation seems to get closest
	ycen = (raCenter-ra0)*cos(dec0*pi/180.)*3600./pixScaleR*-1.*sin(pi*fieldRotation/180.)+(decCenter-dec0)*3600./pixScaleD*1.*cos(pi*fieldRotation/180.)+y0 # OK, this transformation seems to get closest

	iFocusBoundaries=imSubarrayBoundaries(iData.shape,xcen,ycen,val)
	# make the subarray with the new boundaries
	#iFocus = iData[xcen-val:xcen+val,ycen-val:ycen+val]
	iFocus = iData[iFocusBoundaries[0]:iFocusBoundaries[1],iFocusBoundaries[2]:iFocusBoundaries[3]]

	script, div = createBokehImage(iFocus,iFocusBoundaries,800,800, short_name, xcircle=xcen, ycircle=ycen, color=color, val=val)

	return script, div

def displayGImage(request, file, short_name, redshift):
	inFits=pyfits.open(file)
	iHdr=inFits[1].header
	iData=inFits[1].data


	# Get parameters for converting Pixel Coordinates to Celestial Coordinates: Right ascension (RA) and Declination (Dec)
	x0,l0,dl=iHdr['CRPIX1'],iHdr['CRVAL1'],iHdr['CDELT1'] # Get the x-pixel coordinate - to - wavelength mapping
	y0,a0,da=iHdr['CRPIX2'],iHdr['CRVAL2'],iHdr['CDELT2'] # Get the y-pixel coordinate - to - distance in arcsec map
	npixx,npixy=iData.shape[1],iData.shape[0] # get the number of pixels in each direction
	#l1,l2,y1,y2 = l0-x0*dl, l0+(float(npixx)-x0)*dl, a0-y0*da, a0+(float(npixy)-y0)*da

	xDispSize=6.0
	yDispSize=xDispSize*float(npixy)/float(npixx)

	dataBoundaries = grismBoundaries([iData.shape[0],iData.shape[1]],iHdr)

	script, div = createBokehImage(iData, dataBoundaries,865,300,short_name, type=False,redshift=redshift)

	return script, div

def remapPixels(data, minpex=None, maxpex=None):
	datastat = imagestats.ImageStats(data,nclip=3)
	if minpex == None:
		minpex = datastat.mean
	if maxpex == None:
		maxpex = datastat.mean + 10 * datastat.stddev

	m = 1 / (maxpex - minpex)
	b = minpex * -1 / (maxpex - minpex)

	data = data * m + b

	data[data<0]=0
	data[data>1]=1

	return data

def imSubarrayBoundaries(fullImageDataShape,xCenter,yCenter,halfSize):
	#fullImageDataShape is the iData.shape
	#xCenter is the x-coordinate of the relevant galaxy/star in the full image
	#yCenter is the x-coordinate of the relevant galaxy/star in the full image
	#halfSize is the val set by the slider and equivalent to half the size
	xCenter, yCenter, halfSize = int(xCenter), int(yCenter), int(halfSize)
	subArrayLeft,subArrayRight,subArrayBottom,subArrayTop = xCenter - halfSize, xCenter + halfSize, yCenter - halfSize, yCenter + halfSize 
	if subArrayLeft < 0: 
		subArrayLeft = 0
	if subArrayRight >= fullImageDataShape[1] - 1:
		 subArrayRight = fullImageDataShape[1] - 1
	if subArrayBottom < 0:
		subArrayBottom = 0
	if subArrayTop >=  fullImageDataShape[0] - 1:
		subArrayTop = fullImageDataShape[0] - 1
	#return (subArrayLeft,subArrayRight,subArrayBottom,subArrayTop)
	return (subArrayBottom,subArrayTop,subArrayLeft,subArrayRight)

def grismBoundaries(grismStampShape,grismStampHeader):
    # given the shape of the array and the fits header, calculate the minimum and maximum wavelengths and the vertical scale in arcseconds
    iHdr = grismStampHeader
    x0,l0,dl=iHdr['CRPIX1'],iHdr['CRVAL1'],iHdr['CDELT1'] # Get the x-pixel coordinate - to - wavelength mapping
    y0,a0,da=iHdr['CRPIX2'],iHdr['CRVAL2'],iHdr['CDELT2'] # Get the y-pixel coordinate - to - distance in arcsec map
    npixx,npixy=grismStampShape[1],grismStampShape[0] # get the number of pixels in each direction
    l1,l2,y1,y2 = l0-(x0)*dl, l0+(float(npixx)-x0)*dl, a0-(y0)*da, a0+(float(npixy)-y0)*da # set the min wavelength, max wavelength, min distance, max distance
    return (l1,l2,y1,y2) # again, we will use these as the coordinate boundaries for the plots.



def createBokehImage(data, dataBoundaries, plot_width, plot_height, title, type=True, redshift=0 ,xcircle=0, ycircle=0, color="Greys-9",val=100):
	TOOLS="pan,wheel_zoom,box_zoom,reset"

	data = remapPixels(data)

	img = image(image=[data], 
		x_range=[dataBoundaries[0], dataBoundaries[1]], # range of x-values in the Display
		y_range=[dataBoundaries[2], dataBoundaries[3]], # range of y-values in the Display
		x=dataBoundaries[0], # x-coordinate of Origin of display 
		y=dataBoundaries[2], # y-coordinate of Origin of display
		dw=dataBoundaries[1]-dataBoundaries[0], # number of image pixels in x-range of display
		dh=dataBoundaries[3]-dataBoundaries[2], # number of image pixels in y-range of display
		tools=TOOLS,
		palette=[color],
		title=title,
		plot_width=plot_width, # size of the diplay in Screen Pixels
		plot_height=plot_height, # size of the display in Screen pixels
	)

	hold()
	if type:
		annulus([ycircle],xcircle,9.9,10,fill_color="#df1c1c", line_color="#df1c1c")
	else:
		y = [-2,2]
		#creation emition lines
		emlineWavelengthsRest = np.array([3727., 3869., 4861., 4959., 5007., 6563., 6727., 9069., 9532., 10830.])
		emlineNames = np.array(["[O II]","[Ne III]","Hbeta","[O III]","[O III]","Halpha","[S II]","[S III]","[S III]","He I"]) # Can be used to label the vertical lines
		
		for index, em in enumerate(emlineWavelengthsRest):
			emlineWavelengths = em * (1.0 + float(redshift))
			lin = line([emlineWavelengths,emlineWavelengths],y,color="#df1c1c",line_width=2)
			text([emlineWavelengths+20],calculatePositionText(index),emlineNames[index],0,text_color="#df1c1c")	
			
	resources = Resources("inline")

	plot_script, plot_div = components(img, resources)

	html_script = mark_safe(encode_utf8(plot_script))
	html_div = mark_safe(encode_utf8(plot_div))

	figure()

	return html_script, html_div

def calculatePositionText(value):
	value = float(value)/5 + 0.5
	if value > 1.0:
		value = value - 1
	return value

def getPrevGalaxy(id):
	previous = None

	while(previous == None):
		id = int(id) - 1
		if id > 0:
			try:
				previous = Galaxy.objects.get(uniq_id=id)
			except:
				previous = None
		else:
			break;

	return previous

def getNextGalaxy(id):
	next = None

	latest = Galaxy.objects.latest('uniq_id').uniq_id
	while(next == None):
		id = int(id) + 1
		if id < latest:
			try:
				next = Galaxy.objects.get(uniq_id=id)
			except:
				next = None
		else:
			break;

	return next

def getColors():
	return json.load(open('/opt/lampp/www/ds9/ds9s/assets/colors.json'))

@login_required
def viewGalaxy(request, id):
	gal = get_object_or_404(Galaxy, uniq_id=id)
	colors = getColors()

	val = 100
	redshift = 0

	next = getNextGalaxy(id)
	previous = getPrevGalaxy(id)

	features = GalaxyFeatures.objects.filter(galaxy_id = gal.id)

	try:
		analysis = Analysis.objects.filter(user_id=request.user, galaxy_id=gal.id)
	except ObjectDoesNotExist:
		messages.info(request,'No analysis yet.')

	checked, checked_short = checkAllFiles(gal.uniq_id, gal.parfolder.name_par)
		
	#directory = settings.MEDIA_ROOT + "/fits_png/" + gal.parfolder.name_par + "/"
	
	
	f110script, f110div = displayFImage(request, checked[2], gal, checked_short[2], val)				
	
	f160140script, f160140div = displayFImage(request, checked[3], gal,checked_short[3], val)

	g1script, g1div = displayGImage(request, checked[0],checked_short[0],redshift)
	g2script, g2div = displayGImage(request, checked[1],checked_short[1],redshift)

	

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

@login_required
def newParFile(request):
	if request.method == 'POST':
		form = NewParFileForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data['name']
			try:
				if(int(data)): 
					if(exists(basePath+"Par"+str(data)+"_final")):
						uploaded = uploadParFile(request, "Par"+str(data)+"_final")
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
		for x in range(1, 9):
			feat = GalaxyFeatures()
			feat.galaxy_id = gal.id
			feat.galaxyfields_id = x
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
	tab.append(catra) #1
	tab.append(catdec)#2
	tab.append(catmajaxe)#3
	tab.append(catminaxe)#4
	tab.append(catmagf110)#5
	tab.append(catmagautof110)#6
	tab.append(catmagf0)#7
	tab.append(catmagautof0)#8

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