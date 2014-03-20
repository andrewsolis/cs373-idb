from django.shortcuts import *
from django.template import RequestContext

def home(request):
	return render_to_response('home.html', {}, RequestContext(request))

# Create your views here.
def nintendo(request):
	return render_to_response('nintendo.html', {}, RequestContext(request))

def metroid(request):
	return render_to_response('metroid.html', {}, RequestContext(request))

def yoshio_sakamoto(request):
	return render_to_response('yoshio_sakamoto.html', {}, RequestContext(request))

def crash_bandicoot(request):
	return render_to_response('crash_bandicoot.html', {}, RequestContext(request))

def sonic(request):
	return render_to_response('sonic.html', {}, RequestContext(request))

