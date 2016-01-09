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
