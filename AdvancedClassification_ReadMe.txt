1. Data source for MatchMaker dataset: agesonly.csv, matchmaker.csv
  * The agesonly.csv only includes matched ages since it is easier to visualize 2 variables.
  * The matchmaker.csv contains each individual info as each row, the last element in each row (0 or 1) indicates whether this person is a good match..... (This makes the prediction easier, although I am wondering whether in reality, we often simplify problems in this way).
  
2. load_match_data.py
  * Load .cvs match data and generate a list of matchrow objects. Each object contains data as the person's info, and is_good_match to to indicate whether the person is a good match.
  * Using a scatter plot could help tell how the data is divided.
  
3. linear_clasifier.py
  * Using decision tree, the decision boundary will be forced to be vertical or horizontal, which is not good for multiple numerical input that doesn’t exhibit simple relationship.
  * Linear Classifier finds the average of each class and constructs points for each center, when the new data come in, they will be classified into the group of the closest center.
  * Using the calculation of dot products and vectors, we will be able to classify the new points into one of the 2 classes in this code.
  
