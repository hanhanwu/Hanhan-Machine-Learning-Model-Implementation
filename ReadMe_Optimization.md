Optimization Problems


* Group Traveling Optimization Problem

  * A group of people, arrive and depart at the same airport all on the same day. 
  They will also share transportation from and to the airport. How to minimize the cost 
  (flight cost, waiting time, car rent cost and so on)
  * Flight data set: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/flights.txt
  * Generate required data set: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/create_group_schedule_data.py
  * Group schedule optimization: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/group_schedule_optimization.py
  * Optimization Methods
  
  -- Random Search: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/opt_random_search.py
  
  * Random Search should serve as the base line of optimization methods.
  

 -- Hill Climbing: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/opt_hill_climbing.py
 
  * Hill climbing starts from a random solution, looking for better neighbor solutions
 In this process, it walks in the most steep slope till it reached a flat point
 This method will find local optimum but may not be global optimum.


 -- Simulated Annealing: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/opt_simulated_annealing.py
  
  * When the cost is higher, the new solution can still become the current solution with certain probability.
This aims at avoiding local optimum.
The temperature - willingness to accept a worse solution
When the temperature decreases, the probability of accepting a worse solution is less


 -- Genetic Algorithms: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/opt_genetic_alg.py

  * elitism - choose the top solutions in current generation into the next generation
  * The rest solutions in the new generation are created by modifying the current top solutions:
     mutation - a small, random change on an existing solution
     crossover/breeding - combine 2 of the current top solutions
  * The new population has the same size as the old one
  * Aims at avoiding local optimum.

 * It seems that Gentic Algorithms works far better than the other 3 optimization methods in this case.


* General Optimization Algorithms

 * The algorithms I implemented above are too specific to the group travel problem. I am re-writing code here, hoping to ake the algorithms server for border purposes.
 * genetic algorithm general: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/genetic_alg.general.py


* Optimal Assignment Problem
 
 * A simple poker game group assignment implementation: https://github.com/hanhanwu/Hanhan-Machine-Learning-Model-Implementation/blob/master/poker_friends.py
