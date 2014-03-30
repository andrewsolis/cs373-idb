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
	games_list = []
	if(request.method == 'GET'):
		games_list = serializers.serialize("json",Game.objects.order_by('-id').all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(games_list, content_type="application/json")

def games_id(request, id):
	return HttpResponse([], content_type="application/json")

def games_people(request, id):
	return HttpResponse([], content_type="application/json")

def games_companies(request, id):
	return HttpResponse([], content_type="application/json")

def people(request):
	people_list = []
	if(request.method == 'GET'):
		people_list = serializers.serialize("json",Game.objects.order_by('-id').all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(people_list, content_type="application/json")

def people_id(request, id):
	return HttpResponse([], content_type="application/json")

def people_games(request, id):
	return HttpResponse([], content_type="application/json")

def people_companies(request, id):
	return HttpResponse([], content_type="application/json")


def companies(request):
	companies_list = []
	if(request.method == 'GET'):
		companies_list = serializers.serialize("json",Game.objects.order_by('-id').all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(company_list, content_type="application/json")


def companies_id(request, id):
	return HttpResponse([], content_type="application/json")

def companies_games(request, id):
	return HttpResponse([], content_type="application/json")

def companies_people(request, id):
	return HttpResponse([], content_type="application/json")




