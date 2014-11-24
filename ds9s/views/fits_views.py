#-*- coding: utf-8 -*-
from django.conf import settings
import matplotlib
import matplotlib.cm as cm
matplotlib.use('Agg')
matplotlib.rc_file("/etc/matplotlibrc")
import matplotlib.pyplot as plt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from ds9s.models import Galaxy, ParFolder, Analysis, EmissionLineFields, EmissionLine, GalaxyFeatures, GalaxyTypes, Identifications
from ds9s.forms import UploadFitsForm, NewParFileForm
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator
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

from scipy.signal import convolve, boxcar, gaussian
from scipy.interpolate import interp1d

import pdb

from django.utils.safestring import mark_safe

from bokeh.plotting import *
from bokeh.embed import components
from bokeh.resources import Resources
from bokeh.utils import encode_utf8

import stsci.imagestats as imagestats

import json


#-------------------------------- GLOBAL VARIABLES --------------------------------
basePath = "/home/lguibert/test/" #folder where all the ParXXX are

findIn = "/G102_DRIZZLE/"
findIn2 = "/G141_DRIZZLE/"

grismFolder = '/DATA/DIRECT_GRISM/'

expression = r"^aXeWFC3_G102_mef_ID([0-9]+).fits$"
expression2 = r"^aXeWFC3_G141_mef_ID([0-9]+).fits$"
f110w = "F110W_rot_drz.fits"
f160w = "F160W_rot_drz.fits"
f140w = "F140W_rot_drz.fits"

datFolder = "/Spectra/"
minG102 = 7900.
maxG102 = 11700.
minG141 = 11000.
maxG141 = 17500.

redshiftDefault = 1 #default redshift's value. Will be use for the bokeh image
scalingDefault = 150 #default zoom. Will be use for the bokeh image
crossColor = "lime"

TOOLS="pan,wheel_zoom,box_zoom,reset" #all the tools for the bokeh images

emlineWavelengthsRest = np.array([3727., 3869., 4861., 4959., 5007., 6563., 6727., 9069., 9532., 10830.])
emlineNames = ["[O II]","[Ne III]","Hbeta","[O III]","[O III]","Halpha","[S II]","[S III]","[S III]","He I"]
#            [O II]      [Ne III] Hbeta       [O III]        [O III]      Halpha     [S II]     [S III]               [S III]       He I
colors = ["indianred","steelblue","indigo","orange","orange","darkred","darkorchid","palevioletred","palevioletred","yellowgreen"]
#----------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------ VIEW DISPLAY ----------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#This function is for displaying the home page. 
def viewHomeGalaxy(request):
	galaxy_list = Galaxy.objects.values('uniq_id','id','uniq_name','parfolder').order_by('uniq_id') #get here all the needed information from galaxys
	analysis = Analysis.objects.raw('SELECT COUNT(DISTINCT user_id) as count, galaxy_id, id FROM ds9s_analysis group by galaxy_id') #how many analysis was done on galaxys
	
	#here, we just create a dictionnary with for key the galaxy's id and the number of analysis for value
	aly = {}
	for g in galaxy_list:
		aly[g['id']] = 0
	for a in analysis:
		aly[a.galaxy_id] = a.count

	#Django stuff to create pages
	paginator = Paginator(galaxy_list, 15)
	page = request.GET.get('page')
	try:
		galaxys = paginator.page(page)
	except PageNotAnInteger:
		galaxys = paginator.page(1)
	except EmptyPage:
		galaxys = paginator.page(paginator.num_pages)

	#send all the previous values to the homeGalaxy template
	return render(request, 'homeGalaxy.html',locals())


@login_required
def test(request):
	return render(request, 'test.html',locals())

#A simple function to find the galaxy with a unique name. If the name isn't defined any galaxy, the return is none.
def getGalaxyByUniqName(name):
	try:
		gal = Galaxy.objects.get(uniq_name=name)
	except:
		gal = None

	return gal

#This function is basicly the same as the previous one. But, we just return the uid and the folderid. It's useful in the code
def getGalaxyInfodByUniqName(name):
	try:
		gal = Galaxy.objects.get(uniq_name=name)
		uid = gal.uniq_id
		fieldId = gal.parfolder.fieldId_par
		parId = gal.parfolder.id
	except:
		uid = None
		fieldId = None
		parId = None

	return uid, fieldId, parId


