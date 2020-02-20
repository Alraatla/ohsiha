from django.shortcuts import render
from django.http import HttpResponse
import datetime
from apiapp.models import Choice, Question

def index(request):
    questions = Question.objects.all()
    now = datetime.datetime.now()
    html = "<html><body>The time is now %s." % now
    html += "<br>"
    for question in questions:
        html += (question.question_text) + "<br>"

    html += "</body></html>"
    return HttpResponse(html)
