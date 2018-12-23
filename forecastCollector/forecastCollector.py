#!/usr/local/bin/python
# coding: latin-1
import os, sys
from geopy.geocoders import Nominatim
from datetime import datetime,timedelta
import sys, requests
from pymongo import MongoClient

DARK_SKY_API_KEY = "6e8fd42d2b312d4cc94121ef2de8c2bd"
option_list = "exclude=currently,minutely,hourly,alerts&amp;units=si"

location = Nominatim().geocode('Elizabeth, CO', language='en_US')
d_from_date = datetime.strptime('2018-12-24' , '%Y-%m-%d')
d_to_date = datetime.strptime('2018-12-31' , '%Y-%m-%d')
delta = d_to_date - d_from_date
latitude = str(location.latitude)
longitude = str(location.longitude)

client = MongoClient('mongodb://julesuk1:KXzrs6mpjj23HcRT3wtSZMqExbVOEgIFZRx0fZq6Pl2GFyhtJqAQjA7rksXihKrPHRh3gplRMvFPLerEj8rL7g==@julesuk1.documents.azure.com:10255/?ssl=true&replicaSet=globaldb')
db = client['weatherDB']

def getWeatherData():
    print("\nLocation: "+ location.address)

    posts = db.weather

    for i in range(delta.days+1):
        new_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d')
        search_date = new_date+"T00:00:00"
        response = requests.get("https://api.darksky.net/forecast/"+DARK_SKY_API_KEY+"/"+latitude+","+longitude+","+search_date+"?"+option_list)
        json_res = response.json()
#        print (json_res)

        print("\n Create/Update document for: "+(d_from_date + timedelta(days=i)).strftime('%Y-%m-%d %A'))

        precip_type = None
        precip_prob = None
        precip_accumulation = 0
        chance_snow = 0
        chance_rain = 0
        if 'precipProbability' in json_res['daily']['data'][0] and 'precipType' in json_res['daily']['data'][0]:
            precip_type = json_res['daily']['data'][0]['precipType']
            precip_prob = json_res['daily']['data'][0]['precipProbability']
            precip_accumulation = json_res['daily']['data'][0]['precipAccumulation']
        if (precip_type == 'rain' and precip_prob != None):
            chance_rain = precip_prob * 100
        if (precip_type == 'snow' and precip_prob != None):
            chance_snow = precip_prob * 100
            precip_prob *= 100

        print("Min temperature: "+str(json_res['daily']['data'][0]['temperatureMin']))
        print("Max temperature: "+str(json_res['daily']['data'][0]['temperatureMax']))
        print("Realfeel Min temperature: "+str(json_res['daily']['data'][0]['apparentTemperatureMin']))
        print("Realfeel Max temperature: "+str(json_res['daily']['data'][0]['apparentTemperatureMax']))
        print("Wind Speed: "+str(json_res['daily']['data'][0]['windSpeed']))
        print("Wind Gust: "+str(json_res['daily']['data'][0]['windGust']))
        print("Icon: "+str(json_res['daily']['data'][0]['icon']))
        print("Summary: " + json_res['daily']['data'][0]['summary'])
        print("Chance of rain: " + str(chance_rain))
        print("Chance of snow: " + str(chance_snow))
        print("Accummulation: "+str(precip_accumulation))

        post_data = {
            "date": "" +str(new_date) + "",
            "forecasts": [
                {
                "daysAhead": i + 1,
                "minTemperature": json_res['daily']['data'][0]['temperatureMin'],
                "maxTemperature": json_res['daily']['data'][0]['temperatureMax'],
                "realfeelMinTemperature": json_res['daily']['data'][0]['apparentTemperatureMin'],
                "RealfeelMaxTemperature": json_res['daily']['data'][0]['apparentTemperatureMax'],
                "windSpeed": json_res['daily']['data'][0]['windSpeed'],
                "windGust": json_res['daily']['data'][0]['windGust'],
                "icon": "" + str(json_res['daily']['data'][0]['icon']) + "",
                "summary": json_res['daily']['data'][0]['summary'],
                "chanceOfRain": chance_rain,
                "chanceOfSnow": chance_snow,
                "accummulation": precip_accumulation
                }
            ]
        }
        result = posts.insert_one(post_data)
        print('One post: {0}'.format(result.inserted_id))

    return 

def rowOfData():
    return("201812151700,20181216,1,56.0,31.1,0.25,0")

if __name__ == "__main__":
    getWeatherData()
    print("Done")
