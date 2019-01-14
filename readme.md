
#// PROGRAM 1  - Collect and store weather data 

// read weather forecast data
// create/update one document per date, contains forecasts and actual

Uses mongoDB to store data

connection info stored in cfg file - see Google drive, Projects/weather folder for real file
Shell command:
example connection string:
mongodb://julesuk1:KXzrs6mpjj23HcRT3wtSZMqExbVOEgIFZRx0fZq6Pl2GFyhtJqAQjA7rksXihKrPHRh3gplRMvFPLerEj8rL7g==@julesuk1.documents.azure.com:10255/?ssl=true&replicaSet=globaldb
weather
forEcast1
collection name: weather



#// PROGRAM 2 - Compare weather data

// read each document
// temp: calculate difference between forecast high and actual low. 56.0 - 55.2 = 0.8. => Avg differences over time 
// rain: group into 10% buckets, e.g. 0-9, 10-19, 20-29, etc. and record number of times forecast in that range and times it actually rained

