from coinexapi import RequestClient
import time
import csv
import sys

api_key='9657EAED13F4432F90F29B03D4A7470D'
api_secret='25864B70752940DD8D1B0AFC3FFF6695DC5D2A6D49F6C2CE'
kk = RequestClient(api_key, api_secret)

bgap=0
sgap=0

bgrid=0.0013
sgrid=0.0013

amount=1500

initial_b_count=0
initial_s_count=4

#status="restart"
status="continue"

trading_pair={"CETUSDT"}
pair="CETUSDT"

if status=="restart":

    kk.cancel_all(pair)

    kk.ticker(pair)

    bid_price=kk.bid-bgap*bgrid
    ask_price=kk.ask+sgap*sgrid

    count=initial_b_count
    while count>0:
        bid_price=bid_price-bgrid
    
        if bid_price<kk.ask:
            kk.place_order(amount,bid_price,"buy",pair)
        else:
            print " bid price error, pls check"
            sys.exit(0)
        count=count-1
    
    count=initial_s_count
    while count>0:
        ask_price=ask_price+sgrid
        if ask_price>kk.bid:
            kk.place_order(amount,ask_price,"sell",pair)
        else:
            print " ask price error, pls check"
            sys.exit(0)
        count=count-1


for i in range(1,10000):
    for pair in trading_pair:
        
        kk.pending_order(pair)
        kk.ticker(pair)
        
        print kk.buy_count,kk.max_buy,kk.sell_count,kk.min_sell
        
        s_count=initial_b_count-kk.buy_count
        
        if s_count+initial_s_count-kk.sell_count>0 and kk.crypto>amount:
            
            if kk.min_sell==99999:
                kk.min_sell=kk.ask+(sgap+1)*sgrid
            ask_price=kk.min_sell-sgrid
            kk.get_balance(pair[0:3])
            if kk.crypto>amount:
                kk.place_order(amount,ask_price,"sell",pair)
            else:
                print "Insufficient",pair[0:3]         
            
        b_count=initial_s_count-kk.sell_count
         
        if b_count+initial_b_count-kk.buy_count>0 and kk.crypto>amount*(kk.max_buy+bgrid):
            if kk.max_buy==0:
                kk.max_buy=kk.bid-(bgap+1)*bgrid
            bid_price=kk.max_buy+bgrid
            if kk.crypto>amount*(kk.max_buy+bgrid):
                kk.place_order(amount,bid_price,"buy",pair)
            else:
                print "Insufficient USDT!!!"
        
        
    print i,kk.buy_count,kk.sell_count,b_count,s_count   
    time.sleep(5) 
    
    
