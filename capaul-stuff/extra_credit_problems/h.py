# nvanbaak 1 Nov
# Given text input, change all capital letters to lower case unless they're the first letter to follow (.|?|!)

# I think the simplest way to do this is to iterate over the string and set a flag if we find punctuation.

import sys

input_text = sys.stdin.read().strip()

output_text = ""
capital_flag = False

for char in input_text:

    ascii_value = ord(char)

    if capital_flag:
        output_text += char.upper()
        if char not in [" ", ")", "(", "\n"]: capital_flag = False
    else: output_text += char.lower()

    if char in ["!", "?", "."]:
        capital_flag = True

print(output_text)