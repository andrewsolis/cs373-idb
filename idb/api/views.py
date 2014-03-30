from django.core import serializers
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
from json import dumps

from idb.videogames.models import *

def validate_game_json(game_object) :
	return true

def games(request):
	games_list = []
	if(request.method == 'GET'):
		games_list = serializers.serialize("json", Game.objects.all())
	elif(request.method == 'POST'):
		request_data = requset.POST
		for deserialized_object in serializers.deserialize("json", request_data) :
			if (validate_game_json(deserialized_object)):
				pass
				# deserialized_object.save()
	return HttpResponse(games_list, content_type = "application/json")

def games_id(request, game_id):
	game = ""
	if(request.method == 'GET'):
		game = serializers.serialize("json", [Game.objects.get(pk = int(game_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		Game.objects.get(pk = int(game_id)).delete()
	return HttpResponse(game, content_type = "application/json")

def games_people(request, game_id):
	response = "empty"
	game = Game.objects.filter(pk = int(game_id)).values('people')[0] # output: {'people': None}
	people_list = game.get('people')
	if people_list is not None:
		for p in people_list:
			response.append(serializers.serialize("json", Person.objects.filter(pk = int(p)))) 
	return HttpResponse(response, content_type = "application/json")

def games_companies(request, game_id):
	companies_list = []
	if (request.method == 'GET'):
		companies_list = serializers.serialize("json", Company.objects.all())
	return HttpResponse(companies_list, content_type = "application/json")

def people(request):
	people_list = []
	if(request.method == 'GET'):
		people_list = serializers.serialize("json", Person.objects.all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(people_list, content_type = "application/json")

def people_id(request, people_id):
	person = ""
	if(request.method == 'GET'):
		person = serializers.serialize("json", [Person.objects.get(pk = int(people_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		Person.objects.get(pk = int(people_id)).delte()
	return HttpResponse(person, content_type = "application/json")

def people_games(request, people_id):
	return HttpResponse([], content_type = "application/json")

def people_companies(request, people_id):
	return HttpResponse([], content_type = "application/json")

def companies(request):
	companies_list = []
	if(request.method == 'GET'):
		companies_list = serializers.serialize("json",Company.objects.all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(companies_list, content_type = "application/json")
#	return HttpResponse(str(x), content_type = "plain/text")

def companies_id(request, company_id):
	company = ""
	if(request.method == 'GET'):
		company = serializers.serialize("json",[Company.objects.get(pk = int(company_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		Company.objects.get(pk = int(company_id)).delete()
	return HttpResponse(company, content_type = "application/json")

def companies_games(request, company_id):
	return HttpResponse([], content_type = "application/json")

def companies_people(request, company_id):
	return HttpResponse([], content_type = "application/json")
