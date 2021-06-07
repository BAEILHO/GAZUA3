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
#file_handler = logging.FileHandler(f"aggresive_{c_time_log}_log.txt")
file_handler = logging.FileHandler(filename='./log/v9_BTC1.txt')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


#logger.info("aaa : %0.2f", bbb)

access = "ZRRx2FMNNmn8KjefANNB3lQNxHDIzCvvxVpxjwKC"          # 본인 값으로 변경
secret = "9FeUPbYFdfrFHRaE0QJ9nMQ3CGy3u5plVxhdVO6x"          # 본인 값으로 변경
server_url = "https://upbit.com"
upbit = pyupbit.Upbit(access, secret)



init_balance = upbit.get_balance(ticker="KRW")

logger.info("START!!   init balance : %d", init_balance)

ticker_type = "BTC"

#tickers = ['KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-IGNIS', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-ADX', 'KRW-BAT', 'KRW-IOST', 'KRW-DMT', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-EDR', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT']
#tickers = ['KRW-CRE', 'KRW-SOLVE', 'KRW-MBL', 'KRW-TSHP', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-PXL', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-LAMB', 'KRW-HUNT', 'KRW-MARO', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-PCI', 'KRW-STRAX', 'KRW-AQT', 'KRW-BCHA', 'KRW-GLM', 'KRW-QTCON', 'KRW-SSX', 'KRW-META', 'KRW-OBSR', 'KRW-FCT2', 'KRW-LBC', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-DAWN', 'KRW-AXS', 'KRW-STX']


tickers = ['BTC-ETH', 'BTC-LTC', 'BTC-XRP', 'BTC-ETC', 'BTC-OMG', 'BTC-CVC', 'BTC-DGB', 'BTC-SC', 'BTC-SNT', 'BTC-WAVES', 'BTC-NMR', 'BTC-XEM', 'BTC-LBC', 'BTC-QTUM', 'BTC-NXT', 'BTC-BAT', 'BTC-LSK', 'BTC-RDD', 'BTC-STEEM', 'BTC-DOGE', 'BTC-BNT', 'BTC-XLM', 'BTC-ARDR', 'BTC-KMD', 'BTC-ARK', 'BTC-ADX', 'BTC-SYS', 'BTC-ANT', 'BTC-STORJ', 'BTC-GRS', 'BTC-REP', 'BTC-RLC', 'BTC-EMC2', 'BTC-ADA', 'BTC-MANA', 'BTC-SBD', 'BTC-RCN', 'BTC-POWR', 'BTC-DNT', 'BTC-IGNIS', 'BTC-ZRX', 'BTC-TRX', 'BTC-TUSD', 'BTC-LRC', 'BTC-DMT', 'BTC-POLY', 'BTC-PRO', 'BTC-BCH', 'BTC-MFT', 'BTC-LOOM', 'BTC-RFR', 'BTC-RVN', 'BTC-BFT', 'BTC-GO', 'BTC-UPP', 'BTC-ENJ', 'BTC-EDR', 'BTC-MTL', 'BTC-PAX', 'BTC-MOC', 'BTC-ZIL', 'BTC-BSV', 'BTC-IOST', 'BTC-NCASH', 'BTC-DENT', 'BTC-ELF', 'BTC-BTT', 'BTC-VITE', 'BTC-IOTX', 'BTC-SOLVE', 'BTC-NKN', 'BTC-META', 'BTC-ANKR', 'BTC-CRO', 'BTC-FSN', 'BTC-ORBS', 'BTC-AERGO', 'BTC-PI']
#tickers = ['BTC-ATOM', 'BTC-STPT', 'BTC-LAMB', 'BTC-EOS', 'BTC-LUNA', 'BTC-DAI', 'BTC-MKR', 'BTC-BORA', 'BTC-TSHP', 'BTC-WAXP', 'BTC-MED', 'BTC-MLK', 'BTC-PXL', 'BTC-VET', 'BTC-CHZ', 'BTC-FX', 'BTC-OGN', 'BTC-ITAM', 'BTC-XTZ', 'BTC-HIVE', 'BTC-HBD', 'BTC-OBSR', 'BTC-DKA', 'BTC-STMX', 'BTC-AHT', 'BTC-PCI', 'BTC-RINGX', 'BTC-LINK', 'BTC-KAVA', 'BTC-JST', 'BTC-CHR', 'BTC-DAD', 'BTC-TON', 'BTC-CTSI', 'BTC-DOT', 'BTC-COMP', 'BTC-SXP', 'BTC-HUNT', 'BTC-ONIT', 'BTC-CRV', 'BTC-ALGO', 'BTC-RSR', 'BTC-OXT', 'BTC-PLA', 'BTC-MARO', 'BTC-SAND', 'BTC-SUN', 'BTC-SRM', 'BTC-QTCON', 'BTC-MVL', 'BTC-GXC', 'BTC-AQT', 'BTC-AXS', 'BTC-STRAX', 'BTC-BCHA', 'BTC-GLM', 'BTC-FCT2', 'BTC-SSX', 'BTC-FIL', 'BTC-UNI', 'BTC-BASIC', 'BTC-INJ', 'BTC-PROM', 'BTC-VAL', 'BTC-PSG', 'BTC-JUV', 'BTC-CBK', 'BTC-FOR', 'BTC-BFC', 'BTC-LINA', 'BTC-HUM', 'BTC-PICA', 'BTC-CELO', 'BTC-IQ', 'BTC-STX', 'BTC-NEAR', 'BTC-AUCTION', 'BTC-DAWN', 'BTC-FLOW', 'BTC-STRK', 'BTC-PUNDIX', 'BTC-GRT', 'BTC-SNX']



