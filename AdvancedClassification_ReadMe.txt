1. Data source for MatchMaker dataset: agesonly.csv, matchmaker.csv
  * The agesonly.csv only includes matched ages since it is easier to visualize 2 variables.
  * The matchmaker.csv contains each pairs info as each row, the last element in each row (0 or 1) indicates whether these 2 people matched.
  
2. load_match_data.py
  * Load .cvs match data and generate a list of matchrow objects. Each object contains data as the person's info, and match to to indicate whether the person is a good match.
  * Using a scatter plot could help tell how the data is divided.
  
3. linear_clasifier.py
  * Using decision tree, the decision boundary will be forced to be vertical or horizontal, which is not good for multiple numerical input that doesn’t exhibit simple relationship.
  * Linear Classifier finds the average of each class and constructs points for each center, when the new data come in, they will be classified into the group of the closest center.
  * Using the calculation of dot products and vectors, we will be able to classify the new points into one of the 2 classes in this code.
  * The code here only provide a straight dividing live which can be incorrect.
  
4. preprocess_data.py
  * For classifiers in this part (linear_classifier, SVM, kernel methods), they all only deal with numerical data, so need to find ways to convert different nominal data into numerical data. Classifers like decision trees, can hanle both numerical and nominal data, without preprocessing it.
  * Data example: 
39,yes,no,skiing:knitting:dancing,220 W 42nd St New York NY,43,no,yes,soccer:reading:scrabble,824 3rd Ave New York NY,0
23,no,no,football:fashion,102 1st Ave New York NY,30,no,no,snowboarding:knitting:computers:shopping:tv:travel,151 W 34th St New York NY,1

  a. For yes, no answers, change "yes" to 1, change "no" to -1, change empty answer into 0.
  b. For hobies, I am going to build hobby hierarchy, so that for people have exactly same hobbies, the total match score got higher; if they share same category but different hobbies, got high sore too but lower than the first case;
  c. For geo-distances, I'm using geopy to get latitude, longitude based on the address, and measure geo-distance  (Python libraries is so powerful). geopy provides 2 formulas to calculate distances: great-circle and vincenty, I am using vincenty since it is more accurate.
  d. Convert each row of the data input into numerical data row.
  e. Rescale the data, for each column, get their max and min, then using float(r[i]-min[i])/(max[i]-min[i]) to do the rescaling. Since in this way, all the column data will be in range [0,1], so for each row, the data is also on the same scale.
  f. Train the data and get prediction results with rescaled data.
  
  
5. categorize_hobbies.py
  * In order to build the hobby hierarchy in preprocess_data.py, need to check the hobbies data.
  * Here, I am simply creating dictionary to store the hierarchial hobbies, in reality, if we want more accurate result, we can gather attributes data for each item, each category, then calculate the similarity using methods like Jaccard Similarity.
  
