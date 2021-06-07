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
import datetime as dt


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
tmp = sys.argv[0]
tmp2 = tmp.split('.')
tmp6 = ['./log/', tmp2[0], '.txt']
path = "".join(tmp6)
file_handler = logging.FileHandler(filename=f"{path}")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


#logger.info("aaa : %0.2f", bbb)

access = "ZRRx2FMNNmn8KjefANNB3lQNxHDIzCvvxVpxjwKC"          # 본인 값으로 변경
secret = "9FeUPbYFdfrFHRaE0QJ9nMQ3CGy3u5plVxhdVO6x"          # 본인 값으로 변경
server_url = "https://upbit.com"
upbit = pyupbit.Upbit(access, secret)



init_balance = upbit.get_balance(ticker="KRW")

logger.info("START!!   init balance : %d", init_balance)

ticker_type = "KRW"

#tickers = ['KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-IGNIS', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-ADX', 'KRW-BAT', 'KRW-IOST', 'KRW-DMT', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-EDR', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT']
tickers = ['KRW-CRE', 'KRW-SOLVE', 'KRW-MBL', 'KRW-TSHP', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-PXL', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-LAMB', 'KRW-HUNT', 'KRW-MARO', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-PCI', 'KRW-STRAX', 'KRW-AQT', 'KRW-BCHA', 'KRW-GLM', 'KRW-QTCON', 'KRW-SSX', 'KRW-META', 'KRW-OBSR', 'KRW-FCT2', 'KRW-LBC', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-DAWN', 'KRW-AXS', 'KRW-STX']



old_time = dt.datetime.now()
time.sleep(10)
current_time = dt.datetime.now()

delta_time = current_time - old_time
print(old_time)
print(current_time)
print(delta_time)

diff = str(delta_time)
print(diff)
print(diff[2:4])
diff_int = int(diff[2:4])

print(diff_int)


if (ticker_type == "BTC"):
    tickers = pyupbit.get_tickers(fiat="BTC")

global bought_list
global bought_time_list
global check_list
global sell_list
bought_list = {}
bought_time_list = {}
check_list = {}
sell_order_list = []
sell_list = {}

def check_rate_validity(ticker, avg_list):
    cnt = 0
    total_value = 0
    global avg_value
    global new_value_1
    global new_value_2
    avg_value = 0
    new_value_1 = 0
    new_value_2 = 0
    for value in avg_list:
        if (cnt < 8):
            total_value = total_value + value
            if (cnt == 7):
                avg_value = total_value / 8
        elif (cnt == 8):
            new_value_1 = value
        elif (cnt == 9):
            new_value_2 = value
        else:
            abc = 0
        cnt = cnt + 1
    if (new_value_1/avg_value >= 1.01) and (new_value_2/avg_value >= 1.015) and (new_value_1/avg_value < 1.1) and (new_value_2/avg_value < 1.1):
        #logger.info("avg_value : %0.6f   new_value_1/avg_value : %0.6f    new_value_2/avg_value : %0.6f", avg_value, new_value_1/avg_value, new_value_2/avg_value)
        return "valid"
    elif (new_value_2/avg_value >= 1.02) and (new_value_2/avg_value < 1.1) and (ticker_type == "KRW"):
        #logger.info("avg_value : %0.6f   new_value_1/avg_value : %0.6f    new_value_2/avg_value : %0.6f", avg_value, new_value_1/avg_value, new_value_2/avg_value)
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
        rate = new_value / old_value - 1
        total_rate = total_rate + rate
        logger.info("rate : %0.4f   total_rate : %0.4f", rate, total_rate)
    if (total_rate >= 0.15):
        return "valid"
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
    if (new_volume_1/avg_volume >= 2) and (new_volume_2/avg_volume >= 2.2):
        #logger.info("avg_volume : %d   new_volume_1/avg_volume : %0.3f   new_volume_2/avg_volume : %0.3f", avg_volume, new_volume_1/avg_volume, new_volume_2/avg_volume)
        return "valid"
    elif (new_volume_2/avg_volume >= 5) and (ticker_type == "KRW"):
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


