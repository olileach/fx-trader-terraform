import random


trade_region = ['APAC', 'EMEA', ' AMER']
trade_region = random.choices(trade_region, weights=(20, 54, 7), k=1)[0]

print(trade_region[0])