def getNextParFolder(user_id):
	parfolder = None
	act = None
	try:
		last_iden = Identifications.objects.filter(user_id=user_id).order_by('-id')[0]

		if last_iden:
			objects = openQueueFile(last_iden.galaxy.parfolder.fieldId_par)
			lastobject = objects[-1]

			if str(lastobject[2]) == str(last_iden.galaxy.uniq_id):
				parfolder = getNextParFolderByAct(last_iden.galaxy.parfolder_id)
			else:
				parfolder = last_iden.galaxy.parfolder
				act = getIndexObjectById(objects, last_iden.galaxy.uniq_id)
		else:
			parfolder = getOlderParFolder()

	except:
		parfolder = getOlderParFolder()

	return parfolder, act

def getNextParFolderByAct(act_id):
	next = None
	i = 1
	biggerIdParfolder = ParFolder.objects.order_by("-id")[0]

	while next == None:
		try:
			value = int(act_id)+i
			if value > biggerIdParfolder.id:
				break
			else:
				par = ParFolder.objects.get(id=value)
				next = par
		except:
			i += 1

	return next

#Here, we just get the older parFolder. We need this to define on witch folder the user will work first.
def getOlderParFolder():
	try:
		parfolder = ParFolder.objects.order_by('date_upload')[0]
	except:
		parfolder = None

	return parfolder

#The function return the ParXXX file with the data about the queue. 
def openQueueFile(fieldId):
	return np.genfromtxt(createPathParDat(fieldId), dtype=np.str)

def getNextIndexQueue(objects, act):
	next = None
	actual = objects[act]

	for i, obj in enumerate(objects):
		if i > act:
			if obj[2] != actual[2]:
				next = i
				break

	return next



#the most important function in this file. This one is called each time the user will want to access to a galaxy's page.
#More informations with the comments in the function
@login_required
def viewGalaxy(request, name=None): #name is in default at none because we need a begging for the queue.
	if name == None:
		parfolder, act = getNextParFolder(request.user.id) #we take the older folder
		if parfolder == None:
			messages.error(request,"You did all the available galaxy.")
			return redirect("/ds9s/account/reviews/")
		else:
			objects = openQueueFile(parfolder.fieldId_par)#open the relative file
			#get all what we need to display the page
			if act == None:
				act = firstObjectInFile(request, parfolder.fieldId_par, parfolder.id)
			else:
				act = getNextIndexQueue(objects, act)

			gal, next, wavelenghts = queue(request, objects, parfolder.fieldId_par, parfolder.id, act=act)
	else:
		uid, parfolderId, parId = getGalaxyInfodByUniqName(name) #get the galaxy with the name
		if uid != None and parfolderId != None: #if we have something
			objects = openQueueFile(parfolderId) #open the queue file
			act = getIndexObjectById(objects, str(uid)) #get the index in the file for the uniq_id
			if act == None: #if we don't have a index
				return HttpResponseRedirect("/ds9s/") #redirect the user on home page
			else:
				gal, next, wavelenghts = queue(request, objects, parfolderId, parId, act=act)#else, get the galaxy in the queue
		else:
			return HttpResponseRedirect("/ds9s/")

	check = getIdentificationUser(gal.id, request.user.id) #here, we just take the user's previous review on this galaxy

	if check: #if there is a previous review
		if check.redshift: #if the review has a redshift value
			redshift = check.redshift #we take the value for the galaxy's redshift
		else:
			redshift = redshiftDefault #else, we take the default value
	else:
		redshift = redshiftDefault #same thing

	colors = getColors() #we take all the colors for the images

	request.session['unameGal'] = gal.uniq_name #set in session the value of the galaxy's unique name

	#previous = getPrevGalaxy(uid)

	features = GalaxyFeatures.objects.filter(galaxy_id = gal.id) # we take the galaxy's features (values from the .cat files)

	'''try:
		analysis = Analysis.objects.filter(user_id=request.user, galaxy_id=gal.id)
	except ObjectDoesNotExist:
		messages.info(request,'No analysis yet.')'''

	checked, checked_short = checkAllFiles(gal.uniq_id, gal.parfolder.name_par, gal.parfolder.fieldId_par) #if all files exists
		
	#directory = settings.MEDIA_ROOT + "/fits_png/" + gal.parfolder.name_par + "/"

	f110script, f110div = displayFImage(request, checked[2], gal, checked_short[2], scalingDefault)	#create the f110's image			
	
	f160140script, f160140div = displayFImage(request, checked[3], gal,checked_short[3], scalingDefault) #create the f160 or f140's image

	g1script, g1div = displayGImage(request,wavelenghts, checked[0],checked_short[0],redshift) #create the g102 2D's image
	g2script, g2div = displayGImage(request,wavelenghts, checked[1],checked_short[1],redshift)#create the g141 2D's image

	g102DatScript, g102DatDiv = plot1DSpectrum(request,wavelenghts,checked[4],minG102,maxG102,"G102dat",redshift) #create the g102 1D's image
	g141DatScript, g141DatDiv = plot1DSpectrum(request,wavelenghts,checked[5],minG141,maxG141,"G141dat",redshift) #create the g141 1D's image
	

	return render(request, 'viewGalaxy.html',locals())

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------ IMAGE DISPLAY ---------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