bought_list = {}
sell_order_list = []
sell_list = {}

def check_rate_validity(ticker, avg_list):
    cnt = 0
    total_rate = 0
    global avg_rate
    global new_rate_1
    global new_rate_2
    avg_rate = 0
    new_rate_1 = 0
    new_rate_2 = 0
    for rate in avg_list:
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
    if (new_rate_1/avg_rate >= 1.02) and (new_rate_2/avg_rate >= 1.04) and (new_rate_1/avg_rate < 1.1) and (new_rate_2/avg_rate < 1.1):
        #logger.info("avg_rate : %0.6f   new_rate_1/avg_rate : %0.6f    new_rate_2/avg_rate : %0.6f", avg_rate, new_rate_1/avg_rate, new_rate_2/avg_rate)
        return "valid"
    elif (new_rate_2/avg_rate >= 1.05) and (new_rate_2/avg_rate < 1.3) and (ticker_type == "KRW"):
        #logger.info("avg_rate : %0.6f   new_rate_1/avg_rate : %0.6f    new_rate_2/avg_rate : %0.6f", avg_rate, new_rate_1/avg_rate, new_rate_2/avg_rate)
        return "valid"
    else:
        return "invalid"




def check_rate15_validity(ticker):
    cnt = 0
    up_ok = 1
    down_ok = 1
    df = pyupbit.get_ohlcv(f"{ticker}", interval="minute15", count=11)
    old_list = df['close'][0:10]
    new_list = df['close'][1:11]
    total_rate = 0
    list_from_old = old_list.values.tolist()
    list_from_new = new_list.values.tolist()
    for old_value, new_value in zip(list_from_old, list_from_new):
        value = new_value / old_value - 1
        total_rate = total_rate + value
        #logger.info("total_rate : %0.4f", total_rate)
    if (total_rate >= 0.15):
        return "invalid"
    else:
        return "valid"





def check_volume_validity(ticker, volume_list):
    cnt = 0
    total_volume = 0
    global avg_volume
    global new_volume_1
    global new_volume_2
    avg_volume = 0
    new_volume_1 = 0
    new_volume_2 = 0
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
    if (new_volume_1/avg_volume >= 5) and (new_volume_2/avg_volume >= 5):
        #logger.info("avg_volume : %d   new_volume_1/avg_volume : %0.3f   new_volume_2/avg_volume : %0.3f", avg_volume, new_volume_1/avg_volume, new_volume_2/avg_volume)
        return "valid"
    elif (new_volume_2/avg_volume >= 7) and (ticker_type == "KRW"):
        #logger.info("avg_volume : %d   new_volume_1/avg_volume : %0.3f   new_volume_2/avg_volume : %0.3f", avg_volume, new_volume_1/avg_volume, new_volume_2/avg_volume)
        return "valid"
    else:
        return "invalid"
    


