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

price = 107234
new_price = price * 1.324
print("new_price : ", new_price)
if (price < 100):
    unit = 0.1
    print("price is under 100")
elif (price >= 100) and (price < 1000):
    print("price is 100 ~ 1000")
    unit = 1
elif (price >= 1000) and (price < 10000):
    print("price is 1000 ~ 10000")
    unit = 5
elif (price >= 10000) and (price < 100000):
    print("price is 10000 ~ 100000")
    unit = 10
elif (price >= 100000) and (price < 1000000):
    print("price is 10000 ~ 100000")
    unit = 50
elif (price >= 1000000) and (price < 10000000):
    print("price is 10000 ~ 100000")
    unit = 500

new_price_mod = new_price//unit * unit
print("new_price_mod : ", new_price_mod)
