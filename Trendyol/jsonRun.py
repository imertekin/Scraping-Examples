import psycopg2
from psycopg2 import sql
from requests.api import request
from sqlalchemy import create_engine

import requests

from Trendyol import Json_class as js 

import pandas as pd
import time,datetime

from slugify import slugify

pgconn=psycopg2.connect(
    host="localhost",
    port="5432",
    database="trendyol",
    user="postgres",
    password="admin"
)

pgcursor=pgconn.cursor()



engine=create_engine('postgresql+psycopg2://postgres:admin@localhost/trendyol')





# Example search keyword

words=[]

with open('word.txt', 'r') as f:
    for line in f:
        words.append(line.replace('\n',""))



data=js.data_parser()

def add():
    global df
    for i in words:
        try:
            data.run(i,3)
            df=data.data
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            continue
        try:
            df.drop_duplicates(subset=['P_id'],inplace=True)
        
        except:
            print('Error ',i)


add() 

df.to_sql('JsonProduct',engine,if_exists='append',index=False)


