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

def spliter(string,separator):
	string = string.split(separator)		

	return string[0], string[1]

def calculateNumberType(array):
	return None

def calculateNumberContaminate(array):
	return None

def calculateNumberRedshift(array):
	return None

def calculateNumberReviews(array):
	return None


@login_required
@permission_required("ds9s.view_allIdentifications")
@permission_required("ds9s.view_allAnalysis")
def createTxtFile(request):
	valueGals = request.session['valueGals']


	galFields = request.POST.getlist('galFields')
	contaminated = request.POST.getlist('contaminated')
	redshift = request.POST.getlist('redshift')
	galType = request.POST.getlist('galType')
	
	
	gals = []
	galsDone = []
	string = ''

	#pdb.set_trace()
	
	for value in valueGals:
		galId, idenId = spliter(value,'-')

		galFieldsValue = []

		
		# ---------------- Identification values ----------------
		iden = Identifications.objects.get(id=idenId)
		contaminatedGal = iden.contaminated
		redshiftGal = iden.redshift
		typeGalId = iden.galaxytype.id
		typeGalName = iden.galaxytype.name

		# ---------------- Galaxy values ----------------
		galUid = iden.galaxy.uniq_id
		galFieldId = iden.galaxy.parfolder.fieldId_par


		# ---------------- Feature Galaxy ----------------
		for field in galFields:
			try:
				if galId not in galsDone:
					feat = GalaxyFeatures.objects.get(galaxy_id=galId, galaxyfields_id=field)
					galFieldsValue.append([feat.galaxyfields.name,feat.value])
					galsDone.append(galId)
			except:
				print 'Error'


		gals.append([galUid, galFieldId, contaminatedGal, redshiftGal, typeGalName, galFieldsValue])
	
	#now, we have all what we need. We need to change the array's structure
	for gal in gals:
		print gal


	# ---------------- Create the cvs file ----------------
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=export.csv'
	writer = csv.writer(response, csv.excel)
	writer.writerow([
		smart_str(u"Name"),
		smart_str(u"Value"),
	])
	for obj in gals:
		writer.writerow([
			smart_str(obj[0]),
			smart_str(obj[1]),
		])
	
	return response

