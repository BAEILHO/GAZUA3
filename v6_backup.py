# -*- coding: utf-8 -*-
"""
Created on Tue May  4 21:05:17 2021

@author: 1ho79
"""

import pyupbit
import sys
import pandas as pd
import time
import logging


tm = time.localtime()
c_time = time.strftime('%Y-%m/%d %I:%M', tm)
c_time_log = time.strftime('%Y_%m_%d_%I_%M', tm)

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler(f"aggresive_{c_time_log}_log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


#logger.info("aaa : %0.2f", bbb)

access = "ZRRx2FMNNmn8KjefANNB3lQNxHDIzCvvxVpxjwKC"          # 본인 값으로 변경
secret = "9FeUPbYFdfrFHRaE0QJ9nMQ3CGy3u5plVxhdVO6x"          # 본인 값으로 변경
server_url = "https://upbit.com"
upbit = pyupbit.Upbit(access, secret)



init_balance = upbit.get_balance(ticker="KRW")

logger.info("START!!   init balance : %d", init_balance)

   
#'KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 
#'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 
#'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP',
#'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 
#'KRW-TRX', 'KRW-SC', 'KRW-IGNIS', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 
#'KRW-LOOM', 'KRW-BCH', 'KRW-ADX', 'KRW-BAT', 'KRW-IOST', 'KRW-DMT', 'KRW-RFR', 
#'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 
#'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-EDR', 'KRW-QKC', 'KRW-BTT', 
#'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 
#'KRW-TT', 'KRW-CRE', 'KRW-SOLVE', 'KRW-MBL', 'KRW-TSHP', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 
#'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-PXL', 'KRW-STMX', 'KRW-DKA', 
#'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 
#'KRW-TON', 'KRW-SXP', 'KRW-LAMB', 'KRW-HUNT', 'KRW-MARO', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 
#'KRW-MVL', 'KRW-PCI', 'KRW-STRAX', 'KRW-AQT', 'KRW-BCHA', 'KRW-GLM', 'KRW-QTCON', 'KRW-SSX', 
#'KRW-META', 'KRW-OBSR', 'KRW-FCT2', 'KRW-LBC', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 
#'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-DAWN', 'KRW-AXS', 'KRW-STX'
#tickers = ["KRW-ETC", "KRW-XRP", "KRW-ETH", "KRW-WAVES", "KRW-EOS", "KRW-BTG", "KRW-BCH", "KRW-LTC", "KRW-VET", "KRW-DAWN", "KRW-NEO", "KRW-STPT", "KRW-CHZ", "KRW-OMG", "KRW-QTUM", "KRW-MED"]
#tickers = pyupbit.get_tickers(fiat="ALL")

tickers = []
f=open('target_list.txt','r')
for i in f:
#    print(i.strip())
    tickers.append(i.strip())
f.close()

bought_list = []
sell_order_list = []
sell_list = {}

def check_rate_validity(ticker):
    cnt = 0
    total_rate = 0
    avg_rate = 0
    new_rate_1 = 0
    new_rate_2 = 0
    df = pyupbit.get_ohlcv(f"{ticker}", interval="minute1", count=11)
    close_list = df['close'][0:10]
    for rate in close_list:
        if (cnt < 8):
            total_rate = total_rate + rate
            if (cnt == 7):
                avg_rate = total_rate / 8
        elif (cnt == 8):
            new_rate_1 = rate
        elif (cnt == 9):
            new_rate_2 = rate
        else:
            abc = 0
        cnt = cnt + 1
    logger.info("avg_rate : %0.6f   new_rate_1/avg_rate : %0.6f    new_rate_2/avg_rate : %0.6f", avg_rate, new_rate_1/avg_rate, new_rate_2/avg_rate)
    if (new_rate_1/avg_rate >= 1.02) and (new_rate_2/avg_rate >= 1.04) and (new_rate_1/avg_rate < 1.1) and (new_rate_2/avg_rate < 1.1):
        return "valid"
    else:
        return "invaild"


def check_volume_validity(ticker):
    cnt = 0
    total_volume = 0
    avg_volume = 0
    new_volume_1 = 0
    new_volume_2 = 0
    df = pyupbit.get_ohlcv(f"{ticker}", interval="minute1", count=11)
    volume_list = df['volume'][0:10]
    for volume in volume_list:
        if (cnt < 8):
            total_volume = total_volume + volume
            if (cnt == 7):
                avg_volume = total_volume / 8
        elif (cnt == 8):
            new_volume_1 = volume
        elif (cnt == 9):
            new_volume_2 = volume
        else:
            abc = 0
        cnt = cnt + 1
    logger.info("avg_volume : %d   new_volume_1/avg_volume : %0.3f   new_volume_2/avg_volume : %0.3f", avg_volume, new_volume_1/avg_volume, new_volume_2/avg_volume)
    if (new_volume_1/avg_volume >= 2) and (new_volume_2/avg_volume >= 2.2):
        return "valid"
    else:
        return "invaild"
    



status = "standby"

total_benefit = 0

low_price_renewal_past = 0

sell_aggresive_enable = 0
while_cnt = 0

while True:
    logger.info("while")
    if (status == "bought"):
        logger.info("status == bought")
        if (sell_aggresive_enable == 1):
            logger.info("sell_aggresive_enable == 1")
            df = pyupbit.get_ohlcv(f"{target_ticker}", interval="minute1", count=2)
            low_price_renewal = df['low'].iloc[1]
            if (low_price_renewal_cnt >= 3):
                logger.info("low_price_renewal_cnt >= 3")
                target_balance = upbit.get_balance(ticker=f"{target_ticker}")
                upbit.sell_market_order(f"{target_ticker}", target_balance * 0.99)
                time.sleep(10)
                sell_balance = upbit.get_balance(ticker="KRW")
                benefit = sell_balance / buy_balance - 1
                total_benefit = total_benefit + benefit
                low_price_renewal_cnt = 0
                low_price_renewal_past = 0
                logger.info("sell_aggresive : %d      benefit : %0.4f     total_benefit : %0.4f", sell_balance, benefit, total_benefit)
                status="standby"
                continue
            else:
                logger.info("low_price_renewal_cnt >= 3 else")
                if (low_price_renewal <= low_price_renewal_past):
                    logger.info("low_price_renewal <= low_price_renewal_past")
                    low_price_renewal_cnt = low_price_renewal_cnt + 1
                else:
                    logger.info("low_price_renewal <= low_price_renewal_past else")
                    low_price_renewal_cnt = 0
            low_price_renewal_past = low_price_renewal
        else:
            sell_order_list = []
            logger.info("sell_aggresive_enable == 1 else")
            sell_balance_tmp = upbit.get_balance(ticker=f"{target_ticker}")
            sell_balance = sell_balance_tmp * 0.095
            sell_price_tmp = pyupbit.get_current_price(f"{target_ticker}")
            sell_price = buy_price * 1.03
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 1.05
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 1.07
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 1.1
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 1.2
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 1.3
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 1.5
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 2
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 5
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_price = buy_price * 8
            tmp = upbit.sell_limit_order(f"{target_ticker}", sell_price, sell_balance)
            if 'uuid' in tmp:
                sell_order_list.append(tmp['uuid'])
                logger.info("ticker : %s   sell_limit_order : %d", target_ticker, sell_price)
            time.sleep(10)
            sell_list[target_ticker] = sell_order_list
            time.sleep(10)
            #upbit.sell_market_order(f"{target_ticker}", target_balance)
            str = target_ticker
            if (str.startswith('KRW-')):
                sell_balance = upbit.get_balance(ticker="KRW")
            elif (str.startswith('BTC-')):
                sell_balance = upbit.get_balance(ticker="KRW-BTC")
            else:
                abc = 0
            benefit = sell_balance / buy_balance - 1
            total_benefit = total_benefit + benefit
            status="standby"
            #logger.info("sell_3 : %d      benefit : %0.4f     total_benefit : %0.4f", sell_balance, benefit, total_benefit)
            continue
    else:
        logger.info("status == bought else")
        target_ticker = 0
        for ticker in tickers:
            str = ticker
            if (str.startswith('BTC-')):
                check_unit = pyupbit.get_current_price(f"{ticker}")
                if (check_unit < 0.00000100):
                    continue
            if ticker in bought_list:
                logger.info("bought_list has %s", ticker)
                check_price = pyupbit.get_current_price(f"{ticker}")
                ref_price = bought_list[ticker]
                logger.info("ref_price : %0.8f   check_price : %0.8f", ref_price, check_price)
                if (ref_price >= check_price):
                    logger.info("ref_price %0.8f > check_price %0.8f", ref_price, check_price)
                    logger.info("stop_loss %s", ticker)
                    for order in sell_list[ticker]:
                        try:
                            logger.info("cancel_order")
                            upbit.cancel_order(order)
                        except:
                            logger.info("already_cancled")
                        time.sleep(10)
                    time.sleep(10)
                    del sell_list[ticker]
                    del bought_list[ticker]
                    target_balance = upbit.get_balance(ticker=f"{ticker}")
                    logger.info("sell_market_order %s  target_balance : %d", ticker, target_balance)
                    upbit.sell_market_order(f"{ticker}", target_balance * 0.99)
                    continue
            rate_validity = check_rate_validity(ticker)    
            volume_validity = check_volume_validity(ticker)
            time.sleep(0.1)
            df = pyupbit.get_ohlcv(f"{ticker}", interval="minute1", count=11)
            logger.info("ticker : %s   rate_validity : %s  volume_validity : %s", ticker, rate_validity, volume_validity)
            if (rate_validity == "valid") and (volume_validity == "valid"):
                target_ticker = ticker
                break
        if (target_ticker != 0):
            logger.info("target_ticker != 0")
            str = target_ticker
            if (str.startswith('KRW-')):
                buy_price = pyupbit.get_current_price(f"{target_ticker}")
                buy_balance = upbit.get_balance(ticker="KRW")
                upbit.buy_market_order(f"{target_ticker}", buy_balance * 0.3)
            elif (str.startswith('BTC-')):
                buy_price = pyupbit.get_current_price(f"{target_ticker}")
                buy_balance = upbit.get_balance(ticker="KRW-BTC")
                upbit.buy_market_order(f"{target_ticker}", buy_balance * 0.3)
            else:
                abc = 0
            bought_list = {target_ticker:buy_price}
            low_price_renewal_cnt = 0
            low_price_renewal_past = 0
            high_price_renewal_cnt = 0
            high_price_renewal_past = 0
            red_cnt = 0
            blue_cnt = 0
            status="bought"
            logger.info("buy : %d  ticker : %s", buy_balance, target_ticker)
    if (status=="bought"):
        logger.info("status==bought  time sleep 30")
        time.sleep(30)
    else:
        logger.info("status==bought else time sleep 1")
        time.sleep(1)
    if (while_cnt == 20):
        upbit.buy_market_order("KRW-BTC", 10000)
        time.sleep(10)
        btc_price = pyupbit.get_current_price("KRW-BTC")
        btc_balance = 10000/btc_price
        upbit.sell_market_order("KRW-BTC", btc_balance * 0.99)
        time.sleep(10)
        while_cnt = 0
    else:
        while_cnt = while_cnt + 1

        

    
    
    

    #     if (open_value >= close_value):
    #         value = open_value - close_value
    #     else:
    #         value = close_value - open_value
    #     sum = sum + value
    # avg = sum / len(list_from_open)
    # return avg



# while True:
#     print(df)
#     if length_cnt < 10:
#         list_length.append(length)
#         avg_length = avg_cal(list_length)
#         #print("list_length", list_length, "avg_length", avg_length)
#         length_cnt = length_cnt + 1
#         #print(f"{c_time}  length_cnt :", length_cnt)
#         print("length_cnt : %d", length_cnt)
#         continue
#     else:
#         shift(list_length,length)
#         avg_length = avg_cal(list_length)
#         #print("list_length", list_length, "avg_length", avg_length)   
#     time.sleep(30)
    
            
            
            
            
            
            
            
            
            
            
