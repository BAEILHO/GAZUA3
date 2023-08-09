import requests
# for linux
import os.path
# for windows
#path = 'C:\koreainvestment-autotrade-main\koreainvestment-autotrade-main\trade_status.csv'
#from pathlib import path
import re
import json
import datetime
from datetime import timedelta
import time
import yaml
import pandas as pd
import numpy as np

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('(%(asctime)s) %(levelname)s:%(message)s', datefmt ='%m/%d %I:%M:%S %p')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler('output.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


logger.info('------------------------------- 스크립트 실행 -----------------------------------------')


with open('config.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
APP_KEY = _cfg['APP_KEY']
APP_SECRET = _cfg['APP_SECRET']
ACCESS_TOKEN = ""
CANO = _cfg['CANO']
ACNT_PRDT_CD = _cfg['ACNT_PRDT_CD']
DISCORD_WEBHOOK_URL = _cfg['DISCORD_WEBHOOK_URL']
URL_BASE = _cfg['URL_BASE']

def send_message(msg):
    """디스코드 메세지 전송"""
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    requests.post(DISCORD_WEBHOOK_URL, data=message)
    logger.info('디코 메시지: %s',message)

def get_access_token():
    """토큰 발급"""
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
    "appkey":APP_KEY, 
    "appsecret":APP_SECRET}
    PATH = "oauth2/tokenP"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"]
    return ACCESS_TOKEN
    
def hashkey(datas):
    """암호화"""
    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
    'content-Type' : 'application/json',
    'appKey' : APP_KEY,
    'appSecret' : APP_SECRET,
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]
    return hashkey

def get_current_price(code="005930"):
    """현재가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
            "authorization": f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"FHKST01010100"}
    params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":code,
    }
    res = requests.get(URL, headers=headers, params=params)
    return int(res.json()['output']['stck_prpr'])

def get_ohlcv(code,start,end):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST03010100"}
    params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":code,
    "fid_input_date_1":start,
    "fid_input_date_2":end,
    "fid_period_div_code":"D",
    "fid_org_adj_prc":"1"
    }
    res = requests.get(URL, headers=headers, params=params)
    json_output = res.json()['output2']
    tmp_output = pd.DataFrame(json_output)
    output = pd.DataFrame(columns=['stck_bsop_date','stck_clpr','stck_oprc','stck_hgpr','stck_lwpr','acml_vol'])
    output = tmp_output[['stck_bsop_date','stck_clpr','stck_oprc','stck_hgpr','stck_lwpr','acml_vol']]
    #stck_hgpr = int(res.json()['output'][1]['stck_hgpr']) #전일 고가
    #stck_lwpr = int(res.json()['output'][1]['stck_lwpr']) #전일 저가
    #stck_clpr = int(res.json()['output'][1]['stck_clpr']) #전일 종가
    #target_price = stck_oprc + (stck_hgpr - stck_lwpr) * 0.5
    return output

def get_stock_balance():
    """주식 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8434R",
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }
    res = requests.get(URL, headers=headers, params=params)
    stock_list = res.json()['output1']
    evaluation = res.json()['output2']
    stock_dict = {}
    send_message(f"====주식 보유잔고====")
    for stock in stock_list:
        if int(stock['hldg_qty']) > 0:
            stock_dict[stock['pdno']] = stock['hldg_qty']
            send_message(f"{stock['prdt_name']}({stock['pdno']}): {stock['hldg_qty']}주")
            time.sleep(0.1)
    send_message(f"주식 평가 금액: {evaluation[0]['scts_evlu_amt']}원")
    time.sleep(0.1)
    send_message(f"평가 손익 합계: {evaluation[0]['evlu_pfls_smtl_amt']}원")
    time.sleep(0.1)
    send_message(f"총 평가 금액: {evaluation[0]['tot_evlu_amt']}원")
    time.sleep(0.1)
    send_message(f"=================")
    return stock_dict, evaluation[0]['tot_evlu_amt']