def read1DSpectrum(pathToASCIISpectrum,minWavelength=None,maxWavelength=None):
    # The ASCII-format 1D spectrum files are found in the Spectrum/ subdirectory of the data
    # If a minimum or maximum wavelength are specified, the spectra will be trimmed
    spectrumData = np.genfromtxt(pathToASCIISpectrum,dtype=np.float64) # Read in the data from file
    spectrumWavelengths, spectrumFluxes, spectrumUncertainties, spectrumContamination, spectrumZeroOrders = spectrumData[0:,0],spectrumData[0:,1],spectrumData[0:,2],spectrumData[0:,3],spectrumData[0:,4]
    # Filter out NaNs which will cause the plotting functions to fail
    filter1 = np.logical_or(np.isnan(spectrumWavelengths),np.isnan(spectrumFluxes)) # an element evaluates to true if either is NaN
    filter2 = np.logical_or(np.isnan(spectrumUncertainties),np.isnan(spectrumContamination)) # an element evaluates to true if either is NaN
    filter3 = np.logical_not(np.logical_or(filter1,filter2))
    # apply the filter
    spectrumWavelengths, spectrumFluxes, spectrumUncertainties, spectrumContamination, spectrumZeroOrders = spectrumWavelengths[filter3], spectrumFluxes[filter3], spectrumUncertainties[filter3], spectrumContamination[filter3], spectrumZeroOrders[filter3]
    # If minimum or maximum wavelengths are specified, trim spectra accordingly
    if minWavelength:
        filter3 = spectrumWavelengths >= minWavelength
        spectrumWavelengths, spectrumFluxes, spectrumUncertainties, spectrumContamination, spectrumZeroOrders = spectrumWavelengths[filter3], spectrumFluxes[filter3], spectrumUncertainties[filter3], spectrumContamination[filter3], spectrumZeroOrders[filter3]
    if maxWavelength:
        filter3 = spectrumWavelengths <= maxWavelength
        spectrumWavelengths, spectrumFluxes, spectrumUncertainties, spectrumContamination, spectrumZeroOrders = spectrumWavelengths[filter3], spectrumFluxes[filter3], spectrumUncertainties[filter3], spectrumContamination[filter3], spectrumZeroOrders[filter3]
    return spectrumWavelengths, spectrumFluxes, spectrumUncertainties, spectrumContamination, spectrumZeroOrders

def plot1DSpectrum(request,wavelenghts,pathToFile,minWavelength, maxWavelength,title,redshift):
    # Separately read in the G102 and G141 spectra
    wl,f,u,c,z = read1DSpectrum(pathToFile, minWavelength, maxWavelength)
    
    wlmax = max(wl) #
    wlmin = min(wl) #
    #cmax = max(c)
    cmin = min(c) #
    fmax = max(f) #
    #fmin = min(f)
    xplus = 100
    yplus = 0.00000000000000001

    wlmin_f = wlmin-xplus
    wlmax_f = wlmax+xplus
    cmin_f = cmin-yplus
    fmax_f = fmax+yplus

    array = [wlmin_f,wlmax_f]

    request.session['array'+title] = array


    mul = multi_line(xs=[wl,wl],
    	ys=[f,c],
    	color=["black","red"],
    	x_range=[wlmin_f,wlmax_f],
    	y_range=[cmin_f,fmax_f],
    	line_width=2,
    	tools=TOOLS,
    	plot_width=400,
    	plot_height=400,
    	title=title,
    )

    hold()

    for wave in wavelenghts:
    	wave = float(wave)
    	line([wave, wave],y=[cmin-yplus,fmax+yplus],color=crossColor,line_width=2, line_dash="dotted")

    for index, em in enumerate(emlineWavelengthsRest):    	
    	emlineWavelengths = em * (1.0 + float(redshift))
    	lin = line([emlineWavelengths,emlineWavelengths],[cmin-yplus,fmax+yplus],color=colors[index],line_width=2)
    	#text([emlineWavelengths+20],(fmax+(index*(2*yplus)))/2,emlineNames[index],0,text_color=colors[index])	

    resources = Resources("inline")

    plot_script, plot_div = components(mul, resources)

    html_script = mark_safe(encode_utf8(plot_script))
    html_div = mark_safe(encode_utf8(plot_div))

    figure()

    return html_script, html_div

