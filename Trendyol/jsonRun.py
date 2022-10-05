import psycopg2
from psycopg2 import sql
from requests.api import request
from sqlalchemy import create_engine
import requests
import pandas as pd
import time,datetime
from slugify import slugify
from dotenv import load_dotenv
import os

from Trendyol import Json_class as js 


load_dotenv()


pgconn=psycopg2.connect(
    host = os.environ.get("HOST"),
    port = os.environ.get("PORT"),
    database = os.environ.get("DATABASE"),
    user = os.environ.get("USER"),
    password = os.environ.get("PASSWORD")
)

pgcursor=pgconn.cursor()



engine=create_engine(f'postgresql+psycopg2://{os.environ.get("USER")}:{os.environ.get("PASSWORD")}@localhost/trendyol')





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


