'''
Created on Oct 24, 2016

I'm trying to implement a decision tree,
since it is an easy but useful classification tool, understanding its basic algorithm is helpful
CART - chooses the best variable to divide up the data in each step
In order to choose the best variable each step, the divided 2 sets should have least mixed situations
To measure how mixed a set is, we use Gini Impurity or Entropy
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


# for each set of data, count distinct labels, to help find the best variable
def count_label(rows):
    labels = {}
    for r in rows:
        l = r[-1]
        labels.setdefault(l, 0)
        labels[l] += 1
    return labels


# Variable Choose Measure 1 - Gini Impurity, the probability of putting an item to the wrong set. 
## 0 means the same, higher more mixed
def gini_impurity(rows):
    lbs = count_label(rows)
    total_items = len(rows)
    gi = 0
    for l1, ct1 in lbs.items():
        p1 = float(ct1)/total_items
        for l2, ct2 in lbs.items():
            if l1 == l2: continue
            p2 = float(l2)/total_items
            gi += p1*p2
            
    return gi
        

# Variable Choose Measure 2 - Entropy, calculate how mixed the set is/how different the outcomes are different from each other
## 0 means the same, higher more mixed
def entropy(rows):
    log2 = lambda x: log(x)/log(2)
    lbs = count_label(rows)
    total_items = len(rows)
    ep = 0.0
    
    for ct in lbs.values():
        p = float(ct)/total_items
        ep -= p*log2(p)
        
    return ep
        
    
# TO BE CONTINUED...
