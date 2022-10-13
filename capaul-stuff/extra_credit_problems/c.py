# nvanbaak 13 Oct 2022
# print all fractions where numerator and denominator are three digit numbers and
# removing the ones digit of the numerator and the hundreds digit of the denominator
# produces an equivalent fraction

# STRATEGY:
# The naive implementation is just to iterate over all 999 numbers (000 would break) and compare them.
# But since we're only looking at cases of the form **N / N**, we can cut the iteration down to 99 numbers.
# We don't need to worry about whether "0**" constitutes a three-digit number because cancelling the 0
# doesn't change the value of the denominator, meaning the new fraction is 1/10th the value by definition.

for raw_numer in range(10, 100): # we'll add N to the end, so 101 is the minimum here
    for raw_denom in range(1, 100):

        # skip trivial cases
        if raw_numer == raw_denom:
            continue

        for cancel_digit in range(1,10):

            cancelled_fraction = int(raw_numer) / int(raw_denom)

            # set up numerator
            numer = int(f"{raw_numer}{cancel_digit}")

            # set up denom; takes a little more work b/c edge cases
            if int(raw_denom) < 10:
                raw_denom = f"0{raw_denom}"
            denom = int(f"{cancel_digit}{raw_denom}")

            fraction = int(numer) / int(denom)

            if fraction == cancelled_fraction:
                print(f"{numer} / {denom} = {raw_numer} / {raw_denom}")

