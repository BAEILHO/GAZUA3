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
import ccxt

from collections import deque


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
file_handler = logging.FileHandler(filename='./log/v10.txt')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


#logger.info("aaa : %0.2f", bbb)

access = "ZRRx2FMNNmn8KjefANNB3lQNxHDIzCvvxVpxjwKC"          # 본인 값으로 변경
secret = "9FeUPbYFdfrFHRaE0QJ9nMQ3CGy3u5plVxhdVO6x"          # 본인 값으로 변경
server_url = "https://upbit.com"
upbit = pyupbit.Upbit(access, secret)



init_balance = upbit.get_balance(ticker="KRW")

logger.info("START!!   init balance : %d", init_balance)



binance = ccxt.binance()

ticker = "KRW-ETC"


status = "standby"
past_volume = 0
red_cnt = 0
blue_cnt = 0

total_profit = 0

current_high_past = 0
current_low_past = 0


dq = deque(maxlen=10)

while True:
    price = pyupbit.get_current_price(f"{ticker}")
    dq.append(price)
    print(price, dq[0:9])

    


#while True:
#    btc_ohlcv = binance.fetch_ohlcv("BTC/BUSD")
#    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
#    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
#    df.set_index('datetime', inplace=True)
#    if (status == "standby"):
#        current_volume = df['volume'].iloc[498]
#        if (current_volume != past_volume):
#            current_open = df['open'].iloc[498]
#            current_close = df['close'].iloc[498]
#            open_list = df['open'][490:499]
#            close_list = df['close'][490:499]
#            dif_list = open_list - close_list
#            abs_list = abs(dif_list)
#            avg = sum(abs_list)/len(abs_list) * 0.2
#            current_avg = abs(current_open - current_close)
#            if (current_avg > avg):
#                if (current_open < current_close):
#                    red_cnt = red_cnt + 1
#                    blue_cnt = 0
#                else:
#                    blue_cnt = blue_cnt + 1
#                    red_cnt = 0
#                logger.info("red_cnt : %d   blue_cnt : %d", red_cnt, blue_cnt)
#                if (blue_cnt > 3):
#                    logger.info("buy_ready -  red_cnt : %d   blue_cnt : %d", red_cnt, blue_cnt)
#                    status = "buy_ready"
#                    red_cnt = 0
#                    blue_cnt = 0
#                    high_cnt = 0
#                    low_cnt = 0
#            else:
#                logger.info("skip")
#        past_volume = current_volume
#        time.sleep(10)
#    elif (status == "buy_ready"):
#        current_high = df['high'].iloc[499]
#        current_low = df['low'].iloc[499]
#        if (current_high > current_high_past):
#            high_cnt = high_cnt + 1
#        else:
#            high_cnt = 0
#            low_cnt = 0
#        if (current_low < current_low_past):
#            low_cnt = low_cnt + 1
#        if (low_cnt == 0) and (high_cnt >= 3):
#            buy_price = pyupbit.get_current_price(f"{ticker}")
#            buy_balance = upbit.get_balance(ticker="KRW")
#            upbit.buy_market_order(f"{ticker}", buy_balance * 0.9994)
#            status = "bought"
#            logger.info("bought - buy_price : %0.6f   buy_balance : %0.6f", buy_price, buy_balance)
#            red_cnt = 0
#            blue_cnt = 0
#            high_cnt = 0
#            low_cnt = 0
#        time.sleep(5)
#        current_high_past = current_high
#        current_low_past = current_low
#    elif (status == "bought"):
#        current_volume = df['volume'].iloc[498]
#        if (current_volume != past_volume):
#            current_open = df['open'].iloc[498]
#            current_close = df['close'].iloc[498]
#            open_list = df['open'][490:499]
#            close_list = df['close'][490:499]
#            dif_list = open_list - close_list
#            abs_list = abs(dif_list)
#            avg = sum(abs_list)/len(abs_list) * 0.2
#            current_avg = abs(current_open - current_close)
#            if (current_avg > avg):
#                if (current_open < current_close):
#                    red_cnt = red_cnt + 1
#                    blue_cnt = 0
#                else:
#                    blue_cnt = blue_cnt + 1
#                    red_cnt = 0
#                logger.info("red_cnt : %d   blue_cnt : %d", red_cnt, blue_cnt)
#                if (red_cnt > 3):
#                    logger.info("sell_ready -  red_cnt : %d   blue_cnt : %d", red_cnt, blue_cnt)
#                    status = "sell_ready"
#                    red_cnt = 0
#                    blue_cnt = 0
#                    high_cnt = 0
#                    low_cnt = 0
#            else:
#                logger.info("skip")
#        past_volume = current_volume
#        time.sleep(10)
#    elif (status == "sell_ready"):
#        current_high = df['high'].iloc[499]
#        current_low = df['low'].iloc[499]
#        if (current_low <= current_low_past):
#            low_cnt = low_cnt + 1
#        else:
#            high_cnt = 0
#            low_cnt = 0
#        if (current_high > current_high_past):
#            high_cnt = high_cnt + 1
#        if (high_cnt == 0) and (low_cnt >= 3):
#            ticker_price = pyupbit.get_current_price(f"{ticker}")
#            ticker_balance = upbit.get_balance(ticker=f"{ticker}")
#            upbit.sell_market_order(f"{ticker}", ticker_balance * 0.9995)
#            time.sleep(5)
#            sell_balance = upbit.get_balance(ticker="KRW")
#            profit = (sell_balance / buy_balance) - 1
#            total_profit = total_profit + profit
#            logger.info("sell -   ticker_price : %0.6f   sell_balance : %0.6f  profit : %0.6f   total_profit : %0.6f", ticker_price, sell_balance, profit, total_profit)
#            status = "standby"
#            red_cnt = 0
#            blue_cnt = 0
#            high_cnt = 0
#            low_cnt = 0
#        time.sleep(5)
#        current_high_past = current_high
#        current_low_past = current_low
#    else:
#        logger.info("Error")
