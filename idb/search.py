from django.shortcuts import *
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse
import re # regular expressions
import json
from idb.videogames.models import *
from idb.api.views import *
from ast import literal_eval

from django.db.models import Q # query objects

def search_crawl(request, query_string):
    games_list = []
    companies_list = []
    people_list = []
    content = {}

    query_string_list = query_string.split(" ")
    result_list = []

    base_url = 'http://retro-video-games-373.herokuapp.com/'

    games = json.loads(api_games(request).content.decode("utf-8"))
    companies = json.loads(api_companies(request).content.decode("utf-8"))
    people = json.loads(api_people(request).content.decode("utf-8"))
    
    for g in games:
        valid_result = {}
        valid_result['id'] = g['pk']
        valid_result['total'] = 0
        valid_result['url'] = base_url + "games/" + str(valid_result['id']) + "/"

        game = api_games_id(request,g['pk'])
        game_content = json.loads(game.content.decode("utf-8"))
        content = game_content[0]["fields"]
        genres = ""
        for genre in content['genre']:
            genres = genres + genre + ", "
        content['genre'] = genres[:-2]
        content["release_date"] = content["release_date"][:10]

        content["company"] = literal_eval(api_games_companies(request, g['pk']).content.decode("utf-8"))[0]
        content["people"] = literal_eval(api_games_people(request, g['pk']).content.decode("utf-8"))
        
        valid_result['name'] = content['name']

        for s in query_string_list:
            if s.lower() in content['name'].lower():
                valid_result['total'] += 1

            for person in content['people']:
                if s.lower() in person['fields']['name'].lower():
                    valid_result['total'] += 1
            
            if s.lower() in content['system'].lower():
                valid_result['total'] += 1

            if s.lower() in content['gamefaq'].lower():
                valid_result['total'] += 1

            if s.lower() in content['synopsis'].lower():
                valid_result['total'] += 1

            if s.lower() in content['genre'].lower():
                valid_result['total'] += 1

            if s.lower() in content['company']['fields']['name'].lower():
                valid_result['total'] += 1

        if valid_result['total'] > 0:
            games_list.append(valid_result)        

    for c in companies:
        valid_result = {}
        valid_result['id'] = c['pk']
        valid_result['total'] = 0
        valid_result['url'] = base_url + "companies/" + str(valid_result['id']) + "/"

        company = api_companies_id(request,c['pk'])
        company_content = json.loads(company.content.decode("utf-8"))
        content = company_content[0]["fields"]
        content["founded"] = content["founded"][:10]
        
        content["people"] = literal_eval(api_companies_people(request, c['pk']).content.decode("utf-8"))
        content["games"] = literal_eval(api_companies_games(request, c['pk']).content.decode("utf-8"))

        for s in query_string_list:
            if s.lower() in content['name'].lower():
                valid_result['total'] += 1

            for person in content['people']:
                if s.lower() in person['fields']['name']:
                    valid_result['total'] += 1

            for game in content['games']:
                if s.lower() in game['fields']['name']:
                    valid_result['total'] += 1

            if s.lower() in content['description']:
                valid_result['total'] += 1

            if s.lower() in content['location'].lower():
                valid_result['total'] += 1

        if valid_result['total'] > 0:
            companies_list.append(valid_result)


    for p in people:
        valid_result = {}
        valid_result['id'] = p['pk']
        valid_result['total'] = 0
        valid_result['url'] = base_url + "people/" + str(valid_result['id']) + "/"

        person = api_people_id(request,valid_result['id'])
        person_content = json.loads(person.content.decode("utf-8"))
        content = person_content[0]["fields"]
        content['twitter'] = person_content[0]["fields"]["twitter"]
        content["DOB"] = content["DOB"][:10]
        
        content["companies"] = literal_eval(api_people_companies(request, valid_result['id']).content.decode("utf-8"))
        content["games"] = literal_eval(api_people_games(request, valid_result['id']).content.decode("utf-8"))

        for s in query_string_list:
            if s.lower() in content['name'].lower():
                valid_result['total'] += 1

            if s.lower() in content['residence'].lower():
                valid_result['total'] += 1

            for company in content['companies']:
                if s.lower() in company['fields']['name'].lower():
                    valid_result['total'] += 1

            for game in content['games']:
                if s.lower() in game['fields']['name']:
                    valid_result['total'] += 1

            if s.lower() in content['description']:
                valid_result['total'] += 1

        if valid_result['total'] > 0:
            people_list.append(valid_result)


    result_list = games_list + companies_list + people_list
    result_list = sorted(result_list, key = lambda x: x['total'], reverse = True)
    return result_list
