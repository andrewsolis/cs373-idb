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

    result_list = []

    base_url = 'http://retro-video-games-373.herokuapp.com/'

    games = json.loads(api_games(request).content.decode("utf-8"))
    companies = json.loads(api_companies(request).content.decode("utf-8"))
    people = json.loads(api_people(request).content.decode("utf-8"))

    
    for game in games:
        g = {}
        g['pk'] = game['pk']
        u = urllib.request.urlopen(base_url + "games/" + str(g['pk']) + "/")
        soup = BeautifulSoup(u.read())
        gfound = soup.findAll(text = re.compile(query_string, re.IGNORECASE))
        games_list.append(gfound)

    for company in companies:
        c = {}
        c['pk'] = company['pk']
        u = urllib.request.urlopen(base_url + "companies/" + str(c['pk']) + "/")
        companies_list.append(c)

    for person in people:
        p = {}
        p['pk'] = person['pk']
        u = urllib.request.urlopen(base_url + "people/" + str(p['pk']) + "/")
        people_list.append(p)

    return games_list