def stop_loss_monitor(ticker, buy_price, loss, delay, cycle, cancle_order):
    global bought_list
    global sell_list
    while_abort_cnt = 0
    ticker_balance = upbit.get_balance(ticker=f"{ticker}")
    while True:
        check_price = pyupbit.get_current_price(f"{ticker}")
        loss_price = buy_price * (1 + loss)
        if (loss_price > check_price):
            logger.info("STOP_LOSS %s - loss_price %0.1f(%0.1f) > check_price %0.8f",ticker, loss_price, buy_price, check_price)
            if (buy_enable == 1):
                if (cancle_order == 1):
                    for order in sell_list[ticker]:
                        try:
                            logger.info("cancel_order")
                            if (buy_enable == 1):
                                upbit.cancel_order(order)
                        except:
                            logger.info("already_cancled")
                        time.sleep(1)
                    time.sleep(1)
                upbit.sell_market_order(f"{ticker}", ticker_balance * 0.995)
                logger.info("sell_market_order %s  ticker_balance : %d", ticker, ticker_balance)
                time.sleep(10)
            try:
                del sell_list[ticker]
            except:
                abc = 0
            try:
                del bought_list[ticker]
            except:
                abc = 0
            return 1
            break
        else:
            time.sleep(delay)
            while_abort_cnt = while_abort_cnt + 1
        if (while_abort_cnt == cycle):
            #logger.info("It's safe in %d delay and %d cycles.", delay, cycle)
            return 0
            break

def buy(ticker):
    global buy_price
    global buy_balance
    buy_price = pyupbit.get_current_price(f"{ticker}")
    buy_balance = upbit.get_balance(ticker="KRW")
    if (buy_enable == 1):
        upbit.buy_market_order(f"{ticker}", buy_balance * 0.5)
        #time.sleep(1800)
        logger.info("BUY - %s   buy_price : %d,   buy_balance : %d", ticker, buy_price, buy_balance)


def sell(ticker):
    logger.info("SELL - %s", ticker)
    sell_order_list = []
    sell_balance_tmp = upbit.get_balance(ticker=f"{ticker}")
    sell_balance = sell_balance_tmp * 0.333
    sell_price_tmp = pyupbit.get_current_price(f"{ticker}")
    sell_price = buy_price * (1 + target_margin*1/3)
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
    sell_price = buy_price * (1 + target_margin*2/3)
    if (str.startswith('KRW-')):
        new_price = cal_unit(sell_price)
    else:
        new_price = sell_price//1
    tmp = upbit.sell_limit_order(f"{ticker}", new_price, sell_balance)
    if 'uuid' in tmp:
        sell_order_list.append(tmp['uuid'])
        logger.info("ticker : %s   sell_limit_order : %d", ticker, new_price)
    time.sleep(1)
    sell_price = buy_price * (1 + target_margin)
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

total_profit = 0

low_price_renewal_past = 0

sell_aggresive_enable = 0
while_cnt = 0




global buy_enable
buy_enable = 0

sim_cycle_cnt = 0
test_cycle_cnt = 0
test_cycle = 200

#PARAMETER
sim_cycle = 30
global target_margin
target_margin = 15




old_time = dt.datetime.now()
time.sleep(10)
current_time = dt.datetime.now()

delta_time = current_time - old_time
print(old_time)
print(current_time)
print(delta_time)

diff = str(delta_time)
print(diff)
print(diff[2:4])
diff_int = int(diff[2:4])

print(diff_int)

