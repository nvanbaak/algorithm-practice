# nvanbaak 15 Oct 2022
# Given text representing a Frogger map, determine shortest path to victory

# STRATEGY:
# We're going to represent the game state as a grid, then simulate movesets one turn at a time.
# Using numpy might help with that.  We'll have to be aware that cars can move over each other.

import sys
import numpy as np

test_cases = int(sys.stdin.readline().strip())

char_dict = {
    "." : 0.0, # grass, can sit freely
    "-" : 1.0, # road, can't stay during turn
    "&" : 1.0, # frog starting position denotes road underneath
    "~" : 2.0, # water tile, our goal
    "T" : 3.0, # tree, impassible
    "<" : 1.0, # car heading left, we assume road underneath
    ">" : 1.0, # car heading right, we assume road underneath
}

def is_valid_move(map, pos_x, pos_y):
    """
    Returns True if the location on the map is valid to move to.
    False otherwise.
    """
    return map[pos_y][pos_x] < 3

def frog_can_wait(map, frog_x, frog_y):
    """
    Returns True if the frog is on grass.  False otherwise.
    """
    return map[frog_y][frog_x] == 0.0

def update_and_render_cars(map, left_cars, right_cars):
    """
    Given a base map, a list of left-heading cars, and a list of right-heading cars,
    moves each car one index in the appropriate direction and inserts it into the map.
    Returns a copy of the map with the new car positions marked.
    """
    map_width, _ = map.shape()
    rendered_map = map.copy()

    list_index = 0
    for car_tuple in left_cars:
        car_x, car_y = car_tuple
        car_x = car_x-1 if car_x > 0 else map_width-1 # wrap edge movement

        left_cars[list_index] = (car_x, car_y)
        rendered_map[car_y][car_x] = 3.0 # denotes impassible terrain
        list_index += 1

    list_index = 0
    for car_tuple in right_cars:
        car_x, car_y = car_tuple
        car_x = car_x+1 if car_x < map_width-1 else 0 # wrap edge movement

        left_cars[list_index] = (car_x, car_y)
        rendered_map[car_y][car_x] = 3.0 # denotes impassible terrain
        list_index += 1

    return rendered_map

def find_path(map : np.array, frog_x, frog_y, left_cars, right_cars):
    """
    We start from the bottom and solve the map two rows at a time.
    """
    map_width, map_height = map.shape()
    pass


for _ in range(test_cases):
    # build map from input
    height, width = sys.stdin.readline().split()
    print(f"width: {width}; length: {height}")
    case_map = []
    left_cars = []
    right_cars = []
    frog_x = None
    frog_y = None
    for row in range(int(height)):
        map_line = sys.stdin.readline().strip()
        line_list = []
        col_index = 0
        for char in map_line:
            line_list.append(char_dict[char])
            if char == "<":
                left_cars.append((col_index, row))
            elif char == ">":
                right_cars.append((col_index, row))
            elif char == "&":
                frog_x = col_index
                frog_y = row
            col_index += 1

        case_map.append(line_list)

    case_map = np.array(case_map) # convert to np array



    # now we find a path, which will be more difficult than normal because the cars are moving
    # 





