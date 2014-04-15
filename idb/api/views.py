from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
from django.db import models
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
	if (len(request_data.get("companies")) == 0):
		raise
	for company in request_data["companies"]:
		Company.objects.get(pk = int(company))

def validate_images(request_data):
	if (len(request_data["images"]) == 0):
		raise
	for image in request_data["images"]:
		if not non_empty_string(image):
			raise

def validate_videos(request_data):
	if (len(request_data["videos"]) == 0):
		raise
	for video in request_data["videos"]:
		if not non_empty_string(video):
			raise

def validate_game_data(request_data):
	# print(request_data)
	if (not(("name" in request_data) and non_empty_string(request_data["name"]))):
		raise
	if (len(request_data["people"]) == 0):
		raise
	for person in request_data["people"]:
		Person.objects.get(pk = int(person))
	if (len(request_data["genre"]) == 0):
		raise
	if request_data.get("company") is None:
		raise
	else:
		Company.objects.get(pk = int(request_data["company"]))
	if request_data.get("system") is None:
		raise

@csrf_exempt
def api_games(request):
	response = ""
	response_code = 400
	new_game_saved = False
	new_image_saved = False
	if(request.method == 'GET'):
		game_objects = Game.objects.all()
		game_list = []
		for game in game_objects:
			game_dict = literal_eval(serializers.serialize('json', [game], fields=('name')))[0]
			image_list = [image.link for image in game.images()]
			game_dict["fields"]["images"] = image_list
			game_list.append(game_dict)
		response = dumps(game_list)
		response_code = 200
	elif(request.method == 'POST'):
		try:
			request_data = literal_eval(request.read().decode('utf-8'))
			validate_game_data(request_data)
			validate_images(request_data)
			validate_videos(request_data)
			people_list = request_data.pop("people")
			image_list = request_data.pop("images")
			video_list = request_data.pop("videos")
			genre_list = request_data.pop("genre")
			genre_list = [Genre.objects.get(types = genre).pk for genre in genre_list]
			request_data["company"] = Company.objects.get(pk=int(request_data["company"]))
			request_data["system"] = System.objects.get(platform=request_data["system"])
			new_game = Game(**request_data)
			new_game.save()
			new_game_saved = True
			for person in people_list:
				new_game.people.add(int(person))
			for genre in genre_list:
				new_game.genre.add(genre)
			for image in image_list:
				Images(link=image, other_id=new_game.pk, other_type='GM').save()
			for video in video_list:
				Videos(link=video, other_id=new_game.pk, other_type='GM').save()
			response = dumps({"id" : new_game.pk})
			response_code = 201
		except ObjectDoesNotExist:
			if new_game_saved:
				new_game.delete()
			response_code = 404
		except:
			if new_game_saved:
				new_game.delete()
			response_code = 400
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_games_id(request, game_id):
	response = ""
	response_code = 400
	if(request.method == 'GET'):
		try:
			game_object = Game.objects.get(pk = int(game_id))
			game = literal_eval(serializers.serialize("json",[game_object]))
			genre_list = game[0]["fields"]["genre"]
			game[0]["fields"]["system"] = game_object.system.platform
			game[0]["fields"]["genre"] = [Genre.objects.get(pk = int(genre)).types for genre in genre_list]
			game[0]["fields"]["images"] = [image.link for image in game_object.images()]
			game[0]["fields"]["videos"] = [video.link for video in game_object.videos()]
			response = dumps(game)
			response_code = 200
		except:  
			response_code = 404
	elif(request.method == 'PUT'):
		try:
			game_object = Game.objects.get(pk = int(game_id))
			game = literal_eval(serializers.serialize("json",[game_object]))
			request_data = literal_eval(request.read().decode('utf-8'))
			if request_data.get("system") is not None:
				request_data["system"] = System.objects.get(platform=request_data["system"]).pk
			if request_data.get("genre") is not None:
				request_data["genre"] = [Genre.objects.get(types = genre).pk for genre in request_data["genre"]]
			for k in request_data:
				if k in game[0]["fields"]:
					game[0]["fields"][k] = request_data[k]
			validate_game_data(game[0]["fields"])
			if request_data.get("images") is not None:
				validate_images(request_data)
			if request_data.get("videos") is not None:
				validate_videos(request_data)
			game = dumps(game)
			for deserialized_object in serializers.deserialize("json", game):
				deserialized_object.save()
			if request_data.get("images") is not None:
				for image in game_object.images():
					image.delete()
				for image in request_data["images"]:
					Images(link=image, other_id=int(game_id), other_type='GM').save()
			if request_data.get("videos") is not None:
				for video in game_object.videos():
					video.delete()
				for video in request_data["videos"]:
					Videos(link=video, other_id=int(game_id), other_type='GM').save()
			response_code = 204
		except ObjectDoesNotExist:
			response_code = 404
		except:
			response_code = 400
	elif(request.method == 'DELETE'):
		try:
			game_object = Game.objects.get(pk = int(game_id))
			for image in game_object.images():
				image.delete()
			for video in game_object.videos():
				video.delete()
			game_object.delete()
			response_code = 204
		except:
			response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_games_people(request, game_id):
	response = ""
	response_code = 400
	try:
		response = serializers.serialize("json", Game.objects.get(pk = int(game_id)).people.all(), fields=("name"))
		response_code = 200
	except: 
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_games_companies(request, game_id):
	response = ""
	response_code = 400
	try:
		response = serializers.serialize("json", [Game.objects.get(pk = int(game_id)).company], fields=("name"))
		response_code = 200
	except:
		response_code = 404	
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_people(request):
	response = ""
	response_code = 400
	new_person_saved = False
	new_image_saved = False
	if(request.method == 'GET'):
		person_objects = Person.objects.all()
		person_list = []
		for person in person_objects:
			person_dict = literal_eval(serializers.serialize('json', [person], fields=('name')))[0]
			image_list = [image.link for image in person.images()]
			person_dict["fields"]["images"] = image_list
			person_list.append(person_dict)
		response = dumps(person_list)
		response_code = 200
	elif(request.method == 'POST'):
		try:
			request_data = literal_eval(request.read().decode('utf-8'))
			# validates person and throws exception
			validate_person_data(request_data)
			validate_images(request_data)
			validate_videos(request_data)
			company_list = request_data.pop("companies")
			image_list = request_data.pop("images")
			video_list = request_data.pop("videos")
			new_person = Person(**request_data)
			new_person.save()
			new_person_saved = True
			for company in company_list:
				new_person.companies.add(int(company))
			for image in image_list:
				Images(link=image, other_id=new_person.pk, other_type='PPL').save()
			for video in video_list:
				Videos(link=video, other_id=new_person.pk, other_type='PPL').save()
			response = dumps({"id" : new_person.pk})
			response_code = 201
		except ObjectDoesNotExist:
			if new_person_saved:
				new_person.delete()
			response_code = 404
		except:
			if new_person_saved:
				new_person.delete()
			response_code = 400
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_people_id(request, people_id):
	response = ""
	response_code = 400
	if(request.method == 'GET'):
		try:
			people_object = Person.objects.get(pk = int(people_id))
			person = literal_eval(serializers.serialize("json",[people_object]))
			person[0]["fields"]["images"] = [image.link for image in people_object.images()]
			person[0]["fields"]["videos"] = [video.link for video in people_object.videos()]
			response = serializers.serialize("json",[Person.objects.get(pk = int(people_id))])
			response = dumps(person)
			response_code = 200
		except:
			response_code = 404
	elif(request.method == 'PUT'):
		try:
			person_object = Person.objects.get(pk =int(people_id))
			person = literal_eval(serializers.serialize("json",[person_object]))
			request_data = literal_eval(request.read().decode('utf-8'))
			for k in request_data:
				if k in person[0]["fields"]:
					person[0]["fields"][k] = request_data[k]
			validate_person_data(person[0]["fields"])
			if request_data.get("images") is not None:
				validate_images(request_data)
			if request_data.get("videos") is not None:
				validate_videos(request_data)
			person = dumps(person)
			for deserialized_object in serializers.deserialize("json", person): 
				deserialized_object.save()
			if request_data.get("images") is not None:
				for image in person_object.images():
					image.delete()
				for image in request_data["images"]:
					Images(link=image, other_id=int(people_id), other_type='PPL').save()
			if request_data.get("videos") is not None:
				for video in person_object.videos():
					video.delete()
				for video in request_data["videos"]:
					Videos(link=video, other_id=int(people_id), other_type='PPL').save()
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
	response_code = 400
	response = ""
	try:
		result = serializers.serialize("json", Game.objects.filter(people = people_id).all(), fields=("name"))
		if (result == "[]"):
				raise
		response = result
		response_code = 200
	except:
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_people_companies(request, people_id):
	response_code = 400
	response = ""
	try:
		result = serializers.serialize("json", Person.objects.get(pk = int(people_id)).companies.all(), fields=("name"))
		if (result == "[]"):
				raise
		response = result
		response_code = 200
	except:
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_companies(request):
	response = ""
	response_code = 400
	new_company_saved = False
	if(request.method == 'GET'):
		company_objects = Company.objects.all()
		company_list = []
		for company in company_objects:
			company_dict = literal_eval(serializers.serialize('json', [company], fields=('name')))[0]
			image_list = [image.link for image in company.images()]
			company_dict["fields"]["images"] = image_list
			company_list.append(company_dict)
		response = dumps(company_list)
		response_code = 200
	elif(request.method == 'POST'):
		try:
			request_data = literal_eval(request.read().decode('utf-8'))
			# validates company and throws exception
			validate_company_data(request_data)
			validate_images(request_data)
			image_list = request_data.pop("images")
			new_company = Company(**request_data)
			new_company.save()
			new_company_saved = True
			for image in image_list:
				Images(link=image, other_id=new_company.pk, other_type='CP').save()
			# Images(link=image_link, other_id=new_company.pk, other_type='CP').save()
			response = dumps({"id" : new_company.pk})
			response_code = 201
		except:
			if new_company_saved:
				new_company.delete()
			response_code = 400
	return HttpResponse(response, content_type = "application/json", status = response_code)

