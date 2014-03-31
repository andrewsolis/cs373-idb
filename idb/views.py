from django.shortcuts import *
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse
import json
from idb.videogames.models import *
from idb.api.views import *
import time

def home(request):
	return render_to_response('home.html', {}, RequestContext(request))

def games(request):
	games_list = api_games(request)
	result = serializers.deserialize("json", games_list.content)
	return render_to_response('cgp_index.html', {'items': result})

def games_id(request, id):
	game = api_games_id(request,id)
	game_content = json.loads(game.content.decode("utf-8"))
	content = game_content[0]["fields"]
	genres = ""
	for genre in content['genre']:
		genres = genres + genre + ", "
	content['genre'] = genres[:-2]
	return render_to_response('game.html', content)

def games_people(request, id):
	return HttpResponse([], content_type="application/json")

def games_companies(request, id):
	return HttpResponse([], content_type="application/json")

def people(request):
	people_list = api_people(request)
	result = serializers.deserialize("json", people_list.content)
	return render_to_response('cgp_index.html', {'items': result})

def people_id(request, id):
	person = api_people_id(request,id)
	person_content = json.loads(person.content.decode("utf-8"))
	content = person_content[0]["fields"]
	return render_to_response('person.html', content)

def people_games(request, id):
	return HttpResponse([], content_type="application/json")

def people_companies(request, id):
	return HttpResponse([], content_type="application/json")


def companies(request):
	companies_list = api_companies(request)
	result = serializers.deserialize("json", companies_list.content)
	return render_to_response('cgp_index.html', {'items': result})


def companies_id(request, id):
	company = api_companies_id(request,id)
	company_content = json.loads(company.content.decode("utf-8"))
	content = company_content[0]["fields"]
	return render_to_response('company.html', content)

def companies_games(request, id):
	return HttpResponse([], content_type="application/json")

def companies_people(request, id):
	return HttpResponse([], content_type="application/json")
