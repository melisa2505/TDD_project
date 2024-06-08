# Diseño del Sistema de Servicio de Coordenadas y Distancias

## Descripción General

Este documento describe el diseño de un sistema de servicio web desarrollado en Flask que permite a los usuarios obtener coordenadas geográficas de ciudades y calcular la distancia entre dos puntos dados en base a sus coordenadas. El sistema se compone de dos endpoints principales: uno para obtener las coordenadas de una ciudad y otro para calcular la distancia entre dos conjuntos de coordenadas.

## Arquitectura

### Componentes Principales

1. **Servidor Flask**: Proporciona la API para interactuar con los servicios de obtención de coordenadas y cálculo de distancias.
2. **Módulo de Cálculo de Distancias**: Utiliza la fórmula de Haversine para calcular la distancia entre dos puntos geográficos.
3. **Integración con OpenStreetMap**: Realiza solicitudes a la API de OpenStreetMap para obtener las coordenadas de una ciudad.

### Diagrama de Componentes

+-----------------------+
| Flask Web Server |
| |
| +-----------------+ |
| | API Endpoints | |
| | | |
| | - /get_coordinates/
|
| | - /get_distance |
| +-----------------+ |
| |
| +-----------------+ |
| | Distance Module | |
| | | |
| | - calculate_distance() |
| +-----------------+ |
+-----------------------+

+-----------------------+
| OpenStreetMap API |
| |
| +-----------------+ |
| | Coordinates Data| |
| +-----------------+ |
+-----------------------+


## Detalles de Implementación

### Endpoints

#### `GET /get_coordinates/:city_name`

- **Descripción**: Obtiene las coordenadas (latitud y longitud) de la ciudad especificada.
- **Parámetros de Entrada**:
  - `city_name` (str): Nombre de la ciudad.
- **Respuesta**:
  - `200 OK` con JSON:
    ```json
    {
      "success": true,
      "coordinates": {
        "latitude": float,
        "longitude": float
      }
    }
    ```
  - `404 Not Found` con JSON en caso de error:
    ```json
    {
      "success": false,
      "message": "An error occurred: <error_message>"
    }
    ```

#### `POST /get_distance`

- **Descripción**: Calcula la distancia entre dos conjuntos de coordenadas.
- **Parámetros de Entrada** (en el cuerpo de la solicitud):
  - `coordinates1` (dict): Coordenadas del primer punto con `latitude` y `longitude`.
  - `coordinates2` (dict): Coordenadas del segundo punto con `latitude` y `longitude`.
- **Respuesta**:
  - `200 OK` con JSON:
    ```json
    {
      "success": true,
      "distance": float
    }
    ```
  - `400 Bad Request` con JSON en caso de error:
    ```json
    {
      "success": false,
      "message": "Missing coordinates1 or coordinates2 in the request body"
    }
    ```
    O en caso de otro error:
    ```json
    {
      "success": false,
      "message": "An error occurred: <error_message>"
    }
    ```

### Funciones

#### `calculate_distance(coord1, coord2)`

- **Descripción**: Calcula la distancia entre dos puntos geográficos utilizando la fórmula de Haversine.
- **Parámetros**:
  - `coord1` (dict): Coordenadas del primer punto con `latitude` y `longitude`.
  - `coord2` (dict): Coordenadas del segundo punto con `latitude` y `longitude`.
- **Retorno**:
  - `float`: Distancia entre los dos puntos en kilómetros.

#### `get_coordinates(city_name)`

- **Descripción**: Obtiene las coordenadas de una ciudad usando la API de OpenStreetMap.
- **Parámetros**:
  - `city_name` (str): Nombre de la ciudad.
- **Retorno**:
  - `Response`: Respuesta JSON con el estado de éxito y las coordenadas o un mensaje de error.

#### `get_distance()`

- **Descripción**: Calcula la distancia entre dos conjuntos de coordenadas proporcionados en el cuerpo de la solicitud.
- **Parámetros**:
  - `request` (Request): Objeto de solicitud que contiene las coordenadas en formato JSON.
- **Retorno**:
  - `Response`: Respuesta JSON con el estado de éxito y la distancia calculada o un mensaje de error.

## Pruebas

### Pruebas Unitarias

Se deben implementar pruebas unitarias para validar el funcionamiento correcto de cada endpoint y la función de cálculo de distancias. Las pruebas deben cubrir casos como:

- Obtener coordenadas de una ciudad válida.
- Manejar errores al obtener coordenadas de una ciudad inválida.
- Calcular correctamente la distancia entre dos puntos.
- Manejar errores en el cálculo de distancias debido a entradas faltantes o incorrectas.

### Ejemplo de Prueba

```python
def test_get_coordinates(client):
    response = client.get('/get_coordinates/lima,peru')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'coordinates' in data
    assert 'latitude' in data['coordinates']
    assert 'longitude' in data['coordinates']
```

## Conclusion
Este diseño proporciona una solución robusta y escalable para obtener coordenadas geográficas y calcular distancias entre puntos. La utilización de Flask para el servidor web, junto con la API de OpenStreetMap para obtener datos de coordenadas, asegura que el sistema sea eficiente y fácil de mantener.

