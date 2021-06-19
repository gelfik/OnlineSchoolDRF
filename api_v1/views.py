import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from rest_framework import status
from rest_framework.exceptions import APIException

# Create your views here.

def error404(request, exception):
    response_data = {}
    response_data['detail'] = 'Not found.'
    return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")