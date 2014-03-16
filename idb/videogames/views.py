from django.shortcuts import *
from django.template import RequestContext

def home(request):
	return render_to_response('home.html', {}, RequestContext(request))

# Create your views here.
