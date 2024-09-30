import geopy.distance
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from k_means_constrained import KMeansConstrained
from collections import defaultdict
from itertools import permutations 


def get_k_cluster_labels(n_clusters,long_lat_list):
    size_max = 4
    if len(long_lat_list) <= 3:
        size_max = 3
    kmeans = KMeansConstrained(n_clusters=n_clusters, size_min=2, size_max=size_max, random_state=0)
    kmeans.fit_predict(long_lat_list)
    labels = kmeans.labels_
    grouped_lat_longs = defaultdict(list)

    for i,label in enumerate(labels):
        grouped_lat_longs[label].append(long_lat_list[i])

    return list(grouped_lat_longs.values())

def get_distance_meters(coords_1,coords_2):
    return geopy.distance.geodesic(coords_1, coords_2).km * 1000

def compute_path_dist(origin,path):
    total_dist = get_distance_meters(origin,path[0])
    for i in range(1,len(path)):
        total_dist += get_distance_meters(path[i-1],path[i])
    return total_dist

def get_best_path_for_cluster(long_lat_list,midpoint):

    # generate all permuations of paths with first destination as starting point
    perm_list = list(permutations(long_lat_list))

    # compute the order that gives the best path
    best_order = list(perm_list[0])
    best_dist = np.inf
    for i in range(len(perm_list)):
        cur_dist = compute_path_dist(midpoint,perm_list[i]) + get_distance_meters(perm_list[i][-1],midpoint)
        if cur_dist < best_dist:
            best_dist = cur_dist
            best_order = list(perm_list[i])
    
    # concatenate with first destination to give best overall path
    best_overall_path = best_order
    return best_overall_path

def get_best_overall_path(days,long_lat_list,midpoint):
    activities_per_day = get_k_cluster_labels(days,long_lat_list)
    ordered_activities = []

    for day in range(days):
        daily_itinerary = activities_per_day[day]
        ordered_daily_itinerary = get_best_path_for_cluster(daily_itinerary,midpoint)
        ordered_activities.append(ordered_daily_itinerary)

    return ordered_activities

def get_path_names(lat_long_to_name,ordered_activities):
    for day in range(len(ordered_activities)):
        named_activities = []
        for i,location in enumerate(ordered_activities[day]):
            location_tuple = (location[0],location[1])
            named_activities.append(lat_long_to_name[location_tuple])
        ordered_activities[day] = named_activities
        
    return ordered_activities

def find_midpoint(long_lat_list):
    n = len(long_lat_list)
    lat_sum = 0
    lng_sum = 0
    for lat, lng in long_lat_list:
        lat_sum += lat
        lng_sum += lng
    return (lat_sum/n,lng_sum/n)
