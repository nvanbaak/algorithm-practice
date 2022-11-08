# nvanbaak 15 Oct 2022
# Given text representing a Frogger map, determine shortest path to victory

# STRATEGY:
# We're going to represent the game state as a grid, then simulate movesets one turn at a time.
# Using numpy might help with that.  We'll have to be aware that cars can move over each other.

# update 18 Oct: So simple to plan, so technical to execute.

# update 25 Oct:
# I've been poking at this over the last week and have avoided the follow traps:
#   * there's a sneaky test case at the end where there's cars on the water. The naive implementation
#     is to paint road tiles after the cars, but in that case it means painting road tiles over the
#     water tiles, so I refactored the code to keep the map separate and draw the cars afterward.
#   * Was trying to figure out how to keep the frog from infinitely looping on one row.  Settled on 
#     tracking the turns spent on the current row - if it can't find a way forward at that point, it
#     never will.
#   * Large maps with lots of cars will take forever to simulate.  Refactoring car simulation to use
#     a turn counter and only simulating the current and next row cuts down a huge amount of work.
#   * We can further optimize by only working with slices of the initial map.

import sys
import numpy as np

test_cases = int(sys.stdin.readline().strip()) # first line of input tells us how many cases we're solving

char_dict = {
    "." : 0.0, # grass, can sit freely
    "-" : 1.0, # road, can't stay during turn
    "&" : 1.0, # frog starting position denotes road underneath
    "~" : 2.0, # water tile, our goal
    "T" : 3.0, # tree, impassable
    "<" : 1.0, # car heading left, we assume road underneath
    ">" : 1.0, # car heading right, we assume road underneath
}

def is_valid_move(map, pos_x, pos_y):
    """
    Returns True if the location on the map is valid to move to.
    False otherwise.
    """
    can_move = map[pos_x][pos_y] < 3
    return can_move

def frog_can_wait(map, frog_x, frog_y):
    """
    Returns True if the frog is on grass.  False otherwise.
    """
    return map[frog_y][frog_x] == 0.0

def update_and_render_cars(map, map_xy, frog_y, total_turns, left_cars, right_cars):
    """
    Updates the location of each car on the frog's row, as well as the one above it, if any
    :params:
    map: base map
    map_xy: width and height of map
    frog_y: the row the frog is in.  We simulate that row and the one above it.
    total_turns: number of turns since start of path
    left_cars, right_cars: lists of cars headed in respective directions
    Returns a copy of the map with the new car positions marked.
    """
    map_width, map_height = map_xy
    rendered_map = map.copy()

    net_shift = total_turns % map_width # every $width tiles nets no change of position
    # set the frog's row as active
    active_rows = (frog_y, frog_y-1) if frog_y > 0 else [frog_y]

    for row_index in active_rows:
        list_index = 0
        for car_position in left_cars[row_index]:
            new_position = car_position - net_shift
            if new_position < 0:
                new_position += map_width

            left_cars[row_index][list_index] = new_position
            list_index += 1
            rendered_map[row_index][new_position] = 4.0

        list_index = 0
        for car_position in right_cars[row_index]:
            new_position = car_position + net_shift
            if new_position > map_width-1:
                new_position -= map_width

            right_cars[row_index][list_index] = new_position
            list_index += 1
            if rendered_map[row_index][new_position] == 4.0:
                rendered_map[row_index][new_position] = 6.0 # denotes car overlap
            else:
                rendered_map[row_index][new_position] = 5.0

        return rendered_map

