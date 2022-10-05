from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import datetime
from slugify import slugify


class data_parser:

    def __init__(self):

        self.link='https://www.trendyol.com'
        self.id=list()
        self.name=list()
        self.images=list()
        self.brand=list()
        self.ratingscore=list()
        self.totalcount=list()
        self.categoryHierarchy=list()
        self.categoryId=list()
        self.categoryName=list()
        self.url=list()
        self.sellingPrice=list()
        self.originalPrice=list()
        self.discountedPrice=list()
        self.freeCargo=list()
        self.added_time=list()


    
    
    def search(self,ara,i=1):
        self.ara=ara
        

        for j in range(0,i+1):
            search_link=self.link+'/sr?q='+self.ara+'&pi='+str(j)
    
            r=requests.get(search_link)
            soup=BeautifulSoup(r.content,'lxml')
        self.data = str(soup.find_all('script', type='application/javascript')[2])
        self.data=self.data.replace('<script type="application/javascript">window.__SEARCH_APP_INITIAL_STATE__=','')
        self.data=self.data.replace(';window.slpName=\'\';window.TYPageName=\'product_search_result\';window.isSearchResult=true;window.pageType="search";</script>','')

        self.data=json.loads(self.data)
        for i in range(0,len(self.data['products'])):
            try:
                self.id.append(self.data['products'][i]['id'])
            except:
                self.id.append(None)

            self.name.append(self.data['products'][i]['name'])
            self.images.append(self.data['products'][i]['images'][0])
            self.brand.append(self.data['products'][i]['brand']['name'])
            try:
                self.ratingscore.append(self.data['products'][i]['ratingScore']['averageRating'])
                self.totalcount.append(self.data['products'][i]['ratingScore']['totalCount'])
            except:
                self.ratingscore.append(None)
                self.totalcount.append(None)

            self.categoryHierarchy.append(self.data['products'][i]['categoryHierarchy'])
            self.categoryId.append(self.data['products'][i]['categoryId'])
            self.categoryName.append(self.data['products'][i]['categoryName'])
            self.url.append(self.data['products'][i]['url'])
            self.sellingPrice.append(self.data['products'][i]['price']['sellingPrice'])
            self.originalPrice.append(self.data['products'][i]['price']['originalPrice'])
            self.discountedPrice.append(self.data['products'][i]['price']['discountedPrice'])
            self.freeCargo.append(self.data['products'][i]['freeCargo'])
            self.added_time.append(str(datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S")))


        self.product={
            'P_id':self.id,
            'name':self.name,
            'images':self.images,
            'brand':self.brand,
            'ratingScore':self.ratingscore,
            'totalCount':self.totalcount,
            'categoryHierarchy':self.categoryHierarchy,
            'categoryId':self.categoryId,
            'categoryName':self.categoryName,
            'url':self.url,
            'sellingpPice':self.sellingPrice,
            'originalPrice':self.originalPrice,
            'discountedPrice':self.discountedPrice,
            'freeCargo':self.freeCargo,
            'addedTime':self.added_time
        }


    def run(self,key,i=1):
        
        for j in range(1,i+1):
            self.search(key,j)

        self.data=pd.DataFrame.from_dict(self.product)
        self.data['addedTime']=pd.to_datetime(self.data['addedTime'])
        self.data['ratingScore']=self.data['ratingScore'].round(2)
        self.data['slug']=pd.Series(slugify(i) for i in self.data['categoryName'])
       


k=data_parser()

k.run('tişört')
