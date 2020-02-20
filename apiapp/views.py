from django.shortcuts import render
from django.http import HttpResponse
import datetime

def index(request):
    now = datetime.datetime.now()
    html = "<html><body>The time is now %s." % now
    html += "<br>"
    html += "</body></html>"
    return HttpResponse(html)
