import os
from os.path import join, dirname
import eel
import requests
from time import sleep
import pandas as pd
import numpy as np
import urllib.parse
from dotenv import load_dotenv
from time import sleep
from logger import set_logger
logger = set_logger(__name__)

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


yahoo_app_id = os.environ.get("YAHOO_APP_ID")




def fetch_item_from_item_name(item_name_str):
    item_name_list = item_name_str.splitlines()
    item_list = []
    eel.view_log_js('商品情報取得中...')
    for item_name in item_name_list:
        item_name = urllib.parse.quote(item_name)
        request_url = f'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid={yahoo_app_id}&query={item_name}&results=50&start=1&sort=-score'
        sleep(1)
        r = requests.get(request_url)
        resp = r.json()
        total_req_count = 20
        page_item = resp['totalResultsReturned']
        for count in range(total_req_count):
            start = count*50+1
            try:            
                if count != 0 and count != 19:
                    request_url = f'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid={yahoo_app_id}&query={item_name}&results=50&start={start}&sort=-score'
                    r = requests.get(request_url)
                    sleep(1)
                    resp = r.json()
                elif count == 19:
                    request_url = f'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid={yahoo_app_id}&query={item_name}&results=50&start=950&sort=-score'
                    r = requests.get(request_url)
                    sleep(1)
                    resp = r.json()                    
                for i in range(page_item):
                    try:
                        name = resp['hits'][i]['name']
                        price = resp['hits'][i]['price']
                        code = resp['hits'][i]['code']
                        data =[name,price,code]            
                        item_list.append(data)
                    except Exception as e:
                        logger.info(e)
            except Exception as e:
                logger.info(e)
                eel.view_log_js('エラー発生 処理を中断します')

    yahoo_item_df = pd.DataFrame(item_list,columns=['商品名','価格','SKU'])
    yahoo_item_df.index = np.arange(1,len(yahoo_item_df)+1)
    yahoo_item_df.to_csv("yahoo_item_name.csv",encoding='utf_8-sig') 
    eel.view_log_js('完了')


def fetch_item_from_seller_id(seller_id_str):
    seller_id_list = seller_id_str.splitlines()
    item_list = []
    eel.view_log_js('商品情報取得中...')
    for seller_id in seller_id_list:
        request_url = f'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid={yahoo_app_id}&seller_id={seller_id}&results=50&start=1&sort=-score'
        sleep(1)
        r = requests.get(request_url)
        resp = r.json()
        total_req_count = 20
        page_item = resp['totalResultsReturned']
        for count in range(total_req_count):
            start = count*50+1
            try:            
                if count != 0 and count != 19:
                    request_url = f'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid={yahoo_app_id}&seller_id={seller_id}&results=50&start={start}&sort=-score'
                    r = requests.get(request_url)
                    sleep(1)
                    resp = r.json()
                elif count == 19:
                    request_url = f'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid={yahoo_app_id}&seller_id={seller_id}&results=50&start=950&sort=-score'
                    r = requests.get(request_url)
                    sleep(1)
                    resp = r.json()                    
                for i in range(page_item):
                    try:
                        item_name = resp['hits'][i]['name']
                        price = resp['hits'][i]['price']
                        code = resp['hits'][i]['code']
                        data =[item_name,price,code]            
                        item_list.append(data)
                    except Exception as e:
                        pass
            except Exception as e:
                logger.info(e)
                eel.view_log_js('エラー発生 処理を中断します')

    yahoo_item_df = pd.DataFrame(item_list,columns=['商品名','価格','SKU'])
    yahoo_item_df.index = np.arange(1,len(yahoo_item_df)+1)
    yahoo_item_df.to_csv("yahoo_seller_id.csv",encoding='utf_8-sig')
    eel.view_log_js('完了')





if __name__ == "__main__":
    fetch_item_from_item_name()
