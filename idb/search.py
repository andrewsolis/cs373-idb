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
   
    result_list = []

    base_url = 'http://retro-video-games-373.herokuapp.com/'

    games_list = json.loads(api_games(request).content.decode("utf-8"))
    companies_list = json.loads(api_companies(request).content.decode("utf-8"))
    people_list = json.loads(api_people(request).content.decode("utf-8"))

    for game in games_list:
    	result_list.append(game['pk'])
    
    for company in companies_list:
    	result_list.append(company['pk'])
    
    for person in people_list:
    	result_list.append(person['pk'])
    
    return result_list