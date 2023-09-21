import pandas_datareader.data as web
import random
from faker import Faker

symbol_day = {
        'DEXUSUK': 0,
        'DEXDNUS': 0,
        'DEXCAUS': 0,
        'EXJPUS':  0,
        'DEXMXUS': 0,
        'DEXSZUS': 0
    }

def currency_pair(fx_cur):

    d={fx_cur:symbol_day.get(fx_cur)+1}
    symbol_day.update(d)

    print(symbol_day)

    return {
        'DEXUSUK': 'USD/GBP',
        'DEXDNUS': 'DKK/USD',
        'DEXCAUS': 'USD/CAD',
        'EXJPUS': 'USD/JPY',
        'DEXMXUS': 'USD/MXN',
        'DEXSZUS': 'USD/CHF'
    }.get(fx_cur)

for i in range(10):
    fx_base_cur_list = ['DEXUSUK','DEXDNUS','DEXCAUS','EXJPUS','DEXMXUS','DEXSZUS']
    #fx_base_cur_list = ['DEXDNUS','DEXDNUS','DEXDNUS','DEXDNUS','DEXDNUS','DEXDNUS']
    fx_base_cur = random.choices(fx_base_cur_list, weights=(50, 34, 7, 41, 11, 4), k=1)[0]
    df = web.get_data_fred(fx_base_cur)
    fx_rate=df.iat[0, df.columns.get_loc(fx_base_cur)]
    cur_pair=currency_pair(fx_base_cur)
    print(cur_pair, fx_rate)


# Instantiate Faker class object
fake = Faker()
data=fake.profile()
print(data['username'])
print(data['name'])
print(data['mail'])
print(data['job'])
print(data['company'])
