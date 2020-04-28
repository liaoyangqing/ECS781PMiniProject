from flask import Flask, render_template, request, jsonify
import json
from cassandra.cluster import Cluster
import requests
import requests_cache

cluster = Cluster(contact_points=['172.17.0.2'], port=9042)

session = cluster.connect()

requests_cache.install_cache('cityweather', backend='sqlite', expire_after=36000)

app = Flask(__name__)

url_woeid_template = "https://www.metaweather.com/api/location/search/?query={query}"
url_loc_template = "https://www.metaweather.com/api/location/{woeid}/"
#url_template_loc_day_tem = "https://www.metaweather.com/api/location/{woeid}/{date}/"

@app.route('/')
def home():
    return jsonify({'data': 'Welcome to the mini project, to see more information please visit https://github.com/liaoyangqing/ECS781PMiniProject'}), 200


#input a city and return weather and the date
@app.route('/api/get_weather_by_city', methods=['GET'])
def get_weather_by_city():
    # Get the json file that contain those information
    my_query = request.args.get('query')
    # if the returned none
    if (my_query is None):
        return jsonify({'Failure':'No input'}), 400  # if input failure, return 400
    # make the template suitable for this parameter
    id_url = url_woeid_template.format(query=my_query)
    # get the json file which contains id of city
    resp = requests.get(id_url)
    if resp.ok:
        locate = resp.json()
        # Get the first id as the input city to check weather
        woeid = locate[0]['woeid']
        # Use woeid to get the weather of city
        if woeid is None:
            return jsonify({'error': 'can not get id'}), 400
        location_url = url_loc_template.format(woeid=woeid)
        resp1 = requests.get(location_url)
        if resp1.ok:
            weather1 = resp1.json()
            # Date of next day
            date = weather1['consolidated_weather'][0]['created']
            # Weather of next day
            weather = weather1['consolidated_weather'][0]['weather_state_name']
            date_dict = {'date': date}
            weather_dict = {'weather': weather}
            # Create a new dictionary to save weather of nextday
            weaData = dict(date_dict, **weather_dict)
            #store data in the database
            date = str(date)
            weather = str(weather)
            session.execute("""INSERT INTO cityweather.globe("city", "date", "weather")VALUES('{}', '{}', '{}')""".format(my_query, date, weather))
            return jsonify({'city_weather': weaData}), 200  # if succeed, return 200
        else:
            return jsonify({'error': resp.reason}), 404  # if failure in requests, return 404
    else:
        return jsonify({'error': resp.reason}), 404  # if failure in requests, return 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
