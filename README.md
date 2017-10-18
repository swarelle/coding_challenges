## Running the program ##
Note that this program is in Python 2 syntax.
Navigate to the folder containing genre.py. The program is run with the following
command syntax:
                ./genre.py <book list (JSON)> <keywords (csv)>

For example, if the input files are in the same folder and are named books.txt
and keywords.csv, respectively, run the following command to print the genre-
matching result to STDOUT:
                ./cafe.py books.txt keywords.csv


## Trade-offs and edge cases ##
A major trade-off is made to detect all keyword matches, not just to full words
but to parts of words as well. Some examples of these "partial match" cases are:
    - "Inifinite Jest"
    Description contains "subplots" and there is a keyword "subplot"
    - "Hunger Games"
    Description contains "not-too-distant future" and there is a keyword "distant
    future"
    Also contains "fighting" and there is a keyword "fight"

The program originally optimizes for efficiency by splitting the description into
individual words and checks whether each singular word and pair of words matches
with any keywords; however, doing so will omit the above cases as matches, which
is not how the program is expected to behave. In order to account for this, the
program instead iterates through the description character by character and checks
whether the string of the length of each keyword matches any of the given keywords.
This is a trade-off between speed and accuracy. Its slowdown is negligible (by humans)
if book descriptions are not long and the number of genre keywords is not large.

An edge case that the program handles is if there are less than three genres that
we are trying to match a book to - the print_most_likely_genre function catches
any exceptions when trying to get a max score out of an empty dictionary.


## Total time spent ##
Two hours.
