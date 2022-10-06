#!/bin/bash

python3 $1.py < IO/$1.in > $1-output.txt
diff $1-output.txt IO/$1.out --report-identical-files
rm $1-output.txt