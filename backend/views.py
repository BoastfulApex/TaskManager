from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader


def index(request):
    context = {
    }

    html_template = loader.get_template('backend/index.html')
    return HttpResponse(html_template.render(context, request))