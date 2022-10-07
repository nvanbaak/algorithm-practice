#!/bin/bash

start_time=`python3 -c 'from time import time; print(int(round(time() * 1000)))'`
python3 $1.py < IO/$1.in > $1-test.out
end_time=`python3 -c 'from time import time; print(int(round(time() * 1000)))'`
time_elapsed=`echo "$end_time - $start_time" | bc`
echo "Time: $time_elapsed ms"

diff $1-test.out IO/$1.out --report-identical-files -y --suppress-common-lines
rm $1-test.out