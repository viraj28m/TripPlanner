import gmaps_api_call

f = gmaps_api_call.single_gmap_request

location = "Golden Gate Park"
city = "San Francisco, California, United States"

print(f(location, city))
