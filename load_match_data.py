'''
Created on Jan 30, 2016
@author: hanhanwu
The data set are .csv files
The last digit in each row of matchmaker.csv indicates whether the person is a good match... (how come they label people in this way)
'''

def load_csv(file_path, all_num=False):
    rws = []
    for l in file(file_path):
        rw = l.split(',')
        rws.append(matchrow(rw, all_num))
    return rws
    

class matchrow:
    def __init__(self, rw, all_num=False):
        if all_num == True:
            self.data = [float(rw[i]) for i in range(len(rw))]
        else:
            self.data = rw
        self.is_good_match = int(rw[len(rw)-1])
            

def main():
    agesonly_path = '[your agesonly.csv path]'    # download agesonly.csv and change to your own path
    matchmaker_path = '[your matchmaker.csv path]'  #  # download matchmaker.csv and change to your own path
    
    agesonly_rows = load_csv(agesonly_path, True)
    matchmaker_rows = load_csv(matchmaker_path)
    
    print len(agesonly_rows)
    print agesonly_rows[0].data
    print agesonly_rows[0].is_good_match
    
    print len(matchmaker_rows)
    print matchmaker_rows[0].data
    print matchmaker_rows[0].is_good_match
    
if __name__ == '__main__':
    main()