@login_required
def wavelenghing(request, redshift,mode="false"):
	gal = get_object_or_404(Galaxy, uniq_name=request.session['unameGal'])

	checked, checked_short = checkAllFiles(gal.uniq_id, gal.parfolder.name_par, gal.parfolder.fieldId_par)

	if float(redshift) < 0 :
		redshift = 0
	if float(redshift) > 3.:
		redshift = 3

	wavelenghts = request.session['waves'+str(gal.uniq_name)]

	g1script, g1div = displayGImage(request,wavelenghts, checked[0],checked_short[0],redshift)
	g2script, g2div = displayGImage(request,wavelenghts, checked[1],checked_short[1],redshift)
	g102script, g102div = plot1DSpectrum(request,wavelenghts,checked[4],minG102,maxG102,"G102dat",redshift)
	g141script, g141div = plot1DSpectrum(request,wavelenghts,checked[5],minG141,maxG141,"G141dat",redshift)

	#return f110script, f110div, f160script, f160div
	data = g1script, g1div, g2script, g2div, g102script, g102div, g141script, g141div

	if mode != "false":
		src102, div102, src141, div141 = plotModels(request, float(redshift), mode=mode)
		data = data + (src102, div102, src141, div141)


	return HttpResponse(json.dumps(data))

@login_required
def scaling(request, val, color):
	#pdb.set_trace()
	gal = get_object_or_404(Galaxy, uniq_name=request.session['unameGal'])

	colors = getColorsNames()

	checked, checked_short = checkAllFiles(gal.uniq_id, gal.parfolder.name_par, gal.parfolder.fieldId_par)

	if int(val) < 1:
		val = 1
	if int(val) > 300:
		val = 300


	f110script, f110div = displayFImage(request, checked[2], gal, checked_short[2], val, color)
	f160script, f160div = displayFImage(request, checked[3], gal, checked_short[3], val, color)

	#return f110script, f110div, f160script, f160div
	data = f110script, f110div, f160script, f160div
	return HttpResponse(json.dumps(data))

@login_required
def referencing(request, redshift, mode):
	src102, div102, src141, div141 = plotModels(request,float(redshift), mode=mode)

	data = src102, div102, src141, div141
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

	script, div = createBokehImage(iFocus,iFocusBoundaries,400,400, short_name, xcircle=xcen, ycircle=ycen, color=color, val=val)

	return script, div

def displayGImage(request, wavelenghts, file, short_name, redshift):
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



	script, div = createBokehImage(iData, dataBoundaries,430,150,short_name, type=False,redshift=redshift,wavelenghts=wavelenghts)

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



def createBokehImage(data, dataBoundaries, plot_width, plot_height, title, type=True, redshift=0 ,xcircle=0, ycircle=0, color="Greys-9",val=100, wavelenghts=None):
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
		for wave in wavelenghts:
			wave = float(wave)
			line([wave, wave],y=y,color=crossColor,line_width=2, line_dash="dotted")
		
		#creation emition lines
		for index, em in enumerate(emlineWavelengthsRest):
			emlineWavelengths = em * (1.0 + float(redshift))
			lin = line([emlineWavelengths,emlineWavelengths],y,color=colors[index],line_width=2)
			#text([emlineWavelengths+20],calculatePositionText(index),emlineNames[index],0,text_color=colors[index])	
			
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


def createPathParDat(fieldId):
	fieldId = str(fieldId)
	return basePath +"Par"+fieldId+"_final/"+"Par"+fieldId+"lines.dat"

def getIndexObjectById(objects, uniq_id):
	try:
		index = None
		uniq_id = str(uniq_id)
		for i, obj in enumerate(objects):
			if obj[2] == uniq_id:
				index = i
				break

		return index
	except:
		return None

def firstObjectInFile(request,fieldId, parId):
	objects = np.genfromtxt(createPathParDat(fieldId), dtype=np.str)

	index = None

	for i, obj in enumerate(objects):
		gal = Galaxy.objects.get(uniq_id=obj[2],parfolder_id=parId)
		check = getIdentificationUser(gal.id,request.user.id)
		if not check:
			index = i
			break

	return index

def getLastGalaxyReviewed(user_id):
	try :
		iden = Identifications.objects.filter(user_id=user_id).order_by('-date')[0]
	except:
		iden = None
	return iden

