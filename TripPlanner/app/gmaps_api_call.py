import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def single_gmap_request(location, city):
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(os.path.join(BASE_DIR.parent.absolute(), '.env'))

    api_key = os.environ.get('GOOGLE_CLOUD_INTERNAL_KEY')
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {
        'input': location + ", " + city,
        'inputtype': 'textquery',
        'fields': 'place_id,geometry,photos',
        'key': api_key
    }

    response = requests.get(url, params=params)

    data = response.json()
    place_id = data['candidates'][0]['place_id'] if data['candidates'] else None
    lat = data['candidates'][0]['geometry']['location']['lat'] if data['candidates'] else None
    lng = data['candidates'][0]['geometry']['location']['lng'] if data['candidates'] else None
    photos = data['candidates'][0]['photos'] if data['candidates'] and 'photos' in data['candidates'][0] else None
    
    editorialSummary = ""

    for i in range(len(data['candidates'])):
        curPlaceID = data['candidates'][i]['place_id']
        if curPlaceID:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
            'place_id': curPlaceID,
            'fields': 'editorial_summary',
            'key': api_key
            }
            responseEditorial = requests.get(url, params=params)
            dataEditorial = responseEditorial.json()
            if 'error_message' in dataEditorial:
                print(dataEditorial['error_message'])
            if 'result' in dataEditorial and 'editorial_summary' in dataEditorial['result'] and 'overview' in dataEditorial['result']['editorial_summary']:
                editorialSummary = dataEditorial['result']['editorial_summary']['overview']
        if editorialSummary:
            break
    
    if editorialSummary:
        return (place_id, (lat,lng), photos, editorialSummary)

    # try with the keyword "Tourist Attraction"
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {
        'input': location + " Tourist Attraction, " + city,
        'inputtype': 'textquery',
        'fields': 'place_id,geometry,photos',
        'key': api_key
    }

    response2 = requests.get(url, params=params)

    data2 = response2.json()
    place_id2 = data2['candidates'][0]['place_id'] if data2['candidates'] else None
    lat2 = data2['candidates'][0]['geometry']['location']['lat'] if data2['candidates'] else None
    lng2 = data2['candidates'][0]['geometry']['location']['lng'] if data2['candidates'] else None
    photos2 = data2['candidates'][0]['photos'] if data2['candidates'] and 'photos' in data2['candidates'][0] else None

    editorialSummary2 = ""
    for i in range(len(data2['candidates'])):
        curPlaceID = data2['candidates'][i]['place_id']
        if curPlaceID:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
            'place_id': curPlaceID,
            'fields': 'editorial_summary',
            'key': api_key
            }
            responseEditorial2 = requests.get(url, params=params)
            dataEditorial2 = responseEditorial2.json()
            if 'error_message' in dataEditorial2:
                print(dataEditorial2['error_message'])
            if 'result' in dataEditorial2 and 'editorial_summary' in dataEditorial2['result'] and 'overview' in dataEditorial2['result']['editorial_summary']:
                editorialSummary2 = dataEditorial2['result']['editorial_summary']['overview']
        if editorialSummary2:
            break
    
    if editorialSummary2:
        return (place_id2, (lat2,lng2), photos2, editorialSummary2)
    
    return (place_id, (lat,lng), photos, editorialSummary)