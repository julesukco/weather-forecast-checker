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

diff_count = []
diff_count = [0,0,0,0,0,0,0,0,0,0,0,0]
diff_min_temps = []
diff_min_temps = [0,0,0,0,0,0,0,0,0,0,0,0]
diff_max_temps = []
diff_max_temps = [0,0,0,0,0,0,0,0,0,0,0,0]
diff_snow = []
diff_snow = [0,0,0,0,0,0,0,0,0,0,0,0]
diff_rain = []
diff_rain = [0,0,0,0,0,0,0,0,0,0,0,0]
diff_accumulation = []
diff_accumulation = [0,0,0,0,0,0,0,0,0,0,0,0]

client = MongoClient(cfg.dbhost)
db = client['weatherDB']

def analyzeData():

    coll = db.weather

    many_docs = coll.find({"actual":{"$exists": True}}) # empty query means "retrieve all"
    for doc in many_docs:
        #print(doc)
        #print("date: " + str(doc['date']))

        if 'forecasts' in doc and 'actual' in doc:
            #print("maxTemperature: " + str(doc['actual']['maxTemperature']))
            actualMaxTemperature = doc['actual']['maxTemperature']
            actualMinTemperature = doc['actual']['minTemperature']
            actualSnow = doc['actual']['chanceOfSnow']
            actualRain = doc['actual']['chanceOfRain']
            actualAccumulation = doc['actual']['accummulation']

            for forecast in doc['forecasts']:
                forecastMaxTemperature = forecast['maxTemperature']
                forecastMinTemperature = forecast['minTemperature']
                forecastSnow = forecast['chanceOfSnow']
                forecastRain = forecast['chanceOfRain']
                forecastAccumulation = forecast['accummulation']
                #print("days ahead: " + str(forecast['daysAhead']) + ' diff: ' + str(abs(actualMaxTemperature - forecastMaxTemperature)))

                diff_count[forecast['daysAhead']] = diff_count[forecast['daysAhead']] + 1
                diff_max_temps[forecast['daysAhead']] = diff_max_temps[forecast['daysAhead']] + abs(actualMaxTemperature - forecastMaxTemperature)
                diff_min_temps[forecast['daysAhead']] = diff_min_temps[forecast['daysAhead']] + abs(actualMinTemperature - forecastMinTemperature)
                diff_snow[forecast['daysAhead']] = diff_snow[forecast['daysAhead']] + abs(actualSnow - forecastSnow)
                diff_rain[forecast['daysAhead']] = diff_rain[forecast['daysAhead']] + abs(actualRain - forecastRain)
                diff_accumulation[forecast['daysAhead']] = diff_accumulation[forecast['daysAhead']] + abs(actualAccumulation - forecastAccumulation)
                #print("summary diff: " + doc['actual']['summary'] + " vs " + forecast['summary'])

    print('\nTemperature:')
    for i in range(0,10):
        print("Days out " + str(i) + " - avg max diff: " + str(diff_max_temps[i]/diff_count[i]) + " - avg min diff: " + str(diff_min_temps[i]/diff_count[i]))

    print('\nRain/Snow:')
    for i in range(0,10):
        print("Days out " + str(i) + " - avg snow diff: " + str(diff_snow[i]/diff_count[i]) + " - avg rain diff: " + str(diff_rain[i]/diff_count[i]) + " - avg accumulation diff: " + str(diff_accumulation[i]/diff_count[i]))

    return 

if __name__ == "__main__":
    analyzeData()
    print("Done")
