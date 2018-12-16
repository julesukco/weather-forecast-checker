
#// PROGRAM 1  - Collect and store weather data 

// read weather forecast data
// save one row per day of the forecast

// save data to file
currentDateTime, forecastDate, daysInFuture, highTemp, lowTemp, chanceOfRain, chanceOfSnow
201812151700,20181216,1,56.0,31.1,0.25,0
201812151700,20181217,2,52.0,28.4,0,0
201812151700,20181218,3,51.0,22.7,0,1.0

// save actual data to another file 
currentDateTime, actualHighTemp, actualLowTemp, didItRain, didItSnow
201812151700,20181216,1,55.2,30.5,1,0


#// PROGRAM 2 - Process data into format ready to process

// read forcast data
// lookup actual data
currentDateTime, forecastDate, daysInFuture, actualHighTemp, actualLowTemp, actualRain, actualSnow, forecastHighTemp, forecastLowTemp, forecastChanceOfRain, forecastChanceOfSnow
201812151700,20181216,1,55.2,30.5,1,0,56.0,31.1,0.25,0


#// PROGRAM 3 - Compare weather data

// read each line
// temp: calculate difference between forecast high and actual low. 56.0 - 55.2 = 0.8. => Avg differences over time 
// rain: group into 10% buckets, e.g. 0-9, 10-19, 20-29, etc. and record number of times forecast in that range and times it actually rained

