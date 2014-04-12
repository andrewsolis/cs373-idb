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
	result = list(result)
	return render_to_response('cgp_index.html', {'items': result, 'collection': 'Game', 'collections': 'Games'})

def games_id(request, id):
	try: 
		game = api_games_id(request,id)
		game_content = json.loads(game.content.decode("utf-8"))
		content = game_content[0]["fields"]
		genres = ""
		for genre in content['genre']:
			genres = genres + genre + ", "
		content['genre'] = genres[:-2]
		game_content[0]["fields"]["release_date"] = game_content[0]["fields"]["release_date"][:10]
		if len(content['images']) != 0:
			content['images'] = content['images'][0]
		if len(content['videos']) != 0:
			content['videos'] = content['videos'][0]

		company_content = api_games_companies(request, id)
		company_content = serializers.deserialize("json", company_content.content)
		game_content[0]["fields"]["company"] = list(company_content)[0]
		
		people_content = api_games_people(request, id)
		people_content = serializers.deserialize("json", people_content.content)
		game_content[0]["fields"]["people"] = list(people_content)
		return render_to_response('game.html', content)
	except:
		return render_to_response('notFound.html', {}, RequestContext(request))

def people(request):
	people_list = api_people(request)
	result = serializers.deserialize("json", people_list.content)
	return render_to_response('cgp_index.html', {'items': result, 'collection': 'People', 'collections': 'People'})

def people_id(request, id):
	try:
		person = api_people_id(request,id)
		person_content = json.loads(person.content.decode("utf-8"))
		content = person_content[0]["fields"]
		if len(content['images']) != 0:
			content['images'] = content['images'][0]
		if len(content['videos']) != 0:
			content['videos'] = content['videos'][0]
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
	companies_list = api_companies(request)
	result = serializers.deserialize("json", companies_list.content)
	return render_to_response('cgp_index.html', {'items': result, 'collection': 'Company', 'collections': 'Companies'})

def companies_id(request, id):
	try:
		company = api_companies_id(request,id)
		company_content = json.loads(company.content.decode("utf-8"))
		content = company_content[0]["fields"]
		if len(content['images']) != 0: 
			content['images'] = content['images'][0]
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

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['title', 'body',])
        
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

    return render_to_response('search.html', {}, RequestContext(request))