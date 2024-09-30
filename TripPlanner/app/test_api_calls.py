import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR.parent.absolute(), '.env'))

def get_place_id(location):

    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress'
    }

    data = {
        'textQuery': location
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        if 'places' in response_json and response_json['places']:
            first_place = response_json['places'][0]
            place_id = first_place.get('id', 'No ID found')
            formatted_address = first_place.get('formattedAddress', 'No address found')

            print(f"Place ID: {place_id}")
            print(f"Address: {formatted_address}")
            return place_id
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    location = "Stanford University"
    place_id = get_place_id(location)
