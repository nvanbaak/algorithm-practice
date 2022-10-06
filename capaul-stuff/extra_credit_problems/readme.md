These were extra credit problems from the UW Tacoma Graduate Certificate Program in Software Engineering.  My understanding is that they re problems from previous years of the ICPC.

The IO folder has input files (e.g. "a.in") and output files ("a.out").  Scripts are run using file redirection to import input and output to a result file, which will match the output file if I did it right.

The check-answers script checks the output of a given algorithm (passed as an argument) against the expected solution.  For example, to check whether a.py produces the expected output, you would use:
```
sh check_answers.sh a
```