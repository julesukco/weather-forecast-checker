
#// PROGRAM 1  - Collect and store weather data 

// read weather forecast data
// save one row per day of the forecast

Uses mongoDB to store data

Shell command:
mongodb://julesuk1:KXzrs6mpjj23HcRT3wtSZMqExbVOEgIFZRx0fZq6Pl2GFyhtJqAQjA7rksXihKrPHRh3gplRMvFPLerEj8rL7g==@julesuk1.documents.azure.com:10255/?ssl=true&replicaSet=globaldb
weather
forEcast1
collection name: weather


#// PROGRAM 2 - Compare weather data

// read each document
// temp: calculate difference between forecast high and actual low. 56.0 - 55.2 = 0.8. => Avg differences over time 
// rain: group into 10% buckets, e.g. 0-9, 10-19, 20-29, etc. and record number of times forecast in that range and times it actually rained