def get_balance():
    """현금 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-psbl-order"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8908R",
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": "005930",
        "ORD_UNPR": "65500",
        "ORD_DVSN": "01",
        "CMA_EVLU_AMT_ICLD_YN": "Y",
        "OVRS_ICLD_YN": "Y"
    }
    res = requests.get(URL, headers=headers, params=params)
    cash = res.json()['output']['ord_psbl_cash']
    send_message(f"주문 가능 현금 잔고: {cash}원")
    return int(cash)

def buy(code="005930", qty="1", buy_price="1"):
    """주식 지정가 매수"""  
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        "ORD_DVSN": "00",
        "ORD_QTY": str(int(qty)),
        "ORD_UNPR": str(int(buy_price)),
    }
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0802U",
        "custtype":"P",
        "hashkey" : hashkey(data)
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0':
        send_message(f"[지정가 매수 주문 성공]{str(res.json())}")
        return True
    else:
        send_message(f"[지정가 매수 주문 실패]{str(res.json())}")
        return False

def buy_market(code="005930", qty="1"):
    """주식 시장가 매수"""  
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": str(int(qty)),
        "ORD_UNPR": "0",
    }
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0802U",
        "custtype":"P",
        "hashkey" : hashkey(data)
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0':
        send_message(f"[매수 성공]{str(res.json())}")
        return True
    else:
        send_message(f"[매수 실패]{str(res.json())}")
        return False

def sell(code="005930", qty="1"):
    """주식 시장가 매도"""
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": qty,
        "ORD_UNPR": "0",
    }
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0801U",
        "custtype":"P",
        "hashkey" : hashkey(data)
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0':
        send_message(f"[매도 성공]{str(res.json())}")
        return True
    else:
        send_message(f"[매도 실패]{str(res.json())}")
        return False

def check_betting_seed(code,start,end):
    """총체결금액 조회"""  
    PATH = "uapi/domestic-stock/v1/trading/inquire-daily-ccld"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8001R",
        "custtype":"P"
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "INQR_STRT_DT":start,
        "INQR_END_DT":end,
        "SLL_BUY_DVSN_CD": "02",
        "INQR_DVSN": "01",
        "PDNO": code,
        "CCLD_DVSN": "00",
        "ORD_GNO_BRNO": "",
        "ODNO": "",
        "INQR_DVSN_3": "00",
        "INQR_DVSN_1": "",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
        "CMA_EVLU_AMT_ICLD_YN": "Y",
        "OVRS_ICLD_YN": "Y"
    }
    res = requests.get(URL, headers=headers, params=params)
    betting_seed = res.json()['output2']['tot_ccld_amt']
    send_message(f"총체결금액 조회: {code} : {betting_seed}")
    return int(betting_seed)

def check_avg_price(code,start,end):
    """체결평균가 조회"""  
    PATH = "uapi/domestic-stock/v1/trading/inquire-daily-ccld"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8001R",
        "custtype":"P"
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "INQR_STRT_DT":start,
        "INQR_END_DT":end,
        "SLL_BUY_DVSN_CD": "02",
        "INQR_DVSN": "01",
        "PDNO": code,
        "CCLD_DVSN": "00",
        "ORD_GNO_BRNO": "",
        "ODNO": "",
        "INQR_DVSN_3": "00",
        "INQR_DVSN_1": "",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
        "CMA_EVLU_AMT_ICLD_YN": "Y",
        "OVRS_ICLD_YN": "Y"
    }
    res = requests.get(URL, headers=headers, params=params)
    avg_prvs = res.json()['output2']['avg_prvs']
    send_message(f"체결평균가 조회: {code} : {avg_prvs}")
    return int(avg_prvs)

def check_sell_order(code,start,end):
    """주식 선발 주문 조회"""  
    PATH = "uapi/domestic-stock/v1/trading/inquire-daily-ccld"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8001R",
        "custtype":"P"
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "INQR_STRT_DT":start,
        "INQR_END_DT":end,
        "SLL_BUY_DVSN_CD": "01",
        "INQR_DVSN": "01",
        "PDNO": code,
        "CCLD_DVSN": "00",
        "ORD_GNO_BRNO": "",
        "ODNO": "",
        "INQR_DVSN_3": "00",
        "INQR_DVSN_1": "",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
        "CMA_EVLU_AMT_ICLD_YN": "Y",
        "OVRS_ICLD_YN": "Y"
    }
    res = requests.get(URL, headers=headers, params=params)
    out1 = res.json()['output1']['tot_ccld_qty']
    out2 = res.json()['output1']['avg_prvs']
    out3 = res.json()['output2']['tot_ccld_amt']
    out4 = res.json()['output2']['prsm_tlex_smtl']
    send_message(f"매도 주문 체결 조회: {code} : 총체결수량: {out1} 체결평균가: {out2} 총체결금액: {out3} 수수료: {out4}")
    return int(out1), int(out2), int(out3), int(out4)

def check_order(code,start,end):
    """주식 선발 주문 조회"""  
    PATH = "uapi/domestic-stock/v1/trading/inquire-daily-ccld"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8001R",
        "custtype":"P"
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "INQR_STRT_DT":start,
        "INQR_END_DT":end,
        "SLL_BUY_DVSN_CD": "02",
        "INQR_DVSN": "01",
        "PDNO": code,
        "CCLD_DVSN": "00",
        "ORD_GNO_BRNO": "",
        "ODNO": "",
        "INQR_DVSN_3": "00",
        "INQR_DVSN_1": "",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
        "CMA_EVLU_AMT_ICLD_YN": "Y",
        "OVRS_ICLD_YN": "Y"
    }
    res = requests.get(URL, headers=headers, params=params)
    order_completed = res.json()['output2']['tot_ccld_qty']
    send_message(f"선발 주문 체결 조회: {code} : {order_completed}")
    return int(order_completed)

def cov_chk(num):
    tmp_data1 = ohlcv['MA20'].loc[(num-10):(num-2)].mean()
    tmp_data2 = ohlcv['MA60'].loc[(num-10):(num-2)].mean()
    tmp_data3 = ohlcv['MA120'].loc[(num-10):(num-2)].mean()
    tmp_data4 = max(tmp_data1,tmp_data2,tmp_data3)
    tmp_data5 = min(tmp_data1,tmp_data2,tmp_data3)
    if ((tmp_data4 != 0) and (tmp_data4 != "NaN") and (tmp_data5 != 0) and (tmp_data5 != "NaN")):
        tmp_data = tmp_data4 / tmp_data5
    else:
        tmp_data = 100
    return tmp_data

def ma20_down_chk(num):
    tmp_cnt = 0
    tmp_data1 = ohlcv['MA20'].loc[(num-60)]
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN")):
        for t in range((num-55),(num-5),5):
            tmp_data2 = ohlcv['MA20'].loc[t]
            tmp_data3 = tmp_data2 / tmp_data1
            if (tmp_data3 >= 1.05):
                tmp_cnt = tmp_cnt + 1
            tmp_data1 = tmp_data2
    return tmp_cnt

def ma60_down_chk(num):
    tmp_cnt = 0
    tmp_data1 = ohlcv['MA60'].loc[(num-60)]
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN")):
        for t in range((num-55),(num-5),5):
            tmp_data2 = ohlcv['MA60'].loc[t]
            tmp_data3 = tmp_data2 / tmp_data1
            if (tmp_data3 >= 1.03):
                tmp_cnt = tmp_cnt + 1
            tmp_data1 = tmp_data2
    return tmp_cnt

def ma120_down_chk(num):
    tmp_cnt = 0
    tmp_data1 = ohlcv['MA120'].loc[(num-60)]
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN")):
        for t in range((num-55),(num-5),5):
            tmp_data2 = ohlcv['MA120'].loc[t]
            tmp_data3 = tmp_data2 / tmp_data1
            if (tmp_data3 >= 1):
                tmp_cnt = tmp_cnt + 1
            tmp_data1 = tmp_data2
    return tmp_cnt

def rising_candle_chk(num):
    tmp_data1 = ohlcv['stck_oprc'].loc[(num)]
    tmp_data2 = ohlcv['stck_clpr'].loc[(num)]
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN")):
        tmp_data3 = tmp_data2 / tmp_data1
    else:
        tmp_data3 = 100
    return tmp_data3

def past_rising_chk(num):
    tmp_data1 = ohlcv['stck_oprc'].loc[(num-2)]
    tmp_data2 = ohlcv['stck_clpr'].loc[(num-1)]
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN") and (tmp_data2 != 0) and (tmp_data2 != "NaN")):
        tmp_data3 = (tmp_data2 - tmp_data1) / tmp_data1
    else:
        tmp_data3 = 100
    return tmp_data3

def volume_chk(num):
    tmp_data1 = ohlcv['acml_vol'].loc[(num-10):(num-1)].mean()
    tmp_data2 = ohlcv['acml_vol'].loc[(num)]
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN") and (tmp_data2 != 0) and (tmp_data2 != "NaN")):
        tmp_data3 = tmp_data2 / tmp_data1
    else:
        tmp_data3 = 0
    return tmp_data3

def volume_chk2(num):
    tmp_data1 = ohlcv['acml_vol'].loc[num]
    tmp_cnt = 0
    if (num <= 60):
        for i in range(0,(num-5)):
            tmp_data2 = ohlcv['acml_vol'].loc[i]
            if ((tmp_data1 != 0) and (tmp_data1 != "NaN") and (tmp_data2 != 0) and (tmp_data2 != "NaN")):
                if (tmp_data1 < (tmp_data2 * 1.5)):
                    tmp_cnt = tmp_cnt + 1
            else:
                tmp_cnt = 100
    else:
        for i in range((num-120),(num-5)):
            tmp_data2 = ohlcv['acml_vol'].loc[i]
            if ((tmp_data1 != 0) and (tmp_data1 != "NaN") and (tmp_data2 != 0) and (tmp_data2 != "NaN")):
                if (tmp_data1 < (tmp_data2 * 1.5)):
                    tmp_cnt = tmp_cnt + 1
            else:
                tmp_cnt = 100
    return tmp_cnt

def boundary_level300_chk(num):
    if ((num >= 299)):
        tmp_data1 = ohlcv['stck_hgpr'].loc[(num-299):(num-20)].max()
        tmp_data2 = ohlcv['stck_lwpr'].loc[(num-299):(num-20)].min()
        tmp_data3 = ohlcv['stck_clpr'].loc[(num-20):(num-5)].mean()
    else:
        tmp_data1 = ohlcv['stck_hgpr'].loc[0:(num-20)].max()
        tmp_data2 = ohlcv['stck_lwpr'].loc[0:(num-20)].min()
        tmp_data3 = ohlcv['stck_clpr'].loc[(num-20):(num-5)].mean()
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN") and (tmp_data2 != 0) and (tmp_data2 != "NaN") and (tmp_data3 != 0) and (tmp_data3 != "NaN")):
        boundary_level300 = (tmp_data3 - tmp_data2) / (tmp_data1 - tmp_data2)
    else:
        boundary_level300 = 100
    return boundary_level300

def boundary_level500_chk(num):
    if ((num >= 499)):
        tmp_data1 = ohlcv['stck_hgpr'].loc[(num-499):(num-20)].max()
        tmp_data2 = ohlcv['stck_lwpr'].loc[(num-499):(num-20)].min()
        tmp_data3 = ohlcv['stck_clpr'].loc[(num-20):(num-5)].mean()
    else:
        tmp_data1 = ohlcv['stck_hgpr'].loc[0:(num-20)].max()
        tmp_data2 = ohlcv['stck_lwpr'].loc[0:(num-20)].min()
        tmp_data3 = ohlcv['stck_clpr'].loc[(num-20):(num-5)].mean()
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN") and (tmp_data2 != 0) and (tmp_data2 != "NaN") and (tmp_data3 != 0) and (tmp_data3 != "NaN")):
        boundary_level500 = (tmp_data3 - tmp_data2) / (tmp_data1 - tmp_data2)
    else:
        boundary_level500 = 100
    return boundary_level500

def boundary_level700_chk(num):
    if ((num >= 699)):
        tmp_data1 = ohlcv['stck_hgpr'].loc[(num-699):(num-20)].max()
        tmp_data2 = ohlcv['stck_lwpr'].loc[(num-699):(num-20)].min()
        tmp_data3 = ohlcv['stck_clpr'].loc[(num-20):(num-5)].mean()
    else:
        tmp_data1 = ohlcv['stck_hgpr'].loc[0:(num-20)].max()
        tmp_data2 = ohlcv['stck_lwpr'].loc[0:(num-20)].min()
        tmp_data3 = ohlcv['stck_clpr'].loc[(num-20):(num-5)].mean()
    if ((tmp_data1 != 0) and (tmp_data1 != "NaN") and (tmp_data2 != 0) and (tmp_data2 != "NaN") and (tmp_data3 != 0) and (tmp_data3 != "NaN")):
        boundary_level700 = (tmp_data3 - tmp_data2) / (tmp_data1 - tmp_data2)
    else:
        boundary_level700 = 100
    return boundary_level700



def cal_unit(price):
    if (price < 2000):
        unit = 1
    elif (price >= 2000) and (price < 5000):
        unit = 5
    elif (price >= 5000) and (price < 20000):
        unit = 10
    elif (price >= 20000) and (price < 50000):
        unit = 50
    elif (price >= 50000) and (price < 200000):
        unit = 100
    elif (price >= 200000) and (price < 500000):
        unit = 500
    else:
        unit = 1000
    new_price = price//unit * unit
    return new_price

def cal_unit_qty(price,seed):
    if (price < 2000):
        unit = 1
    elif (price >= 2000) and (price < 5000):
        unit = 5
    elif (price >= 5000) and (price < 20000):
        unit = 10
    elif (price >= 20000) and (price < 50000):
        unit = 50
    elif (price >= 50000) and (price < 200000):
        unit = 100
    elif (price >= 200000) and (price < 500000):
        unit = 500
    else:
        unit = 1000
    new_price = price//unit * unit
    qty = seed//new_price
    return qty


def sell_cond_chk(num):
    big_volume_cnt = 0
    acc_volume_ok = 0
    len_volume_list = len(volume_list)
    for f in range(1,len_volume_list):
        if (volume_list[f] >= (first_volume * 0.8)):
            big_volume_cnt = big_volume_cnt + 1
    acc_volume = sum(volume_list[1:num])
    if (acc_volume >= (first_volume * 5)):
        acc_volume_ok = 1
    if ((acc_volume_ok == 1) and (big_volume_cnt >= 2)):
        return 1
    else:
        return 0




#for only linux
#path = '/user/sermlserlkm.txt'
#file = '/serseres.txt'
#if os.path.isfile(file)
#if os.path.exists(file)




# 자동매매 시작


try:
    ACCESS_TOKEN = get_access_token()
    stocks = pd.read_csv('kosdaq_code.csv', encoding='CP949')
    unique_code = stocks['code'].unique()
    len_unique_code = len(unique_code)
    logger.info('ticker: %s',len_unique_code)
    pd.set_option('mode.chained_assignment', None)
    market_opened = 0
    search_time = 0
    search_completed = 0
    first_order_completed = 0
    send_message("===국내 주식 자동매매 프로그램을 시작합니다===")
    while True:
        t_now = datetime.datetime.now()
        t_start = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
        t_2_30 = t_now.replace(hour=2, minute=30, second=0, microsecond=0)
        t_3 = t_now.replace(hour=15, minute=0, second=0, microsecond=0)
        t_end = t_now.replace(hour=15, minute=20, second=0,microsecond=0)
        today = datetime.datetime.today().weekday()
        if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
            send_message("주말이므로 프로그램을 종료합니다.")
            break
        # 공휴일 추가할것
        if t_start < t_now < t_end : # 잔여 수량 매도
            market_opened = 1
        else:
            market_opened = 0
        if t_2_30 < t_now < t_3 : # 
            search_time = 1
        else:
            search_time = 0
        #for only windows
        trade_status_file = 'C:\\koreainvestment-autotrade-main\\koreainvestment-autotrade-main\\trade_status.csv'
        if (os.path.isfile(trade_status_file)):
            logger.info('trade_status.csv is exist. It will be used.')
            trade_status = pd.read_csv('trade_status.csv', encoding='CP949', index_col=0)
        else:
            logger.info('trade_status.csv is not exist. It will be created.')
            trade_status = pd.DataFrame(columns=['code','name','first_buy_price','first_order','first_order_completed','first_date','first_volume','last_order','last_price','betting_seed','last_date','waiting_period','sell_completed','sell','stop_loss','auto_sell','auto_loss','sell_price','stop_loss_price','sell_date','profit','income','balance','total_balance','order_cnt','max_order','over_cnt'])
            trade_status.to_csv('trade_status.csv', encoding='CP949', mode='w')
        total_cash = get_balance() # 보유 현금 조회
        logger.info('total_cash: %s',total_cash)
        stock_dict, total_seed = get_stock_balance() # 보유 주식 조회
        logger.info('total_seed : %s',total_seed)
        betting_seed = int(total_seed) / 15
        new_order = 0
        past_trade_status = trade_status.copy()
        past_code_list = past_trade_status['code'].to_list()
        # 1. CODE SEARCH
        if ((search_time == 1) and (search_completed == 0)):
            for code in unique_code:
                #pattern check
                code_name = stocks['name'][stocks['code'].isin([code])].iloc[0]
                full_code = str(code).zfill(6)
                logger.info('code: %s code_name: %s',code,code_name)
                today_time = datetime.datetime.now()
                dateformat = "%Y%m%d"
                today_date = today_time.strftime(dateformat)
                past_time = today_time - timedelta(days=15)
                past_date = past_time.strftime(dateformat)
                #start=20200305
                #end = 20200501
                try:
                    ohlcv_10days = get_ohlcv(full_code,past_date,today_date)
                    #ohlcv_10days = get_ohlcv(code,past_date,today_date)
                    #ohlcv_10days['acml_vol'] = pd.to_numeric(ohlcv_10days['acml_vol'].str.replace(pat=r'[^\w]', repl=r"", regex=True)
                    ohlcv_10days['acml_vol'] = pd.to_numeric(ohlcv_10days['acml_vol'])
                    chk_list = ohlcv_10days['acml_vol'].to_list()
                    buy_price = 0
                    stop_loss_price = 0
                    zero_volume = 0
                    if zero_volume not in chk_list:
                        ohlcv_err = 0
                        today_volume = ohlcv_10days['acml_vol'].loc[0]
                        avg_volume = ohlcv_10days['acml_vol'].loc[3:9].mean()
                        #print(chk_list)
                        #if (int(today_volume) >= int(avg_volume * 10)):
                        today_volume_chk = today_volume / avg_volume
                        #print(today_volume)
                        #print(avg_volume)
                        if (today_volume_chk >= 10):
                            #logger.info('today_volume more than 10 rate.')
                            #make 700 candle
                            ohlcv_shortage = 0
                            ohlcv_full = pd.DataFrame(columns=['stck_bsop_date','stck_clpr','stck_oprc','stck_hgpr','stck_lwpr','acml_vol'])
                            ohlcv = pd.DataFrame(columns=['stck_bsop_date','stck_clpr','stck_oprc','stck_hgpr','stck_lwpr','acml_vol'])
                            cnt = 0
                            valid_300days = 0
                            valid_500days = 0
                            valid_700days = 0
                            len_ohlcv = 0
                            len_ohlcv_tmp = 0
                            last_date = today_date
                            last_time = datetime.datetime.strptime(str(last_date),dateformat)
                            past_time = last_time - timedelta(days=170)
                            past_date = past_time.strftime(dateformat)
                            for k in range(0,9):
                                try:
                                    #print("past_date:",past_date,"last_date:",last_date)
                                    ohlcv_tmp = get_ohlcv(full_code,past_date,last_date)
                                    len_ohlcv_tmp = len(ohlcv_tmp.axes[0])
                                    #print("len_ohlcv_tmp:",len_ohlcv_tmp)
                                    date_chk_df = ohlcv_tmp['stck_bsop_date']
                                    if ((len_ohlcv_tmp == 100) and ((date_chk_df.isnull().values.any()) == False)):
                                        ohlcv_full = pd.concat([ohlcv_full,ohlcv_tmp])
                                        last_date_tmp = re.sub(r"\[|\]","",str(pd.to_numeric(date_chk_df.tail(n=1).values)))
                                        #print("last_date_tail:",last_date_tmp)
                                        last_time_tmp = datetime.datetime.strptime(str(last_date_tmp),dateformat)
                                        last_time = last_time_tmp - timedelta(days=1)
                                        last_date = last_time.strftime(dateformat)
                                        past_time = last_time - timedelta(days=170)
                                        past_date = past_time.strftime(dateformat)
                                        total_len_ohlcv = len(ohlcv_full.axes[0])
                                        if (total_len_ohlcv >= 300):
                                            valid_300days = 1
                                            #logger.info('300 days candle competed.')
                                        if (total_len_ohlcv >= 500):
                                            valid_500days = 1
                                            #logger.info('500 days candle competed.')
                                        if (total_len_ohlcv >= 700):
                                            valid_700days = 1
                                            #logger.info('700 days candle competed.')
                                    else:
                                        if (total_len_ohlcv <= 300):
                                            ohlcv_shortage = 1
                                        break
                                except Exception as e:
                                    #send_message(f"[일봉 생성 오류 발생]{e}")
                                    ohlcv_err = 1
                                    time.sleep(1)
                                    break
                            if ((valid_300days == 0) and (valid_500days == 0) and (valid_700days == 0)):
                                logger.info('Can\'t find any 300,500,700 daily canldes. skip this ticker.')
                                continue
                            else:
                                #print("more than 700")
                                ohlcv_full.reset_index(drop=True, inplace=True)
                                ohlcv_full.dropna()
                                ohlcv_full = ohlcv_full.loc[::-1]
                                ohlcv_full['MA120'] = ohlcv_full['stck_clpr'].rolling(120).mean()
                                ohlcv_full['MA60'] = ohlcv_full['stck_clpr'].rolling(60).mean()
                                ohlcv_full['MA20'] = ohlcv_full['stck_clpr'].rolling(20).mean()
                                ohlcv_full['MA5'] = ohlcv_full['stck_clpr'].rolling(5).mean()
                                ohlcv_full = ohlcv_full.loc[::-1]
                                if (valid_700days == 1):
                                    ohlcv = ohlcv_full.head(700)
                                    #len_ohlcv = 699
                                elif (valid_500days == 1):
                                    ohlcv = ohlcv_full.head(500)
                                    #len_ohlcv = 499
                                elif (valid_300days == 1):
                                    ohlcv = ohlcv_full.head(300)
                                    #len_ohlcv = 299
                                len_ohlcv = len(ohlcv.axes[0])
                                #print(len_ohlcv)
                                ohlcv = ohlcv.loc[::-1]
                                ohlcv.reset_index(drop=True, inplace=True)
                                ohlcv['stck_bsop_date'] = pd.to_numeric(ohlcv['stck_bsop_date'])
                                ohlcv['stck_clpr'] = pd.to_numeric(ohlcv['stck_clpr'])
                                ohlcv['stck_oprc'] = pd.to_numeric(ohlcv['stck_oprc'])
                                ohlcv['stck_hgpr'] = pd.to_numeric(ohlcv['stck_hgpr'])
                                ohlcv['stck_lwpr'] = pd.to_numeric(ohlcv['stck_lwpr'])
                                ohlcv['acml_vol'] = pd.to_numeric(ohlcv['acml_vol'])
                                ohlcv['MA120'] = pd.to_numeric(ohlcv['MA120'])
                                ohlcv['MA60'] = pd.to_numeric(ohlcv['MA60'])
                                ohlcv['MA20'] = pd.to_numeric(ohlcv['MA20'])
                                ohlcv['MA5'] = pd.to_numeric(ohlcv['MA5'])
                                #print("ohlcv")
                                #cond1 chk
                                cov = cov_chk(len_ohlcv - 1)
                                ma20_down = ma20_down_chk(len_ohlcv - 1)
                                ma60_down = ma60_down_chk(len_ohlcv - 1)
                                ma120_down = ma120_down_chk(len_ohlcv - 1)
                                rising_candle = rising_candle_chk(len_ohlcv - 1)
                                past_rising = past_rising_chk(len_ohlcv - 1)
                                volume_rate = volume_chk(len_ohlcv - 1)
                                volume_rate2 = volume_chk2(len_ohlcv - 1)
                                boundary_level300 = boundary_level300_chk(len_ohlcv - 1)
                                boundary_level500 = boundary_level500_chk(len_ohlcv - 1)
                                boundary_level700 = boundary_level700_chk(len_ohlcv - 1)
                                if (valid_700days == 1):
                                    if (((cov <= 1.05) or ((ma20_down == 0) and (ma60_down == 0) and (ma120_down == 0))) and (past_rising <= 1.15) and (rising_candle <= 1.2) and (rising_candle >= 1.05) and (volume_rate >= 20) and (volume_rate2 == 0) and ((boundary_level300 <= 0.2) or (boundary_level500 <= 0.25) or (boundary_level700 <= 0.3))):
                                        logger.info('cov: %s ma20_down: %s ma60_down: %s ma120_down: %s rising_candle: %s volume_rate: %s volume_rate2: %s boundary_level300: %s boundary_level500: %s boundary_level700: %s',cov,ma20_down,ma60_down,ma120_down,rising_candle,volume_rate,volume_rate2,boundary_level300,boundary_level500,boundary_level700)
                                        logger.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!match!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:%s %s',code,code_name)
                                        new_order = 1
                                elif (valid_500days == 1):
                                    if (((cov <= 1.05) or ((ma20_down == 0) and (ma60_down == 0) and (ma120_down == 0))) and (past_rising <= 1.15) and (rising_candle <= 1.2) and (rising_candle >= 1.05) and (volume_rate >= 20) and (volume_rate2 == 0) and ((boundary_level300 <= 0.2) or (boundary_level500 <= 0.25))):
                                        logger.info('cov: %s ma20_down: %s ma60_down: %s ma120_down: %s rising_candle: %s volume_rate: %s volume_rate2: %s boundary_level300: %s boundary_level500: %s boundary_level700: %s',cov,ma20_down,ma60_down,ma120_down,rising_candle,volume_rate,volume_rate2,boundary_level300,boundary_level500,boundary_level700)
                                        logger.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!match!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:%s %s',code,code_name)
                                        new_order = 1
                                elif (valid_300days == 1):
                                    if (((cov <= 1.05) or ((ma20_down == 0) and (ma60_down == 0) and (ma120_down == 0))) and (past_rising <= 1.15) and (rising_candle <= 1.2) and (rising_candle >= 1.05) and (volume_rate >= 20) and (volume_rate2 == 0) and (boundary_level300 <= 0.2)):
                                        logger.info('cov: %s ma20_down: %s ma60_down: %s ma120_down: %s rising_candle: %s volume_rate: %s volume_rate2: %s boundary_level300: %s boundary_level500: %s boundary_level700: %s',cov,ma20_down,ma60_down,ma120_down,rising_candle,volume_rate,volume_rate2,boundary_level300,boundary_level500,boundary_level700)
                                        logger.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!match!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:%s %s',code,code_name)
                                        new_order = 1
                                if (new_order == 1):
                                    close = ohlcv['stck_clpr'].loc[(len_ohlcv - 1)]
                                    open = ohlcv['stck_oprc'].loc[(len_ohlcv - 1)]
                                    volume = ohlcv['acml_vol'].loc[(len_ohlcv - 1)]
                                    if ((((close - open) / open) > 1.05) and (((close - open) / open) <= 1.10)):
                                        buy_price = close
                                    elif ((((close - open) / open) > 1.10) and (((close - open) / open) <= 1.15)):
                                        buy_price = open + ((close - open) * 0.8) 
                                    elif ((((close - open) / open) > 1.15) and (((close - open) / open) <= 1.2)):
                                        buy_price = open + ((close - open) * 0.6) 
                                    else:
                                        buy_price = open + ((close - open) * 0.6) 
                                    stop_loss_price = ohlcv['stck_oprc'].loc[(len_ohlcv-20):(len_ohlcv-2)].min()
                                    len_trade_status = len(trade_status.axes[0])
                                    #print(len_trade_status)
                                    #code_idx = stocks['company'][stocks['code'].isin([i])].iloc[0]
                                    if (trade_status['code'] == code).any():
                                        #code_idx = trade_status['code'].isin([code]).index()
                                        print("code_exist")
                                    else:
                                        print("code not exist")
                                        buy_price = cal_unit(buy_price)
                                        trade_status.loc[(len_trade_status + 1), 'code'] = code
                                        trade_status.loc[(len_trade_status + 1), 'name'] = code_name
                                        trade_status.loc[(len_trade_status + 1), 'first_buy_price'] = buy_price
                                        trade_status.loc[(len_trade_status + 1), 'first_date'] = today_date
                                        trade_status.loc[(len_trade_status + 1), 'first_order'] = 0
                                        trade_status.loc[(len_trade_status + 1), 'first_order_completed'] = 0
                                        trade_status.loc[(len_trade_status + 1), 'first_volume'] = volume
                                        trade_status.to_csv('trade_status.csv', encoding='CP949', mode='w')
                        time.sleep(1)
                except Exception as e:
                    send_message(f"[종목 Search 중 오류 발생]{e}")
                    logger.info('Can\'t find %s. skip this ticker.', code)
                    time.sleep(1)
                    continue
            search_completed = 1
        # 2. CHECK NEW ORDER 
        #if (trade_status.equals(past_trade_status) == False):
        if ((new_order == 1) and (first_order_completed == 0)):
            trade_status = pd.read_csv('trade_status.csv', encoding='CP949', index_col=0)
            past_code_list = past_trade_status['code'].to_list()
            code_list = trade_status['code'].to_list()
            if (past_code_list != code_list):
                print("trade status is updated.")
                print(past_code_list)
                print(code_list)
                new_code_list = list(set(code_list) - set(past_code_list))
                len_new_code_list = len(new_code_list)
                if (len_new_code_list >= 1):
                    print(new_code_list)
                    for f_code in new_code_list:
                        first_buy_price = int(trade_status['first_buy_price'][trade_status['code'].isin([f_code])].iloc[0])
                        code_idx_list = trade_status['code'][trade_status['code'].isin([f_code])].index.to_list()
                        len_code_idx_list = len(code_idx_list)
                        if (len_code_idx_list == 1):
                            code_idx = code_idx_list[0]
                            full_code = str(f_code).zfill(6)
                            print(first_buy_price)
                            try:
                                buy(full_code,1,first_buy_price)
                                trade_status[code_idx, 'first_order'] = 1
                                trade_status[code_idx, 'first_date'] = today_date
                                trade_status.to_csv('trade_status.csv', encoding='CP949', mode='w')
                            except Exception as e:
                                send_message(f"[선발 매수 주문 실패]{e}")
                                logger.info('Can\'t find %s. skip this ticker.', code)
                                time.sleep(1)
                                continue
                        else:
                            send_message(f"[code 1개 이상 발견.]{e}")
                            logger.info('code was found more then 1. %s. skip this ticker.', code)
                first_order_completed = 1
        # 3. CHECK FIRST ORDER COMPLETE
        target_list = trade_status['code'][trade_status['first_order_completed'].isin([0])].to_list()
        len_target_list = len(target_list)
        if (len_target_list >= 1):
            for t_code in target_list:
                full_code = str(t_code).zfill(6)
                past_time = today_time - timedelta(days=20)
                past_date = past_time.strftime(dateformat)
                first_buy_price = int(trade_status['first_buy_price'][trade_status['code'].isin([t_code])].iloc[0])
                try:
                    complete_qty = check_order(full_code,past_date,today_date)
                    print(complete_qty)
                    if (complete_qty == 1):
                        logger.info('선발 매수 체결 확인', full_code)
                        code_idx_list = trade_status['code'][trade_status['code'].isin([t_code])].index.to_list()
                        len_code_idx_list = len(code_idx_list)
                        if (len_code_idx_list == 1):
                            code_idx = code_idx_list[0]
                            try:
                                buy_qty = cal_unit_qty(first_buy_price,betting_seed)
                                buy_market(full_code,buy_qty)
                                time.sleep(10)
                                avg_prvs = check_avg_price(full_code,past_date,today_date)
                                time.sleep(10)
                                betting_seed = check_betting_seed(full_code,past_date,today_date)
                                trade_status[code_idx, 'last_order'] = 1
                                trade_status[code_idx, 'last_price'] = avg_prvs
                                trade_status[code_idx, 'betting_seed'] = betting_seed
                                trade_status[code_idx, 'last_date'] = today_date
                                trade_status[code_idx, 'order_cnt'] = 1
                                trade_status.to_csv('trade_status.csv', encoding='CP949', mode='w')
                                send_message(f"[후발 매수 주문 완료]{e}")
                                logger.info('Can\'t find %s. skip this ticker.', code)
                                time.sleep(1)
                            except Exception as e:
                                send_message(f"[후발 매수 주문 실패]{e}")
                                logger.info('Can\'t find %s. skip this ticker.', code)
                                time.sleep(1)
                                continue
                        else:
                            send_message(f"[code 1개 이상 발견.]{e}")
                            logger.info('code was found more then 1. %s. skip this ticker.', code)
                except Exception as e:
                    send_message(f"[check_order 내 error 발견]{e}")
                    logger.info('There is an error in \'check_order\' process. skip this ticker.', code)
                    time.sleep(1)
                    continue
        # 4. CHECK SELL CONDITION
        sell_chk = 0
        target_list = trade_status['code'][trade_status['last_order'].isin([1])].to_list()
        len_target_list = len(target_list)
        if (len_target_list >= 1):
            for t_code in target_list:
                full_code = str(t_code).zfill(6)
                today_time = datetime.datetime.now()
                dateformat = "%Y%m%d"
                today_date = today_time.strftime(dateformat)
                last_date_tmp = int(trade_status['last_date'][trade_status['code'].isin([t_code])].iloc[0])
                last_time = datetime.datetime.strptime(str(last_date_tmp),dateformat)
                last_date = last_time.strftime(dateformat)
                first_volume = int(trade_status['first_volume'][trade_status['code'].isin([t_code])].iloc[0])
                betting_seed = int(trade_status['betting_seed'][trade_status['code'].isin([t_code])].iloc[0])
                chk_ohlcv = get_ohlcv(full_code,past_date,today_date)
                #sell check
                #stop_loss check
                #auto sell check
                #auto loss check
                chk_ohlcv['acml_vol'] = pd.to_numeric(chk_ohlcv['acml_vol'])
                volume_list = chk_ohlcv['acml_vol'].to_list()
                sell_chk = sell_cond_chk(k)
                if (sell_chk == 1):
                    try:
                        # 하나라도 매수됬는지 확인
                        total_qty = check_order(full_code,past_date,today_date)
                        time.sleep(10)
                        if (total_qty >= 1):
                            logger.info('매도 확인', full_code)
                            sell(full_code,total_qty)
                            time.sleep(30)
                            total_qty, avg_price, total_amt, total_fee = check_sell_order(code,past_date,today_date)
                            time.sleep(30)
                            stock_dict, total_balance = get_stock_balance() # 보유 주식 조회
                            balance = total_amt - total_fee
                            last_time = datetime.datetime.strptime(last_date,dateformat)
                            date_diff = today_time - last_time
                            waiting_period = date_diff.days
                            code_idx_list = trade_status['code'][trade_status['code'].isin([t_code])].index.to_list()
                            len_code_idx_list = len(code_idx_list)
                            if (len_code_idx_list == 1):
                                code_idx = code_idx_list[0]
                                trade_status[code_idx, 'waiting_period'] = waiting_period
                                trade_status[code_idx, 'sell_completed'] = 1
                                trade_status[code_idx, 'sell'] = 1
                                trade_status[code_idx, 'stop_loss'] = 0
                                trade_status[code_idx, 'auto_sell'] = 0
                                trade_status[code_idx, 'auto_loss'] = 0
                                trade_status[code_idx, 'sell_price'] = avg_price
                                trade_status[code_idx, 'sell_date'] = today_date
                                trade_status[code_idx, 'balance'] = balance
                                trade_status[code_idx, 'total_balance'] = total_balance
                                trade_status[code_idx, 'income'] = balance / betting_seed
                                trade_status[code_idx, 'profit'] = (balance - betting_seed) / betting_seed



                            code_idx_list = trade_status['code'][trade_status['code'].isin([t_code])].index.to_list()
                            len_code_idx_list = len(code_idx_list)
                            if (len_code_idx_list == 1):
                                code_idx = code_idx_list[0]
                                try:
                                    buy_qty = cal_unit_qty(first_buy_price,betting_seed)
                                    buy_market(full_code,buy_qty)
                                    time.sleep(10)
                                    avg_prvs = check_avg_price(full_code,past_date,today_date)
                                    time.sleep(10)
                                    betting_seed = check_betting_seed(full_code,past_date,today_date)
                                    trade_status[code_idx, 'last_order'] = 1
                                    trade_status[code_idx, 'last_price'] = avg_prvs
                                    trade_status[code_idx, 'betting_seed'] = betting_seed
                                    trade_status[code_idx, 'last_date'] = today_date
                                    trade_status.to_csv('trade_status.csv', encoding='CP949', mode='w')
                                    send_message(f"[후발 매수 주문 완료]{e}")
                                    logger.info('Can\'t find %s. skip this ticker.', code)
                                    time.sleep(1)
                                except Exception as e:
                                    send_message(f"[후발 매수 주문 실패]{e}")
                                    logger.info('Can\'t find %s. skip this ticker.', code)
                                    time.sleep(1)
                                    continue
                            else:
                                send_message(f"[code 1개 이상 발견.]{e}")
                                logger.info('code was found more then 1. %s. skip this ticker.', code)
                    except Exception as e:
                        send_message(f"[check_order 내 error 발견]{e}")
                        logger.info('There is an error in \'check_order\' process. skip this ticker.', code)
                        time.sleep(1)
                        continue
        if t_end < t_now:  # PM 03:20 ~ :프로그램 종료
            send_message("프로그램을 종료합니다.")
            break
#symbol_list = ["005930","035720","000660","069500"] # 매수 희망 종목 리스트
#sym = ["005930"] # 매수 희망 종목 리스트
#sym = ["365340"] # 매수 희망 종목 리스트
#sym_list = ["005930","365340","290520","260660"]
# 2. CHECK FIRST ORDER COMPLETED
except Exception as e:
    send_message(f"[오류 발생]{e}")
    time.sleep(1)