def queue(request, objects, fieldId, parId, act=0):
	#pdb.set_trace()
	actual = objects[act]

	maxValue = len(objects)
	i = 0
	wavelenghts = []
	next = None

	while act + i < maxValue:		
		nextInFile = objects[act + i]

		gal = Galaxy.objects.get(uniq_id=nextInFile[2],parfolder_id=parId)
		check = getIdentificationUser(gal.id,request.user.id)

		if not check:
			if nextInFile[2] == actual[2]:
				wavelenghts.append(nextInFile[3])
				i += 1
			else: 
				next = Galaxy.objects.raw("SELECT g.id, g.uniq_id, g.parfolder_id FROM `ds9s_galaxy` g INNER JOIN ds9s_parfolder pf ON (g.parfolder_id = pf.id) WHERE g.uniq_id = %s AND pf.fieldId_par = %s", [nextInFile[2], nextInFile[0]])[0]			
				break
		else:
			if nextInFile[2] == actual[2]:
				wavelenghts.append(nextInFile[3])
			i += 1 

	actualEnd = Galaxy.objects.raw("SELECT g.id, g.uniq_id, g.parfolder_id FROM `ds9s_galaxy` g INNER JOIN ds9s_parfolder pf ON (g.parfolder_id = pf.id) WHERE g.uniq_id = %s AND pf.fieldId_par = %s", [actual[2], actual[0]])[0]
	request.session['waves'+str(actualEnd.uniq_name)] = wavelenghts

	return actualEnd, next, wavelenghts



def getColors():
	return json.load(open('/opt/lampp/www/ds9/ds9s/assets/colors.json'))

def getColorsNames():
	colors = getColors()
	names = []

	for color in colors["colors"]:
		names.append(color["name"])

	return names

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------- PAR FILE -------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

def checkAllFiles(gal_id, par_name, par_id):
	base = basePath + par_name 
	g102 =  base + findIn + "aXeWFC3_G102_mef_ID"+str(gal_id)+".fits"
	g141 = base + findIn2 + "aXeWFC3_G141_mef_ID"+str(gal_id)+".fits"

	base_grism = base + grismFolder
	f110w_f = base_grism + f110w
	f160w_f = base_grism + f160w
	f140w_f = base_grism + f140w

	g102dat = base + datFolder + "Par" + str(par_id) + "_G102_BEAM_" + str(gal_id) + "A.dat" 
	g141dat = base + datFolder + "Par" + str(par_id) + "_G141_BEAM_" + str(gal_id) + "A.dat" 

	filesToCheck = [g102,g141,f110w_f,f140w_f,f160w_f,g102dat,g141dat]

	checked = []
	checked_short = []
	for index, f in enumerate(filesToCheck):
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
@permission_required("ds9s.add_parfolder", login_url="/ds9s/")
def newParFile(request):
	parfolders, parids = getParfoldersAndId()

	if request.method == 'POST':		
		form = NewParFileForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data['name']
			try:
				if(int(data)): 
					if(exists(basePath+"Par"+str(data)+"_final")):
						uploaded = uploadParFile(request, "Par"+str(data)+"_final")
						if uploaded:
							return redirect("/ds9s/")
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

def getParfoldersAndId():
	parfolders = getParfoldersBaseDirectory()
	parids = getFieldIdFromParfolder(parfolders)

	return parfolders, parids

def getParfoldersBaseDirectory():
	folders = listdir(basePath)
	parfolders = []
	exp = "Par[0-9]+_final"

	parfolderUploaded = ParFolder.objects.values("name_par")
	names = []

	for par in parfolderUploaded:
		names.append(par['name_par'])

	for folder in folders:
		if re.match(exp, folder) is not None: 
			if folder not in names:
				parfolders.append(folder)

	return parfolders

def getFieldIdFromParfolder(parfolders):
	fieldids = []

	for parfolder in parfolders:
		parid = split(parfolder, "_")
		parid = parid[0]
		parid = split(parid, 'Par')
		parid = parid[1]
		fieldids.append(parid)

	return fieldids


def uploadParFile(request, name=None):
	if name is None:
		messages.error('Error in the folder\'s name')
		return redirect("/ds9s/newParFile/")
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
					addFileDatabase(ids_final, par.id, getTypeSecondFiles(par.fieldId_par))
				except:
					messages.error(request, u"Error during the saving.")
					par.delete()
					return False

				messages.success(request, u"File saved in database.")
				return True
		else:
			messages.error(request, u"File already in database.")
			return False	

def getTypeSecondFiles(fieldId):
	value = None
	par = "Par"+fieldId+"_final"

	toCheck = basePath + par +grismFolder + f140w
	toCheck2 = basePath + par +grismFolder + f160w

	if exists(toCheck):
		value = True
	elif exists(toCheck2):
		value = False

	return value

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

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------- REFERENCE ------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

def genG102Wavelengths():
    l = 7319.
    ls=[]
    while l<=12623.:
        ls.append(l)
        l=l+24.
    return np.array(ls,dtype=np.float64)

