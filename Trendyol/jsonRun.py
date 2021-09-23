import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

from Trendyol import Json_class as js 

import pandas as pd
import time,datetime



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
        data.run(i,3)
        df=pd.DataFrame.from_dict(data.product)
    try:
        df.drop_duplicates(subset=['P_id'],inplace=True)

    except:
        print('Error',i)


add() 

df
df.to_sql('JsonProduct',engine,if_exists='append',index=False)


