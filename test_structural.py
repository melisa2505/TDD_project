from example import app
import pytest
import random

@pytest.fixture 
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_can_call_existing_endpoints_of_the_appi(client):
    response = client.get('/get_coordinates/lima,peru')
    response = response.get_json()

    assert response['success'] == True

def test_cannot_call_non_existing_endpoints_of_the_app(client):
    response = client.get('/get_information/lima,peru')
    status_code = response.status_code
    assert status_code == 404    

def test_endpoint_returns_something(client):
    response = client.get('/get_coordinates/lima,peru')
    response = response.get_json()

    assert response['success'] == True
    assert 'coordinates' in response
    assert 'latitude' in response['coordinates']
    assert 'longitude' in response['coordinates']

    response2 = client.get('/get_coordinates/cusco')
    response2 = response2.get_json()

    assert response2['success'] == True
    assert 'coordinates' in response2
    assert 'latitude' in response2['coordinates']
    assert 'longitude' in response2['coordinates']

    body = {
        "coordinates1": response['coordinates'],
        "coordinates2": response2['coordinates']
    }

    response = client.post('/get_distance', json = body)
    response = response.get_json()

    assert response['success'] == True
    assert 'distance' in response


def test_the_result_is_correct_for_simple_cases(client):
    response = client.get('/get_coordinates/lima,peru')
    response = response.get_json()

    assert response['success'] == True
    assert response['coordinates']['latitude'] == -12.0621065
    assert response['coordinates']['longitude'] == -77.0365256

    response2 = client.get('/get_coordinates/cusco')
    response2 = response2.get_json()

    assert response2['success'] == True
    assert response2['coordinates']['latitude'] == -13.5170887
    assert response2['coordinates']['longitude'] == -71.9785356

    body = {
        "coordinates1": response['coordinates'],
        "coordinates2": response2['coordinates']
    }

    response = client.post('/get_distance', json = body)
    response = response.get_json()

    assert response['success'] == True
    DObtenido = response['distance'] 
    DEsperado = 570.1554498306485
    assert abs(DObtenido - DEsperado) < 2


city_list = ['lima,peru', 'cusco', 'santiago,chile', 'buenos aires,argentina', 'quito,ecuador', 'la paz,bolivia', 'asuncion,paraguay', 'montevideo,uruguay', 'caracas,venezuela', 'bogota,colombia']


#testeando la función get_coordinates
@pytest.mark.parametrize("city_name", city_list)
def test_the_result_is_correct_for_all_input_get_coordinates(client, city_name):
    response = client.get(f'/get_coordinates/{city_name}')
    response = response.get_json()

    assert response['success'] == True
    assert 'coordinates' in response
    assert 'latitude' in response['coordinates']
    assert 'longitude' in response['coordinates']

body_list = []
for i in range(100):
    coord1 = {'latitude': random.uniform(-90, 90), 'longitude': random.uniform(-180, 180)}
    coord2 = {'latitude': random.uniform(-90, 90), 'longitude': random.uniform(-180, 180)}
    body_list.append({'coordinates1': coord1, 'coordinates2': coord2})


#testeando la función get_distance
@pytest.mark.parametrize("body_item", body_list)
def test_the_result_is_correct_for_all_input_get_distance(client, body_item):
    response = client.post('/get_distance', json = body_item)
    response = response.get_json()

    assert response['success'] == True
    assert 'distance' in response
    assert response['distance'] >= 0
    assert response['distance'] <= 20037.49
