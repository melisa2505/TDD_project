from flask import Flask, request, jsonify
import requests
import math

app = Flask(__name__)

def calculate_distance(coord1, coord2):
    # Haversine formula to calculate distance between two lat/long points
    R = 6371  # Radius of the Earth in km
    lat1, lon1 = coord1['latitude'], coord1['longitude']
    lat2, lon2 = coord2['latitude'], coord2['longitude']

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance 

@app.route('/get_coordinates/<city_name>', methods=['GET'])
def get_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    headers = {'User-Agent': 'testing'}
    response = requests.get(url, headers=headers)

    try:
        response.raise_for_status()
        data = response.json()
        lat = data[0]['lat']
        lon = data[0]['lon']
        return jsonify({
            "success": True,
            "coordinates": {'latitude': float(lat), 'longitude': float(lon)}
        }), 200
    except requests.exceptions.HTTPError as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }), 404
    
    
@app.route('/get_distance', methods=['POST'])
def get_distance():
    try:
        coord1 = request.json['coordinates1'] 
        coord2 = request.json['coordinates2']
    except KeyError:
        return jsonify({
            "success": False,
            "message": "Missing coordinates1 or coordinates2 in the request body"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }), 400

    distance = calculate_distance(coord1, coord2)
    return jsonify({
        "success": True,
        "distance": distance
    }), 200

if __name__ == '__main__':
    app.run(debug=True)


