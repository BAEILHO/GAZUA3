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

#tickers = []
#f=open('target_list.txt','r')
#for i in f:
##    print(i.strip())
#    tickers.append(i.strip())
#f.close()

tickers = pyupbit.get_tickers(fiat="ALL")

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
    


def check_deadcoin(ticker):
    cnt = 0
    df = pyupbit.get_ohlcv(f"{ticker}", interval="minute1", count=11)
    open_list = df['open'][0:10]
    close_list = df['close'][0:10]
    for open_value, close_value in zip(open_list, close_list):
        if (open_value == close_value):
            cnt = cnt + 1
    if (cnt >= 5):
        return "dead"
    else:
        return "alive"




def check_unit(ticker):
    str = ticker
    if (str.startswith('BTC-')):
        unit = pyupbit.get_current_price(f"{ticker}")
        logger.info("%0.8f", unit)
        if (unit < 0.00000100):
            return "small"
        else:
            return "big"



for ticker in tickers:
    dead_validity = check_deadcoin(ticker)
    unit_validity = check_unit(ticker)
    logger.info("%s : %s   %s", ticker, dead_validity, unit_validity)
