1. mock_Chinese_stock_price.py
  * In this file, the 500 generated stock price will be the dataset used in models
  * get_stockset() returns data set with less attribute, and the range between each attribute does not vary too much
  * get_stockset_various() has added more attributes, some maybe useless attribute and some may have very huge values
  
2. euclidean_distance.py
 * Calculate the euclidean distance between 2 vectors. Each vector represents the attrobutes of each item. The 2 vectors must have same attributes
 
3. KNN.py
 * Find top k similar items for a new item. 
 * Un-weighted KNN using euclidean distance by default.
 * Weighted KNN using gaussian function as defaust weight function.
  * 3 weight methods, based on "the weight declines when the distance increases"
   * Inverse Weight function: fast and easy to implement, but overweight close items which makes the algorithm more sensite to the noise.
   * Subtraction Weight function: won't overweight close items, but the weight will finally drop to 0. In some cases this cannot help make prediction at all, since there is nothing close enough to be ocnsidered as neighbors, then both the weight and the average will be 0.
   * Gaissian Weight function: the weight is 1 when the distance is 0, the weight is always larger than 0, so it is always be able to make predictions.
   
4. cross_validation.py
 * Using cross validation to test a model. In this code, the model is KNN(un-weighted and weighted).
 * With the help of cross validation, we can tune the parameters of the model to see which set of parameters give better results without getting overfit.
 * Note: I am using monte carlo cross validation here, when it is fine to do many times iterations, monte carlo is better than k-fold cross validation. Because using folds will have the limitation for the number of folds, depends on the size of the dataset. Therefore, larger folds will become uncessary since it will repeat previous tests. Using percentages with random() seldom get repeated tests and allows more times tests. However, when the data is huge, sometimes, using k-fold in Spark mllib is more accurate and faster than monte carlo cross validation, by just using a few folds.
 
5. optimization.py   (Optimization is good because, here you can see which attributes are important immediately)
 * Using annealing optimization - an algorithm used for global optimum. It is often used when the search space is discrete.
 * For problems where finding the precise global optimum is less important than finding an acceptable global optimum in a fixed amount of time, simulated annealing may be preferable to alternatives such as brute-force search or gradient descent.
 * The cost function is used to decide whether to update to the new feature vector in each step of optimization loop. In this code, users have the freedom to decide which algorithm will be used in the cross validation of the cost function.
 
 * genetic optimization algorithm, it mimics the nature and try to optimize each generation by selection the top elites and use them to do mutation/crossover to form the rest of new solutions and bring all these together into the next generatino. So it assumes that each generation has the same amount of population.
 * I think genetic algorithm is very interesting. I am outputing the average score and the best score for each genration, they are not in decreasing or ascending order. Looks like philosophy.
 
Note: In both optimization methods, we are using domain to tell the range of each attribute.
      In both optimization, I dind't do value check. For example, to check whether the generated age is larger than 0. In practical situation, these checks should be added for different situations.
 
6. heterogeneous_data.py
 * By using rescale, we can control the influence from each attribute. For unnecessary attribute, we can set its scale value as 0.
 * By using normalization, we put each attribut between [0,1]. For unnecessary attribute, we can choose not to choose it.
 Note: both rescaling and normalization here are all belong to feature rescaling.
 This link is good: http://www.dataminingblog.com/standardization-vs-normalization/
 To understand why people wants to normalize variance, this is because  sometimes people may be only interested in how many standard deviations a feature value is away from mean instead of the actual variance value.  
 
7. probability_guess.py
 * Telling the probabilities that a new item belongs to each range/category
 * plot the probabilities using Python matplotlib
  a. cumulative probabilities - shows the probability that the result is under a given upperbound
  b. probability graph - shows probabilities for different price point in a smooth way. In order to make the graph smooth, the algorithm assumed that the probability at each point is a weighted average of the surrounding probabilities. Using gaussian function to calcualte the weight for each nearby 2 points, their sv will be added up using the weight multiply the probability between these 2 points.
  
8. eBay_test.py, eBay_price_predict.py
 * get eBay products price as the training data, using the implemented KNN, weighted KNN for price prediction.
 * eBay_test.py is the one to get the right category id, since using keyword search for eBay products, it will return all the relative products. In this case, instead of just return wine, it also returns other wine products. You can also use the sample code here to help other data filtering work.
 * In order to get eBay data, need to go to eBay developer web page and apply for application keys.
