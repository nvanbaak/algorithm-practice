# nvanbaak 13 October 2022

# STRATEGY:
# Rather than iterate over all numbers to find the primes and then check for palindromes,
# I'm going to iterate over the palindromes and check if they're primes.  That should be 
# less computationally intensive.  The hard part is going to be writing a function for 
# base conversion because that's new for me.

import sys

digit_dict = {
    "0" : 0,
    "1" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "a" : 10,
    "b" : 11,
    "c" : 12,
    "d" : 13,
    "e" : 14,
    "f" : 15,
    "g" : 16,
    "h" : 17,
    "i" : 18,
    "j" : 19,
    "k" : 20,
    "l" : 21,
    "m" : 22,
    "n" : 23,
    "o" : 24,
    "p" : 25,
    "q" : 26,
    "r" : 27,
    "s" : 28,
    "t" : 29,
    "u" : 30,
    "v" : 31,
    "w" : 32,
    "x" : 33,
    "y" : 34,
    "z" : 35
}
digit_list = "0123456789abcdefghijklmnopqrstuvwxyz"

def check_if_prime(num_to_check):
    """
    iterates up to square root of num to check for factors
    """
    num_to_check = int(num_to_check)
    root = int(num_to_check**0.5)+1

    if num_to_check < 2: return False
    if num_to_check == 2: return True
    if num_to_check > 2:
        if num_to_check % 2 == 0: return False
        for num in range(3,root,2):
            if num_to_check % num == 0: return False

    return True

def convert_to_base_ten(num, base_from):
    """
    given an integer num >= 0 in base base_from, returns the number in base 10
    """
    # In base N, each digit of a number represents that number times N^X, where
    # X is that digit's position in the number.

    # trivial case
    if base_from == 10: return num

    # iterate over number digits
    # python iterates left to right so we reverse the number first
    reversed_num = str(num)[::-1]
    total = 0
    digit_position = 1

    for digit in reversed_num:
        if digit != 0:
            digit_base_ten = digit_dict[digit]
            digit_value = digit_base_ten * (base_from ** digit_position)
            total += digit_value
        digit_position += 1

    return total

def search_palindromes(test_str, str_len, odd_num, digit_add, digit_options, base):
    """
    Recursively develops each possible palindromic string using the provided set of digits.
    When the limit defined by digit_add is reached, checks if the number is prime.
    :params:
    test_str: palindromic string being built.  Use "".
    str_len: current length of the string.  Use 0.
    odd_num: boolean indicating whether the required number of digits is odd
    digit_add: total number of digits in the finished palindrome.
    digit_options: a string with each allowed digit
    base: the base the numebr is in
    return: the total number of prime palindromes in the search space.
    """

    # base case
    if str_len >= digit_add:
        reverse_str = test_str[::-1]

        # remove first character of reverse string for odd number of digits to avoid repeating middle digit
        if odd_num and digit_add > 1:
            reverse_str = reverse_str[1:]
        elif odd_num and digit_add == 1:
            reverse_str = ""

        final_str = f"{test_str}{reverse_str}"

        base_ten_value = convert_to_base_ten(final_str, base)

        if check_if_prime(base_ten_value):
            return 1
        else: return 0

    # recursive case
    else:
        total_primes = 0
        new_len = str_len + 1

        for digit in digit_options:
            new_str = f"{test_str}{digit}"
            primes_found = search_palindromes(new_str, new_len, odd_num, digit_add, digit_options, base)
            total_primes += primes_found
        return total_primes

while True:
    input = sys.stdin.readline().split()
    digits = int(input[0])
    base = int(input[1])

    if digits == 0: break

    # derive problem information
    odd_num_of_digits = digits % 2 == 1
    digit_additions = int(digits//2) + 1 if odd_num_of_digits else int(digits//2)
    digit_options = digit_list[:base]

    # search palindromes for primes
    # we run the first pass outside of the recursive function so we can eliminate even numbers
    primes_found = 1 if digits == 1 else 0 # this algo doesn't find 2, so we're counting it manually

    skip_because_even = True
    for digit in digit_options:
        if skip_because_even:
            skip_because_even = False
            continue

        primes_found += search_palindromes(digit, 1, odd_num_of_digits, digit_additions, digit_options, base)
        skip_because_even = True

    print(f"The number of {digits}-digit palindromic primes < 2^31 in base {base}.")
    print(f"What is {primes_found}?\n")

