# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
import requests
import logging


# Create your views here.
def convert(request):
    print("got request")
    if request.method != "GET":
        return HttpResponseBadRequest(content="Invalid request type")
    try:
        dataFile = "currency.csv"
        respFile = requests.get("http://wwwnui.akamai.com/tm-interview/currency_exchange.csv")
        open(dataFile, "w").write(respFile.content)
    except:
        logging.error("Unable to open url to get the csv file")
        return HttpResponseServerError(content="Unable to fetch todays rates")

    currencyPair = request.GET['q']
    print("currency_pair: " + currencyPair)
    
    with open(dataFile, "r") as f:
        lines = f.readlines()
        header = lines[0]
        currencyPairs = header.split(",")
        if currencyPair not in currencyPairs:
            return HttpResponseBadRequest("Invalid currency pair requsted")
        idx = currencyPairs.index(currencyPair)
        data = lines[1].split(",")
        return HttpResponse("{'currencyValue' : " + str(data[idx]) + "}", content_type='application/json')
    
        
