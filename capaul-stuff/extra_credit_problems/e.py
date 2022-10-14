# nvanbaak 14 October 2022
# given match results of Rock Paper Scissors, determine which player won the match

# STRATEGY:
# This one seems very simple and there's no reason it can't run in linear time.

import sys

# define dictionary for round results
rps_dict = {
    "RS": 1,
    "PR": 1,
    "SP": 1,
    "RP": 2,
    "PS": 2,
    "SR": 2,
    "RR": 0,
    "PP": 0,
    "SS": 0
}

# first line is number of cases
test_cases = int(sys.stdin.readline().strip())

for _ in range(test_cases):

    rounds = int(sys.stdin.readline().strip())
    player_one_wins = 0
    player_two_wins = 0

    for _ in range(rounds):
        moves = sys.stdin.readline().strip().replace(" ", "")
        if rps_dict[moves] == 1: player_one_wins += 1
        elif rps_dict[moves] == 2: player_two_wins += 1

    if player_one_wins == player_two_wins: print("TIE")
    elif player_one_wins > player_two_wins: print("Player 1")
    else: print("Player 2")