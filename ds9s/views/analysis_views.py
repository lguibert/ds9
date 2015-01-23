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
	request.session['postIdGal'] = selectedGalaxy

	numGalSelected = len(selectedGalaxy)

	galFields = GalaxyFields.objects.all()

	emiFields = EmissionLineFields.objects.all()

	emiLines = EmissionLine.objects.all()

	#gals = Galaxy.objects.all()

	return render(request, 'selectedGalaxy.html', locals())

@login_required
@permission_required("ds9s.view_allIdentifications")
@permission_required("ds9s.view_allAnalysis")
def createTxtFile(request):
	postIdsGal = request.session['postIdGal']

	galFields = request.POST.getlist('galFields')
	emiFields = request.POST.getlist('emiFields')
	emiLines = request.POST.getlist('emiLines')
	contaminated = request.POST.getlist('contaminated')
	redshift = request.POST.getlist('redshift')
	galType = request.POST.getlist('galType')
	

	galFieldsValueFinal = []
	emiFieldsFinal = []
	emiLinesFinal = []
	string = ''

	#pdb.set_trace()

	print postIdsGal

	for galId in postIdsGal:
		galFieldsValue = []
		emiFields = []
		emiLines = []
		for field in galFields:
			try:
				feat = GalaxyFeatures.objects.get(galaxy_id=galId, galaxyfields_id=field)
				galFieldsValue.append([feat.galaxyfields.name,feat.value])
			except:
				print "Error"
			

		galFieldsValueFinal = galFieldsValue

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=export.csv'
	writer = csv.writer(response, csv.excel)
	writer.writerow([
		smart_str(u"Name"),
		smart_str(u"Value"),
	])
	for obj in galFieldsValueFinal:
		writer.writerow([
			smart_str(obj[0]),
			smart_str(obj[1]),
		])
	
	return response

'''
	for value in galFieldsValueFinal:
		string = string + value[0] + ':' + str(value[1]) + ','

	finalFile = open('tmp/export.txt','w')
	finalFile.write(string)
	finalFile.close()

	f = 'tmp/export.txt'

	wrapper = FileWrapper(file(f))
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=export.txt'
	response['Content-Length'] = os.path.getsize(f)


	return response'''