def genG141Wavelengths():
    l = 9449.
    ls=[]
    while l<=18516.5:
        ls.append(l)
        l=l+46.5
    return np.array(ls,dtype=np.float64)

def trimSpec(wavelength,flux,minWavelength,maxWavelength):
    filt = np.logical_and(wavelength >= minWavelength, wavelength <= maxWavelength)
    return wavelength[filt],flux[filt]

def smootheInterpolateSpec(wavelength,flux,newWavelength,npixBoxcar):
    smootheFlux = convolve(flux,boxcar(npixBoxcar),mode="same")
    finterp = interp1d(wavelength,smootheFlux,bounds_error=False,fill_value=0.0)
    smootheFlux = finterp(newWavelength)
    return smootheFlux/smootheFlux.max()

def Gauss(l,l0,sigma,amp):
    return amp * np.exp((-1.0*(l-l0)**2)/(2.0*sigma**2))

def createGalaxySpectra(redshift,galaxyFullWidth=4.):
    # Create three model spectra with different EW for emission lines,  
    # Adapt to galaxy size and magnitude? Maybe size for now.
    # Generate observed-frame spectra in X Angs. increments; 
    # convolve with a gaussian to match galaxy size spread;
    # smoothe and interpolate.
    deltal = 2. # set the wavelength scale of the initial spectrum
    lineFullWidth = deltal * 3. # nyquist sample the lines
    wavelengths102 = genG102Wavelengths()
    wavelengths141 = genG141Wavelengths()
    wavelengthsInit = []
    l=wavelengths102[0]
    while l <= wavelengths141[-1]:
        wavelengthsInit.append(l)
        l = l + deltal
    wavelengthsInit = np.array(wavelengthsInit,dtype=np.float64)
    emlineWavelengths = emlineWavelengthsRest * (1.0 + redshift) # Given a redshift, calculate the wavelength coordinates of the vertical lines
    emlineStrengths = np.array([5.,0.25,1.0,1.66,5.,4.,0.4,0.133,0.4,0.1],dtype=np.float64) # relative to Hbeta (?)
    fluxesStrong = np.zeros(len(wavelengthsInit),dtype=np.float64) + 1.0 # Observed Ha EW = 500.
    fluxesMiddle = np.zeros(len(wavelengthsInit),dtype=np.float64) + 1.0 # Observed Ha EW = 100
    fluxesWeak = np.zeros(len(wavelengthsInit),dtype=np.float64) + 1.0 # Observed Ha EW = 50.
    for i in range(len(wavelengthsInit)):
        for j in range(len(emlineWavelengths)):
            # EW*F_lambda = S F_lambda dlambda
            ampFactor = 500. / (lineFullWidth/2.35 * np.sqrt(2.0*pi) * emlineStrengths[5])
            fluxesStrong[i] = fluxesStrong[i] + Gauss(wavelengthsInit[i],emlineWavelengths[j],lineFullWidth/2.35,ampFactor*emlineStrengths[j])
            ampFactor = 100. / (lineFullWidth/2.35 * np.sqrt(2.0*pi) * emlineStrengths[5])
            fluxesMiddle[i] = fluxesMiddle[i] + Gauss(wavelengthsInit[i],emlineWavelengths[j],lineFullWidth/2.35,ampFactor*emlineStrengths[j])
            ampFactor = 50. / (lineFullWidth/2.35 * np.sqrt(2.0*pi) * emlineStrengths[5])
            fluxesWeak[i] = fluxesWeak[i] + Gauss(wavelengthsInit[i],emlineWavelengths[j],lineFullWidth/2.35,ampFactor*emlineStrengths[j])
    # now convolve with the galaxy gaussian
    nWin = 12
    pixConvert102 = 24./deltal * galaxyFullWidth/2.35
    pixConvert141, pixConvert102 = int(pixConvert102*46.5/24.), int(pixConvert102)
    fStrong102 = convolve(fluxesStrong,gaussian(nWin*pixConvert102,std=pixConvert102),mode="same")
    fMiddle102 = convolve(fluxesMiddle,gaussian(nWin*pixConvert102,std=pixConvert102),mode="same")
    fWeak102 = convolve(fluxesWeak,gaussian(nWin*pixConvert102,std=pixConvert102),mode="same")
    fStrong141 = convolve(fluxesStrong,gaussian(nWin*pixConvert141,std=pixConvert141),mode="same")
    fMiddle141 = convolve(fluxesMiddle,gaussian(nWin*pixConvert141,std=pixConvert141),mode="same")
    fWeak141 = convolve(fluxesWeak,gaussian(nWin*pixConvert141,std=pixConvert141),mode="same")
    finterp = interp1d(wavelengthsInit,fStrong102,bounds_error=False,fill_value=0.0)
    fStrong102 = finterp(wavelengths102)
    finterp = interp1d(wavelengthsInit,fMiddle102,bounds_error=False,fill_value=0.0)
    fMiddle102 = finterp(wavelengths102)
    finterp = interp1d(wavelengthsInit,fWeak102,bounds_error=False,fill_value=0.0)
    fWeak102 = finterp(wavelengths102)
    finterp = interp1d(wavelengthsInit,fStrong141,bounds_error=False,fill_value=0.0)
    fStrong141 = finterp(wavelengths141)
    finterp = interp1d(wavelengthsInit,fMiddle141,bounds_error=False,fill_value=0.0)
    fMiddle141 = finterp(wavelengths141)
    finterp = interp1d(wavelengthsInit,fWeak141,bounds_error=False,fill_value=0.0)
    fWeak141 = finterp(wavelengths141)
    #return wavelengths102,wavelengths141,fStrong102,fMiddle102,fWeak102,fStrong141,fMiddle141,fWeak141
    galSpec102 = np.zeros((len(wavelengths102),4),dtype=np.float64)
    galSpec141 = np.zeros((len(wavelengths141),4),dtype=np.float64)
    galSpec102[0:,0] = wavelengths102
    galSpec102[0:,1] = fStrong102
    galSpec102[0:,2] = fMiddle102
    galSpec102[0:,3] = fWeak102
    galSpec141[0:,0] = wavelengths141
    galSpec141[0:,1] = fStrong141
    galSpec141[0:,2] = fMiddle141
    galSpec141[0:,3] = fWeak141
    return galSpec102,galSpec141

