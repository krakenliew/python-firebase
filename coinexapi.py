from __future__ import unicode_literals
import time
import hashlib
import json as complex_json
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)
http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=1, read=2))


class RequestClient(object):
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    def __init__(self, coinex_access_id, coinex_secret_key,headers={}):

        self.access_id = coinex_access_id   
        self.secret_key = coinex_secret_key
        self.url = 'https://api.coinex.com'
        self.headers = self.__headers
        #self.headers.update(headers)

    @staticmethod
    def get_sign(params, secret_key):
        sort_params = sorted(params)
        data = []
        for item in sort_params:
            data.append(item + '=' + str(params[item]))
        str_params = "{0}&secret_key={1}".format('&'.join(data), secret_key)
        token = hashlib.md5(str_params).hexdigest().upper()
        return token

    def set_authorization(self, params):
        params['access_id'] = self.access_id
        params['tonce'] = int(time.time()*1000)
        self.headers['AUTHORIZATION'] = self.get_sign(params, self.secret_key)

    def request(self, method, url, params={}, data='', json={}):
        method = method.upper()
        if method in ['GET', 'DELETE']:
            self.set_authorization(params)
            result = http.request(method, url, fields=params, headers=self.headers)
        else:
            if data:
                json.update(complex_json.loads(data))
            self.set_authorization(json)
            encoded_data = complex_json.dumps(json).encode('utf-8')
            result = http.request(method, url, body=encoded_data, headers=self.headers)
        return result

    def get_account(self):
        response = self.request('GET', '{url}/v1/balance/'.format(url=self.url))
    
        while response.status!=200:
            response = self.request('GET', '{url}/v1/balance/'.format(url=self.url))
            print response.status, "Error"
    
        resp = json.loads(response.data)
        # print resp
    
        self.btc=float(resp['data']['BTC']['available'])
        self.eth=float(resp['data']['ETH']['available'])
        self.bch=float(resp['data']['BCH']['available'])
        self.usd=float(resp['data']['USDT']['available'])
        self.cet=float(resp['data']['CET']['available'])
        self.ltc=float(resp['data']['LTC']['available'])
        self.eos=float(resp['data']['EOS']['available'])
        self.dash=float(resp['data']['DASH']['available'])
        
    def get_balance(self,asset):
        response = self.request('GET', '{url}/v1/balance/'.format(url=self.url))
    
        while response.status!=200:
            response = self.request('GET', '{url}/v1/balance/'.format(url=self.url))
            print response.status, "Error"
    
        resp = json.loads(response.data)
    
        # print resp
        if asset=="BTC":
            self.crypto=float(resp['data']['BTC']['available'])
        elif asset=="BCH":
            self.crypto=float(resp['data']['BCH']['available'])
        elif asset=="ETH":
            self.crypto=float(resp['data']['ETH']['available'])
        elif asset=="WINGS":
            self.crypto=float(resp['data']['WINGS']['available'])
        elif asset=="CET":
            self.crypto=float(resp['data']['CET']['available'])
        elif asset=="USDT":
            self.crypto=float(resp['data']['USDT']['available'])
        elif asset=="XMR":
            self.crypto=float(resp['data']['XMR']['available'])
            

    def pending_order(self,market_type):
        params = {'market': market_type, 'limit':100 }
        response = self.request('GET','{url}/v1/order/pending'.format(url=self.url),params=params)
        while response.status!=200:
            response = self.request('GET','{url}/v1/order/pending'.format(url=self.url),params=params)
            print "Pending Error"
        resp=json.loads(response.data)
        
        self.buy_pending=0
        self.sell_pending=0
        self.buy_count=0
        self.sell_count=0
        self.max_buy=0
        self.min_sell=99999
        
        for item in resp['data']['data']:
            if item['type']=='sell':
                self.sell_pending=self.sell_pending+float(item['left'])
                self.sell_count=self.sell_count+1
                
                if float(item['price'])<self.min_sell:
                    
                    self.min_sell=float(item['price'])
                    
            elif item['type']=='buy':
                self.buy_pending=self.buy_pending+float(item['left'])
                self.buy_count=self.buy_count+1
                if float(item['price'])>self.max_buy:
                    self.max_buy=float(item['price'])
        
        return resp['data']['data']
        
    def order_details(self,id, market_type):
        a = time.time() * 1000
        params = {"access_id": self.access_id,'id': id, 'market': market_type,"tonce": a,}
        response = self.request('GET','{url}/v1/order'.format(url=self.url),params=params)
        while response.status!=200:
            response = self.request('GET','{url}/v1/order'.format(url=self.url),params=params)
            print "Order Error"
        resp=json.loads(response.data)
        self.pending=resp['data']['left']
        
        
    def ticker(self,market_type):
    
        params = {'market': market_type}
        response = self.request('GET','{url}/v1/market/ticker'.format(url=self.url),params=params)

        resp = json.loads(response.data)
        data=resp['data']['ticker']
        
        self.ask=float(data['sell'])
        self.bid=float(data['buy'])
        self.last=float(data['last'])
        
        return data
        

    


    def order_finished(self, market_type, page, limit):
    
        params = {'market': market_type,'page': page,'limit': limit }
        response = self.request('GET','{url}/v1/order/finished'.format(url=self.url), params=params)
        print (response.status)


    def place_order(self,amount,price,side,pair):
        a = time.time() * 1000
        
        data = {
            "access_id": self.access_id,
            "amount": amount,
            "price": price,
            "type": side,
            "market":pair,
            "tonce": a,
        }

        response = self.request('POST','{url}/v1/order/limit'.format(url=self.url),json=data,)
        print response.status
        while response.status!=200:
            response = self.request('POST','{url}/v1/order/limit'.format(url=self.url),json=data,)
            print "Place Order Error"
        resp = json.loads(response.data)
        print resp
        if resp['data']!={}:
            self.order_id=resp['data']['id']
            self.order_price=float(resp['data']['price'])
            self.create_time=resp['data']['create_time']
            self.order_status="success"
        else:
            print resp['message']
            self.order_status="fail"
        return self.order_status
        
        
    
    


    def put_market(self):
    
        data = {"amount": "1", "type": "sell", "market": "CETBCH" }

        response = self.request('POST','{url}/v1/order/market'.format(url=self.url), json=data, )
        print (response.content)


    def cancel_order(self, id, market):
     
        data = {"id": id, "market": market, }
        

        response = self.request('DELETE','{url}/v1/order/pending'.format(url=self.url), params=data,)
        print "Cancelled"
        resp = response.data
        
        
    def cancel_all(self, market):
     
        resp=self.pending_order(market)
        
        for item in resp:
            self.cancel_order(item['id'],market)
        print "All Cancelled"
        

           
     

    def order_book(self, pair, limit):
        a = time.time() * 1000
        
    
        if pair[-4:]=="USDT":
            merge="0.0001"
        else:
            merge="0.00000001"
    
        params = {"market":pair.lower(), "merge": merge, "limit": limit}
    
        response = self.request('GET','{url}/v1/market/depth'.format(url=self.url),params=params,)
    
        print response.status
        while response.status != 200:
            response = self.request('GET','{url}/v1/market/depth'.format(url=self.url),params=params,)
            print response.status, " Order Book Error"
        
        resp = json.loads(response.data)
   
        self.bid1=float(resp['data']['bids'][0][0])
        self.bid1vol=float(resp['data']['bids'][0][1])
        self.bid2=float(resp['data']['bids'][1][0])
        self.bid2vol=float(resp['data']['bids'][1][1])
        self.ask1=float(resp['data']['asks'][0][0])
        self.ask1vol=float(resp['data']['asks'][0][1])
        self.ask2=float(resp['data']['asks'][1][0])
        self.ask2vol=float(resp['data']['asks'][1][1])
        
        return resp
    

    def rsi(self, pair, period, limit):
         
        params = {"market":pair.lower(), "type": period, "limit": limit}
           
        response = self.request('GET','{url}/v1/market/kline'.format(url=self.url),params=params,)
       
        while response.status!=200:
             response = self.request('GET','{url}/v1/market/kline'.format(url=self.url),params=params,)
             print "RSI Error"
        
        resp = json.loads(response.data)
        data=resp['data']        
        
        gain=0
        loss=0

        for i in range(0,limit):

            if data[i][1]<data[i][2]:
                current_gain=float(data[i][2])-float(data[i][1])
                gain=gain+current_gain
            elif data[i][1]>data[i][2]:
                current_loss=float(data[i][1])-float(data[i][2])
                loss=loss+current_loss
        '''
        self.ticker(pair)
        
        if self.last>data[limit-1][2]:
            gain=gain+self.last-float(data[limit-1][2])
        else:
            loss=loss+float(data[limit-1][2])-self.last
        '''
        
        ave_gain=gain/(limit)
        ave_loss=loss/(limit)
        
        if ave_loss==0:
            rs=1
        else:
            rs=ave_gain/ave_loss

        rsi= round(100 - (100)/(1+rs),2)

        return rsi
        
        
    def mov_average(self, pair, period, limit):
         
        params = {"market":pair.lower(), "type": period, "limit": limit}
           
        response = self.request('GET','{url}/v1/market/kline'.format(url=self.url),params=params,)
       
        while response.status!=200:
             response = self.request('GET','{url}/v1/market/kline'.format(url=self.url),params=params,)
             print "Moving Average Error"
        
        resp = json.loads(response.data)
        data=resp['data'] 
        
        total_close=0
        
        for i in range(0,limit):

            total_close=total_close+float(data[i][2])
            
        mov_ave=total_close/limit
        
        return mov_ave

    def datas(self, pair, period, limit):
        params = {"market":pair.lower(), "type": period, "limit": 2+limit}
           
        response = self.request('GET','{url}/v1/market/kline'.format(url=self.url),params=params,)
       
        while response.status!=200:
             response = self.request('GET','{url}/v1/market/kline'.format(url=self.url),params=params,)
             print "Data Error"
        
        resp = json.loads(response.data)
        sdata=resp['data']
        
        data=[float(x[2]) for x in sdata]

        return data 
        
        
        
    def sma(self,data,window):
        
        if len(data) < window:
            return None
        #print sum(data[-window:]) / float(window)
        return sum(data[-window:]) / float(window)
        
        

    def ema(self,data, window, position=None, previous_ema=None):
        
        if len(data) < window+2:
            return None
        c = float(2/(window + 1))
        
        if not previous_ema:
            
            return self.ema(data, window, 2, self.sma(data[int(-window-2):-2], window))
        else:
            current_ema = (c * data[-position]) + ((1 - c) * previous_ema)
            if position > 0:
                return self.ema(data, window, position - 1, current_ema)
            return previous_ema
            
    
    def macd(self, data,window):
        
        ema12=self.ema(data,12)
        ema26=self.ema(data,26)
        
        print ema12,ema26


