# ECS781PMiniProject (get today's weather of the city )
This is the mini project of cloud computing.

This project used MetaWeather, which is an automated weather data aggregator that takes the weather predictions from various forecasters and calculates the most likely outcome.(see more at https://www.metaweather.com)

# 1.preparation
Pull the Cassandra Docker Image
```
sudo apt update

sudo apt install docker.io

sudo docker pull cassandra:latest
```
create a cassandra in a docker:
```
sudo docker run --name cassandra-project -p 9042:9042 -d cassandra:latest
sudo docker start cassandra-project
```
use CQL to start a database:
```
sudo docker exec -it cassandra-project cqlsh
```
create a keyspace for the data and the table we specified(don't forget ';')：
```
CREATE KEYSPACE cityweather WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE cityweather.globe(city varchar PRIMARY KEY,date varchar, weather varchar);
```
# 2.Serving the application
download the requirements.txt, myapp.py and Dockerfile, and then bulit image by:
```
sudo docker build . --tag = cityweather:v1
sudo docker run -p 8080:8080 cityweather:v1
```
# REST api requests
# request introduction, method = 'GET'
```
curl -i https://localhost:8000/
```
or use browser visit https://localhost:8000/

# request the weather by city
```
curl -i -H "Content-Type: application/json" -X GET -d '{"query":"city_name"}' http://localhost:8080/api/location/search/?query={query}
```
or visit http://localhost:8080/api/get_weather_by_city?query=cityname


# delete the data in the casssandra database by city
```
curl -i -H "Content-Type: application/json" -X DELETE -d '{"query":"shanghai"}' http://localhost:8080/delete_by_city
```


















