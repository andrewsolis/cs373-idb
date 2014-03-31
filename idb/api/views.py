from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
from idb.videogames.models import *
from ast import literal_eval
from json import dumps, loads

def non_empty_string(string):
	return len(''.join(string).split()) != 0

def validate_company_data(request_data):
	if (not(("name" in request_data) and non_empty_string(request_data["name"]))):
		raise

def validate_person_data(request_data):
	if (not(("name" in request_data) and non_empty_string(request_data["name"]))):
		raise
	if len(request_data["companies"]) == 0:
		raise
	for company in request_data["companies"]:
		Company.objects.get(pk = int(company))	


def validate_game_data(request_data):
	raise

@csrf_exempt
def api_games(request):
	response = ""
	response_code = 400
	if(request.method == 'GET'):
		response = serializers.serialize("json", Game.objects.all())
		response_code = 200
	elif(request.method == 'POST'):
		try:
			game = literal_eval(serializers.serialize("json",[Game.objects.get(pk =int(game_id))]))
			request_data = literal_eval(request.read().decode('utf-8'))
			for k in request_data:
				if k in game[0]["fields"]:
					game[0]["fields"][k] = request_data[k]
			game = dumps(game)
			for deserialized_object in serializers.deserialize("json", game):
				deserialized_object.save()
				response_code = 204
		except ObjectDoesNotExist:
			response_code = 404
		except:
			response_code = 400
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_games_id(request, game_id):
	response = ""
	response_code = 400
	if(request.method == 'GET'):
		try:
			response = serializers.serialize("json",[Game.objects.get(pk = int(game_id))])
			response_code = 200
		except:
			response_code = 404
	elif(request.method == 'PUT'):
		try:
			game = literal_eval(serializers.serialize("json",[Game.objects.get(pk =int(game_id))]))
			request_data = literal_eval(request.read().decode('utf-8'))
			for k in request_data:
				if k in game[0]["fields"]:
					game[0]["fields"][k] = request_data[k]
			game = dumps(game)
			for deserialized_object in serializers.deserialize("json", game):
				deserialized_object.save()
				response_code = 204
		except ObjectDoesNotExist:
			response_code = 404
		except:
			response_code = 400
	elif(request.method == 'DELETE'):
		try:
			Game.objects.get(pk = int(game_id)).delete()
			response_code = 204
		except:
			response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_games_people(request, game_id):
	response = ""
	response_code = 400
	try:
		people_dictionary = Game.objects.get(pk = int(game_id)).values('people')[0]
		person_id = people_dictionary.get('people')
		if person_id is not None:
			response = serializers.serialize("json", Person.objects.get(pk = int(person_id))) 
		response_code = 200
	except: 
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_games_companies(request, game_id):
	response = ""
	response_code = 400
	try:
		company_dictionary = Game.objects.get(pk = int(game_id)).values('company')[0]
		company_id = company_dictionary.get('company')
		if company_id is not None:
			response = serializers.serialize("json", Company.objects.get(pk = int(company_id)))
		response_code = 200
	except:
		response_code = 404	
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_people(request):
	response = ""
	response_code = 400
	new_person_saved = False
	if(request.method == 'GET'):
		response = serializers.serialize("json", Person.objects.all())
		response_code = 200
	elif(request.method == 'POST'):
		try:
			request_data = literal_eval(request.read().decode('utf-8'))
			# validates person and throws exception
			validate_person_data(request_data)
			company_list = request_data["companies"]
			request_data.pop("companies")
			new_person = Person(**request_data)
			new_person_saved = True
			new_person.save()
			for company in company_list:
				new_person.companies.add(int(company))
			response_code = 201
		except ObjectDoesNotExist:
			if new_person_saved:
				new_person.delete()
			response_code = 400
		except:
			response_code = 400
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_people_id(request, people_id):
	response = ""
	response_code = 400
	if(request.method == 'GET'):
		try:
			response = serializers.serialize("json",[Person.objects.get(pk = int(people_id))])
			response_code = 200
		except:
			response_code = 404
	elif(request.method == 'PUT'):
		try:
			person = literal_eval(serializers.serialize("json",[Person.objects.get(pk =int(people_id))]))
			request_data = literal_eval(request.read().decode('utf-8'))
			validate_person_data(request_data)
			for k in request_data:
				if k in person[0]["fields"]:
					person[0]["fields"][k] = request_data[k]
			person = dumps(person)
			for deserialized_object in serializers.deserialize("json", person): 
				deserialized_object.save()
				response_code = 204
		except ObjectDoesNotExist:
			response_code = 404
		except:
			response_code = 400
	elif(request.method == 'DELETE'):
		try:
			Person.objects.get(pk = int(people_id)).delete()
			response_code = 204
		except:
			response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_people_games(request, people_id):
	response = ""
	response_code = 400
	try:
		games = Game.objects.get(people = people_id)
		if games is not None:
			response = serializers.serialize("json", games)
		response_code = 200
	except:
		response_code = 404 
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_people_companies(request, people_id):
	response = ""
	response_code = 400
	try:
		person_dictionary = Person.objects.get(pk = int(people_id)).values('companies')[0]
		company_id = person_dictionary.get('companies')
		if company_id is not None:
			response = serializers.serialize("json", Company.objects.get(pk = int(company_id))) 
		response_code = 200
	except:
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_companies(request):
	response = ""
	response_code = 400
	if(request.method == 'GET'):
		response = serializers.serialize("json",Company.objects.all())
		response_code = 200
	elif(request.method == 'POST'):
		try:
			request_data = literal_eval(request.read().decode('utf-8'))
			# validates company and throws exception
			validate_company_data(request_data)
			Company(**request_data).save()
			response_code = 201
		except:
			response_code = 400
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_companies_id(request, company_id):
	response = ""
	response_code = 400
	if(request.method == 'GET'):
		try:
			response = serializers.serialize("json",[Company.objects.get(pk = int(company_id))])
			response_code = 200
		except:
			response_code = 404
	elif(request.method == 'PUT'):
		try:
			company = literal_eval(serializers.serialize("json",[Company.objects.get(pk =int(company_id))]))
			request_data = literal_eval(request.read().decode('utf-8'))
			for k in request_data:
				if k in company[0]["fields"]:
					company[0]["fields"][k] = request_data[k]
			company = dumps(company)
			for deserialized_object in serializers.deserialize("json", company):
				deserialized_object.save()
				response_code = 204
		except ObjectDoesNotExist:
			response_code = 404
		except:
			response_code = 400
	elif(request.method == 'DELETE'):
		try:
			Company.objects.get(pk = int(company_id)).delete()
			response_code = 204
		except:
			response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_companies_games(request, company_id):
	response = ""
	response_code = 400
	try:
		games = Game.objects.get(company = company_id)
		if games is not None:
			response = serializers.serialize("json", games) 
		response_code = 200
	except:
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_companies_people(request, company_id):
	response = ""
	response_code = 400
	try:
		people = Person.objects.get(companies = company_id)
		if people is not None:
			response = serializers.serialize("json", people) 
		response_code = 200
	except:
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)