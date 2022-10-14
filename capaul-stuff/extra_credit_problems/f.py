# nvanbaak 14 Oct 2022
# Given a number in base -2 — yes, you read that right — convert it to decimal

# STRATEGY:
# So, weird binary to decimal I can do just fine.  Already wrote that code for problem d.
# Decimal to weird binary: I have no idea where to start, so I'm going to play around with 
# some things and see if they work.  I have a vague idea that something resembling long division
# is correct.
# update: after thinking on it, 32 = 64 + -32.  So we have the ability to produce any given power of 2.
# That's only part of the puzzle, though.
# update 2: I think we need to convert to binary first, then programmatically flip the negative indices

# TODO: refactor using numpy

import sys

test_cases = int(sys.stdin.readline().strip())

def weird_to_decimal(num):
    """
    given a number in base -2, returns the decimal representation
    """
    iter_num = num[::-1]
    total = 0
    digit_position = 0
    for digit in iter_num:
        total += int(digit) * ((-2)**digit_position)
        digit_position += 1
    return total

def decimal_to_weird(num):
    """
    Converts a decimal number to weird binary
    """
    # trivial case
    if num == 0: return 0

    # first get binary
    binary = str(bin(num)).replace("0b","")
    negative_flag = 1 if binary[0] == "-" else 0
    if negative_flag:
        binary = binary[1:]
    digit_list = []
    for digit in binary[::-1]:
        digit_list.append(int(digit))

    index = 0
    number_len = len(digit_list)
    while index < number_len:
        # get digit
        curr_digit = digit_list[index]

        # if there's a 2 (because a previous digit got pushed up),
        # increment the next digit, adding it if it's not there
        if curr_digit == 2:
            if index + 1 >= number_len:
                digit_list.append(1)
                number_len += 1
            else:
                digit_list[index+1] += 1
            
            # then set to 0
            digit_list[index] = 0

        # next, if this is a negative space, add 1 to the next digit to cancel out
        if (index + negative_flag) % 2 == 1:
            if curr_digit == 1:
                if index + 1 >= number_len:
                    digit_list.append(1)
                    number_len += 1
                else:
                    digit_list[index+1] += 1

        index += 1

    result = ""
    for digit in digit_list:
        result = f"{digit}{result}"

    return result

for _ in range(test_cases):
    input = sys.stdin.readline().split()
    number = input[1]

    if input[0] == "b":
        result = weird_to_decimal(number)
        print(f"From binary: {number} is {result}")
    else:
        result = decimal_to_weird(int(number))
        print(f"From decimal: {number} is {result}")