def getModels(redshift,mode="star"):
    if mode=="star":
        modelSpectraData102=np.load("StellarSpectraG102.npy")
        modelSpectraData141=np.load("StellarSpectraG141.npy")
    elif mode=="quasar":
        modelSpectraData=np.load("QuasarSpectrum.npy")
        quasarWavelengths, quasarFlux = modelSpectraData[0:,0]*(1.0+redshift), modelSpectraData[0:,1]
        l102 = genG102Wavelengths()
        l141 = genG141Wavelengths()
        dl = (quasarWavelengths[-1] - quasarWavelengths[0])/float(len(quasarWavelengths))
        modelFlux102 = smootheInterpolateSpec(quasarWavelengths,quasarFlux,l102,int(24./dl))
        modelFlux141 = smootheInterpolateSpec(quasarWavelengths,quasarFlux,l141,int(46.5/dl))
        modelSpectraData102=np.zeros((len(l102),2),dtype=np.float64)
        modelSpectraData141=np.zeros((len(l141),2),dtype=np.float64)
        modelSpectraData102[0:,0] = l102
        modelSpectraData102[0:,1] = modelFlux102
        modelSpectraData141[0:,0] = l141
        modelSpectraData141[0:,1] = modelFlux141
    elif mode=="galaxy":
        modelSpectraData102, modelSpectraData141 =  createGalaxySpectra(redshift)
    else:
        return None
    return modelSpectraData102,modelSpectraData141

def plotModels(request, redshift, mode="star"):
	modelSpectra102, modelSpectra141 = getModels(redshift, mode=mode)

	g102 = request.session['arrayG102dat']
	g141 = request.session['arrayG141dat']

	script102, div102 = createReference(modelSpectra102,redshift, g102[0], g102[1])
	script141, div141 = createReference(modelSpectra141,redshift, g141[0], g141[1])

	return script102, div102, script141, div141

def createReference(data,redshift, xmin, xmax):
	pcolors = ['black','red','blue']

	#maxd = np.amax(data)
	#mind = min(np.amin(data,axis=0)) #big problem here

	for i in range(data.shape[1]-1):
		mul = line(x=data[0:,0], 
			y=data[0:,i+1], 
			tools=TOOLS, 
			color=pcolors[i%3],
			plot_width=400,
			plot_height=400,
			x_range=[xmin,xmax]
		)

	hold()

	for index, em in enumerate(emlineWavelengthsRest):
		emlineWavelengths = em * (1.0 + float(redshift))
		line([emlineWavelengths,emlineWavelengths],[0,1],color=colors[index],line_width=2)
		#text([emlineWavelengths+20],(fmax+(index*(2*yplus)))/2,emlineNames[index],0,text_color=colors[index])	

	resources = Resources("inline")

	plot_script, plot_div = components(mul, resources)

	html_script = mark_safe(encode_utf8(plot_script))
	html_div = mark_safe(encode_utf8(plot_div))

	figure()

	return html_script, html_div

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#---------------------------------- ADD IDENTIFICATION & ANALYSIS -------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------


