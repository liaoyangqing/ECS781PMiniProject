# ECS781PMiniProject (get today's weather of the city )
mini project of cloud computing
MetaWeather is an automated weather data aggregator that takes the weather predictions from various forecasters and calculates the most likely outcome.(https://www.metaweather.com)

# set up

CREATE KEYSPACE cityweather WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE cityweather (city text PRIMARY KEY,date text, weather text);

# REST api requests