def sim_profit():
    sim_total_profit = 0
    sim_avg_profit = 0
    sim_total_ticker_cnt = 0
    sim_plus_cnt = 0
    global bought_time_list
    global buy_enable
    buy_enable = 0
    for ticker in tickers:
        if ticker in check_list:
            sim_total_ticker_cnt = sim_total_ticker_cnt + 1
            ref_price = check_list[ticker]
            bought_time = bought_time_list[ticker]
            current_time = dt.datetime.now()
            delta_time = current_time - bought_time
            diff = str(delta_time)
            valid_candle_cnt = int(diff[2:4])
            #count=31 will be changed.
            df_t = pyupbit.get_ohlcv(f"{ticker}", interval="minute1", count=31)
            if (valid_candle_cnt > 30):
                high_list = df_t['high']
                low_list = df_t['low']
            else:
                start_idx = 30 - valid_candle_cnt
                high_list = df_t['high'][start_idx:30]
                low_list = df_t['low'][start_idx:30]
            avg_list = (high_list + low_list) / 2
            sim_avg = sum(avg_list)/len(avg_list)
            current_profit = sim_avg/ref_price - 1
            sim_total_profit = sim_total_profit + current_profit
            sim_avg_profit = sim_total_profit / sim_total_ticker_cnt
            if (current_profit > 0):
                sim_plus_cnt = sim_plus_cnt + 1
            logger.info("sim result - %s   bought_time : %s  buy_price : %0.1f  avg_price : %0.1f  current_profit : %0.6f   sim_avg_profit : %0.6f   valid_candle_cnt : %d", ticker, bought_time, ref_price, sim_avg, current_profit, sim_avg_profit, valid_candle_cnt)
    if (sim_avg_profit > 1.03):
        buy_enable = 1
        logger.info("buy_enable = 1")
        target_margin = sim_avg_profit
    else:
        buy_enable = 0
        logger.info("buy_enable = 0")
    logger.info("sim_avg_profit : %0.6f   sim_plus_cnt/sim_total_ticker_cnt : %d/%d", sim_avg_profit, sim_plus_cnt, sim_total_ticker_cnt)




while True:
    #logger.info("while")
    if (status == "bought"):
        logger.info("status : %s", status)
        if (buy_enable == 1):
            #upbit.sell_market_order(f"{ticker}", ticker_balance)
            sell_list[ticker] = sell(ticker)
            logger.info("sell_list[ticker] : %s", sell_list[ticker])
            if (str.startswith('KRW-')):
                sell_balance = upbit.get_balance(ticker="KRW")
            elif (str.startswith('BTC-')):
                sell_balance = upbit.get_balance(ticker="KRW-BTC")
            else:
                abc = 0
            profit = sell_balance / buy_balance - 1
            total_profit = total_profit + profit
        status="standby"
        #logger.info("sell_3 : %d      profit : %0.4f     total_profit : %0.4f", sell_balance, profit, total_profit)
        continue
    elif (status == "standby"):
        #logger.info("status : %s", status)
        ticker_found = 0
        for ticker in tickers:
            if ticker in bought_list:
                #logger.info("bought_list has %s", ticker)
                buy_price = bought_list[ticker]
                stop_loss_monitor(ticker, buy_price, -0.02, 10, 2, 1)
            else:
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
                    ticker_found = ticker
                    break
        if (ticker_found != 0):
            ticker = ticker_found
            ticker_price = pyupbit.get_current_price(f"{ticker}")
            logger.info("ticker %s (%0.1f) is found.", ticker, ticker_price)
            logger.info("avg_value : %0.6f   new_value_1/avg_value : %0.6f    new_value_2/avg_value : %0.6f", avg_value, new_value_1/avg_value, new_value_2/avg_value)
            logger.info("avg_volume : %d   new_volume_1/avg_volume : %0.3f   new_volume_2/avg_volume : %0.3f", avg_volume, new_volume_1/avg_volume, new_volume_2/avg_volume)
            rate15_validity = check_rate15_validity(ticker)
            if (rate15_validity == "valid"):
                #logger.info("rate15_validity is valid")
                buy(ticker)
                current_time = dt.datetime.now()
                bought_time_list[ticker] = current_time
                bought_list[ticker] = buy_price
                check_list[ticker] = buy_price
                stop_loss = stop_loss_monitor(ticker, buy_price, -0.02, 10, 60, 0)
                if (stop_loss == 1):
                    status = "standby"
                else:
                    status = "bought"
            else:
                logger.info("rate15_validity is invalid")
    else:
        logger.info("Error1")
    if (sim_cycle_cnt == sim_cycle):
        sim_profit()
        sim_cycle_cnt = 0
        check_list = {}
        bought_time_list = {}
        sell_order_list = []
        sell_list = {}
    else:
        sim_cycle_cnt = sim_cycle_cnt + 1
    if (test_cycle_cnt == test_cycle):
        upbit.buy_market_order("KRW-BTC", 6000)
        test_cycle_cnt = 0
    else:
        test_cycle_cnt = test_cycle_cnt + 1
