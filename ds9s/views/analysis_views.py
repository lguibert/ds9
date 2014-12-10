#-*- coding: utf-8 -*-
from ds9s.models import Galaxy, ParFolder, Analysis, EmissionLineFields, EmissionLine, GalaxyFeatures, GalaxyTypes, Identifications
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from django.utils.safestring import mark_safe

import numpy as np
import scipy.special
from bokeh.plotting import figure, quad
from bokeh.embed import components
from bokeh.resources import Resources
from bokeh.utils import encode_utf8

import json


TOOLS="pan,wheel_zoom,box_zoom,reset"


@login_required
def getReviewUser(request):
	identifications = Identifications.objects.filter(user_id=request.user.id)

	return render(request, 'analysis.html',locals()) 

@login_required
def viewAllReviews(request):
	idens = Identifications.objects.raw("SELECT COUNT(`galaxy_id`) as reviews, i.* FROM ds9s_identifications  i group by `galaxy_id`")

	#SELECT AVG(`redshift`) as avgRedshit, COUNT(`galaxy_id`) as numReview, `galaxy_id` FROM ds9s_identifications  group by `galaxy_id` order by `galaxy_id`
	return render(request, 'reviews.html',locals())

@login_required
def viewReviewAnalysis(request, uniq_name):
	gal = get_object_or_404(Galaxy, uniq_name=uniq_name)
	idens = Identifications.objects.filter(galaxy_id=gal.id)

	redshifts = []

	for iden in idens:
		try:
			redshift = float(iden.redshift)
		except:
			redshift = iden.redshift
		redshifts.append(redshift)

	redshifts = json.dumps(redshifts)

	return render(request, 'reviewAnalysis.html',locals())


def createHistogram(data):
	hist, edges = np.histogram(data)

	p1 = quad(
		top=hist,
		bottom=0,
		left=edges[:-1],
		right=edges[1:],
	    fill_color="#036564",
	    line_color="#033649",
	    tools=TOOLS,
    )

	resources = Resources("inline")

	plot_script, plot_div = components(p1, resources)

	html_script = mark_safe(encode_utf8(plot_script))
	html_div = mark_safe(encode_utf8(plot_div))

	figure()

	return html_script, html_div