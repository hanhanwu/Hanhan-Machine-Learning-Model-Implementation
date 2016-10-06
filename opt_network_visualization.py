'''
Created on Oct 2, 2016
In a network where nodes are linked together, it may looks messy
Finding the least messy way to visualize the network, is an optimization problem

In this example, I'm planning to visualize Chinese gourmet and their ingredients
Isn't it so fascinating that with limited ingredients, you can make tons of different Chinese food :) 
Here, I removed those basic ingredients such as salt, water, pepper, onion, etc.
'''

import random
import genetic_alg_general
import simulated_annealing_general
import networkx as nx
import matplotlib.pyplot as plt



gourmet_lst = ["8 treasure porridge", "8 treasure rice puding", "red bean, barley rice soup", "spicy eggplant noodles",
                   "tomato egg soup", "tomato egg noodles", "cucumber fried rice", "tomato fried rice", "spicy tofu"]
ingredients = ["red bean", "barley rice", "date", "black bean", "rose peanut", "dried longan", "honey", "sweet rice",
                   "eggplant", "tomato", "avocado", "tofu", "bean stick", "egg", "sesame oil", "rice", 
                   "cucumber", "carrot", "shrimp", "noodles", "mild spice"]
    
my_links = [
             ("8 treasure porridge", 
              ("red bean", "barley rice", "date", "black bean", "rose peanut", "dried longan", "honey", "sweet rice")),
             ("8 treasure rice puding", 
              ("red bean", "sweet rice", "dried longan", "honey", "date")),
             ("red bean, barley rice soup", ("red bean", "barley rice")),
             ("spicy eggplant noodles", ("eggplant", "carrot", "noodles", "egg", "mild spice")),
             ("tomato egg soup", ("tomato", "egg", "tofu", "sesame oil", "shrimp")),
             ("tomato egg noodles", ("tomato", "egg", "noodles", "tofu", "sesame oil", "shrimp")),
             ("cucumber fried rice", ("cucumber", "rice", "egg", "carrot")),
             ("tomato fried rice", ("tomato", "egg", "bean stick", "rice", "avocado", "carrot")),
             ("spicy tofu", ("tofu", "mild spice"))
             ]


all_nodes = gourmet_lst
all_nodes.extend(ingredients)


def get_all_links():
    all_links = []
    for t in my_links:
        gourmet = t[0]
        for ingredient in t[1]:
            all_links.append((gourmet, ingredient))
    return all_links
    


# count how many 2 lines are crossing based on the coordinates of their ends
def count_cross(v):
    coord_dct = dict([(all_nodes[i], (v[i*2], v[i*2+1])) for i in range(len(all_nodes))])
    ct = 0
    
    all_links = get_all_links()
    
    # check whether current line will cross the rest lines
    for i in range(len(all_links)):
        (x1, y1), (x2, y2) = coord_dct[all_links[i][0]], coord_dct[all_links[i][1]]
        for j in range(i+1, len(all_links)):
            (x3, y3), (x4, y4) = coord_dct[all_links[j][0]], coord_dct[all_links[j][1]]
            
            den = float((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
            # 2 lines are parallel when den is 0
            if den == 0: continue
            
            ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))/den
            ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3))/den
            
            if ua>0 and ua<1 and ub>0 and ub<1:
                ct += 1
    return ct


def draw_solution(sol):
    G=nx.Graph()
    coord_dct = dict([(all_nodes[i], (sol[i*2], sol[i*2+1])) for i in range(len(all_nodes))])
    
    for t in my_links:
        gourmet = t[0]
        G.add_node(gourmet, pos=coord_dct[gourmet])
        for ingredient in t[1]:
            G.add_node(ingredient, pos=coord_dct[ingredient])
            G.add_edge(gourmet, ingredient)
            
    nx.draw(G, with_labels = True)
    plt.show()



def main():
    domain = [(4, 10)]*(len(all_nodes)*2+2)
     
    # genetic alg 
    optimal_solution1 = genetic_alg_general.genetic_alg_general(domain, count_cross)
    print optimal_solution1
    draw_solution(optimal_solution1[1])
     
    # simulated annealing
    optimal_solution2 = simulated_annealing_general.simulated_annealing(domain, count_cross)
    print optimal_solution2
    draw_solution(optimal_solution2[0])
if __name__ == '__main__':
    main()
