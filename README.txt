~* Functionalities
- Basic functionality as described in prompt
- Optimized travel route (scripts automatically run the optimizing function)
- Unit of distance (only by running the bash script)
Note: vacationing-salesman.py uses sys.argv to retrieve the cities rather than using
sys.stdin, but vacationing-salesman-stdin.py uses sys.stdin. However, the user cannot
specify the distance's units when using vacationing-salesman-stdin.py.
Note 2: In order to run the non-optimized distance function, the user currently needs
to manually comment out the following lines from the code of either version of the
Python script:
                        optimized_results = optimizeDist(cities,unit)
                        cities = optimized_results[0]
                        distances = optimized_results[1]
Then uncomment the line "distances = findDist(cities, unit)" just above the code
the user just commented out.


~* Running the code with the option of indicating units
1. Ensure that geopy is installed (on a mac, you can install it by running "pip install
geopy" in the terminal)
2. Run the following line in your terminal, and replace "/usr/local/bin/python" in
run.sh with the result your terminal outputs.
                                which python
3. Using the terminal, navigate to the folder containing my solution files and run
the following line:
                            sh run.sh <cities> <unit>
Where "<cities>" should be replaced with the name of the text file (in the same directory)
containing the "City, Country" pairs and "<unit>" should be replaced with either
"mi" or "km" to indicate the preferred unit. If a unit is not given, the script
will automatically use miles as the unit.


~* Running the code without the option of indicating units (but uses stdin)
1. Ensure that geopy is installed (on a mac, you can install it by running "pip install
geopy" in the terminal)
2. Using the terminal, navigate to the folder containing my solution files and run
the following line:
                    python vacationing-salesman-stdin.py < <cities>
Where "<cities>" should be replaced with the name of the text file (in the same
directory) containing the "City, Country" pairs.


~* Design choices
I wrote my solution in Python because of the following three reasons:
- its simple, intuitive syntax
- the ease of compiling and running the code from the terminal
- the ease of importing libraries and interacting with stdin and stdout

The design choices that I mainly considered is how to wrap the Python script.
I chose to write a bash script that calls the Python script vacationing-salesman.py
to achieve the option for the user to input the distance's units, but that is
using sys.argv to retrieve the cities rather than using stdin - if the Python
script were still to use stdin, that means the indication of the distance's
unit must be within the text file with the cities since there can only be one
stdin input at a time. The instructions on running both Python scripts are described
above.

As a note, both scripts default to using miles as the distance unit.


~* Next steps
Given more time, I would find out how to make Python scripts to allow for an option
(I looked into optparse and argparse but didn't have time to implement them) or
for bash scripts to allow for multiple optional arguments so that the user doesn't
need to go into the code to switch between the "regular" and "optimized" distance
functions.

I would also try to implement the option for mode of travel by searching for
libraries that retrieve data from online maps, such as Google Maps data, then
switch between the modes using if blocks checking for the user input string.
