from django.shortcuts import render
from django.http import JsonResponse
import requests
import os
import gmaps_api_call
import chatgpt_api_call
import path
from pathlib import Path
from dotenv import load_dotenv
from collections import defaultdict
import numpy as np
import json
from django.http import JsonResponse

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR.parent.absolute(), '.env'))

def test_get(location):
    # generate attractions list from ChatGPT
    generated_text = chatgpt_api_call.city_chatgpt_request(location)
    list_of_attractions = generated_text.split("\n")
    list_of_all_dicts = []
    lat_long_list = []
    lat_long_dict = defaultdict(int)

    # get latitude and longitude from GMAPS API
    for index, attraction in enumerate(list_of_attractions):
        gmaps_info_tuple = gmaps_api_call.single_gmap_request(attraction)
        place_id, lat_long, photos = gmaps_info_tuple
        info_dict = {'name': attraction,
                        'place_id': place_id,
                        'lat': lat_long[0],
                        'lng': lat_long[1],
                        'photo_info': photos}
        list_of_all_dicts.append(info_dict)
        lat_long_list.append(lat_long)
        lat_long_dict[lat_long] = index
    
    # pass latitude and longitudes into path function 
    # HARDCODED TO ONLY TAKE FIRST DAY FOR NOW
    ordered_activities = path.get_best_overall_path(1,lat_long_list)[0]
    permutation = []
    for activity in ordered_activities:
        lat_long_tuple = (activity[0],activity[1])
        permutation.append(lat_long_dict[lat_long_tuple])
    list_of_all_dicts = np.array(list_of_all_dicts)
    list_of_all_dicts[permutation]

    # pass this ordered list to the front-end
    midpoint = path.find_midpoint(lat_long_list)
    midpoint_and_ordered_list = {'midpoint' : midpoint,
                                    'locations_info_list' :list_of_all_dicts}
    return midpoint_and_ordered_list

print(test_get("San Francisco"))

# TEST