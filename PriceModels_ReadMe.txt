1. mock_Chinese_stock_price.py
  * In this file, the 500 generated stock price will be the dataset used in models
  
2. euclidean_distance.py
 * Calculate the euclidean distance between 2 vectors. Each vector represents the attrobutes of each item. The 2 vectors must have same attributes
 
3. K_Nearest_Neighobur.py
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
 * Note: when dividing the data in cross validation here, I think using percentage instead of folds to divide is better. Because using folds will have the limitation for the number of folds, depends on the size of the dataset. Therefore, larger folds will become uncessary since it will repeat previous tests. Using percentages with random() seldom get repeated tests and allows more times tests.
 
5. optimization_alg.py
 * Using annealing optimization - an algorithm used for global optimum. It is often used when the search space is discrete.
 * For problems where finding the precise global optimum is less important than finding an acceptable global optimum in a fixed amount of time, simulated annealing may be preferable to alternatives such as brute-force search or gradient descent.
