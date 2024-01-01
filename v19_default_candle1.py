import FinanceDataReader as fdr
fdr.__version__
#from google.colab import files
#myfile = files.upload()
import sys
import time
import pandas as pd
import math
import numpy as np
import warnings
warnings.filterwarnings("ignore")

import random
#stocks = pd.read_html('상장법인목록.xls', header=0, converters={'종목코드': str})[0]
stocks = pd.read_csv('kosdaq_candle/output_file_1.csv', encoding='CP949')
#stocks = pd.read_csv('all_data_MA_simple.csv', encoding='CP949')
#stocks = pd.read_csv('test55.csv', encoding='CP949')
unique_code = stocks['code'].unique()
print("ticker:",len(unique_code))


pd.set_option('mode.chained_assignment', None)

def gap_chk(num):
    tmp_data1 = single_stock['Close'].loc[(num-1)]
    tmp_data2 = single_stock['Open'].loc[num]
    tmp_data3 = tmp_data2 / tmp_data1
    return tmp_data3

def boundary_level300_chk(num):
    if ((num >= 300)):
        tmp_data1 = single_stock['High'].loc[(num-300):(num-20)].max()
        tmp_data2 = single_stock['Low'].loc[(num-300):(num-20)].min()
        tmp_data3 = single_stock['Close'].loc[(num-20):(num-5)].mean()
    else:
        tmp_data1 = single_stock['High'].loc[0:(num-20)].max()
        tmp_data2 = single_stock['Low'].loc[0:(num-20)].min()
        tmp_data3 = single_stock['Close'].loc[(num-20):(num-5)].mean()
    boundary_level300 = (tmp_data3 - tmp_data2) / (tmp_data1 - tmp_data2)
    return boundary_level300

def boundary_level500_chk(num):
    if ((num >= 500)):
        tmp_data1 = single_stock['High'].loc[(num-500):(num-20)].max()
        tmp_data2 = single_stock['Low'].loc[(num-500):(num-20)].min()
        tmp_data3 = single_stock['Close'].loc[(num-20):(num-5)].mean()
    else:
        tmp_data1 = single_stock['High'].loc[0:(num-20)].max()
        tmp_data2 = single_stock['Low'].loc[0:(num-20)].min()
        tmp_data3 = single_stock['Close'].loc[(num-20):(num-5)].mean()
    boundary_level500 = (tmp_data3 - tmp_data2) / (tmp_data1 - tmp_data2)
    return boundary_level500

def boundary_level700_chk(num):
    if ((num >= 700)):
        tmp_data1 = single_stock['High'].loc[(num-700):(num-20)].max()
        tmp_data2 = single_stock['Low'].loc[(num-700):(num-20)].min()
        tmp_data3 = single_stock['Close'].loc[(num-20):(num-5)].mean()
    else:
        tmp_data1 = single_stock['High'].loc[0:(num-20)].max()
        tmp_data2 = single_stock['Low'].loc[0:(num-20)].min()
        tmp_data3 = single_stock['Close'].loc[(num-20):(num-5)].mean()
    boundary_level700 = (tmp_data3 - tmp_data2) / (tmp_data1 - tmp_data2)
    return boundary_level700

def boundary_level3_chk(num):
    tmp_data1 = single_stock['Close'].loc[(num-40):(num-5)].mean()
    tmp_data2 = single_stock['Open'].loc[(num-1)]
    tmp_data3 = single_stock['Close'].loc[(num-1)]
    boundary_level = (tmp_data2 + ((tmp_data3 - tmp_data2) / 2)) / tmp_data1
    return boundary_level

def sell_cond_chk(num):
    big_volume_cnt = 0
    acc_volume_ok = 0
    for f in range(1,num):
        if (volume_slice[f] >= (volume * 0.8)):
            big_volume_cnt = big_volume_cnt + 1
    acc_volume = sum(volume_slice[1:num])
    if (acc_volume >= (volume * 5)):
        acc_volume_ok = 1
    if ((acc_volume_ok == 1) and (big_volume_cnt >= 2)):
        return 1
    else:
        return 0


def cov_chk(num):
    tmp_data1 = single_stock['MA20'].loc[(num-10):(num-2)].mean()
    tmp_data2 = single_stock['MA60'].loc[(num-10):(num-2)].mean()
    tmp_data3 = single_stock['MA120'].loc[(num-10):(num-2)].mean()
    tmp_data4 = max(tmp_data1,tmp_data2,tmp_data3)
    tmp_data5 = min(tmp_data1,tmp_data2,tmp_data3)
    tmp_data = tmp_data4 / tmp_data5
    return tmp_data

def boundary_level_chk(num):
    tmp_data1 = single_stock['High'].loc[(num-60):(num-20)].max()
    tmp_data2 = single_stock['Low'].loc[(num-60):(num-20)].min()
    tmp_data3 = single_stock['Close'].loc[(num-20):(num-5)].mean()
    boundary_level = (tmp_data3 - tmp_data2) / (tmp_data1 - tmp_data2)
    return boundary_level

