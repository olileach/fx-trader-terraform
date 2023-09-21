#
#  Copyright 2010-2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import random
import json
import time
import os
from datetime import datetime
import pandas_datareader.data as web
from faker import Faker
from geopy.geocoders import Nominatim
import random

# Instantiate Faker class object
fake = Faker()

geolocator = Nominatim(user_agent="MyApp")

config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)

symbol_day = {
        'DEXUSUK': 0,
        'DEXDNUS': 0,
        'DEXCAUS': 0,
        'EXJPUS':  0,
        'DEXMXUS': 0,
        'DEXSZUS': 0
    }

fx_trader_stream = os.environ["FX_TRADE_STREAM"]
region = os.environ["AWS_REGION"]

kinesis_client = boto3.client('kinesis', config=config, region_name=region)

def handler(event, context):

    print(event)
    print(("Current Lambda event payload {}").format(event))
    if event.get('trader_executions'):
        print(("Number of traders to execute {}").format(event.get('trader_executions')))
        count = int(event.get('trader_executions'))
    else:
        count = 1

    for i in range(0, int(count)):

        fx_dict = {}

        volume_list = ['1000', '5000', '10000', '20000', '50000', '100000']

        broker_list = ["Pepperstone", "IC Markets" , "FP Markets",  "Admiral Markets", \
                    "Roboforex" , "AvaTrade", "Interactive Brokers", "HF Markets" , "IG Markets" , "eToro"]

        trader_status_list = ['NEW', 'PENDING_NEW', 'FILLED', 'REJECTED', 'REJECTED_EXPIRED', 'RFQ']
        
        # Getting trader location details
        try:
            trader_regions = ['APAC', 'EMEA', 'AMER']
            trader_region = random.choices(trader_regions, weights=(8,5,3), k=1)[0]
            trader_cities= trader_location(trader_region)
            trader_city = random.choices(trader_cities)[0]
            trader_coordinates_locator = locations(trader_city)
        except:
            print("error getting coordinates")

        # Trade CODES
        trader_code_dict = { 	"FXA_00":"Trade requested and submitted to exchange.",
                                "FXA_01":"Invalid request. A change is needed.",
                                "FXA_02":"Cutoff has been reached for the requested currency pair.",
                                "FXA_03":"Order request submitted on an expired quote.",
                                "FXA_04":"Request performed outside of the trading desk opening hours.",
                                "FXA_05":"Value date for the request currency pair is not a business date.",
                                "FXA_06":"Request exceeds the maximum or minimum transaction limit.",
                                "FXA_07":"Duplicate request detection triggered.",
                                "FXA_08":"Credit check failed.",
                                "FXA_09":"Combination of instrument, tenor and/or currency pair is not allowed.",
                                "FXA_10":"Trade requested and submitted to exchange but not filled."
                            }

        trader_status = random.choices(trader_status_list, weights=(50, 30, 15, 11, 3, 25), k=1)[0]

        if trader_status in ['REJECTED', 'REJECTED_EXPIRED']:
            trader_code_value = random.choice(list(trader_code_dict.values()))
            trader_code_key = [key for key,value in trader_code_dict.items() if value == trader_code_value]
            trader_code = {trader_code_key[0]:trader_code_value}
        elif trader_status == 'PENDING_NEW':
            trader_code = {"FXA_10":"Trade requested and submitted to exchange but not filled."}
        else:
            trader_code = {"FXA_00":"Trade requested and submitted to exchange."}
        
        trader_code = list(trader_code)[0]

        data= fake.profile()

        fx_base_cur_list = ['DEXUSUK','DEXDNUS','DEXCAUS','EXJPUS','DEXMXUS','DEXSZUS']
        fx_base_cur = random.choices(fx_base_cur_list, weights=(50, 34, 7, 41, 11, 4), k=1)[0]
        df = web.get_data_fred(fx_base_cur)
        trade_day = currency_pair_trade_day(fx_base_cur)
        fx_rate=df.iat[trade_day, df.columns.get_loc(fx_base_cur)]
        cur_pair=currency_pair(fx_base_cur)

        fx_dict.update({'current_rate' : fx_rate})
        fx_dict.update({'trader_region': trader_region})
        fx_dict.update({'trader_city': trader_city})
        fx_dict.update({'trader_latidude': trader_coordinates_locator["latitude"]})
        fx_dict.update({'trader_longitude': trader_coordinates_locator["longitude"]})
        fx_dict.update({'base_currency': 'USD'})
        fx_dict.update({'target_currency': cur_pair.strip('USD').strip('/')})
        fx_dict.update({'currency_pair': cur_pair})
        fx_dict.update({'volume': volume_list[random.randint(0,5)]})
        fx_dict.update({'broker': broker_list[random.randint(0,9)]})
        fx_dict.update({'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]})
        fx_dict.update({'status' : trader_status})
        fx_dict.update({'trader_code_dict': trader_code_dict})
        fx_dict.update({'trader_code': trader_code})
        fx_dict.update({'stock_exchange': stock_exchange()})
        fx_dict.update({'total_traders' : count})
        fx_dict.update({'username': data['username']})
        fx_dict.update({'name': data['name']})
        fx_dict.update({'phone': data['ssn']})

        print(("FX Trade payload {}").format(fx_dict))
        print(("Sending FX Trade payload to {} Kinesis Stream ").format(fx_trader_stream))
        
        put_record(fx_dict)

        print("Payload sent successfully to Kinesis Stream")

def put_record(fx_dict):
    key=random.choice(['1','2','3','4','5','6','7','8','9','10'])
    error=True
    i=0
    retries=30
    while error==True:
        try:
            print(f"Kinsis put record attempt {i}")
            response = kinesis_client.put_record(
                StreamName=fx_trader_stream,
                Data=json.dumps(fx_dict),
                PartitionKey=key
            )
            print(response)
            error=False
        except ClientError as e:
            sleeptime = random.uniform(1, 5)
            print(e)
            print(f"Error putting records on stream. Trying {i} of {retries} times")
            time.sleep(sleeptime)
            i+=1
            print(f"Setting error retry for Kinesis Put Records to {i}")
            if i>retries:
                error=False

def stock_exchange():
	
	stock_exchange_dict = {
		"New York Stock Exchange":"XNYS",
		"Nasdaq":"XNAS",
		"Shanghai Stock Exchange":"XSHG",
		"Euronext":"XAMS",
		"Euronext":"XBRU",
		"Euronext":"XMSM",
		"Euronext":"XLIS",
		"Euronext":"XMIL",
		"Euronext":"XOSL",
		"Euronext":"XPAR",
		"Shenzhen Stock Exchange":"XSHE",
		"Japan Exchange Group":"XJPX",
		"Hong Kong Stock Exchange":"XHKG",
		"Johannesburg Stock Exchange":"XJS",
		"Bombay Stock Exchange":"XBOM",
		"National Stock Exchange":"XNSE",
		"London Stock Exchange":"XLON",
		"Saudi Stock Exchange":"XSAU",
		"Toronto Stock Exchange":"XTSE",
		"SIX Swiss Exchange":"XSWX",
		"Nasdaq Nordic and Baltic Exchanges":"Europe",
		"Korea Exchange":"XKOS",
		"Australian Securities Exchange":"XASX",
		"Taiwan Stock Exchange":"XTAI"
	}

	res = key, val = random.choice(list(stock_exchange_dict.items()))
	return(res)

def currency_pair_trade_day(fx_cur):

    v=symbol_day.get(fx_cur)+1
    d={fx_cur:v}
    symbol_day.update(d)
    return(v)
        
def currency_pair(fx_cur):

    return {
        'DEXUSUK': 'USD/GBP',
        'DEXDNUS': 'DKK/USD',
        'DEXCAUS': 'USD/CAD',
        'EXJPUS': 'USD/JPY',
        'DEXMXUS': 'USD/MXN',
        'DEXSZUS': 'USD/CHF'
    }.get(fx_cur)

def locations(city):

    city_locations={'Chennai': {'latitude': 13.0836939, 'longitude': 80.270186}, 'Mumbai': {'latitude': 19.08157715, 'longitude': 72.88662753964906}, 'Hyderabad': {'latitude': 17.360589, 'longitude': 78.4740613}, 'Kolkata': {'latitude': 22.5726459, 'longitude': 88.3638953}, 'Bangalore': {'latitude': 12.9767936, 'longitude': 77.590082}, 'Delhi': {'latitude': 28.6273928, 'longitude': 77.1716954}, 'Pune': {'latitude': 18.521428, 'longitude': 73.8544541}, 'Ahmedabad': {'latitude': 23.0216238, 'longitude': 72.5797068}, 'Surat': {'latitude': 45.9383, 'longitude': 3.2553}, 'London': {'latitude': 51.5073359, 'longitude': -0.12765}, 'Manchester': {'latitude': 53.4794892, 'longitude': -2.2451148}, 'Birmingham': {'latitude': 52.4796992, 'longitude': -1.9026911}, 'Bristol': {'latitude': 51.4538022, 'longitude': -2.5972985}, 'Liverpool': {'latitude': 53.4071991, 'longitude': -2.99168}, 'Edinburgh': {'latitude': 55.9533456, 'longitude': -3.1883749}, 'Glasgow': {'latitude': 55.861155, 'longitude': -4.2501687}, 'Leeds': {'latitude': 53.7974185, 'longitude': -1.5437941}, 'Newcastle upon Tyne': {'latitude': 54.9738474, 'longitude': -1.6131572}, 'Brighton': {'latitude': 50.8214626, 'longitude': -0.1400561}, 'Cardiff': {'latitude': 51.4816546, 'longitude': -3.1791934}, 'Sheffield': {'latitude': 53.3806626, 'longitude': -1.4702278}, 'York': {'latitude': 53.9590555, 'longitude': -1.0815361}, 'Nottingham': {'latitude': 52.9534193, 'longitude': -1.1496461}, 'Belfast': {'latitude': 54.596391, 'longitude': -5.9301829}, 'Bath': {'latitude': 51.3813864, 'longitude': -2.3596963}, 'Coventry': {'latitude': 52.4081812, 'longitude': -1.510477}, 'Leicester': {'latitude': 52.6362, 'longitude': -1.1331969}, 'Southampton': {'latitude': 50.9025349, 'longitude': -1.404189}, 'Portsmouth': {'latitude': 50.800031, 'longitude': -1.0906023}, 'Norwich': {'latitude': 52.6285576, 'longitude': 1.2923954}, 'Chester': {'latitude': 53.1908873, 'longitude': -2.8908955}, 'San Francisco': {'latitude': 37.7790262, 'longitude': -122.419906}, 'Los Angeles': {'latitude': 34.0536909, 'longitude': -118.242766}, 'New York': {'latitude': 40.7127281, 'longitude': -74.0060152}, 'Chicago': {'latitude': 41.8755616, 'longitude': -87.6244212}, 'Washington': {'latitude': 38.8950368, 'longitude': -77.0365427}, 'Seattle': {'latitude': 47.6038321, 'longitude': -122.330062}, 'San Diego': {'latitude': 32.7174202, 'longitude': -117.1627728}, 'Philadelphia': {'latitude': 39.9527237, 'longitude': -75.1635262}, 'Houston': {'latitude': 29.7589382, 'longitude': -95.3676974}, 'Las Vegas': {'latitude': 36.1672559, 'longitude': -115.148516}, 'Nevada': {'latitude': 39.5158825, 'longitude': -116.8537227}, 'Miami': {'latitude': 25.7741728, 'longitude': -80.19362}, 'Dallas': {'latitude': 32.7762719, 'longitude': -96.7968559}, 'Austin': {'latitude': 30.2711286, 'longitude': -97.7436995}, 'Denver': {'latitude': 39.7392364, 'longitude': -104.984862}, 'San Antonio': {'latitude': 29.4246002, 'longitude': -98.4951405}, 'Nashville': {'latitude': 36.1622767, 'longitude': -86.7742984}, 'Phoenix': {'latitude': 33.4484367, 'longitude': -112.074141}, 'San Jose': {'latitude': 37.3361663, 'longitude': -121.890591}, 'Oakland': {'latitude': 37.8044557, 'longitude': -122.271356}, 'Portland': {'latitude': 45.5202471, 'longitude': -122.674194}}
    return(city_locations.get(city))

def trader_location(trader_region):


    if trader_region == 'AMER': return ["San Francisco",
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
    
    if trader_region == 'EMEA': return ["London",
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

    if trader_region == 'APAC': return['Chennai',
                    'Mumbai',
                    'Hyderabad',
                    'Kolkata',
                    'Bangalore',
                    'Delhi',
                    'Pune',
                    'Ahmedabad',
                    'Surat']