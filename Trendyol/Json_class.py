from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

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


    
    
    def search(self,ara,i=1):
        self.ara=ara
        

        for j in range(0,i+1):
            search_link=self.link+'/sr?q='+self.ara+'&pi='+str(j)
    
            r=requests.get(search_link)
            soup=BeautifulSoup(r.content,'lxml')

        self.data = str(soup.find('script', type='application/javascript'))
        self.data=self.data.replace('<script type="application/javascript">window.__SEARCH_APP_INITIAL_STATE__=','')
        self.data=self.data.replace(';window.slpName=\'\';window.TYPageName=\'product_search_result\';window.isSearchResult=true;window.pageType="search";</script>','')

        self.data=json.loads(self.data)

        for i in range(0,24):
            self.id.append(self.data['products'][i]['id'])
            self.name.append(self.data['products'][i]['name'])
            self.images.append(self.data['products'][i]['images'][0])
            self.brand.append(self.data['products'][i]['brand']['name'])
            self.ratingscore.append(self.data['products'][i]['ratingScore']['averageRating'])
            self.totalcount.append(self.data['products'][i]['ratingScore']['totalCount'])
            self.categoryHierarchy.append(self.data['products'][i]['categoryHierarchy'])
            self.categoryId.append(self.data['products'][i]['categoryId'])
            self.categoryName.append(self.data['products'][i]['categoryName'])
            self.url.append(self.data['products'][i]['url'])
            self.sellingPrice.append(self.data['products'][i]['price']['sellingPrice'])
            self.originalPrice.append(self.data['products'][i]['price']['originalPrice'])
            self.discountedPrice.append(self.data['products'][i]['price']['discountedPrice'])
            self.freeCargo.append(self.data['products'][i]['freeCargo'])


        self.product={
            'id':self.id,
            'name':self.name,
            'images':self.images,
            'brand':self.brand,
            'ratingscore':self.ratingscore,
            'totalcount':self.totalcount,
            'categoryHierarchy':self.categoryHierarchy,
            'categoryId':self.categoryId,
            'categoryName':self.categoryName,
            'url':self.url,
            'sellingpPice':self.sellingPrice,
            'originalPrice':self.originalPrice,
            'discountedPrice':self.discountedPrice,
            'freeCargo':self.freeCargo
        }


    def run(self,key,i):
        self.__init__()
        for j in range(1,i+1):
            self.search(key,j)


# k=data_parser()

# k.search('tişört',2)

# k.product

# pp=pd.DataFrame.from_dict(k.product)

# pp.info()

# pp.head()

# for i in range(1,3):
#     k.search('tişört',i)

# pp['ratingscore'].round(1)

# k.run('tişört',2)