def check_deadcoin(ticker, open_list, close_list, high_list):
    cnt = 0
    for open_value, close_value, high_value in zip(open_list, close_list, high_list):
        if (open_value == close_value) and (open_value == high_value):
            cnt = cnt + 1
    if (cnt >= 4):
        return "dead"
    else:
        return "alive"




def check_unit(ticker):
    str = ticker
    if (str.startswith('BTC-')):
        unit = pyupbit.get_current_price(f"{ticker}")
        if (unit < 0.00000100):
            return "small"
        else:
            return "big"





def cal_unit(price):
    if (price < 100):
        unit = 0.1
    elif (price >= 100) and (price < 1000):
        unit = 1
    elif (price >= 1000) and (price < 10000):
        unit = 5
    elif (price >= 10000) and (price < 100000):
        unit = 10
    elif (price >= 100000) and (price < 1000000):
        unit = 50
    elif (price >= 1000000) and (price < 10000000):
        unit = 500
    new_price = price//unit * unit
    return new_price



def sell(ticker):
    logger.info("sell  ticker : %s", ticker)
    sell_order_list = []
    sell_balance_tmp = upbit.get_balance(ticker=f"{ticker}")
    sell_balance = sell_balance_tmp * 0.095
    sell_price_tmp = pyupbit.get_current_price(f"{ticker}")
    sell_price = buy_price * 1.1
    str = ticker
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 1.2
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 1.5
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 2
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 2.5
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 3
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 4
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 5
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 6
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * 7
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    return sell_order_list







status = "standby"

total_benefit = 0

low_price_renewal_past = 0

sell_aggresive_enable = 0
while_cnt = 0




