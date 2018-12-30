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

now = datetime.now()
start = now + timedelta(days=-1)
later = now + timedelta(days=10)
d_from_date = datetime.strptime(start.strftime('%Y-%m-%d') , '%Y-%m-%d')
d_to_date = datetime.strptime(later.strftime('%Y-%m-%d') , '%Y-%m-%d')
delta = d_to_date - d_from_date
latitude = str(location.latitude)
longitude = str(location.longitude)

client = MongoClient('mongodb://julesuk1:KXzrs6mpjj23HcRT3wtSZMqExbVOEgIFZRx0fZq6Pl2GFyhtJqAQjA7rksXihKrPHRh3gplRMvFPLerEj8rL7g==@julesuk1.documents.azure.com:10255/?ssl=true&replicaSet=globaldb')
db = client['weatherDB']

def getWeatherData():
    print("\nLocation: "+ location.address)

    posts = db.weather
#    posts = db.weatherTest

    for i in range(delta.days):
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

        windGust = 0
        if 'windGust' in json_res['daily']['data'][0]:
            windGust = json_res['daily']['data'][0]['windGust']

        print("Min temperature: "+str(json_res['daily']['data'][0]['temperatureMin']))
        print("Max temperature: "+str(json_res['daily']['data'][0]['temperatureMax']))
        print("Realfeel Min temperature: "+str(json_res['daily']['data'][0]['apparentTemperatureMin']))
        print("Realfeel Max temperature: "+str(json_res['daily']['data'][0]['apparentTemperatureMax']))
        print("Wind Speed: "+str(json_res['daily']['data'][0]['windSpeed']))
        print("Wind Gust: "+str(windGust))
        print("Icon: "+str(json_res['daily']['data'][0]['icon']))
        print("Summary: " + unicode(json_res['daily']['data'][0]['summary']).encode('utf8'))
        print("Chance of rain: " + str(chance_rain))
        print("Chance of snow: " + str(chance_snow))
        print("Accummulation: "+str(precip_accumulation))

        existing_dict = posts.find_one({'date': str(new_date)})
        if (existing_dict != None):
#            print(existing_dict)
            if str(new_date) == str(d_from_date)[:10]:
                existing_dict.update(
                    {
                        "actual": {
                            "minTemperature": json_res['daily']['data'][0]['temperatureMin'],
                            "maxTemperature": json_res['daily']['data'][0]['temperatureMax'],
                            "realfeelMinTemperature": json_res['daily']['data'][0]['apparentTemperatureMin'],
                            "RealfeelMaxTemperature": json_res['daily']['data'][0]['apparentTemperatureMax'],
                            "windSpeed": json_res['daily']['data'][0]['windSpeed'],
                            "windGust": windGust,
                            "icon": "" + str(json_res['daily']['data'][0]['icon']) + "",
                            "summary": json_res['daily']['data'][0]['summary'],
                            "chanceOfRain": chance_rain,
                            "chanceOfSnow": chance_snow,
                            "accummulation": precip_accumulation
                        }
                    }
                )
            else:
                existing_dict['forecasts'].append(
                    {
                        "daysAhead": i-1,
                        "minTemperature": json_res['daily']['data'][0]['temperatureMin'],
                        "maxTemperature": json_res['daily']['data'][0]['temperatureMax'],
                        "realfeelMinTemperature": json_res['daily']['data'][0]['apparentTemperatureMin'],
                        "RealfeelMaxTemperature": json_res['daily']['data'][0]['apparentTemperatureMax'],
                        "windSpeed": json_res['daily']['data'][0]['windSpeed'],
                        "windGust": windGust,
                        "icon": "" + str(json_res['daily']['data'][0]['icon']) + "",
                        "summary": json_res['daily']['data'][0]['summary'],
                        "chanceOfRain": chance_rain,
                        "chanceOfSnow": chance_snow,
                        "accummulation": precip_accumulation
                    }
                )
#            print(existing_dict)
            posts.update_one(
                {"date": str(new_date)},
                {"$set": existing_dict},
                upsert = True
                )
        else:
            post_data = {
                "date": str(new_date),
                "forecasts": [
                    {
                    "daysAhead": i-1,
                    "minTemperature": json_res['daily']['data'][0]['temperatureMin'],
                    "maxTemperature": json_res['daily']['data'][0]['temperatureMax'],
                    "realfeelMinTemperature": json_res['daily']['data'][0]['apparentTemperatureMin'],
                    "RealfeelMaxTemperature": json_res['daily']['data'][0]['apparentTemperatureMax'],
                    "windSpeed": json_res['daily']['data'][0]['windSpeed'],
                    "windGust": windGust,
                    "icon": "" + str(json_res['daily']['data'][0]['icon']) + "",
                    "summary": json_res['daily']['data'][0]['summary'],
                    "chanceOfRain": chance_rain,
                    "chanceOfSnow": chance_snow,
                    "accummulation": precip_accumulation
                    }
                ]
            }
            posts.update_one(
                {"date": str(new_date)},
                {"$set": post_data},
                upsert = True
                )
    return 

if __name__ == "__main__":
    getWeatherData()
    print("Done")
