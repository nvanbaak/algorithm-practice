# 6 Oct 22 nvanbaak
# given a set of names and lines of random text, determine which names are present in the text

# STRATEGY:
# This won't scale well, but I'm tempted to just throw the names in a list,
# split the text into words, and check if each word is in the list
# You know what, we'll start there and optimize later

import sys

problem_sets = int(sys.stdin.readline().strip())

for problem in range(problem_sets):
    print(f"Test set {problem+1}:")
    # we make a list of names and a corresponding list of attendance
    name_count = int(sys.stdin.readline().strip())
    names = []
    attendance = []
    for _ in range(name_count):
        name = sys.stdin.readline().strip()
        names.append(name)
        attendance.append(False)

    # split the data stream into words
    data_line_count = int(sys.stdin.readline().strip())
    for _ in range(data_line_count):
        data_line = sys.stdin.readline().strip()
        data = str(data_line).split(" ")
        for word in data:
            # if the word's one of our names, mark them present
            if word in names:
                name_index = names.index(word)
                attendance[name_index] = True

    # print role call
    index = 0
    for name in names:
        attendance_status = "present" if attendance[index] else "absent"
        print(f"{name} is {attendance_status}")
        index += 1
    print()
