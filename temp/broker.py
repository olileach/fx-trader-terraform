import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import random
import json
import time
import os
from datetime import datetime 
from random_phone import RandomUkPhone
from forex_python.converter import CurrencyRates

def main():

    count = 1

    for i in range(0, int(count)):

        fx_dict = {}

        volume_list = ['1000', '5000', '10000', '20000', '50000', '100000']

        broker_list = ["Pepperstone", "IC Markets" , "FP Markets",  "Admiral Markets", \
                    "Roboforex" , "AvaTrade", "Interactive Brokers", "HF Markets" , "IG Markets" , "eToro"]

        trade_status_list = ['NEW', 'PENDING_NEW', 'FILLED', 'REJECTED', 'REJECTED_EXPIRED']
        
        trade_region = ['APAC', 'EMEA', ' AMER']

        trade_code_dict = { 	"FXA_00":"Trade requested and submitted to exchange.",
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

        trade_status = random.choice(trade_status_list)

        if trade_status in ['REJECTED', 'REJECTED_EXPIRED']:
            trade_code_value = random.choice(list(trade_code_dict.values()))
            trade_code_key = [key for key,value in trade_code_dict.items() if value == trade_code_value]
            trade_code = {trade_code_key[0]:trade_code_value}
        elif trade_status == 'PENDING_NEW':
            trade_code = {"FXA_10":"Trade requested and submitted to exchange but not filled."}
        else:
            trade_code = {"FXA_00":"Trade requested and submitted to exchange."}
        
        trade_code = list(trade_code)[0]

        c = CurrencyRates()
        rukp = RandomUkPhone()

        fx_base_cur_list = ['GBP','USD','AUD','JPY']
        fx_base_cur = random.choices(fx_base_cur_list, weights=(20, 54, 7, 11), k=1)

        


        fx_base_cur_rates=c.get_rates(fx_base_cur)
        fx_random_cur=random.randint(0, len(fx_base_cur))
        fx_cur = (list(fx_base_cur_rates.keys())[fx_random_cur])

        fx_rate = c.get_rate(fx_base_cur, fx_cur)

        fx_dict.update({'current_rate' : fx_rate})
        fx_dict.update({'region': trade_region[random.randint(0,2)]})
        fx_dict.update({'base_currency': fx_base_cur})
        fx_dict.update({'target_currency': fx_cur})
        fx_dict.update({'currency_pair':fx_base_cur+fx_cur})
        fx_dict.update({'volume': volume_list[random.randint(0,5)]})
        fx_dict.update({'broker': broker_list[random.randint(0,9)]})
        fx_dict.update({'broker_phone': rukp.random_landline()})
        fx_dict.update({'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]})
        fx_dict.update({'status' : trade_status})
        fx_dict.update({'trade_code_dict': trade_code_dict})
        fx_dict.update({'trade_code': trade_code})
        fx_dict.update({'stock_exchange': stock_exchange()})
        fx_dict.update({'total_trades' : count})

        print(("FX Trade payload {}").format(fx_dict))

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
    
if (__name__ == "__main__"):
    main()