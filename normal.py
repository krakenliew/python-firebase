import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from coinexapi import RequestClient
import time

cred = credentials.Certificate('./jonvi.json')
default_app = firebase_admin.initialize_app(cred)
client = firestore.client()
docs = client.collection('trading_bot').get()
indicator_target = 'normal'


apikeys = {}
apisecrets = {}
names = {}
tradingpairs = []
normal_target_1 = {}
normal_target_2 = {}
normal_amount = {}
normal_stop_value = {}
normal_buy_zone = {}
normal_percentage_value = {}

# for i in range(1, 10000):
   
for doc in docs:
    # print( json.dumps(doc.to_dict(), indent=4))
    
    data = doc.to_dict()
    if(data['indicator'] == indicator_target):
        # print json.dumps(data, indent=4)
        apikeys[data['trading_pair']] = data['api_key'] 
        apisecrets[data['trading_pair']] = data['secret_key'] 
        names [data['trading_pair']]= data['bot_name'] 
        tradingpairs.append( data['trading_pair'] )
        normal_target_1[data['trading_pair']] = data['normal_target_1']
        normal_target_2[data['trading_pair']] = data['normal_target_2']
        normal_amount[data['trading_pair']] = data['normal_amount']
        normal_stop_value[data['trading_pair']] = data['normal_stop_value']
        normal_buy_zone[data['trading_pair']] = data['normal_buy_zone']
        normal_percentage_value[data['trading_pair']] = data['normal_percentage_value']


users=[{'api_key':apikeys,
    'api_secret':apisecrets,
    'name':names,
    'trading_pair':tradingpairs,
    'normal_target_1':normal_target_1,
    'normal_target_2':normal_target_2,
    'normal_amount':normal_amount,
    'normal_stop_value':normal_stop_value,
    'normal_buy_zone':normal_buy_zone,
    'normal_percentage_value':normal_percentage_value
    }]

print json.dumps(users, indent=4)
time.sleep(2)