@csrf_exempt
def api_companies_id(request, company_id):
	response = ""
	response_code = 400
	if(request.method == 'GET'):
		try:
			company_object = Company.objects.get(pk = int(company_id))
			company = literal_eval(serializers.serialize("json",[company_object]))
			company[0]["fields"]["images"] = [image.link for image in company_object.images()]
			response = dumps(company)
			response_code = 200
		except:
			response_code = 404
	elif(request.method == 'PUT'):
		try:
			company_object = Company.objects.get(pk =int(company_id))
			company = literal_eval(serializers.serialize("json",[company_object]))
			request_data = literal_eval(request.read().decode('utf-8'))
			# validates company and throws exception
			for k in request_data:
				if k in company[0]["fields"]:
					company[0]["fields"][k] = request_data[k]
			validate_company_data(company[0]["fields"])
			if request_data.get("images") is not None:
				validate_images(request_data)
			company = dumps(company)
			for deserialized_object in serializers.deserialize("json", company):
				deserialized_object.save()
			if request_data.get("images") is not None:
				for image in company_object.images():
					image.delete()
				for image in request_data["images"]:
					Images(link=image, other_id=int(company_id), other_type='CP').save()
			response_code = 204
		except ObjectDoesNotExist:
			response_code = 404
		except:
			response_code = 400
	elif(request.method == 'DELETE'):
		try:
			company_object = Company.objects.get(pk = int(company_id))
			for image in company_object.images():
				image.delete()
			company_object.delete()
			response_code = 204
		except:
			response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_companies_games(request, company_id):
	response = ""
	response_code = 400
	try:
		result = serializers.serialize("json", Game.objects.filter(company = company_id), fields=("name"))
		if (result == "[]"):
			raise
		response = result
		response_code = 200
	except:
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_companies_people(request, company_id):
	response = ""
	response_code = 400
	try:
		result = serializers.serialize("json", Person.objects.filter(companies = company_id), fields=("name"))
		if (result == "[]"):
			raise
		response = result
		response_code = 200
	except:
		response_code = 404
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_genre(request):
	response = ""
	response_code = 200
	response = serializers.serialize("json", Genre.objects.all())
	return HttpResponse(response, content_type = "application/json", status = response_code)

def api_system(request):
	response = ""
	response_code = 200
	response = serializers.serialize("json", System.objects.all())
	return HttpResponse(response, content_type = "application/json", status = response_code)