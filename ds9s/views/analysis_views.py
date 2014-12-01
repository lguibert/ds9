#-*- coding: utf-8 -*-
from ds9s.models import Galaxy, ParFolder, Analysis, EmissionLineFields, EmissionLine, GalaxyFeatures, GalaxyTypes, Identifications
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def getReviewUser(request):
	identifications = Identifications.objects.filter(user_id=request.user.id)

	return render(request, 'analysis.html',locals()) 

@login_required
def viewAllReviews(request):
	idens = Identifications.objects.all()

	#SELECT AVG(`redshift`) as avgRedshit, COUNT(`galaxy_id`) as numReview, `galaxy_id` FROM ds9s_identifications  group by `galaxy_id` order by `galaxy_id`
	return render(request, 'reviews.html',locals()) 