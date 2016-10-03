'''
Created on Oct 2, 2016
In a network where nodes are linked together, it may looks messy
Finding the least messy way to visualize the network, is an optimization problem

In this example, I'm planning to visualize Chinese gourmet and their ingredients
Isn't it so fascinating that with limited ingredients, you can make tons of different Chinese food :) 
Here, I removed those basic ingredients such as salt, water, pepper, onion, etc.
'''


def main():
    gourmet_lst = ["8 treasure porridge", "8 treasure rice puding", "red bean, barley rice soup", "spicy eggplant noodles",
                   "tomato egg soup", "tomato egg noodles", "cucumber fried rice", "tomato fried rice", "spicy tofu"]
    ingredients = ["red bean", "barley rice", "date", "black bean", "rose peanut", "dried longan", "honey", "sweet rice",
                   "eggplant", "tomato", "avocado", "tofu", "bean stick", "egg", "sesame oil", "rice", 
                   "cucumber", "carrot", "shrimp", "noodles", "mild spice"]
    
    links = [
             ("8 treasure porridge", 
              ("red bean", "barley, rice", "date", "black bean", "rose peanut", "dried longan", "honey", "sweet rice")),
             ("8 treasure rice puding", 
              ("red bean", "sweet rice", "dried longan", "honey", "date")),
             ("red bean, barley rice soup", ("red bean", "barley rice soup")),
             ("spicy eggplant noodles", ("eggplant", "carrot", "noodles", "egg", "mild spice")),
             ("tomato egg soup", ("tomato", "egg", "tofu", "sesame oil", "shrimp")),
             ("tomato egg noodles", ("tomato", "egg", "noodles", "tofu", "sesame oil", "shrimp")),
             ("cucumber fried rice", ("cucumber", "rice", "egg", "carrot")),
             ("tomato fried rice", ("tomato", "egg", "bean stick", "rice", "avocado", "carrot")),
             ("spicy tofu", ("tofu", "mild spice"))
             ]
    
if __name__ == '__main__':
    main()
