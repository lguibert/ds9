#-*- coding: utf-8 -*-
from ds9s.models import Galaxy, ParFolder, Analysis, EmissionLineFields, EmissionLine, GalaxyFeatures, GalaxyTypes, Identifications, GalaxyFields
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count

from django.utils.safestring import mark_safe

import numpy as np
import scipy.special
from bokeh.plotting import figure, quad, ColumnDataSource
from bokeh.embed import components
from bokeh.resources import Resources
from bokeh.utils import encode_utf8
from bokeh.models import HoverTool

import json

from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.core.servers.basehttp import FileWrapper
import csv

import os

import pdb


TOOLS="pan,wheel_zoom,box_zoom,reset, hover"


@login_required
def getReviewUser(request):
	identifications = Identifications.objects.filter(user_id=request.user.id)

	return render(request, 'analysis.html',locals()) 

@login_required
@permission_required("ds9s.view_allIdentifications")
@permission_required("ds9s.view_allAnalysis")
def viewAllReviews(request):
	idens = Identifications.objects.raw("SELECT COUNT(`galaxy_id`) as reviews, i.* FROM ds9s_identifications  i group by `galaxy_id`")

	return render(request, 'reviews.html',locals())

@login_required
@permission_required("ds9s.view_allIdentifications")
@permission_required("ds9s.view_allAnalysis")
def viewReviewAnalysis(request, uniq_name):
	gal = get_object_or_404(Galaxy, uniq_name=uniq_name)
	idens = Identifications.objects.filter(galaxy_id=gal.id)

	redshifts = []

	for iden in idens:
		redshift = iden.redshift

		if redshift == None:
			redshift = 0.

		redshifts.append(float(redshift))

	html, div = createHistogram(redshifts)	

	return render(request, 'reviewAnalysis.html',locals())


def createHistogram(data):
	hist, edges = np.histogram(data,bins=3000)

	plot = figure(
		tools=TOOLS,
		x_range=[min(edges)-0.05,max(edges)+0.05],
		plot_width=1100, 
		title="",
	)

	plot.quad(
		top=hist,
		bottom=0,
		left=edges[:-1],
		right=edges[1:],
		fill_color="#036564",
		line_color="#033649",
		
	)

	hover = plot.select(dict(type=HoverTool))	
	hover.tooltips = [('index','$index')]
	hover.snap_to_data = False

	resources = Resources("inline")

	plot_script, plot_div = components(plot, resources)

	html_script = mark_safe(encode_utf8(plot_script))
	html_div = mark_safe(encode_utf8(plot_div))

	figure()

	return html_script, html_div


@login_required
@permission_required("ds9s.view_allIdentifications")
@permission_required("ds9s.view_allAnalysis")
def export(request):
	idens = Identifications.objects.all()
	featuresX = []
	featuresY = []
	done = [] #array who will contain uniq_id who was already x & y getted
	#fluxs = []
	#fluxerrs = []

	for iden in idens:
		id = iden.galaxy.uniq_id
		idPar = iden.galaxy.parfolder_id

		if [id,idPar] not in done:
			x_space = GalaxyFeatures.objects.get(galaxy_id=iden.galaxy_id, galaxyfields_id=1)
			y_space = GalaxyFeatures.objects.get(galaxy_id=iden.galaxy_id, galaxyfields_id=2)
			#flux = Analysis.objects.get(galaxy_id=iden.galaxy_id, emissionlinefield_id=10)
			#fluxerr = Analysis.objects.get(galaxy_id=iden.galaxy_id, emissionlinefield_id=11)

			featuresX.append(x_space.value)
			featuresY.append(y_space.value)	
			#fluxs.append(flux)
			#fluxerrs.append(fluxerr)
			done.append([id,idPar])
		else:
			featuresX.append(None)
			featuresY.append(None)	
	
	del done #deleting of done			

	gals = getGalaxyOnceFromIden(idens)

	return render(request, 'export.html', locals())


def getGalaxyOnceFromIden(idens):
	gals = []

	for iden in idens:
		id = iden.galaxy.uniq_id
		idPar = iden.galaxy.parfolder.fieldId_par

		if [id,idPar] not in gals:
			gals.append([id,idPar])

	return gals

