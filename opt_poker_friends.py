'''
Created on Sep 6, 2016
A group of friends want to play poker game for fun
Each game group allows 2 people, each person all have their top 2 choices to form a group
How to make groups to make the largest amount of people happy is an optimization problem
'''
import random
import sys
import genetic_alg_general


game_groups = ["fire", "water", "earth", "wind", "void"]
top_choices = [
                   ("Hanhan", ("fire", "water")),
                   ("Cherry", ("water", "void")),
                   ("Yan", ("earth", "wind")),
                   ("Laura", ("fire", "wind")),
                   ("Big_Sea", ("void", "earth")),
                   ("Andrew", ("wind", "void")),
                   ("Albert", ("wind", "earth")),
                   ("Alice", ("water", "wind")),
                   ("Uzma", ("fire", "void")),
                   ("Einstein", ("fire", "earth"))
               ]


# randomly assign empty slot but guarantee each gamer get an available slot, and all slots will be used
def random_assign(num_group, num_top_choice):
    num_gamers = num_group * num_top_choice
    slots = []
    assign_vec = [0]*num_gamers
    for i in range(num_group):
        slots += [i, i]
        
    for j in range(num_gamers):
        slot_idx = random.randint(0, len(slots)-1)
        assign_vec[j] = slots[slot_idx] 
        del slots[slot_idx]
    
    return assign_vec


# the cost function
def assign_cost(assign_vec):
    cost = 0
    for a in range(len(assign_vec)):
        assigned_group = game_groups[assign_vec[a]]
        gamer_choices = top_choices[a][1]
        if gamer_choices[0] == assigned_group: continue
        elif gamer_choices[1] == assigned_group: cost +=1
        else: cost += 3
        
    return cost


# random search optimization
def optimal_assign(max_iter = 1000):
    optimal_vec = None
    min_cost = sys.maxint
    num_group = len(game_groups)
    num_top_choice = len(top_choices[0][1])
    
    for k in range(max_iter):
        assign_vec = random_assign(num_group, num_top_choice)
        cost = assign_cost(assign_vec)
        if cost < min_cost:
            optimal_vec = assign_vec
            min_cost = cost
            
    return optimal_vec


def print_solution(optimal_vec):
    for a in range(len(optimal_vec)):
        print top_choices[a][0] + ': ' + game_groups[optimal_vec[a]]



def main():
    # random search optimization
    optimal_vec = optimal_assign()
    print_solution(optimal_vec)
    
    
    # ************* try genetic optimization****************#
    num_slots = len(top_choices)
    domain = [(0,len(game_groups)-1)]*num_slots
    
    genetic_optimal_vec = genetic_alg_general.genetic_alg_general(domain, assign_cost)[1]
    print_solution(genetic_optimal_vec)
    
if __name__ == "__main__":
    main()
