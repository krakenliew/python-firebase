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
indicator_target = 'sup_res'


apikeys = {}
apisecrets = {}
names = {}
tradingpairs = []
sell_1 = {}
sell_2 = {}
sup_res_amount = {}
sup_res_stop_loss = {}
support_value = {}
resistant_value = {}

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
        sell_1[data['trading_pair']] = data['sell_1']
        sell_2[data['trading_pair']] = data['sell_2']
        sup_res_amount[data['trading_pair']] = data['sup_res_amount']
        sup_res_stop_loss[data['trading_pair']] = data['sup_res_stop_loss']
        support_value[data['trading_pair']] = data['support_value']
        resistant_value[data['trading_pair']] = data['resistant_value']


users=[{'api_key':apikeys,
    'api_secret':apisecrets,
    'name':names,
    'trading_pair':tradingpairs,
    'sell_1':sell_1,
    'sell_2':sell_2,
    'sup_res_amount':sup_res_amount,
    'sup_res_stop_loss':sup_res_stop_loss,
    'support_value':support_value,
    'resistant_value':resistant_value
    }]

print json.dumps(users, indent=4)
time.sleep(2)
# for user in users:
#     kk = RequestClient(user['api_key'],user['api_secret'])
#     print user['name']
#     kk.get_account()
#     print kk.usd, kk.cet