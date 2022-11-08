# nvanbaak 1 Nov 2022
# Given text representing a Frogger map, determine shortest path to victory

# STRATEGY:
# Alright, so I tried this once (see g_prototype.py) and I realized that a 2D map with procedural car movement is
# basically a 3D map where the 3rd axis is time.  So rather than simulating car movement, we're going to generate
# a 3D array of all car positions over time, which means we can just use Djikstra's Algorithm to find the best path.

import sys
from typing import Tuple
import numpy as np

test_cases = int(sys.stdin.readline().strip()) # first line of input tells us how many cases we're solving

char_dict = {
    "." : 0.0, # grass, can sit freely
    "-" : 0.1, # road, can't stay during turn
    "&" : 1.1, # frog starting position denotes road underneath
    "<" : 0.1, # car heading left, we assume road underneath
    ">" : 0.1, # car heading right, we assume road underneath
    "~" : 0.2, # water tile, our goal
    "T" : -1.0, # tree, impassable
}

def get_next_square(map_height, x_from, y_from, z_from, direction):
    """
    returns a set of map coordinates based on the given
    :params:
    map_rows: number of rows in the map
    map_columns: number of columns in the map
    x_from: x of the square we're reckoning from
    y_from: y of the square we're reckoning from
    z_from: z of the square we're reckoning from
    direction: "left","right","down","up"
    returns:
        left: (x-1,y,z+1)
        right: (x+1,y,z+1),
        up: (x,y-1,z+1)
        down: (x,y,z+1)
    """
    # z moves by one in all cases
    new_z = z_from+1 if z_from < map_height-1 else 0

    if direction == "left":
        new_x = map_height-1 if x_from == 0 else x_from-1
        return (new_x, y_from, new_z)
    elif direction == "right":
        new_x = 0 if x_from >= map_height-1 else x_from+1
        return (new_x, y_from, new_z)
    elif direction == "down":
        return (x_from, y_from, new_z)
    elif direction == "up":
        if y_from == 0: raise Exception(f"Attempted to move past top edge of map at ({x_from},{y_from},{z_from})")
        return (x_from, y_from-1, new_z)
    else:
        raise Exception(f"Invalid direction keyword '{direction}'")

for _ in range(test_cases):
    # build map from input
    map_rows, map_columns = sys.stdin.readline().split()
    map_rows = int(map_rows)
    map_columns = int(map_columns)

    # setup tracking variables
    frog_x = None
    frog_y = None

    # case_map = np.empty((map_rows, map_columns, map_columns),dtype=object)
    case_map = np.zeros((map_rows, map_columns, map_columns))

    # build the map and collect data about its contents
    for y_index in range(int(map_rows)):
        row = sys.stdin.readline().strip()

        for x_index in range(map_columns):
            tile = row[x_index]
            tile_value = char_dict[tile]

            if tile == "&":
                frog_x = x_index
                frog_y = y_index

            tile_is_left_car = tile == "<"
            tile_is_right_car = tile == ">"

            car_x = x_index

            for z_index in range(map_columns):
                case_map[y_index][x_index][z_index] += tile_value
                if tile_is_left_car:
                    case_map[y_index][car_x][z_index] = -1.
                    next_square = get_next_square(
                            map_columns,
                            car_x, y_index, z_index,
                            "left")
                    car_x = next_square[0]
                elif tile_is_right_car:
                    case_map[y_index][car_x][z_index] = -1.
                    next_square = get_next_square(
                            map_columns,
                            car_x, y_index, z_index,
                            "right")
                    car_x = next_square[0]

    # implement modified Djikstra's
    frog_tile = (frog_x, frog_y, 0)
    candidate_tiles = [frog_tile]
    shortest_path = -1

    while candidate_tiles:
        # print(f"Stack: {candidate_tiles}")
        tile_x, tile_y, tile_z = candidate_tiles.pop()
        current_value = case_map[tile_y][tile_x][tile_z]
        print(f"currently evaluating {tile_x},{tile_y},{tile_z} with tile value {current_value}")

        directions = ["left","right","up"]
        if round(current_value % 1 ,1) != 0.1: directions.insert(0, "down")

        for direction in directions:
            next_x, next_y, next_z = get_next_square(
                    map_columns, tile_x,tile_y,tile_z,
                    direction)

            next_value = case_map[next_y][next_x][next_z]
            print(f"{direction} neighbor tile ({next_x},{next_y},{next_z}) has value {next_value}")

            if next_value == 0.2:
                if shortest_path < 0:
                    shortest_path = int(current_value)
                elif current_value < shortest_path:
                    shortest_path = int(current_value)
            elif next_value >= 0: # if it's pathable

                if next_value < 1: # if we haven't visited
                    # since road tiles are 0.1 and grass tiles are 0.0, multiplying by 11 means road tiles increase path length while grass does not

                    path_length = int(current_value) + (next_value*11)
                    case_map[next_y][next_x][next_z] = path_length
                    candidate_tiles.append((next_x,next_y,next_z))

                else: # if we've already visited

                    next_tile_value = next_value % 1
                    path_length = current_value + (next_tile_value*11)

                    # stop here unless we've found a shorter route
                    if path_length < next_value:
                        case_map[next_y][next_x][next_z] = path_length
                        candidate_tiles.append((next_x,next_y,next_z))

    print(case_map)

    if shortest_path > 0: print(shortest_path)
    else: print("Impassable")