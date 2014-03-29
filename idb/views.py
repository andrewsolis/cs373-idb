from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse
import json

from idb.videogames.models import *

def home(request):
	return render_to_response('home.html', {}, RequestContext(request))

# Create your views here.
def metroid(request):
	return render_to_response('metroid.html', {}, RequestContext(request))

def crash_bandicoot(request):
	return render_to_response('crash_bandicoot.html', {}, RequestContext(request))

def sonic(request):
	return render_to_response('sonic.html', {}, RequestContext(request))

def yoshio_sakamoto(request):

	return render_to_response('yoshio_sakamoto.html', {}, RequestContext(request))

def naoto_oshima(request):
	return render_to_response('naoto_oshima.html', {}, RequestContext(request))

def andy_gavin(request):
	return render_to_response('andy_gavin.html', {}, RequestContext(request))

def nintendo(request):
	return render_to_response('nintendo.html', {}, RequestContext(request))

def sega(request):
	return render_to_response('sega.html', {}, RequestContext(request))

def naughtydog(request):
	return render_to_response('naughtydog.html', {}, RequestContext(request))

def games_index(request):
	return render_to_response('games_index.html', {}, RequestContext(request))

def people_index(request):
	return render_to_response('people_index.html', {}, RequestContext(request))

def companies_index(request):
	return render_to_response('companies_index.html', {}, RequestContext(request))



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
