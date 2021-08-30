import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

import TrendyolData 




pgconn=psycopg2.connect(
    host="localhost",
    port="5432",
    database="trendyol",
    user="postgres",
    password="admin"
)

pgcursor=pgconn.cursor()



engine=create_engine('postgresql+psycopg2://postgres:1994Fikret@localhost/trendyol')





# Example search keyword

keywords=['erkek','kadın','tişört','pantolon','ceket','çocuk','mutfak','banyo','bahçe','elbise','araba','termos','elektronik',
'market','ayakkabı','mobilya','bardak','kitap','çorap','aksesuar','tencere','halı','tabak']




exe=TrendyolData.Clean()

# Run Function

def add():

    for i in keywords:
        exe.run(i,2)
        exe.clean_df()
    try:
        exe.data.to_sql('Product',engine,if_exists='append',index=False)
    except:
        pass

add()