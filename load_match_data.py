'''
Created on Jan 30, 2016
@author: hanhanwu
The data set are .csv files
The last digit in each row of matchmaker.csv indicates whether the 2 people matched.
Plot the agesonly .csv into scatter plot
'''
from pylab import *

def load_csv(file_path, all_num=False):
    rws = []
    for l in file(file_path):
        rw = l.split(',')
        rws.append(matchrow(rw, all_num))
    return rws

#plot men's ages versus women's ages, match shows red o, mismatch shows green +
def plotagematches(rows):
    xm = [r.data[0] for r in rows if r.match == 1]
    ym = [r.data[1] for r in rows if r.match == 1]
    
    xn = [r.data[0] for r in rows if r.match == 0]
    yn = [r.data[1] for r in rows if r.match == 0]
    
    plot(xm, ym, 'ro')
    plot(xn, yn, 'g+')
    
    show()
    

class matchrow:
    def __init__(self, rw, all_num=False):
        if all_num == True:
            self.data = [float(rw[i]) for i in range(len(rw))]
        else:
            self.data = rw
        self.match = int(rw[len(rw)-1])
            

def main():
    agesonly_path = '[your own agesonly.csv path]'    # download agesonly.csv and change to your own path
    matchmaker_path = '[your own matchmaker.csv path]'  #  # download matchmaker.csv and change to your own path
    
    agesonly_rows = load_csv(agesonly_path, True)
    matchmaker_rows = load_csv(matchmaker_path)
    
    print len(agesonly_rows)
    print agesonly_rows[0].data
    print agesonly_rows[0].match
    
    print len(matchmaker_rows)
    print matchmaker_rows[0].data
    print matchmaker_rows[0].match
    
    # I am wondering whether the data is all from white people (just kidding)
    plotagematches(agesonly_rows)
    
if __name__ == '__main__':
    main()
