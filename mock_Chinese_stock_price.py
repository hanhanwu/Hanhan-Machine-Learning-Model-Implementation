'''
Created on Jan 7, 2016
@author: hanhanwu
Chinese stock market is funny, when the price goes up to a certain time, it will drop dramatically
In this file, I am going to create a mock-up Chinese stock price data
'''
from random import random, randint

# rating simply represents the investment of a stock, rating will be in range [1 10]
# age indicates the years when a company appear in the stock market
# duration is calculated from last price bottom till now
def get_stock_price(rating, age, duration):
    # suppose more investment, longer age has longer price_peak_time
    price_peak_time = 7 + 0.8*rating + 0.2*age
    
    price = rating*0.5
    
    # when passed the peak time, price will start to drop
    if duration > price_peak_time:
        price = price*(5-(duration-price_peak_time))
    else:
        price = price*(5+(price_peak_time- duration))
        
    if price < 0:
        price = 0
        
    return price


def get_stockset():
    stocks = []
    
    # randomly create 500 stocks
    for i in range(500):
        rating = randint(1, 10)
        age = randint(1, 20)
        duration = randint(1, 50)
        
        price = get_stock_price(rating, age, duration)
        # add some noise
        price *= (random()*0.4 + 0.8)
        
        stocks.append({'input': (rating, age, duration), 'price': price})
        
    return stocks
    

def main():
    print get_stock_price(9, 2, 10)
    print get_stock_price(2, 30, 3)
    print get_stock_price(5, 7, 20)
    
    print get_stockset()[0]
    print get_stockset()[3]
    
if __name__ == '__main__':
    main()
