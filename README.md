# ECS781PMiniProject (get today's weather of the city )
mini project of cloud computing
MetaWeather is an automated weather data aggregator that takes the weather predictions from various forecasters and calculates the most likely outcome.(https://www.metaweather.com)

# set up

CREATE KEYSPACE cityweather WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE cityweather.globe (city text PRIMARY KEY,date text, weather text);

# Kubernetes based load balancing
Install Kubernetes

sudo snap install microk8s --classic
Develop an nginx application,listening on port 80, and names the deployment "covid19-web"

sudo microk8s.kubectl run cityweather-web --image==cityweather:v4 --port=8080
See the pods created:

sudo microk8s.kubectl get pods
Expose cluster to the external world

sudo microk8s.kubectl expose deployment cityweather-web --type=LoadBalancer
Scaling up application

sudo microk8s.kubectl scale deployment cityweather-web --replicas=5
Check the replias

sudo microk8s.kubectl get pods
cleaning up
Delete the load-balancing service:

sudo microk8s.kubectl delete service cityweather-web
# REST api requests