def find_path(map : np.array, map_xy, frog_xy, left_cars, right_cars, turns_on_this_row, turns_on_road, total_turns, min_solution, max_solution):
    """
    Recursive function that steps through the map to find the path with the fewest road tiles.
    The algorithm:
        - always attempts to go forward first
        - prioritizes grass over road

    :params:
    map: a np array detailing the terrain
    map_xy: a tuple containing width and height of the map
            so we don't have to re-calculate in each recursion
    frog_xy: coordinates of frog
    left_cars, right_cars: lists of tuples detailing coordinates of each car
    turns_on_this_row: number of turns spent on the current row
    turns_on_road: cumulative turns spent on road this path
    total_turns: cumulative turns spent on solution
    min_solution: the minimum number of turns we could have spent on road tiles
    max_solution: the maximum number of turns we could have spend on road tiles

    returns: the final number of turns spent on road tiles, or -1 if no path to water exists
    """
    frog_x, frog_y = frog_xy

    # increment counters
    if map[frog_x][frog_y] == 1.0: turns_on_road += 1
    total_turns += 1
    turns_on_this_row += 1

    # frog and cars move at the same time, which functionally means the frog's movement
    # options are determined after the cars move
    rendered_map = update_and_render_cars(map, map_xy, frog_y, total_turns, left_cars, right_cars)

    # determine pathing options
    path_options = []
    solution = -1

    # case: forward
    if frog_y > 0: # only attempt to move forward if we're not on the last row
        if is_valid_move(rendered_map, frog_x, frog_y-1):
            # if it's a water tile, we're done
            if rendered_map[frog_y-1][frog_x] == 2.0: return turns_on_road
            else:
                new_frog_xy = (frog_x, frog_y-1)
                turns_on_next_row = 0
                solution = find_path(case_map, map_xy, new_frog_xy, left_cars.copy(), right_cars.copy(), turns_on_next_row, turns_on_road, total_turns, min_solution, max_solution)
                if solution <= min_solution:
                    return solution

    # evaluate same-row options only if we haven't used up our time on this row
    if turns_on_this_row <= map_xy[0]:
        # case: right
        if is_valid_move(rendered_map, frog_x+1, frog_y):
            if frog_x >= map_xy[0]-1:
                new_x = 0
                path_options.append((new_x, frog_y))
            else: path_options.append((frog_x+1, frog_y))

        # case: left
        if is_valid_move(rendered_map, frog_x-1, frog_y):
            if frog_x == 0:
                new_x = map_xy[0]-1
                path_options.append((new_x, frog_y))
            else: path_options.append((frog_x-1, frog_y))

        # case: wait
        if frog_can_wait(rendered_map, frog_x, frog_y):
            path_options.append((frog_x, frog_y))

    # evaluate cases
    for path_step in path_options:
        solution_option = find_path(case_map, map_xy, path_step, left_cars.copy(), right_cars.copy(), turns_on_this_row, turns_on_road, total_turns, min_solution, max_solution)

        if solution_option <= min_solution:
            return solution_option

        if solution == -1 and solution_option > solution:
            solution = solution_option
        elif solution > -1 and solution_option < solution:
            solution = solution_option

    return solution


for _ in range(test_cases):
    # build map from input
    height, width = sys.stdin.readline().split()

    # setup tracking variables
    map_contents = []
    left_cars = []
    right_cars = []
    frog_xy = None
    road_counts = []

    # build the map and collect data about its contents
    for row in range(int(height)):
        map_line = sys.stdin.readline().strip()
        line_list = []
        left_cars_this_row = []
        right_cars_this_row = []
        col_index = 0
        road_tiles_this_row = 0
        for char in map_line:
            line_list.append(char_dict[char])
            if char == "<":
                left_cars_this_row.append(col_index)
                road_tiles_this_row += 1
            elif char == ">":
                right_cars_this_row.append(col_index)
                road_tiles_this_row += 1
            elif char == "&":
                frog_xy = (col_index, row)
                road_tiles_this_row += 1
            elif char == "-":
                road_tiles_this_row += 1
            col_index += 1

        map_contents.append(line_list)
        road_counts.append(road_tiles_this_row)
        left_cars.append(left_cars_this_row)
        right_cars.append(right_cars_this_row)

    case_map = np.array(map_contents) # convert to np array
    map_xy = case_map.shape

    # determine best and worst cases
    min_solution = 0
    max_solution = 0
    for road_count in road_counts:
        if road_count > 0: # basically this lets us skip rows with no road tiles
            min_solution += 1
            max_solution += road_count

    # skip trivial cases
    if min_solution == 1:
        print(1)
        continue

    solution = find_path(case_map, map_xy, frog_xy, left_cars, right_cars, 0, 0, 0, min_solution, max_solution)
    if solution > 0: print(solution)
    else: print("Impassable")
