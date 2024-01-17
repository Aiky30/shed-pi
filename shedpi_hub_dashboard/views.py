from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    response = TemplateResponse(request, "shedpi_hub_dashboard/index.html", {})
    return response
