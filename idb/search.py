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
    query_string = query_string.split(" ")
    games_list = []
    companies_list = []
    people_list = []
    
    result_list = []

    base_url = 'http://retro-video-games-373.herokuapp.com/'

    games = json.loads(api_games(request).content.decode("utf-8"))
    companies = json.loads(api_companies(request).content.decode("utf-8"))
    people = json.loads(api_people(request).content.decode("utf-8"))

    for game in games:
    	games_list.append(game['pk'])
    
    for company in companies:
    	companies_list.append(company['pk'])
    
    for person in people:
    	people_list.append(person['pk'])
    
    return result_list