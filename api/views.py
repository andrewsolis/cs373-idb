from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse
import json

from idb.videogames.models import *

def games(request):
	x = Game.objects.order_by('-name')[:]
	if len(x):
		games_list = json.dumps(x)
	else:
		games_list = {}

	return HttpResponse(games_list, content_type="application/json")

def people(request):
	x = Person.objects.order_by('-id')[:]
	if len(x):
		people_list = json.dumps(x)
	else:
		people_list = {}

	return HttpResponse(people_list, content_type="application/json")

def companies(request):
	x = Company.objects.order_by('-id')[:]
	if len(x):
		company_list = json.dumps(x)
	else:
		company_list = {}

	return HttpResponse(company_list, content_type="application/json")
