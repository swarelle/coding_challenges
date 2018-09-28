Coding challenge completed for Fin for an internship application for Summer 2018.

Original challenge description: https://gist.github.com/johngraham262/9a78c4e2c68eb2fa6918c4f3636fd331

## Running the program ##
Navigate to the folder containing cafe.sh. The program is run with the following
command syntax:
                ./cafe.py <mode> <input file> <output file>
If you wish to run the FIFO algorithm, use 0 for the mode; if you wish to run my
second algorithm, use 1 for the mode.

For example, if the input JSON file is in the same folder and is named input.json,
and you wish to store the output data to output.json in the same folder, run the
following command to get the FIFO solution:
                ./cafe.py 0 input.json output.json


## Design decisions ##
I included all the code in one Python file named cafe.py, since the program doesn't
require complicated object relationships. I created the following classes:
    - Cafe
        Contains the functionality of the program, including the two serving
        algorithms and attributes that store the parameters given by the user
        and the output data
    - InvalidInputDataException
        Extends from the Exception class to indicate that the input JSON is invalid
    - InvalidInputModeException
        Extends from the Exception class to indicate that the given mode is invalid
Tests are in tests.py and are done on the Cafe class's two serving algorithms.


## Second solution ##
I chose to optimize for the number of drinks made (so the cafe can attract more
customers). The code currently fails the general test, and it is implemented with
too many if-else statements. Given more time, I would find a way to meet the goal
of this algorithm using a dynamic programming approach and to rely less on if-else
statements since they make code unclear and easily leave out edge cases.