def ma20_down_chk(num):
    tmp_cnt = 0
    tmp_data1 = single_stock['MA20'].loc[(num-60)]
    for t in range((num-55),(num-5),5):
        tmp_data2 = single_stock['MA20'].loc[t]
        tmp_data3 = tmp_data2 / tmp_data1
        if (tmp_data3 >= 1.05):
            tmp_cnt = tmp_cnt + 1
        tmp_data1 = tmp_data2
    return tmp_cnt

def stop_loss_chk(num):
    tmp_data1 = single_stock['Close'].loc[(num-20):(num-1)].min()
    return tmp_data1


def close_down_chk(num):
    tmp_data1 = single_stock['Close'].loc[(num-20):(num-5)].min()
    tmp_data2 = single_stock['Open'].loc[num]
    tmp_data3 = tmp_data2 / tmp_data1
    return tmp_data3

def ma60_down_chk(num):
    tmp_cnt = 0
    tmp_data1 = single_stock['MA60'].loc[(num-60)]
    for t in range((num-55),(num-5),5):
        tmp_data2 = single_stock['MA60'].loc[t]
        tmp_data3 = tmp_data2 / tmp_data1
        if (tmp_data3 >= 1.03):
            tmp_cnt = tmp_cnt + 1
        tmp_data1 = tmp_data2
    return tmp_cnt


def ma120_down_chk(num):
    tmp_cnt = 0
    tmp_data1 = single_stock['MA120'].loc[(num-60)]
    for t in range((num-55),(num-5),5):
        tmp_data2 = single_stock['MA120'].loc[t]
        tmp_data3 = tmp_data2 / tmp_data1
        if (tmp_data3 >= 1):
            tmp_cnt = tmp_cnt + 1
        tmp_data1 = tmp_data2
    return tmp_cnt

def ma60_120_interval_mean_chk(num):
    tmp_data4 = 0
    for t in range((num-60),num):
        tmp_data1 = single_stock['MA60'].loc[t]
        tmp_data2 = single_stock['MA120'].loc[t]
        tmp_data3 = tmp_data2 / tmp_data1
        tmp_data4 = tmp_data4 + tmp_data3
    tmp_data = tmp_data4 / 60
    return tmp_data

def ma60_120_interval_chk(num):
    tmp_data1 = single_stock['MA60'].loc[num]
    tmp_data2 = single_stock['MA120'].loc[num]
    tmp_data = tmp_data2 / tmp_data1
    return tmp_data

def ma60_counting_chk(num):
    tmp_cnt = 0
    for y in range((num-60),num):
        tmp_data1 = single_stock['MA60'].loc[y-1]
        tmp_data2 = single_stock['MA60'].loc[y]
        if (tmp_data1 > tmp_data2):
            tmp_cnt = tmp_cnt + 1
    tmp_data3 = tmp_cnt / 60
    return tmp_data3

def ma120_counting_chk(num):
    tmp_cnt = 0
    for p in range((num-60),num):
        tmp_data1 = single_stock['MA120'].loc[p-1]
        tmp_data2 = single_stock['MA120'].loc[p]
        if (tmp_data1 > tmp_data2):
            tmp_cnt = tmp_cnt + 1
    tmp_data3 = tmp_cnt / 60
    return tmp_data3

def ma120_cnt_chk(num):
    tmp_cnt = 0
    for i in range((num-10),0,-1):
        tmp_data1 = single_stock['MA120'].loc[i]
        tmp_data2 = single_stock['High'].loc[i]
        if (tmp_data1 > tmp_data2):
            tmp_cnt = tmp_cnt + 1
        else:
            break
    return tmp_cnt

def big_deal_chk(max_value,close):
    tmp_data = max_value / close
    return tmp_data

def close_level_chk(num):
    tmp_data1 = single_stock['Close'].loc[num]
    tmp_data2 = single_stock['MA60'].loc[num]
    tmp_data3 = single_stock['MA120'].loc[num]
    tmp_data4 = (tmp_data1 - min(tmp_data2,tmp_data3)) / abs(tmp_data3 - tmp_data2)
    return tmp_data4

def descending_chk(num):
    tmp_data1 = single_stock['MA60'].loc[(num-60):num].mean()
    tmp_data2 = single_stock['MA120'].loc[(num-60):num].mean()
    tmp_data = tmp_data2 / tmp_data1
    return tmp_data

def volume_chk2(num):
    tmp_data1 = single_stock['Volume'].loc[num]
    tmp_cnt = 0
    if (num <= 120):
        for i in range(0,(num-5)):
            tmp_data2 = single_stock['Volume'].loc[i]
            if (tmp_data1 < (tmp_data2 * 2)):
                tmp_cnt = tmp_cnt + 1
    else:
        for i in range((num-120),(num-5)):
            tmp_data2 = single_stock['Volume'].loc[i]
            if (tmp_data1 < (tmp_data2 * 2)):
                tmp_cnt = tmp_cnt + 1
    return tmp_cnt

def volume_chk(num):
    tmp_data1 = single_stock['Volume'].loc[(num-10):(num-3)].mean()
    tmp_data2 = single_stock['Volume'].loc[(num)]
    tmp_data3 = tmp_data2 / tmp_data1
    return tmp_data3

