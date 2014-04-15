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
		person_content[0]["fields"]["DOB"] = person_content[0]["fields"]["DOB"][:10]
		
		company_content = api_people_companies(request, id)
		company_content = serializers.deserialize("json", company_content.content)
		person_content[0]["fields"]["companies"] = list(company_content)

		game_content = api_people_games(request, id)
		game_content = serializers.deserialize("json", game_content.content)
		person_content[0]["fields"]["games"] = list(game_content)
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
		company_content[0]["fields"]["founded"] = company_content[0]["fields"]["founded"][:10]
		
		people_content = api_companies_people(request, id)
		people_content = serializers.deserialize("json", people_content.content)
		company_content[0]["fields"]["people"] = list(people_content)

		game_content = api_companies_games(request, id)
		game_content = serializers.deserialize("json", game_content.content)
		company_content[0]["fields"]["games"] = list(game_content)
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
	result = serializers.deserialize("json", games_list.content)
	result = list(result)
	numGames = len(result)
	for i in result:
		game = api_games_id(request,i.object.pk)
		game_content = json.loads(game.content.decode("utf-8"))
		content = game_content[0]["fields"]
		copies.append(content["copies"])
		game_names.append(content["name"])
		for i in content["genre"]:
			genre_dict[i] += 1
	for key in genre_dict:
		genre_names.append(key)
		genres.append(genre_dict[key])	

	result = serializers.deserialize("json", companies_list.content)
	result = list(result)
	for i in result:
		company = api_companies_id(request, i.object.pk)
		company_content = json.loads(company.content.decode("utf-8"))
		content = company_content[0]["fields"]
		company_content[0]["fields"]["games"] = list(serializers.deserialize("json", api_companies_games(request, i.object.pk).content))
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
	query_string_lowercase = ''
	games_list = []
	companies_list = []
	people_list = []

	if ('q' in request.GET) and request.GET['q'].strip():
			query_string = request.GET['q']
			query_string_lowercase = query_string.lower()
			query_string_lowercase = query_string_lowercase.split("or")
			for q in query_string_lowercase:
				
				entry_query = get_query(q, ['synopsis','name',])

				games_list.extend(Game.objects.filter(entry_query))
				for g in games_list:
					g.type = 'games'
				
				entry_query = get_query(q, ['name','description','location',])
				companies_list.extend(Company.objects.filter(entry_query))
				for c in companies_list:
					c.type = 'companies'

				entry_query = get_query(q, ['name','description', 'residence',])
				people_list.extend(Person.objects.filter(entry_query))
				for p in people_list:
					p.type = 'people'

	result_list = list(chain(games_list, companies_list, people_list))
	result_list =list(set(result_list))
	# return HttpResponse(query_string, content_type = "application/json")
	return render_to_response('search.html', {'items': result_list, 'query' : query_string})

def error404(request):
	return render_to_response('notFound.html')