while True:
    logger.info("while")
    if (status == "bought"):
        logger.info("status : %s", status)
        #upbit.sell_market_order(f"{target_ticker}", target_balance)
        sell_list[ticker] = sell(target_ticker)
        logger.info("sell_list[ticker] : %s", sell_list[ticker])
        if (str.startswith('KRW-')):
            sell_balance = upbit.get_balance(ticker="KRW")
        elif (str.startswith('BTC-')):
            sell_balance = upbit.get_balance(ticker="KRW-BTC")
        else:
            abc = 0
        benefit = sell_balance / buy_balance - 1
        total_benefit = total_benefit + benefit
        status="sell_ready"
        #logger.info("sell_3 : %d      benefit : %0.4f     total_benefit : %0.4f", sell_balance, benefit, total_benefit)
        continue
    elif (status == "standby"):
        logger.info("status : %s", status)
        target_ticker = 0
        for ticker in tickers:
            df = pyupbit.get_ohlcv(f"{ticker}", interval="minute1", count=11)
            high_list = df['high'][0:10]
            low_list = df['low'][0:10]
            open_list = df['open'][0:10]
            close_list = df['close'][0:10]
            volume_list = df['volume'][0:10]
            avg_list = (high_list + low_list) / 2
            dead_validity = check_deadcoin(ticker, open_list, close_list, high_list)
            unit_validity = check_unit(ticker)
            if (dead_validity == "dead"):
                #logger.info("%s is dead", ticker)
                continue
            else:
                if (unit_validity == "small"):
                    #logger.info("%s is small", ticker)
                    continue
            rate_validity = check_rate_validity(ticker, avg_list)    
            volume_validity = check_volume_validity(ticker, volume_list)
            time.sleep(0.1)
            #logger.info("ticker : %s   rate_validity : %s  volume_validity : %s", ticker, rate_validity, volume_validity)
            if (rate_validity == "valid") and (volume_validity == "valid"):
                target_ticker = ticker
                break
        if (target_ticker != 0):
            logger.info("target_ticker %s is found.", target_ticker)
            logger.info("avg_rate : %0.6f   new_rate_1/avg_rate : %0.6f    new_rate_2/avg_rate : %0.6f", avg_rate, new_rate_1/avg_rate, new_rate_2/avg_rate)
            logger.info("avg_volume : %d   new_volume_1/avg_volume : %0.3f   new_volume_2/avg_volume : %0.3f", avg_volume, new_volume_1/avg_volume, new_volume_2/avg_volume)
            rate15_validity = check_rate15_validity(target_ticker)
            if (rate15_validity == "valid"):
                logger.info("rate15_validity is valid")
                str = target_ticker
                if (str.startswith('KRW-')):
                    buy_price = pyupbit.get_current_price(f"{target_ticker}")
                    buy_balance = upbit.get_balance(ticker="KRW")
                    upbit.buy_market_order(f"{target_ticker}", buy_balance * 0.7)
                elif (str.startswith('BTC-')):
                    buy_price = pyupbit.get_current_price(f"{target_ticker}")
                    buy_balance = upbit.get_balance(ticker="KRW-BTC")
                    upbit.buy_market_order(f"{target_ticker}", buy_balance * 0.990)
                bought_list[target_ticker] = buy_price
                status="bought"
                logger.info("buy : %d  ticker : %s", buy_balance, target_ticker)
                while_abort_cnt =0
                time.sleep(3)
                target_balance = upbit.get_balance(ticker=f"{target_ticker}")
                while True:
                    check_price = pyupbit.get_current_price(f"{target_ticker}")
                    if (buy_price > check_price):
                        logger.info("buy_price %0.8f > check_price %0.8f", buy_price, check_price)
                        logger.info("stop_loss %s", target_ticker)
                        logger.info("sell_market_order %s  target_balance : %d", target_ticker, target_balance)
                        upbit.sell_market_order(f"{target_ticker}", target_balance * 0.99)
                        status="standby"
                        time.sleep(300)
                        break
                    else:
                        time.sleep(1)
                        while_abort_cnt = while_abort_cnt + 1
                    if (while_abort_cnt == 300):
                        logger.info("It's safe in 5min.")
                        break
            else:
                logger.info("rate15_validity is invalid")
    elif (status == "sell_ready"):
        if ticker in bought_list:
            logger.info("bought_list has %s", ticker)
            ref_price = bought_list[ticker]
            rest_order_cnt = 0
            rest_order_cnt_past = 0
            cycle_cnt = 0
            while True:
                check_price = pyupbit.get_current_price(f"{ticker}")
                if (ref_price > check_price):
                    logger.info("ref_price %0.8f > check_price %0.8f", ref_price, check_price)
                    logger.info("stop_loss %s", ticker)
                    for order in sell_list[ticker]:
                        try:
                            logger.info("cancel_order")
                            upbit.cancel_order(order)
                        except:
                            logger.info("already_cancled")
                        time.sleep(1)
                    del sell_list[ticker]
                    del bought_list[ticker]
                    target_balance = upbit.get_balance(ticker=f"{ticker}")
                    logger.info("sell_market_order %s  target_balance : %d", ticker, target_balance)
                    upbit.sell_market_order(f"{ticker}", target_balance * 0.99)
                    time.sleep(300)
                    status="standby"
                    break
                else:
                    check_order_list = upbit.get_order(ticker)
                    rest_order_cnt = len(check_order_list)
                    if (rest_order_cnt == rest_order_cnt_past):
                        cycle_cnt = cycle_cnt + 1
                    else:
                        cycle_cnt = 0
                    if (cycle_cnt == 30):
                        logger.info("%s is quiet. sell now", ticker)
                        for order in sell_list[ticker]:
                            try:
                                logger.info("cancel_order")
                                upbit.cancel_order(order)
                            except:
                                logger.info("already_cancled")
                            time.sleep(1)
                        time.sleep(10)
                        del sell_list[ticker]
                        del bought_list[ticker]
                        target_balance = upbit.get_balance(ticker=f"{ticker}")
                        logger.info("sell_market_order %s  target_balance : %d", ticker, target_balance)
                        upbit.sell_market_order(f"{ticker}", target_balance * 0.99)
                        status="standby"
                        time.sleep(300)
                        break
                    else:
                        time.sleep(10)
                        rest_order_cnt_past = rest_order_cnt
        else:
            logger.info("Error1")