def rising_candle_chk(num):
    tmp_data1 = single_stock['Open'].loc[(num)]
    tmp_data2 = single_stock['Close'].loc[(num)]
    tmp_data3 = tmp_data2 / tmp_data1
    return tmp_data3

def touch_ma120_chk(num):
    tmp_data1 = single_stock['MA60'].loc[num]
    tmp_data2 = single_stock['MA120'].loc[num]
    tmp_data3 = single_stock['High'].loc[num]
    #if (tmp_data3 >= (tmp_data2 - (tmp_data2 - tmp_data1) * 0.2)):
    if (tmp_data3 >= tmp_data2):
        return 1
    else:
        return 0

#def touch_ma120_chk(num):
#    tmp_data1 = single_stock['MA120'].loc[(num-120):(num-10)].min()
#    tmp_data2 = single_stock['High'].loc[(num-120):(num-10)].max()
#    tmp_data3 = single_stock['High'].loc[(num-5):num].max()
#    if ((tmp_data1 >= tmp_data2) and (tmp_data1 <= tmp_data3)):
#        return 1
#    else:
#        return 0

#def touch_line60(low,value60,value120,num):
#    num = num - 120
#    tmp_data1 = value60_line['Close'].loc[num]
#    tmp_data2 = value120_line['Close'].loc[num]
#    if ((tmp_data2 > tmp_data1) and (low <= ((tmp_data2 - tmp_data1) * 0.3))):
#        return 1
#    else:
#        return 0
#
#def out_line60(low,value60,num):
#    num = num - 120
#    tmp_data1 = value60_line['Close'].loc[num]
#    if (tmp_data1 >= low):
#        return 1
#    else:
#        return 0


def no_touch_ma120_chk(num):
    no_touch_ma120_chk_cnt = 0
    for n in range((num-60),(num-10)):
        tmp_data1 = single_stock['MA120'].loc[n]
        tmp_data2 = single_stock['High'].loc[n]
        if ((tmp_data2 >= tmp_data1)):
            no_touch_ma120_chk_cnt = no_touch_ma120_chk_cnt + 1
    for n in range((num-3),num):
        tmp_data1 = single_stock['MA120'].loc[n]
        tmp_data2 = single_stock['High'].loc[n]
        tmp_data3 = single_stock['Open'].loc[n]
        tmp_data4 = single_stock['Close'].loc[n]
        if ((tmp_data3 >= tmp_data4) and (tmp_data3 >= tmp_data1)):
            no_touch_ma120_chk_cnt = 100
    return no_touch_ma120_chk_cnt

def e_5_20_ma_chk(num):
    e_5_20_ma_cnt = 0
    ma5_is_big = 2
    for n in range((num-10),(num+1)):
        tmp_data1 = single_stock['MA5'].loc[n]
        tmp_data2 = single_stock['MA20'].loc[n]
        if ((ma5_is_big == 0) and tmp_data1 >= tmp_data2):
            e_5_20_ma_cnt = e_5_20_ma_cnt + 1
        if (tmp_data1 <= tmp_data2):
            ma5_is_big = 0
        else:
            ma5_is_big = 1
    if (e_5_20_ma_cnt >= 1):
        return 1
    else:
        return 0

def r_array_chk(num):
    r_chk_cnt = 0
    for n in range((num-120),(num-20)):
        tmp_data1 = single_stock['MA120'].loc[n]
        tmp_data2 = single_stock['MA60'].loc[n]
        tmp_data3 = single_stock['MA20'].loc[n]
        tmp_data4 = single_stock['MA5'].loc[n]
        if ((tmp_data1 >= tmp_data2) and (tmp_data2 >= tmp_data3) and (tmp_data3 >= tmp_data4)):
            r_chk_cnt = r_chk_cnt + 1
    if (r_chk_cnt >= 50):
        return 1
    else:
        return 0

fv_date = ""
filter_cnt = 0
filter_date = ""
buy_cnt = 0
sell_cnt = 0
auto_sell_cnt = 0
cut_cnt = 0
stop_loss_cnt = 0
auto_loss_cnt = 0
df = pd.DataFrame(columns=['COM_NAME','I','LOW30_DATE', 'HIGH30_DATE', 'LOW30_STOP_LOSS_DATE', 'SUCCESS', 'DATE','OPEN','CLOSE','HIGH','LOW','VOLUME','BUY','BUY_PRICE','BUY_DATE','FV_DATE','FV_CNT','VOLUME_RATE','VOLUME_RATIO','AVG_VOLUME_RATE','SELL','SELL_PRICE','STOP_LOSS_COND','SELL_DATE','STOP_LOSS_DATE','CUT_DATE','AUTO_SELL','STOP_LOSS','CUT','BENIFIT','BUY_PRICE_RATE','LOW10_RATE','LOW30_RATE','HIGH10_RATE','HIGH30_RATE','CLOSE10_RATE','CLOSE30_RATE','BUY_PRICE','SELL_PERIOD','AUTO_SELL_PERIOD','STOP_LOSS_PERIOD','CUT_PERIOD','BOUNDARY_LEVEL','MA60_120_INTERVAL','FV_LIST'])
fv_df = pd.DataFrame(columns=['Date','FV','Volume'])
#unique_code = [67370]
# search big volume
loop_cnt = 0
code_len = len(unique_code)
for i in unique_code:
    #if i in code_list:
    loop_cnt = loop_cnt + 1
    status = int(round((loop_cnt / code_len), 2) * 100)
    #print(loop_cnt)
    status2 = round((loop_cnt / code_len), 2) * 100
    #print(status2)
    print("{}%".format(status))
    com_name = stocks['company'][stocks['code'].isin([i])].iloc[0]
    init_idx = stocks['company'][stocks['code'].isin([i])].iloc[0]
