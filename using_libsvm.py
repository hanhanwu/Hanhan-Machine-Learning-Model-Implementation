'''
Created on Feb 9, 2016
@author: hanhanwu
Most of the code here should be operated in the terminal, under the libsvm/python path
'''
import preprocess_data
import load_match_data

# using agesonly.csv
# Step1. the output into terminal, type "matches, features = [your output]"
agesonly_path = '[change to your agesonly.csv path]'  # change to your agesonly.csv path
agesonly_rows = load_match_data.load_csv(agesonly_path, True)
matches = []
features = []
 
for r in agesonly_rows:
    matches.append(r.match)
    features.append(r.data)
 
print matches,',',features
 
 
# Step2. In the terminal, type following code line by line
from svmutil import *
prob = svm_problem(matches, features)
pm_ages = svm_parameter('-t 2')  # indicates using radial-basis function
m = svm_train(prob, pm_ages)
# [1] is the the ground truth, used for calculating the accuracy ; [28.0, 26.0] is the new point
p_labels, p_acc, p_vals = svm_predict([1], [[28.0, 26.0]], m) 


# using matchmaker.csv
# Step1. the output into terminal, type "matches, features = [your output]"
matchmaker_path = '[your matchmaker.csv path]'   # change to your matchmaker.csv path
ls = file(matchmaker_path)
numerical_rows = preprocess_data.to_numerical(ls)
rescaled_data = preprocess_data.rescale_data(numerical_rows)
matches = []
features = []

for r in rescaled_data:
    matches.append(r.match)
    features.append(r.data)
    
print matches,',',features


# Step2. In the terminal, type following code line by line
from svmutil import *
prob = svm_problem(matches, features)
pm_matchmaker = svm_parameter('-t 2')  # indicates using radial-basis function
m = svm_train(prob, pm_matchmaker)
# [1] is the the ground truth, used for calculating the accuracy ; [28.0, 26.0] is the new point
p_labels, p_acc, p_vals = svm_predict([0, 1], [[28.0, -1, -1, 26.0, -1, 1, 2, 0.8], [28.0, -1, 1, 26.0, -1, 1, 2, 0.8]], m) 





