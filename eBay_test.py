'''
Created on Jan 23, 2016
@author: hanhanwu
Note: have to use eBay Product AppID here, NOT the Sandbox AppID
'''
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json

def get_categories(appid, keyword):
    try:
        api = Connection(appid=appid, config_file=None)
        response = api.execute('findItemsAdvanced', {'keywords': keyword}).json()
        
        item_dict = json.loads(response)
        items = item_dict['searchResult']['item']
        categories = {}
        for item in items:
            c_id = item['primaryCategory']['categoryId']
            c_name = item['primaryCategory']['categoryName']
            categories.update({c_id: c_name})
               
        print len(categories)
        for k,v in categories.items():
            print k, v
    
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
    
def main():
    # check the categories for keyword 'wine', because it may return other items relate to wine but not wine
    appid = '[Your eBay Product AppID]'  # Change this to your eBay product AppID
    search_keyword = 'wine'
    get_categories(appid, search_keyword)
    
if __name__ == '__main__':
    main()
    

    

