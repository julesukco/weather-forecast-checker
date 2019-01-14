#!/usr/local/bin/python
# coding: latin-1
import os, sys
from datetime import datetime,timedelta
import sys
from pymongo import MongoClient
import databaseconfig as cfg

now = datetime.now()
start = now + timedelta(days=-1)
later = now + timedelta(days=10)
d_from_date = datetime.strptime(start.strftime('%Y-%m-%d') , '%Y-%m-%d')
d_to_date = datetime.strptime(later.strftime('%Y-%m-%d') , '%Y-%m-%d')
delta = d_to_date - d_from_date

client = MongoClient(cfg.dbhost)
db = client['weatherDB']

def analyzeData():

    coll = db.weather

    many_docs = coll.find({"actual":{"$exists": True}}) # empty query means "retrieve all"
    for doc in many_docs:
#        print(doc)
        print("date: " + str(doc['date']))

        if 'forecasts' in doc and 'actual' in doc:
            print("maxTemperature: " + str(doc['actual']['maxTemperature']))
            actualMaxTemperature = doc['actual']['maxTemperature']

            for forecast in doc['forecasts']:
                forecastMaxTemperature = forecast['maxTemperature']
                print("days ahead: " + str(forecast['daysAhead']) + " days ahead: " + str(forecast['maxTemperature']) + ' diff: ' + str(actualMaxTemperature - forecastMaxTemperature))
                print("summary diff: " + doc['actual']['summary'] + " vs " + forecast['summary'])

    return 

if __name__ == "__main__":
    analyzeData()
    print("Done")
