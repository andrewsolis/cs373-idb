from django.shortcuts import *
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse
import json
from idb.videogames.models import *
from idb.api.views import *
from idb.search import *
from itertools import chain
from ast import literal_eval
import time
from types import *

def home(request):
	return render_to_response('home.html', {}, RequestContext(request))

def games(request):
	games_list = json.loads(api_games(request).content.decode("utf-8"))
	return render_to_response('cgp_index.html', {'items': games_list, 'collection': 'Game', 'collections': 'Games'})

def games_id(request, id):
	try: 
		game = api_games_id(request,id)
		game_content = json.loads(game.content.decode("utf-8"))
		content = game_content[0]["fields"]
		genres = ""
		for genre in content['genre']:
			genres = genres + genre + ", "
		content['genre'] = genres[:-2]
		content["release_date"] = content["release_date"][:10]

		content["company"] = literal_eval(api_games_companies(request, id).content.decode("utf-8"))[0]
		content["people"] = literal_eval(api_games_people(request, id).content.decode("utf-8"))

		return render_to_response('game.html', content)
	except:
		return render_to_response('notFound.html', {}, RequestContext(request))

def people(request):
	people_list = json.loads(api_people(request).content.decode("utf-8"))
	return render_to_response('cgp_index.html', {'items': people_list, 'collection': 'Person', 'collections': 'People'})

def people_id(request, id):
	try:
		person = api_people_id(request,id)
		person_content = json.loads(person.content.decode("utf-8"))
		content = person_content[0]["fields"]
		content['twitter'] = person_content[0]["fields"]["twitter"]
		content["DOB"] = content["DOB"][:10]
		
		content["companies"] = literal_eval(api_people_companies(request, id).content.decode("utf-8"))
		content["games"] = literal_eval(api_people_games(request, id).content.decode("utf-8"))

		return render_to_response('person.html', content)
	except:
		return render_to_response('notFound.html', {}, RequestContext(request))

def companies(request):
	companies_list = json.loads(api_companies(request).content.decode("utf-8"))
	return render_to_response('cgp_index.html', {'items': companies_list, 'collection': 'Company', 'collections': 'Companies'})

def companies_id(request, id):
	try:
		company = api_companies_id(request,id)
		company_content = json.loads(company.content.decode("utf-8"))
		content = company_content[0]["fields"]
		content["founded"] = content["founded"][:10]
		
		content["people"] = literal_eval(api_companies_people(request, id).content.decode("utf-8"))
		content["games"] = literal_eval(api_companies_games(request, id).content.decode("utf-8"))

		return render_to_response('company.html', content)
	except:
		return render_to_response('notFound.html', {}, RequestContext(request))

def stats(request):
	copies = []
	game_names = []
	games_per_company = []
	company_names = []
	genre_names = []
	genres = []

	games_list = api_games(request)
	companies_list = api_companies(request)
	genres_list = api_genre(request)
	genre_dict = {"Side Scroller":0, "Platforming":0, "Racing":0, "Party":0, "Arcade":0,"Strategy":0,"Fighting":0,"Action-Adventure":0, "Role-Playing Game":0, "Sports":0, "Shooter":0, "Beat 'em up":0, "FPS":0, "Simulation":0, "Strategy":0, "Puzzle":0, "Card":0, "Board":0}
	result = json.loads(games_list.content.decode("utf-8"))
	result = list(result)
	numGames = len(result)
	for i in result:
		game = api_games_id(request,i["pk"])
		game_content = json.loads(game.content.decode("utf-8"))
		content = game_content[0]["fields"]
		copies.append(content["copies"])
		game_names.append(content["name"])
		for i in content["genre"]:
			genre_dict[i] += 1
	for key in genre_dict:
		genre_names.append(key)
		genres.append(genre_dict[key])	

		result = json.loads(companies_list.content.decode("utf-8"))
	result = list(result)
	for i in result:
		company = api_companies_id(request, i["pk"])
		company_content = json.loads(company.content.decode("utf-8"))
		content = company_content[0]["fields"]
		company_content[0]["fields"]["games"] = list(json.loads(api_companies_games(request, i["pk"]).content.decode("utf-8")))
		games_per_company.append(len(content["games"]))
		company_names.append(content["name"])

	copies = json.dumps(copies)
	game_names = json.dumps(game_names)
	company_names = json.dumps(company_names)
	games_per_company = json.dumps(games_per_company)
	genre_names = json.dumps(genre_names)
	genres = json.dumps(genres)
	return render_to_response('stats.html', {"copies":copies,"numGames": numGames, "game_names":game_names, "games_per_company":games_per_company, "company_names":company_names, "genre_names":genre_names, "genres":genres}, RequestContext(request))

def search(request):
	query_string = ''

	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']

	result_list = search_crawl(request, str(query_string))
	return HttpResponse(result_list, content_type = "application/json")
	
def sql(request):
	return render_to_response('sql.html', {}, RequestContext(request))

def error404(request):
	return render_to_response('notFound.html')