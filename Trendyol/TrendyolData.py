from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, time







class T_Product:

    def __init__(self):
        self.url_list=[]
        
        self.link='https://www.trendyol.com'
        self.kargo=False
        self.first_prc=''
        self.second_prc=''
        self.ProductDscPrice=''
        self.Product_No=''
        self.data={
                'Product_No':[],
                'Product_BreadCrum':[],
                'Product_MinCatagory':[],
                'Add_date':[],
                'Product_Name':[],
                'Product_Brand':[],
                'Product_Free_Shipping':[],
                'Product_Org_Price':[],
                'Product_Dsc_Price':[],
                'Product_Cart_Price':[],
                'Product_insize':[],
                'Product_outsize':[],
                'Product_Ratings':[],
                'Product_url':[],
                'Product_img_url':[],
                
            }

    # Anahtar Kelime Arama 

    def search(self,ara,i=1):
        self.url_list=[]
        self.ara=ara

        for j in range(0,i+1):
            search_link=self.link+'/sr?q='+self.ara+'&pi='+str(j)
        
            r=requests.get(search_link)
            soup=BeautifulSoup(r.content,'html.parser')
        
            for links in soup.find_all('div',class_='p-card-wrppr'):
                url=links.a.get('href')           
                self.url_list.append(url)
        


    #Sayfada ki ürünlerin bilgilerini parse etme

    def ProductDetail(self,product):
        #Trendyol Linki girilirse boşlukla değiştiriyor
        # If Trendyol Link is entered, it replaces it with a space.
        
        product=product.replace('https://www.trendyol.com','')
        self.product_link=self.link+product
        if self.url_list==[]:
            self.url_list.append(self.product_link)
        print('Ürün Linki',self.product_link)
        
        
        #requests ve soup işlemleri
        #requests and soup operations
        r=requests.get(self.product_link)
        soup=BeautifulSoup(r.content,'html.parser')
        

        #Product_No

        lhs,rhs=self.product_link.split('-p-',1)
        if len(rhs.split('-p-',1))>1 :
            rhs=rhs.split('-p-',1)[1]
            self.Product_No=rhs.split('?')[0]
            print("Product No : ",self.Product_No)
        else:
            self.Product_No=rhs.split('?')[0]
            print("Product No : ",self.Product_No)



        #Product BreadCrum
        self.Product_BreadCrum=[]
        if soup.find_all('div',class_='breadcrumb full-width'):
            for i in soup.find_all('div',class_='breadcrumb full-width'):
                for j in range(0,len(i.find_all('span'))):
                    self.Product_BreadCrum.append(i.find_all('span')[j].text)
            if soup.find('div',class_='pr-in-cn').a:
                self.Product_BreadCrum=self.Product_BreadCrum[:-1]
            print('Product_BreadCrum : ',self.Product_BreadCrum)

        #En alt Kategori
        if len(self.Product_BreadCrum)>0:
            self.Product_MinCatagory=self.Product_BreadCrum[-1]
            print('Product_MinCatagory : ', self.Product_MinCatagory)


        # Ürün İsmi
        #Product Name
        self.ProductName=soup.find('div',class_='pr-in-cn').span.text
        print(self.ProductName)


        #EKlenme Tarihi
        now=datetime.now()
        self.now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        

        #Kargo Ücretsiz mi sorgusu
        # Free Shipping query
        if soup.find('div',class_='stamps').text:
            self.kargo=True
            print(self.kargo,soup.find('div',class_='stamps').text)
        else:
            self.kargo=False
            print(self.kargo,'KARGO BEDAVA DEĞİL')

        # Ürün Yıldız Sayısı
        # Product Ratings
        if soup.find('div',class_='pr-in-rnr'):
            self.ProductRatings=soup.find('div',class_='ttl').span.text     
            print(self.ProductRatings)
        else:
            self.ProductRatings=''
            print('Henüz Yorum Yok')

        # Ürünün ilk fiyatı indirimli fiyatı     
        # Product original price and discounted price  
        self.ProductOrginalPrice=soup.find('div',class_='pr-bx-nm').find_all('span')
        for i in self.ProductOrginalPrice:
            if i['class'][0]=='prc-org':
                self.first_prc=i.text
                
                print('ilk fiyat',self.first_prc)
            elif i['class'][0]=='prc-slg':
                self.second_prc=i.text
                print('ikinci fiyat',self.second_prc)
        
        # Sepetteki İndirim oranı ve sepetteki indirimli fiyat
        # if there is discount in cart 
        # discount ratio and discounted price
        if soup.find('div',class_='pr-bx-dsc'):
            self.DscRatio=soup.find('div',class_='pr-bx-pr-dsc').div.text
            print(self.DscRatio)
            self.ProductDscPrices=soup.find('div',class_='pr-bx-pr-dsc').find_all('span')
            for i in self.ProductDscPrices:
                self.ProductDscPrice=i.text
                print('DSC PRİCE',i.text)
       
        # ürün beden bilgisi
        # Product size
        self.inSize=[]
        self.outSize=[]
        if soup.find('div',class_='pr-in-at-sp'):
            
            elemnt_size=soup.find('div',class_='pr-in-at-sp').find_all('div',class_='sp-itm')
            element_outSize=soup.find('div',class_='pr-in-at-sp').find_all('div',class_='so')
            for i in elemnt_size:
                self.inSize.append(i.text)
            for i in element_outSize:
                self.outSize.append(i.text)
                if i.text in self.inSize:
                    self.inSize.remove(i.text)
            
            print('olmayan Bedenler:',self.outSize)
            print('Olan Bedenler :',self.inSize)

        # Ürün Marka bilgisi
        # Product Brand 
        if soup.find('h1',class_='pr-new-br'):
            self.marka=soup.find('h1',class_='pr-new-br').text
            span=soup.find('h1',class_='pr-new-br').span.text
            self.marka=self.marka.replace(span,'')    

        # ürün resim url
        #Product image urls
        if soup.find('img',class_='ph-gl-img'):
            self.img_url=soup.find('img',class_='ph-gl-img')['src']
            print('img_url',self.img_url)
        else:
            self.img_url=''
        
        



     # DataFrame Oluşturma

    def CreateFrame(self):
        
        self.data['Product_No'].append(self.Product_No)
        self.data['Add_date'].append(self.now_str) 
        self.data['Product_Name'].append(self.ProductName)
        self.data['Product_BreadCrum'].append(self.Product_BreadCrum)
        self.data['Product_MinCatagory'].append(self.Product_MinCatagory)
        self.data['Product_Brand'].append(self.marka)
        self.data['Product_Free_Shipping'].append(self.kargo)
        self.data['Product_Org_Price'].append(self.first_prc)
        self.data['Product_Dsc_Price'].append(self.second_prc)
        self.data['Product_Cart_Price'].append(self.ProductDscPrice)
        self.data['Product_insize'].append(self.inSize)
        self.data['Product_outsize'].append(self.outSize)
        self.data['Product_Ratings'].append(self.ProductRatings)
        self.data['Product_url'].append(self.product_link)
        self.data['Product_img_url'].append(self.img_url)

        self.df=pd.DataFrame(self.data)




    def start(self):
        for i in self.url_list:
            self.ProductDetail(i)
            self.CreateFrame()
            self.first_prc=''
            self.second_prc=''
            self.ProductDscPrice=''
            



class Clean:
    
    def __init__(self):
        self.test=T_Product()
        
    def run(self,a,i=1):

        try:   
            self.test.search(a,i)
            self.test.start()
            self.data=self.test.df
        except:
            pass
        
    def clean_df(self):

        for i in self.data.columns:
            try:               
                self.data[i] = self.data[i].apply(lambda y: np.nan if len(y)==0 else y)
                if i=='Add_date':
                    self.data[i]=self.data[i].astype(datetime)                                
                if i!='Product_insize' and i!='Product_outsize' and i!='Product_BreadCrum' and i!='Add_date':
                    self.data[i]=self.data[i].str.replace('.', '',regex=True)
                    self.data[i]=self.data[i].replace(r'^\s*$', np.NaN, regex=True)
                    self.data[i]=self.data[i].str.replace(' TL', '')    
                    self.data[i]=self.data[i].str.replace(',', '.')
                    self.data[i]=self.data[i].astype(float)
            except:
                pass
                
        
        
        
