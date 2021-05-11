from bs4 import BeautifulSoup
import requests
import pandas as pd


class T_Product:

    def __init__(self):
        self.url_list=[]
        
        self.link='https://www.trendyol.com'
        self.kargo=False
        self.first_prc=''
        self.second_prc=''
        self.ProductDscPrice=''
        self.data={
                'Product_Name':[],
                'Product_Brand':[],
                'Product_Free_Shipping':[],
                'Product_Org_Price':[],
                'Product_Dsc_Price':[],
                'Product_Cart_Price':[],
                'Product_insize':[],
                'Product_outsize':[],
                'Product_Ratings':[],
                'Product_img_url':[]
            }

    def search(self,ara):
        self.url_list=[]
        self.ara=ara
        search_link=self.link+'/sr?q='+self.ara
        
        r=requests.get(search_link)
        soup=BeautifulSoup(r.content,'html.parser')
        soup.find_all('div',class_='p-card-wrppr')
        for links in soup.find_all('div',class_='p-card-wrppr'):
            url=links.a.get('href')           
            self.url_list.append(url)
        


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
        
        # Ürün İsmi
        #Product Name
        self.ProductName=soup.find('div',class_='pr-in-cn').span.text
        print(self.ProductName)

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
        if soup.find('div',class_='pr-in-at-sp'):
            self.inSize=[]
            self.outSize=[]
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


    def CreateFrame(self):
        
        for i in self.url_list:
           
            self.data['Product_Name'].append(self.ProductName)
            self.data['Product_Brand'].append(self.marka)
            self.data['Product_Free_Shipping'].append(self.kargo)
            self.data['Product_Org_Price'].append(self.first_prc)
            self.data['Product_Dsc_Price'].append(self.second_prc)
            self.data['Product_Cart_Price'].append(self.ProductDscPrice)
            self.data['Product_insize'].append(self.inSize)
            self.data['Product_outsize'].append(self.outSize)
            self.data['Product_Ratings'].append(self.ProductRatings)
            self.data['Product_img_url'].append(self.img_url)

        self.df=pd.DataFrame(self.data)




# Search bar Testing

# test=T_Product()
# test.search('Tişört')

# After Searching, scraping for all urls

# for i in test.url_list:
#     test.ProductDetail(i)

# scraping for Single Product

# test.ProductDetail('https://www.trendyol.com/trendyolmilla/beyaz-kolsuz-basic-orme-t-shirt-twoss20ts0021-p-35503716?boutiqueId=568034&merchantId=968')


# Create DataFrame from single or all products


# test.CreateFrame()


