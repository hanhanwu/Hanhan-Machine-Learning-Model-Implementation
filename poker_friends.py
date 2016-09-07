'''
Created on Sep 6, 2016
A group of friends want to play poker game for fun
Each game group allows 2 people, each person all have their top 2 choices to form a group
How to make groups to make the largest amount of people happy is an optimization problem
'''


def main():
    game_groups = ["fire", "water", "earth", "wind", "void"]
    top2choices = [
                   ("Hanhan", ("fire", "water")),
                   ("Baby_Emmanuel", ("void", "water")),
                   ("Yan", ("earth", "wind")),
                   ("Laura", ("fire", "wind")),
                   ("Big_Sea", ("water", "earth")),
                   ("Andrew", ("wind", "void")),
                   ("Albert", ("wind", "earth")),
                   ("Alice", ("water", "wind")),
                   ("Uzma", ("fire", "void")),
                   ("Einstein", ("fire", "earth"))
                   ]
    
if __name__ == "__main__":
    main()