@login_required
@permission_required("ds9s.view_allIdentifications")
@permission_required("ds9s.view_allAnalysis")
def selectedGalaxy(request):
	selectedGalaxy = request.POST.getlist('selectedGalaxy')
	request.session['valueGals'] = selectedGalaxy

	numGalSelected = len(selectedGalaxy)

	galFields = GalaxyFields.objects.all()

	emiFields = EmissionLineFields.objects.all()

	emiLines = EmissionLine.objects.all()

	#gals = Galaxy.objects.all()

	return render(request, 'selectedGalaxy.html', locals())

def spliterArray(array,separator):
	first = []
	second = []

	for entry in array:
		entry = entry.split(separator)
		first.append(entry[0])
		second.append(entry[1])		

	return first, second

def spliterString(string,separator):
	string = string.split(separator)

	return string[0], string[1]

def countReviews(array):	
	final = []

	for entry in array:
		done = False

		if final:
			for f in final:
				if f[0] == entry:
					f[1] += 1
					done = True
					break
		else:
			final.append([entry,1])
			done = True

		if done == False:
			final.append([entry,1])						

	return final

def getDataIden(array, contaminated, redshift, galType):
	data = []
	ids = []

	for id in array:	
		result = [0, 0, 0, 0]
		iden = Identifications.objects.get(id=id)

		galId = str(iden.galaxy_id)
		if galId not in ids:
			ids.append(galId)

		result[0] = str(iden.galaxy_id)

		if contaminated == True:
			result[1] = iden.contaminated
		if redshift == True:
			result[2] = iden.redshift
		if galType == True:
			result[3] = iden.galaxytype_id

		data.append(result)

	return data, ids

def calculateNumberContaminated(array):
	final = []

	for a in array:
		done = False
		for f in final:
			if f[0] == a[0]:
				if a[1] == True:
					f[1] += 1
				done = True
				break

		if done == False:
			final.append([a[0],boolToInt(a[1])])	

	return final

def incrementBase(base, data):
	save = base[0]
	del base[0]

	for b in base[0]:
		if b[0] == data[-1]:
			b[1] += 1

	base.insert(0,save)

	return base


def calculateNumberGalaxyType(data):
	typeArray = [] #[[id,[1,0,name],[2,0,name],[3,0,name],[4,0,name],[5,0,name],[6,0,name],[7,0,name],[8,0,name]],...]

	act = data[0][0]
	base = newBase(act)
	for d in data:
		if d[0] == act:
			base = incrementBase(base,d)
		else:				
			typeArray.append(base)		
			base = newBase(d[0])
			act = d[0]		

			base = incrementBase(base,d)
		
	else:
		typeArray.append(base)

	return typeArray

def incrementInterval(intervals, redshift):
	save = intervals[0]
	del intervals[0]

	if redshift == None:
		redshift = 0.0

	for i in intervals[0]:
		if redshift >= i[0] and redshift < i[1]:
			i[2] += 1

	intervals.insert(0,save)
	return intervals

def calculateRedshiftInterval(data):
	invertalArray = []
	act = data[0][0]	
	intervalRedshift = newRedshiftIntervalArray(act) #[id,[[0,0.01,0],[0.01,0.02,0],...]]		
		
	for d in data:
		if d[0] == act:
			intervalRedshift = incrementInterval(intervalRedshift, d[2])
		else:
			invertalArray.append(intervalRedshift)
			intervalRedshift = newRedshiftIntervalArray(d[0])
			act = d[0]

			intervalRedshift = incrementInterval(intervalRedshift, d[2])
	else:
		invertalArray.append(intervalRedshift)

	return invertalArray
			
def mergeTwoArray(first, second):
	for f in first:
		for s in second:
			if s[0] == f[0]:
				s[1].append(f[1])
				break

	return second

def countValuesIden(idenIds, contaminated, redshift, galType):
	data, ids = getDataIden(idenIds , contaminated, redshift, galType)

	if contaminated == True:
		contaminatedArray = calculateNumberContaminated(data) #[[id, num],...]

	if galType == True:
		typesArray = calculateNumberGalaxyType(data)

	#count how redshift there is between 0 and 3 with 0.01 step (default values)
	if redshift == True:
		redshiftInvertal = calculateRedshiftInterval(data)


	#here, we put all array in one
	final = [] #[[id, []],...]

	for id in ids:
		final.append([id, []])

	if contaminatedArray:
		final = mergeTwoArray(contaminatedArray, final)

	if typesArray:
		final = mergeTwoArray(typesArray, final)

	#if redshiftInvertal:
	#	final = mergeTwoArray(redshiftInvertal, final)

	return final

