from django.core import serializers
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
from json import dumps

from idb.videogames.models import *

def games(request):
	games_list = []
	if(request.method == 'GET'):
		games_list = serializers.serialize("json",Game.objects.order_by('-id').all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(games_list, content_type="application/json")
#	return HttpResponse(str(x), content_type="plain/text")

def games_id(request, game_id):
	if(request.method == 'GET'):
		game = serializers.serialize("json",[Game.objects.get(pk = int(game_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		pass

	return HttpResponse(game, content_type="application/json")

def games_people(request, id):
#	game = 
#	myPeople = serializers.serialize("json",)
	return HttpResponse([], content_type="application/json")

def games_companies(request, id):

	return HttpResponse([], content_type="application/json")



def people(request):
	people_list = []
	if(request.method == 'GET'):
		people_list = serializers.serialize("json",Person.objects.order_by('-id').all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(people_list, content_type="application/json")
#	return HttpResponse(str(x), content_type="plain/text")

def people_id(request, people_id):
	if(request.method == 'GET'):
		person = serializers.serialize("json",[Person.objects.get(pk = int(people_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		pass

	return HttpResponse(person, content_type="application/json")

def people_games(request, id):
	return HttpResponse([], content_type="application/json")

def people_companies(request, id):
	return HttpResponse([], content_type="application/json")

def companies(request):
	companies_list = []
	if(request.method == 'GET'):
		companies_list = serializers.serialize("json",Company.objects.order_by('-id').all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(companies_list, content_type="application/json")
#	return HttpResponse(str(x), content_type="plain/text")

def companies_id(request, company_id):
	if(request.method == 'GET'):
		company = serializers.serialize("json",[Company.objects.get(pk = int(company_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		pass

	return HttpResponse(company, content_type="application/json")

def companies_games(request, id):
	return HttpResponse([], content_type="application/json")

def companies_people(request, id):
	return HttpResponse([], content_type="application/json")