#  com_name = com_name2.iloc[0]
    single_stock = stocks[stocks['code'].isin([i])]
    single_stock.reset_index(drop=True, inplace=True)
    single_stock_len = len(stocks[stocks['code'].isin([i])])
#  result.insert(6, 'code', i, True)
    #time.sleep(0.5)
    close_all_level_chk = single_stock['High'].loc[0:(single_stock_len-1)].max()
    avg_volume = single_stock['Volume'].loc[0:(single_stock_len-1)].mean()
    jump_cnt = 0
    print(com_name, i, single_stock_len)
    for j in range(0, single_stock_len):
        if (jump_cnt > 0):
            jump_cnt = jump_cnt - 1
            continue
        else:
            if ((j >= 201) and (j < (single_stock_len-201))):
                jump_cnt = jump_cnt - 1
                today_date =  single_stock['Date'].loc[j]
                fv_list = ""
                del fv_df
                fv_df = pd.DataFrame(columns=['Date','FV','Volume'])
                #stocks = pd.read_csv('test55.csv', encoding='CP949')
                #df2 = df[(df['VOLUME_RATE'] >= 1) & (df['Date'] < date)]
                tmp_single_stock = single_stock[(single_stock['Date'] < today_date)]
                avg_volume = tmp_single_stock['Volume'].mean()
                tmp_single_stock['VOLUME_RATE_AVG'] = tmp_single_stock['Volume'] / avg_volume
                tmp_single_stock['VOLUME_RATE_JA'] = tmp_single_stock['Volume'].rolling(10).mean()
                tmp_single_stock['VOLUME_RATE_JA'] = tmp_single_stock['VOLUME_RATE_JA'].shift(2).fillna(999999999)
                tmp_single_stock['RISING'] = tmp_single_stock['Close'] / tmp_single_stock['Open']
                fv_list = tmp_single_stock['Close'][(tmp_single_stock['RISING'] >= 1.05) & ((tmp_single_stock['VOLUME_RATE_AVG'] >= 10) | ((tmp_single_stock['Volume'] / tmp_single_stock['VOLUME_RATE_JA']) >= 20)) & ((tmp_single_stock['Close'] * tmp_single_stock['Volume']) >= 10000000000)].to_list()
                fv_df['Date'] = tmp_single_stock['Date'][(tmp_single_stock['RISING'] >= 1.05) & ((tmp_single_stock['VOLUME_RATE_AVG'] >= 10) | ((tmp_single_stock['Volume'] / tmp_single_stock['VOLUME_RATE_JA']) >= 20)) & ((tmp_single_stock['Close'] * tmp_single_stock['Volume']) >= 10000000000)]
                fv_df['FV'] = tmp_single_stock['Close'][(tmp_single_stock['RISING'] >= 1.05) & ((tmp_single_stock['VOLUME_RATE_AVG'] >= 10) | ((tmp_single_stock['Volume'] / tmp_single_stock['VOLUME_RATE_JA']) >= 20)) & ((tmp_single_stock['Close'] * tmp_single_stock['Volume']) >= 10000000000)]
                fv_df['Volume'] = tmp_single_stock['Volume'][(tmp_single_stock['RISING'] >= 1.05) & ((tmp_single_stock['VOLUME_RATE_AVG'] >= 10) | ((tmp_single_stock['Volume'] / tmp_single_stock['VOLUME_RATE_JA']) >= 20)) & ((tmp_single_stock['Close'] * tmp_single_stock['Volume']) >= 10000000000)]
                fv_df.reset_index(drop=True, inplace=True)
                fv_list.sort()
                while True:
                    tmp_fv_list = fv_list
                    len_tmp_fv_list = len(tmp_fv_list)
                    remove_cnt = 0
                    for i in range(0,(len_tmp_fv_list-2)):
                        if ((tmp_fv_list[i+1] / tmp_fv_list[i]) <= 1.05):
                            remove_cnt = 1
                            volume1 = fv_df['Volume'][fv_df['FV'].isin([tmp_fv_list[i]])].to_list()
                            volume1 = sum(volume1)
                            volume2 = fv_df['Volume'][fv_df['FV'].isin([tmp_fv_list[i+1]])].to_list()
                            volume2 = sum(volume2)
                            if (volume1 >= volume2):
                                fv_df = fv_df[fv_df.Volume != volume2]
                                fv_list.remove(tmp_fv_list[i+1])
                            else:
                                fv_df = fv_df[fv_df.Volume != volume1]
                                fv_list.remove(tmp_fv_list[i])
                            break
                    tmp_fv_list = fv_list
                    if (remove_cnt == 0):
                        break
                fv_df.reset_index(drop=True, inplace=True)
                fv_list = fv_df['FV'].to_list()
                fv_list.sort()
                fv_list = np.unique(fv_list)
                fv_list = list(fv_list)
                len_fv_list = len(fv_list)
                if (len_fv_list >= 0):
                    down_cnt = 0
                    rise_cnt = 0
                    current_fv = 0
                    past_fv = 0
                    tmp_single_stock_len = len(tmp_single_stock[tmp_single_stock['code'].isin([i])])
                    #for j in range(0, tmp_single_stock_len):
                    #    tmp_open2 =  tmp_single_stock['Open'].loc[j]
                    #    tmp_close2 =  tmp_single_stock['Close'].loc[j]
                    #    tmp_min = min(tmp_open2, tmp_close2)
                    #    tmp_max = max(tmp_open2, tmp_close2)
                    #    tmp_fv_list2 = []
                    #    np_fv_list2 = np.array(fv_list)
                    #    result_list2 = (np_fv_list2 > tmp_min) & (np_fv_list2 < tmp_max)
                    #    tmp_fv_list2 = np_fv_list2[result_list2]
                    #    tmp_fv_list2.sort()
                    #    len_tmp_fv_list2 = len(tmp_fv_list2)
                    #    if (len_tmp_fv_list2 >= 1):
                    #        current_fv = tmp_fv_list2[0]
                    #        if (current_fv > past_fv):
                    #            rise_cnt = rise_cnt + 1
                    #            down_cnt = 0
                    #        elif (current_fv < past_fv):
                    #            down_cnt = down_cnt + 1
                    #            rise_cnt = 0
                    #        past_fv = current_fv
                    open =  single_stock['Open'].loc[j]
                    past_open =  single_stock['Open'].loc[j-1]
                    close = single_stock['Close'].loc[j]
                    past_close = single_stock['Close'].loc[j-1]
                    high =  single_stock['High'].loc[j]
                    low  =  single_stock['Low'].loc[j]
                    volume = single_stock['Volume'].loc[j]
                    future_volume =  single_stock['Volume'].loc[(j+1):(j+80)].sum()
                    past_volume  =  single_stock['Volume'].loc[(j-80):j].sum()
                    volume_ratio = future_volume / past_volume
                    past_close10 = single_stock['Close'].loc[(j-20):(j-10)].mean()
                    if ((j >= 500)):
                        max_value = single_stock['High'].loc[(j-500):j].max()
                    else:
                        max_value = single_stock['High'].loc[0:j].max()
                    next_volume = single_stock['Volume'].loc[(j+1)]
                    #volume_rate = volume / past_volume10
                    date = single_stock['Date'].loc[j]
                    value120 = single_stock['MA120'].loc[j]
                    past10_value120 = single_stock['MA120'].loc[(j-10)]
                    value60  = single_stock['MA60'].loc[j]
                    value20  = single_stock['MA20'].loc[j]
                    value5   = single_stock['MA5'].loc[j]
