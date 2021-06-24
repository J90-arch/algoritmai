#open_hours.py

from datetime import datetime
from datetime import date

import pytz

import tensorflow as tf
import numpy as np

def is_open():

    est = pytz.timezone('est')

    def is_weekend():
        today = datetime.now(est)
        weekday = today.weekday()
        if weekday >= 5: return True
        else: return False


    def is_pre_market_open():
        start = datetime.now(est).replace(hour=12, minute=00, second=00, tzinfo=est)
        end = datetime.now(est).replace(hour=13, minute=30, second=00, tzinfo=est)
        now = datetime.now(est).replace(tzinfo=est)

        if end >= now >= start: return True
        else: return False

    def is_post_market_open():
        start = datetime.now(est).replace(hour=20, minute=00, second=00, tzinfo=est)
        end = datetime.now(est).replace(hour=22, minute=30, second=00, tzinfo=est)
        now = datetime.now(est).replace(tzinfo=est)

        if end >= now >= start: return True
        else: return False

    def is_market_open():
        start = datetime.now(est).replace(hour=13, minute=30, second=00, tzinfo=est)
        end = datetime.now(est).replace(hour=20, minute=00, second=00, tzinfo=est)
        now = datetime.now(est).replace(tzinfo=est)

        if end >= now >= start: return True
        else: return False

    def is_holiday():
        today = datetime.now(est)
        today = str(today)
        today = today[5:10]
        if today == "02-15":
            return True
        elif today == "04-02":
            return True
        elif today == "05-31":
            return True
        elif today == "07-05":
            return True
        elif today == "09-06":
            return True
        elif today == "11-25":
            return True
        elif today == "12-24":
            return True
        else: return False

    if is_weekend():
        print ("market is closed, because it's the end of the week")
        return False
    elif is_holiday():
        print ("market is closed, because it's a NYSE holiday")
        return False
    else:
        if is_pre_market_open():
            #print ("pre market is open")
            print ("market is closed")
            return False
        elif is_post_market_open():
            #print ("post market is open")
            print ("market is closed")
            return False
        elif is_market_open():
            #print ("market is open")
            return True
        else:
            print ("market is closed")
            return False

# print(is_open())