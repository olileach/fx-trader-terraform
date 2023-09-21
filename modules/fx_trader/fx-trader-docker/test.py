# Import the required library
from geopy.geocoders import Nominatim
import random
import time

from geopy.exc import GeocoderTimedOut

def do_geocode(address, attempt=1, max_attempts=5):
    try:
        return geopy.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_geocode(address, attempt=attempt+1)
        raise



# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")

def trader_location(trader_region):

    
    if trader_region == 'AMER': return \
                    ["San Francisco",
                    "Los Angeles",
                    "New York",
                    "Chicago",
                    "Washington",
                    "Seattle",
                    "San Diego",
                    "Philadelphia",
                    "Houston",
                    "Las Vegas",
                    "Nevada",
                    "Miami",
                    "Dallas",
                    "Houston",
                    "Austin",
                    "Denver",
                    "San Antonio",
                    "Nashville",
                    "Phoenix",
                    "San Jose",
                    "Oakland",
                    "Portland"]
    
    if trader_region == 'EMEA': return \
                    ["London",
                    "Manchester",
                    "Birmingham",
                    "Bristol",
                    "Liverpool",
                    "Edinburgh",
                    "Glasgow",
                    "Leeds",
                    "Newcastle upon Tyne",
                    "Brighton",
                    "Cardiff",
                    "Sheffield",
                    "York",
                    "Nottingham",
                    "Belfast",
                    "Bath",
                    "Coventry",
                    "Leicester",
                    "Southampton",
                    "Portsmouth",
                    "Norwich",
                    "Chester"]

    if trader_region == 'APAC': return \
                    ['Chennai',
                    'Mumbai',
                    'Hyderabad',
                    'Kolkata',
                    'Bangalore',
                    'Delhi',
                    "Pune",
                    'Ahmedabad',
                    'Surat']
  

def locations(trader_city):

    trader_city_dict={'Chennai': {'latitude': 13.0836939, 'longitude': 80.270186}, 'Mumbai': {'latitude': 19.08157715, 'longitude': 72.88662753964906}, 'Hyderabad': {'latitude': 17.360589, 'longitude': 78.4740613}, 'Kolkata': {'latitude': 22.5726459, 'longitude': 88.3638953}, 'Bangalore': {'latitude': 12.9767936, 'longitude': 77.590082}, 'Delhi': {'latitude': 28.6273928, 'longitude': 77.1716954}, 'Pune': {'latitude': 18.521428, 'longitude': 73.8544541}, 'Ahmedabad': {'latitude': 23.0216238, 'longitude': 72.5797068}, 'Surat': {'latitude': 45.9383, 'longitude': 3.2553}, 'London': {'latitude': 51.5073359, 'longitude': -0.12765}, 'Manchester': {'latitude': 53.4794892, 'longitude': -2.2451148}, 'Birmingham': {'latitude': 52.4796992, 'longitude': -1.9026911}, 'Bristol': {'latitude': 51.4538022, 'longitude': -2.5972985}, 'Liverpool': {'latitude': 53.4071991, 'longitude': -2.99168}, 'Edinburgh': {'latitude': 55.9533456, 'longitude': -3.1883749}, 'Glasgow': {'latitude': 55.861155, 'longitude': -4.2501687}, 'Leeds': {'latitude': 53.7974185, 'longitude': -1.5437941}, 'Newcastle upon Tyne': {'latitude': 54.9738474, 'longitude': -1.6131572}, 'Brighton': {'latitude': 50.8214626, 'longitude': -0.1400561}, 'Cardiff': {'latitude': 51.4816546, 'longitude': -3.1791934}, 'Sheffield': {'latitude': 53.3806626, 'longitude': -1.4702278}, 'York': {'latitude': 53.9590555, 'longitude': -1.0815361}, 'Nottingham': {'latitude': 52.9534193, 'longitude': -1.1496461}, 'Belfast': {'latitude': 54.596391, 'longitude': -5.9301829}, 'Bath': {'latitude': 51.3813864, 'longitude': -2.3596963}, 'Coventry': {'latitude': 52.4081812, 'longitude': -1.510477}, 'Leicester': {'latitude': 52.6362, 'longitude': -1.1331969}, 'Southampton': {'latitude': 50.9025349, 'longitude': -1.404189}, 'Portsmouth': {'latitude': 50.800031, 'longitude': -1.0906023}, 'Norwich': {'latitude': 52.6285576, 'longitude': 1.2923954}, 'Chester': {'latitude': 53.1908873, 'longitude': -2.8908955}, 'San Francisco': {'latitude': 37.7790262, 'longitude': -122.419906}, 'Los Angeles': {'latitude': 34.0536909, 'longitude': -118.242766}, 'New York': {'latitude': 40.7127281, 'longitude': -74.0060152}, 'Chicago': {'latitude': 41.8755616, 'longitude': -87.6244212}, 'Washington': {'latitude': 38.8950368, 'longitude': -77.0365427}, 'Seattle': {'latitude': 47.6038321, 'longitude': -122.330062}, 'San Diego': {'latitude': 32.7174202, 'longitude': -117.1627728}, 'Philadelphia': {'latitude': 39.9527237, 'longitude': -75.1635262}, 'Houston': {'latitude': 29.7589382, 'longitude': -95.3676974}, 'Las Vegas': {'latitude': 36.1672559, 'longitude': -115.148516}, 'Nevada': {'latitude': 39.5158825, 'longitude': -116.8537227}, 'Miami': {'latitude': 25.7741728, 'longitude': -80.19362}, 'Dallas': {'latitude': 32.7762719, 'longitude': -96.7968559}, 'Austin': {'latitude': 30.2711286, 'longitude': -97.7436995}, 'Denver': {'latitude': 39.7392364, 'longitude': -104.984862}, 'San Antonio': {'latitude': 29.4246002, 'longitude': -98.4951405}, 'Nashville': {'latitude': 36.1622767, 'longitude': -86.7742984}, 'Phoenix': {'latitude': 33.4484367, 'longitude': -112.074141}, 'San Jose': {'latitude': 37.3361663, 'longitude': -121.890591}, 'Oakland': {'latitude': 37.8044557, 'longitude': -122.271356}, 'Portland': {'latitude': 45.5202471, 'longitude': -122.674194}}

    print(len(trader_city_dict))
    return(trader_city_dict.get(trader_city))

def main():

    lat_dict={}
    
    for trader_region in ["APAC", "EMEA", "AMER"]:

        trader_cities= trader_location(trader_region)
        print('---------------------------------')
        print(trader_cities)
        for city in trader_cities:
            print(city)
            time.sleep(2)
            _x=None
            try:
                _x = geolocator.geocode(city)
                d = {}
                d[city]={"latitude" : _x.latitude, "longitude": _x.longitude}
                lat_dict.update(d)
            except:
                print("An exception occurred")
    
    return(lat_dict)


# Getting trader location details
trader_regions = ['APAC', 'EMEA', 'AMER']
trader_region = random.choices(trader_regions, weights=(8,5,3), k=1)[0]
trader_cities= trader_location(trader_region)
trader_city = random.choices(trader_cities)[0]
trader_coordinates_locator = locations(trader_city)
print(trader_coordinates_locator)
print(len(trader_coordinates_locator))
