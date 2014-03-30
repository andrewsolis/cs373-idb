from django.core import serializers
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
from json import dumps
from django.views.decorators.csrf import csrf_exempt
from idb.videogames.models import *

def validate_game_json(game_object) :
	return true

@csrf_exempt
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

@csrf_exempt
def games_id(request, game_id):
	response = "empty"
	if(request.method == 'GET'):
		response = serializers.serialize("json", [Game.objects.get(pk = int(game_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		Game.objects.get(pk = int(game_id)).delete()
	return HttpResponse(response, content_type = "application/json")

def games_people(request, game_id):
	response = "empty"
	people_dictionary = Game.objects.filter(pk = int(game_id)).values('people')[0] # output: {'people': None}
	people_list = people_dictionary.get('people')
	if people_list is not None:
		for person_id in people_list:
			response.append(serializers.serialize("json", Person.objects.filter(pk = int(person_id)))) 
	return HttpResponse(response, content_type = "application/json")

def games_companies(request, game_id):
	response = "empty"
	company_dictionary = Game.objects.filter(pk = int(game_id)).values('company')[0] # output: {'company': 1}
	company_id = company_dictionary.get('company')
	if company_id is not None:
		response = serializers.serialize("json", Company.objects.filter(pk = int(company_id)))
	return HttpResponse(response, content_type = "application/json")

@csrf_exempt
def people(request):
	people_list = []
	if(request.method == 'GET'):
		people_list = serializers.serialize("json", Person.objects.all())
	elif(request.method == 'POST'):
		pass
	return HttpResponse(people_list, content_type = "application/json")

@csrf_exempt
def people_id(request, people_id):
	response = ""
	if(request.method == 'GET'):
		response = serializers.serialize("json", [Person.objects.get(pk = int(people_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		Person.objects.get(pk = int(people_id)).delete()
	return HttpResponse(response, content_type = "application/json")

def people_games(request, people_id):
	return HttpResponse([], content_type = "application/json")

def people_companies(request, people_id):
	return HttpResponse([], content_type = "application/json")

@csrf_exempt
def companies(request):
	companies_list = []
	if(request.method == 'GET'):
		companies_list = serializers.serialize("json",Company.objects.all())
	elif(request.method == 'POST'):
		pass
	return HttpResponse(companies_list, content_type = "application/json")

@csrf_exempt
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
