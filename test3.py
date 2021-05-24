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

   
#tickers = ["KRW-ETC", "KRW-XRP", "KRW-ETH", "KRW-WAVES", "KRW-EOS", "KRW-BTG", "KRW-BCH", "KRW-LTC", "KRW-VET", "KRW-DAWN", "KRW-NEO", "KRW-STPT", "KRW-CHZ", "KRW-OMG", "KRW-QTUM", "KRW-MED"]

ticker = "BTC-NMR"
df = pyupbit.get_ohlcv(f"{ticker}", interval="minute1", count=11)
close_list = df['close'][0:10]
volume_list = df['volume'][0:10]

str = ticker
if (str.startswith('KRW-')):
    print("KRW")
elif (str.startswith('BTC-')):
    print("BTC")
else:
    print("not")
