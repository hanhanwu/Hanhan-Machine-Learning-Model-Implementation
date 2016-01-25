'''
Created on Jan 23, 2016
@author: hanhanwu
Note: have to use eBay Product AppID here, NOT the Sandbox AppID
'''

import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import KNN
import json
import optimization

def get_items(appid, search_keyword, categoryId):
    results = []
    try:
        api = Connection(appid=appid, config_file=None)
        response = api.execute('findItemsAdvanced', {'keywords': search_keyword}).json()

        item_dict = json.loads(response)
        items = item_dict['searchResult']['item']
        
        for item in items:
            c_id = item['primaryCategory']['categoryId']
            if c_id != categoryId:
                continue
            autoPay = bool_to_bit(item['autoPay'])
            currentPrice = float(item['sellingStatus']['currentPrice']['value'])
            condition = float(item['condition']['conditionId'])
            results.append({'input': (autoPay, condition), 'price': currentPrice})
            
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        
    return results
        

def bool_to_bit(v):
    if v.lower() == 'false':
        return 1
    else:
        return 2


def main():
    appid = '[Your eBay Product AppID]'  # Change this to your eBay product AppID
    search_keyword = 'wine'
    categoryId = '38182'  # red wine
    
    items = get_items(appid, search_keyword, categoryId)
    
    # using un-weighted KNN
    print 'using un-weighted KNN:'
    print KNN.get_KNN(items, (1,1000), k = 3)
    print KNN.get_KNN(items, (2,2000), k = 3)
    print '*********************'
    
    # using weighted KNN
    print 'weighted KNN using Gaussian function:'
    print KNN.get_weightedKNN(items, (1,1000), k = 3)
    print KNN.get_weightedKNN(items, (2,1000), k = 3)
    print KNN.get_weightedKNN(items, (2,2000), k = 3)
    
    
if __name__ == '__main__':
    main()
