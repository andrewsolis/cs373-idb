from django.core import serializers
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
from json import dumps

from idb.videogames.models import *

def games(request):
	games_list = []
	if(request.method == 'GET'):
		games_list = serializers.serialize("json",Game.objects.order_by('-id').all())
	elif(request.method == 'POST'):
		pass

	return HttpResponse(games_list, content_type="application/json")
#	return HttpResponse(str(x), content_type="plain/text")

