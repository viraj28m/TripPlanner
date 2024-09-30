import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def get_dist_and_time(locations):
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(os.path.join(BASE_DIR.parent.absolute(), '.env'))

    # set up origin point
    origin = locations[0]
    origin_dict =  {
                    'location': {
                        'latLng': {
                            'latitude': origin[0],
                            'longitude': origin[1],
                            },
                        },
                    }
    
    destination = locations[-1]
    destination_dict =  {
                        'location': {
                            'latLng': {
                                'latitude': destination[0],
                                'longitude': destination[1],
                                },
                            },
                        }

    intermediates = []
    for i in range(1,len(locations)-1):
        location = locations[i]
        intermediates_dict = {
                            'location': {
                                'latLng': {
                                    'latitude': location[0],
                                    'longitude': location[1],
                                    },
                                },
                            }
        intermediates.append(intermediates_dict)

    api_key = os.environ.get('GOOGLE_CLOUD_INTERNAL_KEY')

    # parameters for call
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.legs',
    }

    json_data = {
        'origin': origin_dict,
        'destination': destination_dict,
        'intermediates': intermediates,
        'travelMode': 'DRIVE',
        'routingPreference': 'TRAFFIC_AWARE',
        'computeAlternativeRoutes': False,
        'routeModifiers': {
            'avoidTolls': False,
            'avoidHighways': False,
            'avoidFerries': False,
            },
        'languageCode': 'en-US',
        'units': 'IMPERIAL',
    }

    response = requests.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)

    data = response.json()

    trip_duration_list = []
    if 'routes' in data.keys():
        for trip_duration in data['routes'][0]['legs']:
            duration = float("{:.1f}".format(int(trip_duration['duration'][:-1])/60))
            trip_duration_list.append(duration)

    return trip_duration_list
    