def newRedshiftIntervalArray(id, start = 0, end = 3, step = 0.01):
	allValues = np.arange(start, end+step, step)
	final = [id]
	intervals = []

	for i, a in enumerate(allValues):
		if a != allValues[-1]:
			low = a
			high = allValues[i+1]

			interval = [low, high, 0]

			if interval not in intervals:
				intervals.append(interval)

	final.append(intervals)

	return final

def createRefRedshiftIntervalArray(start = 0, end = 3, step = 0.01):
	allValues = np.arange(start, end+step, step)

	final = []

	for i, a in enumerate(allValues):
		if a != allValues[-1]:
			low = a
			high = allValues[i+1]

			interval = smart_str('['+ str(low) +','+ str(high) +']')

			if interval not in final:
				final.append(interval)

	return final

def newBase(id):
	types = GalaxyTypes.objects.all()
	base = [id]
	array = []

	for t in types:		
		array.append([t.id,0,t.name])

	base.append(array)

	return base

def boolToInt(value):
	if value == True:
		return 1
	elif value == False:
		return 0
	else:
		return 0

def toBoolean(value):
	correctTrue = [1,'true',True,'True','1']
	correctFalse  = [0, 'false', False, 'False','0']

	if value in correctFalse:
		end = False
	elif value in correctTrue:
		end = True
	else:
		end = False

	return end

def splitPointData(data):
	data = data.split('.')
	return data[0], data[1], data[2]

def rebuildArray(array):
	final = []

	for a in array:
		splited = splitPointData(a[0])
		final.append([splited[0],[splited[1], splited[2], a[1]]])

	return final


@login_required
@permission_required("ds9s.view_allIdentifications")
@permission_required("ds9s.view_allAnalysis")
def createTxtFile(request):
	valueGalsIdens = request.session['valueGals']
	galFields = request.POST.getlist('galFields')
	
	contaminated = toBoolean(request.POST.get('contaminated',False))
	redshift = toBoolean(request.POST.get('redshift',False))
	galType = toBoolean(request.POST.get('galType',False))
	

	galAndFolderIds, idenIds = spliterArray(valueGalsIdens, '-')

	#[id,number]
	numberReviews = countReviews(galAndFolderIds) #count number of review(s) per galaxy
	numberReviewsWithIds = rebuildArray(numberReviews)

	#[idGal, numContaminated, [[galTypeId, number],[galTypeId, number],...], [[0,0.01,number],...]]
	idens = countValuesIden(idenIds, contaminated, redshift, galType)

	final = []

	for review in numberReviewsWithIds:
		for i in idens:
			if review[0] == i[0]:
				save = i[1]
				del i
				save.insert(0,review[1][2])	
				save.insert(0,review[1][1])	
				save.insert(0,review[1][0])	
				final.append(save)
				break


	#print final

	refArray = createRefRedshiftIntervalArray()
	refArray.insert(0,smart_str(u"Possible emission line"))
	refArray.insert(0,smart_str(u"Not real"))
	refArray.insert(0,smart_str(u"Galaxy with one emission line"))
	refArray.insert(0,smart_str(u"Nothing"))
	refArray.insert(0,smart_str(u"Galaxy with emission line"))
	refArray.insert(0,smart_str(u"Galaxy without emission line"))
	refArray.insert(0,smart_str(u"Quasar"))
	refArray.insert(0,smart_str(u"Star"))
	refArray.insert(0,smart_str(u"Contaminated"))
	refArray.insert(0,smart_str(u"Number of reviews"))
	refArray.insert(0,smart_str(u"Field Id"))
	refArray.insert(0,smart_str(u"Uniq Id"))

		
	# ---------------- Create the cvs file ----------------
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=export.csv'
	writer = csv.writer(response, csv.excel)
	writer.writerow(refArray)

	
	writer.writerows(final)	
		
	
	return response



