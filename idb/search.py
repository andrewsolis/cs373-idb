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
        valid_result['url'] = base_url + "games/" + str(valid_result['id'])

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

    # for company in companies:
    #     c = {}
    #     c['name'] = company['fields']['name']
    #     c['pk'] = company['pk']
    #     c['url'] = base_url + "companies/" + str(c['pk']) + "/"
    #     c['total'] = 0
    #     u = urllib.request.urlopen(c['url'])
    #     soup = BeautifulSoup(u.read())
    #     for s in query_string_list:
    #         cfound = soup.findAll(text = re.compile(s, re.IGNORECASE))
    #         c[s] = len(cfound)
    #         if(c[s] > 0): 
    #             c['total'] = c['total'] + 1
    #     if(c['total'] > 0):
    #         companies_list.append(c)

    # for person in people:
    #     p = {}
    #     p['name'] = person['fields']['name']
    #     p['pk'] = person['pk']
    #     p['url'] = base_url + "people/" + str(p['pk']) + "/"
    #     p['total'] = 0
    #     u = urllib.request.urlopen(p['url'])
    #     soup = BeautifulSoup(u.read())
    #     for s in query_string_list:
    #         pfound = soup.findAll(text = re.compile(s, re.IGNORECASE))
    #         p[s] = len(pfound)
    #         if(p[s] > 0): 
    #             p['total'] = p['total'] + 1
    #     if(p['total'] > 0):
    #         people_list.append(p)

    # result_list = games_list + companies_list + people_list
    # result_list = sorted(result_list, key = lambda x: x['total'], reverse = True)
    return games_list