def addIdentification(gal_id, user_id, galtype_id, redshift, contaminated):
	try:
		iden = Identifications()
		iden.galaxy_id = gal_id
		iden.user_id = user_id
		iden.galaxytype_id = galtype_id
		iden.redshift = redshift
		iden.contaminated = contaminated
		iden.save() 
		return True
	except:
		return False


def addAnalys(gal_id, user_id, emissionline_id, emissionlinefield_id, value):
	try:
		aly = Analysis()
		aly.galaxy_id = gal_id
		aly.user_id = user_id
		aly.emissionline_id = emissionline_id
		aly.emissionlinefield_id = emissionlinefield_id
		aly.value = value
		aly.save()
		return True
	except:
		return False

def getEmissionLineFields():
	return EmissionLineFields.objects.all()

def getIdEmissionLineFieldByName(name):
	fields = getEmissionLineFields()

	id = None

	for field in fields:
		if field.name == name:
			id = field.id
			break

	return id


def getEmissionLines():
	return EmissionLine.objects.all()

def getIdEmissionLineByName(name):
	lines = getEmissionLines()

	id = None

	for line in lines:
		if line.name == name:
			id = line.id
			break

	return id

def getGalaxyTypes():
	return GalaxyTypes.objects.values("id","nameForId")

def getIdOfType(typeObj):
	types = getGalaxyTypes()

	objId = None

	for t in types:
		if typeObj == t["nameForId"]:
			objId = t["id"]

	return objId

def secureRedshift(redshift):
	if redshift < 0:
		redshift = 0
	elif redshift > 3:
		redshift = 3

	return redshift

def getIdentificationUser(gal_id, user_id):
	try:
		iden = Identifications.objects.get(galaxy_id=gal_id, user_id=user_id)
	except ObjectDoesNotExist:
		iden = False

	return iden

def setNoneRedshist(typeObjId, redshift):
	if typeObjId in [5,1]:
		redshift = None
	else:
		redshift = secureRedshift(float(redshift))

	return redshift

def secureContaminated(contaminated):
	if contaminated == None:
		contaminated = 0

	return contaminated

#function who will be called by urls to begin adding
#id is the galaxy id from the database
def saveUserReview(request, id, uniq_name, next_uniq_name):
	user_id = request.user.id
	check = getIdentificationUser(id, user_id)

	if not check:
		typeObj = request.POST.get("typeObject")
		typeObjId = getIdOfType(typeObj)

		if typeObjId != None:
			redshift = setNoneRedshist(typeObjId, request.POST.get("redshift"))

			contaminated = secureContaminated(request.POST.get("contaminated"))

			'''linecheck = []
			for index, em in enumerate(emlineWavelengthsRest):
				value = em * (1.0 + float(redshift))
				linecheck.append(addAnalys(id, user_id, index,value))'''


			identification = addIdentification(id, user_id, typeObjId, redshift, contaminated)

			if identification:				
				if next_uniq_name == "None":
					messages.success(request, "You successfully identified the object and finish this queue. Click again on 'Let's Go'.")
					return HttpResponseRedirect("/ds9s/account/reviews/")
				else:
					messages.success(request, "You successfully identified the object.")
					return HttpResponseRedirect("/ds9s/view/"+str(next_uniq_name)+"/")
				
			else:
				messages.error(request, "Error during saving.")
				return HttpResponseRedirect("/ds9s/view/"+uniq_name+"/")
		else:
			messages.error(request, "Error in the object's value.")
			return HttpResponseRedirect("/ds9s/view/"+uniq_name+"/")
	else:
		messages.error(request, "You already identified this object.")
		return HttpResponseRedirect("/ds9s/view/"+uniq_name+"/")

def getIdenById(iden_id):
	#try:
	iden = Identifications.objects.get(id=iden_id)
	#except:
	#	iden = None

	return iden

def updateIden(iden, typeObjId, redshift, contaminated):
	try:
		iden.galaxytype_id = typeObjId
		iden.redshift = redshift
		iden.contaminated = contaminated
		iden.save()
		return True
	except:
		return False

def updateUserReview(request, rev_id):
	typeObj = request.POST.get("typeObject")
	typeObjId = getIdOfType(typeObj)

	if typeObjId != None:
		redshift = setNoneRedshist(typeObjId, request.POST.get("redshift"))

		contaminated = secureContaminated(request.POST.get("contaminated"))

		iden = getIdenById(rev_id)
		checkUpdate = updateIden(iden, typeObjId, redshift, contaminated)

		if checkUpdate:
			messages.success(request, "You successfully updated your review.")			
		else:
			messages.error(request, "Error during saving.")

	return HttpResponseRedirect("/ds9s/account/reviews/")


	