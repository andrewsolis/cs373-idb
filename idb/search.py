from django.shortcuts import *
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse
import re # regular expressions
from bs4 import BeautifulSoup
import urllib.request
from idb.api.views import *
import json

from django.db.models import Q # query objects

def search_crawl(request, query_string):
    games_list = []
    companies_list = []
    people_list = []

    query_string_list = query_string.split(" ")
    result_list = []

    base_url = 'http://retro-video-games-373.herokuapp.com/'

    games = json.loads(api_games(request).content.decode("utf-8"))
    companies = json.loads(api_companies(request).content.decode("utf-8"))
    people = json.loads(api_people(request).content.decode("utf-8"))

    
    for game in games:
        g = {}
        g['name'] = game['fields']['name']
        g['pk'] = game['pk']
        g['url'] = base_url + "games/" + str(g['pk']) + "/"
        g['total'] = 0
        u = urllib.request.urlopen(g['url'])
        soup = BeautifulSoup(u.read())
        for s in query_string_list:
            gfound = soup.findAll(text = re.compile(s, re.IGNORECASE))
            g[s] = len(gfound)
            if(g[s] > 0): 
                g['total'] = g['total'] + 1
        if(g['total'] > 0):
            games_list.append(g)        

    for company in companies:
        c = {}
        c['name'] = company['fields']['name']
        c['pk'] = company['pk']
        c['url'] = base_url + "companies/" + str(c['pk']) + "/"
        c['total'] = 0
        u = urllib.request.urlopen(c['url'])
        soup = BeautifulSoup(u.read())
        for s in query_string_list:
            cfound = soup.findAll(text = re.compile(s, re.IGNORECASE))
            c[s] = len(cfound)
            if(c[s] > 0): 
                c['total'] = c['total'] + 1
        if(c['total'] > 0):
            companies_list.append(c)

    for person in people:
        p = {}
        p['name'] = person['fields']['name']
        p['pk'] = person['pk']
        p['url'] = base_url + "people/" + str(p['pk']) + "/"
        p['total'] = 0
        u = urllib.request.urlopen(p['url'])
        soup = BeautifulSoup(u.read())
        for s in query_string_list:
            pfound = soup.findAll(text = re.compile(s, re.IGNORECASE))
            p[s] = len(pfound)
            if(p[s] > 0): 
                p['total'] = p['total'] + 1
        if(p['total'] > 0):
            people_list.append(p)

    result_list = games_list + companies_list + people_list
    result_list = sorted(result_list, key = lambda x: x['total'], reverse = True)
    return result_list
