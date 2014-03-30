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
def api_games(request):
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
def api_games_id(request, game_id):
	response = "empty"
	if(request.method == 'GET'):
		response = serializers.serialize("json", [Game.objects.get(pk = int(game_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		Game.objects.get(pk = int(game_id)).delete()
	return HttpResponse(response, content_type = "application/json")

def api_games_people(request, game_id):
	response = "empty"
	people_dictionary = Game.objects.filter(pk = int(game_id)).values('people')[0]
	person_id = people_dictionary.get('people')
	if person_id is not None:
		response = serializers.serialize("json", Person.objects.filter(pk = int(person_id))) 
	return HttpResponse(response, content_type = "application/json")

def api_games_companies(request, game_id):
	response = "empty"
	company_dictionary = Game.objects.filter(pk = int(game_id)).values('company')[0]
	company_id = company_dictionary.get('company')
	if company_id is not None:
		response = serializers.serialize("json", Company.objects.filter(pk = int(company_id)))
	return HttpResponse(response, content_type = "application/json")

@csrf_exempt
def api_people(request):
	people_list = []
	if(request.method == 'GET'):
		people_list = serializers.serialize("json", Person.objects.all())
	elif(request.method == 'POST'):
		pass
	return HttpResponse(people_list, content_type = "application/json")

@csrf_exempt
def api_people_id(request, people_id):
	response = ""
	if(request.method == 'GET'):
		response = serializers.serialize("json", [Person.objects.get(pk = int(people_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		Person.objects.get(pk = int(people_id)).delete()
	return HttpResponse(response, content_type = "application/json")

def api_people_games(request, people_id):
	response = "empty"
	games = Game.objects.filter(people = people_id)
	if games is not None:
		response = serializers.serialize("json", games) 
	return HttpResponse(response, content_type = "application/json")

def api_people_companies(request, people_id):
	response = "empty"
	person_dictionary = Person.objects.filter(pk = int(people_id)).values('companies')[0]
	company_id = person_dictionary.get('companies')
	if company_id is not None:
		response = serializers.serialize("json", Company.objects.filter(pk = int(company_id))) 
	return HttpResponse(response, content_type = "application/json")

@csrf_exempt
def api_companies(request):
	companies_list = []
	if(request.method == 'GET'):
		companies_list = serializers.serialize("json",Company.objects.all())
	elif(request.method == 'POST'):
		pass
	return HttpResponse(companies_list, content_type = "application/json")

@csrf_exempt
def api_companies_id(request, company_id):
	company = ""
	if(request.method == 'GET'):
		company = serializers.serialize("json",[Company.objects.get(pk = int(company_id))])
	elif(request.method == 'PUT'):
		pass
	elif(request.method == 'DELETE'):
		Company.objects.get(pk = int(company_id)).delete()
	return HttpResponse(company, content_type = "application/json")

def api_companies_games(request, company_id):
	response = "empty"
	games = Game.objects.filter(company = company_id)
	if games is not None:
		response = serializers.serialize("json", games) 
	return HttpResponse(response, content_type = "application/json")

def api_companies_people(request, company_id):
	response = "empty"
	people = Person.objects.filter(companies = company_id)
	if people is not None:
		response = serializers.serialize("json", people) 
	return HttpResponse(response, content_type = "application/json")