#                    rand_int = random.randint(1,100)
                    #if (rand_int == 1):
                    #if ((volume_rate >= 10) and (volume > (avg_volume * 5))):
                    descending = 1
                    big_deal = 1
                    volume_rate = volume_chk(j)
                    volume_rate2 = volume_chk2(j)
                    avg_volume_rate = volume / avg_volume
                    touch_ma120 = 1
                    ma120_cnt = 1
                    ma60_120_interval_mean = 1
                    ma60_120_interval = 1
                    #r_array = 1
                    r_array = 1
                    e_5_20_ma = 1
                    #e_5_20_ma = 1
                    close_level = 1
                    ma60_counting = 1
                    ma120_counting = 1
                    no_touch_ma120 = 1
                    boundary_level = 1
                    boundary_level2 = 1
                    rising_candle = 1
                    cov = cov_chk(j)
                    close_down = close_down_chk(j)
                    ma20_down = ma20_down_chk(j)
                    ma60_down = ma60_down_chk(j)
                    ma120_down = ma120_down_chk(j)
                    #descending = descending_chk(j)
                    #big_deal = big_deal_chk(max_value,past_close10)
                    #volume_rate = volume_chk(j)
                    #touch_ma120 = touch_ma120_chk(j)
                    #ma120_cnt = ma120_cnt_chk(j)
                    #ma60_120_interval_mean = ma60_120_interval_mean_chk(j)
                    #ma60_120_interval = ma60_120_interval_chk(j)
                    ##r_array = r_array_chk(j)
                    #r_array = 1
                    #e_5_20_ma = e_5_20_ma_chk(j)
                    ##e_5_20_ma = 1
                    #close_level = close_level_chk(j)
                    #ma60_counting = ma60_counting_chk(j)
                    #ma120_counting = ma120_counting_chk(j)
                    #no_touch_ma120 = no_touch_ma120_chk(j)
                    #boundary_level = boundary_level_chk(j)
                    boundary_level3 = boundary_level3_chk(j)
                    boundary_level300 = boundary_level300_chk(j)
                    boundary_level500 = boundary_level500_chk(j)
                    boundary_level700 = boundary_level700_chk(j)
                    rising_candle = rising_candle_chk(j)
                    gap = gap_chk(j)
                    #if ((open <= value120) and (descending >= 1) and (ma60_120_interval_mean >= 1.15)and (ma60_120_interval >= 1.1) and (value120 > value60) and (close_level >= 0.6) and (big_deal >= 3) and (ma60_counting >= 0.8) and (ma120_counting >= 0.8) and ((boundary_level <= 0.3) or (boundary_level2 <= 0.3))):
                    #if ((no_touch_ma120 <= 3) and (rising_candle >= 1.03) and (volume_rate >= 3) and (open <= value120) and (descending >= 1) and (ma60_120_interval_mean >= 1.1)and (ma60_120_interval >= 1.1) and (value120 > value60) and (close_level >= 0.6) and (big_deal >= 1.5) and (ma60_counting >= 0.7) and (ma120_counting >= 0.8) and ((boundary_level <= 0.5) or (boundary_level2 <= 0.3))):
                    tmp_fv_list = []
                    np_fv_list = np.array(fv_list)
                    result_list = (np_fv_list > open) & (np_fv_list < close)
                    tmp_fv_list = np_fv_list[result_list]
                    tmp_fv_list.sort()
                    len_tmp_fv_list = len(tmp_fv_list)
                    if (len_tmp_fv_list >= 0):
                        #FV = 0
                        #fv_date = 0
                        #fv_idx = 0
                        #FV = tmp_fv_list[0]
                        #fv_date = fv_df['Date'][fv_df['FV'].isin([FV])].values
                        #fv_idx = fv_list.index(FV)
                        FV = 0
                        fv_date = 0
                        fv_idx = 0
                        #print(fv_list)
                        #print(FV, fv_idx)
                        #if ((gap >= 1.05) and (rising_candle <= 1.2) and (rising_candle >= 1.05) and (volume_rate >= 20) and (boundary_level3 <= 1.2)):
                        if (((cov <= 1.05) or ((ma20_down == 0) and (ma60_down == 0) and (ma120_down == 0))) and (rising_candle <= 1.2) and (rising_candle >= 1.05) and (volume_rate >= 20) and (volume_rate2 == 0) and ((boundary_level300 <= 0.15) or (boundary_level500 <= 0.2) or (boundary_level700 <= 0.2))):
                            filter_date = date
                            filter_cnt = filter_cnt + 1
                            candle_limit = single_stock['Volume'].loc[(j-2):j].max()
                            ma120_cnt = 0
                            low_slice  =  single_stock['Low'].loc[(j+1):(j+80)]
                            high_slice  =  single_stock['High'].loc[(j+1):(j+80)]
                            close_slice  =  single_stock['Close'].loc[(j+1):(j+80)]
                            open_slice  =  single_stock['Open'].loc[(j+1):(j+80)]
                            volume_slice  =  single_stock['Volume'].loc[(j+1):(j+80)]
                            low10_slice  =  single_stock['Low'].loc[(j+1):(j+10)]
                            high10_slice  =  single_stock['High'].loc[(j+1):(j+10)]
                            ma120_slice  =  single_stock['MA120'].loc[(j+1):(j+80)]
                            ma60_slice  =  single_stock['MA60'].loc[(j+1):(j+80)]
                            ma20_slice  =  single_stock['MA20'].loc[(j+1):(j+80)]
                            ma5_slice  =  single_stock['MA5'].loc[(j+1):(j+80)]
                            date_slice  =  single_stock['Date'].loc[(j+1):(j+80)]
                            low_slice.reset_index(drop=True, inplace=True)
                            high_slice.reset_index(drop=True, inplace=True)
                            close_slice.reset_index(drop=True, inplace=True)
                            open_slice.reset_index(drop=True, inplace=True)
                            volume_slice.reset_index(drop=True, inplace=True)
                            ma120_slice.reset_index(drop=True, inplace=True)
                            ma60_slice.reset_index(drop=True, inplace=True)
                            ma20_slice.reset_index(drop=True, inplace=True)
                            ma5_slice.reset_index(drop=True, inplace=True)
                            date_slice.reset_index(drop=True, inplace=True)
                            high10 = single_stock['High'].loc[(j+1):(j+10)].max()
                            high30 = single_stock['High'].loc[(j+1):(j+80)].max()
                            low10 = single_stock['Low'].loc[(j+1):(j+10)].min()
                            change10 = single_stock['Change'].loc[(j+1):(j+10)].mean()
                            change30 = single_stock['Change'].loc[(j+1):(j+80)].mean()
                            close10 = single_stock['Close'].loc[(j+1):(j+10)].mean()
                            close30 = single_stock['Close'].loc[(j+1):(j+80)].mean()
                            high10_rate = high10 / close
                            low10_rate = low10 / close
                            close10_rate = close10 / close
                            close30_rate = close30 / close
                            high30_date_df = pd.DataFrame(columns=['High'])
                            high30_date_df['High'] =  single_stock['High'].loc[(j+1):(j+80)]
                            high30_date_df.reset_index(drop=True, inplace=True)
                            high30_date_list = high30_date_df['High'][high30_date_df['High'].isin([high30])].index.to_list()
                            high30_date_list.sort()
                            high30_date = high30_date_list[0]
                            if (high30_date != 0):
                                low30 = single_stock['Low'].loc[(j+1):(j+high30_date)].min()
                                low30_date_df = pd.DataFrame(columns=['Low'])
                                low30_date_df['Low'] =  single_stock['Low'].loc[(j+1):(j+high30_date)]
                                low30_date_df.reset_index(drop=True, inplace=True)
                                low30_date_list = low30_date_df['Low'][low30_date_df['Low'].isin([low30])].index.to_list()
                                low30_date_list.sort()
                                low30_date = low30_date_list[0]
                            else:
                                low30 = single_stock['Low'].loc[j].min()
                                low30_date = 0
                            #print("filter_date")
                            #print(filter_date)
                            #print("high30")
                            #print(high30)
                            #print("high30_date")
                            #print(high30_date)
                            #print("low30_date_df")
                            #print(low30_date_df)
                            #print("low30")
                            #print(low30)
                            #print("low30_date_list")
                            #print(low30_date_list)
                            #fv_idx = fv_list.index(FV)
                            #buy_condition = open + ((close - open) * 0.70)
                            #buy_condition = close
                            buy_price = ""
                            buy = 0
                            sell = 0
                            auto_sell = 0
                            auto_loss = 0
                            stop_loss = 0
                            stop_loss_day_cnt = 0
                            stop_loss_valid = 0
                            cut = 0
                            cut_cnt = 0
                            up_cnt = 0
                            buy_date = ""
                            sell_date = ""
                            stop_loss_date = ""
                            cut_date = 0
                            auto_sell_date = ""
                            trade_start = ""
                            sell_period = ""
                            auto_sell_period = ""
                            cut_period = 0
                            stop_loss_period = ""
                            benifit = "NA"
                            #buy_condition = tmp_fv_list[0] * 1.005
                            ##buy_condition = open + ((close - open) / 2)
                            #sell_price = buy_condition * 1.15
                            ##stop_loss_condition = buy_condition * 0.9
                            #stop_loss_condition = stop_loss_chk(j)
                            #if (len_fv_list == 1):
                            #    sell_price = buy_condition * 1.15
                            #    #stop_loss_condition = past_open
                            #elif (FV == fv_list[0]):
                            #    sell_price = fv_list[0] + ((fv_list[1] - fv_list[0]) * 0.9)
                            #    #stop_loss_condition = buy_condition - ((fv_list[1] - fv_list[0]) * 0.9)
                            #elif (FV == fv_list[(len_fv_list-1)]):
                            #    sell_price = buy_condition * 1.15
                            #    stop_loss_condition = buy_condition - ((fv_list[(len_fv_list-1)] - fv_list[(len_fv_list-2)]) * 1.03)
                            #    #stop_loss_condition = fv_list[(len_fv_list-2)] * 0.97
                            #else:
                            #    sell_price = fv_list[fv_idx] + ((fv_list[fv_idx+1] - fv_list[fv_idx]) * 0.9)
                            #    stop_loss_condition = fv_list[fv_idx] - ((fv_list[fv_idx] - fv_list[fv_idx-1]) * 1.03)
                            #    #stop_loss_condition = fv_list[fv_idx-1] * 0.99
                            #if ((stop_loss_condition * 1.2) <= buy_condition):
                            #    stop_loss_condition = stop_loss_chk(j)
                            #if ((stop_loss_condition * 1.2) <= buy_condition):
                            #    stop_loss_condition = buy_condition * 0.85
                            #if (sell_price >= (buy_condition * 1.2)):
                            #    sell_price = buy_condition * 1.2
                            if ((((close - open) / open) > 1.05) and (((close - open) / open) <= 1.10)):
                                buy_condition = close
                            elif ((((close - open) / open) > 1.10) and (((close - open) / open) <= 1.15)):
                                buy_condition = open + ((close - open) * 0.8) 
                            elif ((((close - open) / open) > 1.15) and (((close - open) / open) <= 1.2)):
                                buy_condition = open + ((close - open) * 0.6) 
                            else:
                                buy_condition = open + ((close - open) * 0.6) 
                            sell_price = 0
                            stop_loss_condition =  single_stock['Open'].loc[(j-20):(j-1)].min()
                            low30_value_df = pd.DataFrame(columns=['Low'])
                            low30_value_df['Low'] =  single_stock['Low'].loc[(j+1):(j+high30_date)]
                            low30_value_df.reset_index(drop=True, inplace=True)
                            low30_value_list = low30_value_df['Low'][(low30_value_df['Low'] <= stop_loss_condition)].index.to_list()
                            low30_value_list.sort()
                            low30_value_list_len = len(low30_value_list)
                            #print("low30_value_list")
                            #print(low30_value_list)
                            #print("stop_loss_condition")
                            #print(stop_loss_condition)
                            if (low30_value_list_len >= 1):
                                low30_stop_loss_date = low30_value_list[0]
                            else:
                                low30_stop_loss_date = 500
                            low30_rate = low30 / buy_condition
                            high30_rate = high30 / buy_condition
                            if (high30_date <= low30_stop_loss_date):
                                success = 1
                            else:
                                success = 0
                            for k in range(0,80):
                                tmp_low = low_slice[k]
                                tmp_volume = volume_slice[k]
                                tmp_high = high_slice[k]
                                tmp_close = close_slice[k]
                                tmp_open = open_slice[k]
                                tmp_ma120 = ma120_slice[k]
                                tmp_ma60 = ma60_slice[k]
                                tmp_ma20 = ma20_slice[k]
                                tmp_ma5 = ma5_slice[k]
                                tmp_date = date_slice[k]
                                ma_list = [tmp_ma5, tmp_ma20, tmp_ma60, tmp_ma120]
                                ma_list.sort()
                                sell_price = 0
                                sell_chk = sell_cond_chk(k)
                                if ((buy == 0) and (k < 15) and (tmp_high >= high)):
                                    break
                                if ((buy == 0) and (k < 15) and (tmp_low <= buy_condition) and (tmp_volume <= (volume * 0.5))):
                                    trade_start = k
                                    buy_price = buy_condition
                                    buy = 1
                                    buy_cnt = buy_cnt + 1
                                    buy_date = tmp_date
                                    continue
                                if ((buy == 1) and (sell == 0) and (stop_loss == 0) and (sell_chk == 1)):
                                    sell_price = tmp_close
                                    benifit = (sell_price / buy_price) - 1
                                    sell = 1
                                    sell_cnt = sell_cnt + 1
                                    sell_period = k - trade_start
                                    sell_date = tmp_date
                                    break
                                if ((buy == 1) and (stop_loss_condition >= tmp_low)):
                                    benifit = (stop_loss_condition / buy_price) -1
                                    stop_loss = 1
                                    stop_loss_cnt = stop_loss_cnt + 1
                                    stop_loss_period = k - trade_start
                                    stop_loss_date = tmp_date
                                    break
                                if ((k == 79) and (buy == 1) and (sell == 0)):
                                    sell_price = tmp_close
                                    benifit = (tmp_close / buy_price) - 1
                                    if ((tmp_close >= buy_price)):
                                        auto_sell = 1
                                        auto_sell_cnt = auto_sell_cnt + 1
                                        auto_sell_period = k - trade_start
                                    else:
                                        auto_loss = 1
                                        auto_loss_cnt = auto_loss_cnt + 1
                                        auto_loss_period = k - trade_start
                                    break
                            if (buy_price != ""):
                                buy_price_rate = buy_price / close
                                jump_cnt = 30
                                df2 = pd.DataFrame(data=[[com_name, i, low30_date, high30_date, low30_stop_loss_date, success, filter_date, open, close, high, low, volume, buy, buy_price, buy_date, fv_date, len_fv_list, volume_rate, volume_ratio, avg_volume_rate, sell, sell_price, stop_loss_condition, sell_date, stop_loss_date, cut_date, auto_sell, stop_loss, cut, benifit, buy_price_rate, low10_rate, low30_rate, high10_rate, high30_rate, close10_rate, close30_rate, buy_price, sell_period, auto_sell_period, stop_loss_period, cut_period, boundary_level, ma60_120_interval, fv_list]], columns=['COM_NAME','I','LOW30_DATE', 'HIGH30_DATE', 'LOW30_STOP_LOSS_DATE', 'SUCCESS', 'DATE','OPEN','CLOSE','HIGH','LOW','VOLUME','BUY','BUY_PRICE','BUY_DATE','FV_DATE','FV_CNT','VOLUME_RATE','VOLUME_RATIO','AVG_VOLUME_RATE','SELL','SELL_PRICE','STOP_LOSS_COND','SELL_DATE','STOP_LOSS_DATE','CUT_DATE','AUTO_SELL','STOP_LOSS','CUT','BENIFIT','BUY_PRICE_RATE','LOW10_RATE','LOW30_RATE','HIGH10_RATE','HIGH30_RATE','CLOSE10_RATE','CLOSE30_RATE','BUY_PRICE','SELL_PERIOD','AUTO_SELL_PERIOD','STOP_LOSS_PERIOD','CUT_PERIOD','BOUNDARY_LEVEL','MA60_120_INTERVAL','FV_LIST'])
                                df = df.append(df2)
df.to_csv("tmp.csv", encoding='CP949', mode='w')
time.sleep(1)
tmp_stocks = pd.read_csv('tmp.csv', encoding='CP949')
tmp_df = tmp_stocks[tmp_stocks.columns.difference(['NAME','CODE','DATE'])]
all_mean = tmp_df.mean()
all_mean_data = pd.DataFrame(data=all_mean)
tmp_df_t = all_mean_data.T
print(tmp_df_t)
df3 = tmp_stocks.append(tmp_df_t, ignore_index=True)
#df = pd.concat([df,tmp_df_t])
name = sys.argv[0].split('.')[0]
name_ext = name + '.' + 'csv'
df3.to_csv(name_ext, encoding='CP949', mode='w')

print("filter:",filter_cnt,"buy:",buy_cnt,"sell:",sell_cnt,"auto_sell:",auto_sell_cnt,"stop_loss:",stop_loss_cnt)