#!/bin/bash

py -3 $1.py < IO/$1.in > $1-test.out
diff $1-test.out IO/$1.out --report-identical-files -y --suppress-common-lines --strip-trailing-cr
rm $1-test.out