'''
Created on Oct 24, 2016

I'm trying to implement a decision tree,
since it is an easy but useful classification tool, understanding its basic algorithm is helpful
CART - chooses the best variable to divide up the data in each step
'''

class decision_node:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col                       # column index of the criteria to be tested
        self.value = value                   # the value that the column needs to match to get the TRUE result
        self.results = results               # results for the branch, it will be None except for end nodes
        self.fb = fb                         # child node if it's FALSE
        self.tb = tb                         # child node if it's TRUE


def divide_data(rows, col, value):
    split_function = None
    
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[col] >= value    # Python lambda is a type of function
    else:
        split_function = lambda row: row[col] == value
        
    st1 = [row for row in rows if split_function(row)]
    st2 = [row for row in rows if not split_function(row)]
    
    return st1, st2


# TO BE CONTINUED...
