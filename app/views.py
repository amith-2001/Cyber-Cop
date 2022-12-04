from django.shortcuts import render

# Create your views here.
import re
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.conf import settings
import json
import main
from django.shortcuts import render
import requests

# @api_view(["POST"])
# def function1(filepath):
#     c = json.loads(filepath.body)
#     d = main.analyse(c)
#     return Response(c)

@api_view(["POST"])
def function1(filepath):
    # response = requests.GET.get('api/')
    # c = json.loads(response.body)
    # c = request.GET.get('title')
    # print(c)
    a = json.loads(filepath.body)
    d = main.analyse(a)
    return Response(d)

