import FinanceDataReader as fdr
fdr.__version__
#from google.colab import files
#myfile = files.upload()
import sys
import time
import pandas as pd
import math
import numpy

import random
#stocks = pd.read_html('상장법인목록.xls', header=0, converters={'종목코드': str})[0]
stocks = pd.read_csv('get_all_ohlcv.csv', encoding='CP949')
#stocks = pd.read_csv('test55.csv', encoding='CP949')
#unique_code = stocks['code'].unique()
#print("ticker:",len(unique_code))
#
#stocks_len = len(stocks)


stocks['MA120'] = stocks['Close'].rolling(120).mean()
stocks['MA60'] = stocks['Close'].rolling(60).mean()
stocks['MA20'] = stocks['Close'].rolling(20).mean()
stocks['MA5'] = stocks['Close'].rolling(5).mean()

stocks.to_csv("ma_out.csv", encoding='CP949', mode='w')

#df = pd.DataFrame(columns=['NAME','CODE','DATE','OPEN','CLOSE','HIGH','LOW','VOLUME','MA120','MA60','MA20','MA5'])
##unique_code = [67370]
## search big volume
#stocks['MA']
#for i in unique_code:
#    st
#    com_name = stocks['company'][stocks['code'].isin([i])].iloc[0]
#    init_idx = stocks['company'][stocks['code'].isin([i])].iloc[0]
##  com_name = com_name2.iloc[0]
#    single_stock = stocks[stocks['code'].isin([i])]
#    single_stock.reset_index(drop=True, inplace=True)
#    single_stock_len = len(stocks[stocks['code'].isin([i])])
##  result.insert(6, 'code', i, True)
#    print(com_name, i, single_stock_len)
#    #time.sleep(0.5)
#    close_all_level_chk = single_stock['High'].loc[0:(single_stock_len-1)].max()
#    avg_volume = single_stock['Volume'].loc[0:(single_stock_len-1)].mean()
#    value120_line = pd.DataFrame(columns=['CLOSE'])
#    value60_line = pd.DataFrame(columns=['CLOSE'])
#    value20_line = pd.DataFrame(columns=['CLOSE'])
#    value5_line = pd.DataFrame(columns=['CLOSE'])
#    for j in range(0, single_stock_len):
#        print("start - make line")
#        for i in range(200,(single_stock_len-31)):
#            tmp_avg120_close = single_stock['CLOSE'].loc[(i-119):i].mean()
#            tmp_avg60_close = single_stock['CLOSE'].loc[(i-59):i].mean()
#            tmp_avg20_close = single_stock['CLOSE'].loc[(i-19):i].mean()
#            tmp_avg5_close = single_stock['CLOSE'].loc[(i-4):i].mean()
#            value120_line.loc[i] = tmp_avg120_close
#            value60_line.loc[i] = tmp_avg60_close
#            value20_line.loc[i] = tmp_avg20_close
#            value5_line.loc[i] = tmp_avg5_close
#        print("end - make line")
#        if ((j >= 200) and (j < (single_stock_len-31))):
#            open =  single_stock['Open'].loc[j]
#            close = single_stock['CLOSE'].loc[j]
#            high =  single_stock['High'].loc[j]
#            low  =  single_stock['Low'].loc[j]
#            volume = single_stock['Volume'].loc[j]
#            past_volume10 = single_stock['Volume'].loc[(j-10):(j-3)].mean()
#            past_volume3 = single_stock['Volume'].loc[(j-2):j].mean()
#            past_close10 = single_stock['CLOSE'].loc[(j-10):(j-1)].mean()
#            if ((j >= 500)):
#                max_value = single_stock['High'].loc[(j-500):j].max()
#            else:
#                max_value = single_stock['High'].loc[0:j].max()
#            next_volume = single_stock['Volume'].loc[(j+1)]
#            volume_rate = volume / past_volume10
#            date = single_stock['Date'].loc[j]
#            value120 = value120_line['CLOSE'].loc[j]
#            value60  = value60_line['CLOSE'].loc[j]
#            value20  = value20_line['CLOSE'].loc[j]
#            value5   = value5_line['CLOSE'].loc[j]
##            rand_int = random.randint(1,100)
#            #if (rand_int == 1):
#            #if ((volume_rate >= 10) and (volume > (avg_volume * 5))):
#            descending_chk = descending_chk(value60_line,value120_line,j)
#            big_deal_chk = big_deal_chk(max_value,past_close10,2)
#            volume_chk = volume_chk(past_volume3,past_volume10)
#            touch_line120_chk = touch_line120_chk(high,value120)
#            reverse_array_chk = reverse_array_chk(value60_line,value120_line,j)
#            exceed_5_20_line_chk = exceed_5_20_line_chk(value5_line,value20_line,j)
#            if ((descending_chk == "1") and (big_deal_chk == "1") and (volume_chk == "1") and (touch_line120_chk == "1") and (reverse_array_chk == "1") and (exceed_5_20_line_chk == "1")):
#                df2 = pd.DataFrame(data=[[com_name, i, date, open, close, high, low, volume]], columns=['NAME','CODE','DATE','OPEN','CLOSE','HIGH','LOW','VOLUME'])
#                df = df.append(df2)
#df.to_csv("tmp.csv", encoding='CP949', mode='w')
#time.sleep(10)
#tmp_stocks = pd.read_csv('tmp.csv', encoding='CP949')
#tmp_df = tmp_stocks[tmp_stocks.columns.difference(['NAME','CODE','DATE'])]
#all_mean = tmp_df.mean()
#all_mean_data = pd.DataFrame(data=all_mean)
#tmp_df_t = all_mean_data.T
#print(tmp_df_t)
#df3 = tmp_stocks.append(tmp_df_t, ignore_index=True)
##df = pd.concat([df,tmp_df_t])
#name = sys.argv[0].split('.')[0]
#name_ext = name + '.' + 'csv'
#df3.to_csv(name_ext, encoding='CP949', mode='w')
#
#