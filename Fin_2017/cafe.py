#!/usr/bin/python

import sys
import json


class Cafe:
    def __init__(self, mode, input_data, output_file):
        """ Parses the input arguments from the command line """
        # The two algorithms only need the brewing time for each drink
        self.drinks_time = {"tea": 3, "latte": 4, "affogato": 7}

        self.mode = mode
        self.input_data = input_data
        self.output_file = output_file

        # Making this changeable so I can test a short general case for the
        # second algorithm
        self.open_time = 100

        # Initialize output data as an empty list
        self.output_data = []

    def open_for_business(self):
        self.__check_input_validity()

        # Run the FIFO algorithm
        if self.mode == 0:
            self.__fifo()

        # Run the algorithm for getting the shortest average wait time
        elif self.mode == 1:
            self.__prioritize_number_of_drinks()

        # Invalid mode
        else:
            raise InvalidInputModeException("Input mode is invalid")

        self.__write_output()

    def __fifo(self):
        """
        Finds the baristas' serving data of the given drinks with a FIFO algorithm
        @param input_data - loaded JSON data from the input file
        returns nothing
        """
        barista_one = 0
        barista_two = 0
        for order in self.input_data:
            # If either barista finished making a drink before the next order, update
            # their time to be when the next order comes in
            order_time = order["order_time"]
            if barista_one < order_time:
                barista_one = order_time
            if barista_two < order_time:
                barista_two = order_time

            time_to_make = self.drinks_time[order["type"]]
            barista_one_total = barista_one + time_to_make
            barista_two_total = barista_two + time_to_make

            # Barista one can make it quicker and it's still not closing time
            if (barista_one_total <= barista_two_total) and (barista_one <= self.open_time):
                self.output_data.append({
                    "order_id": order["order_id"],
                    "start_time": barista_one,
                    "barista_id": 1
                })
                barista_one = barista_one_total

            # Barista two can make it quicker and it's still not closing time
            elif (barista_two_total < barista_one_total) and (barista_two <= self.open_time):
                self.output_data.append({
                    "order_id": order["order_id"],
                    "start_time": barista_two,
                    "barista_id": 2
                })
                barista_two = barista_two_total

            # No more orders can be taken because it's past closing time
            else:
                break

    def __prioritize_number_of_drinks(self):
        """
        Finds the baristas' serving data of the given drinks to optimize the number
        of drinks made
        @param input_data - loaded JSON data from the input file
        returns nothing
        """
        # No orders to process
        if len(self.input_data) == 0:
            return

        # Represents the time that the barista will be free and the time their
        # current drink takes to make. "index" keeps track of which element to
        # change if the order of drink-making needs to be changed
        barista_one = {"free_at": 0, "make_time": 0, "index": 0}
        barista_two = barista_one.copy()
        curr_order = 0

        # i represents the number of minutes after the cafe opening
        for i in range(0, self.open_time):

            # This nested for loop checks the orders that came in before this minute
            while (curr_order < len(self.input_data) and
                   self.input_data[curr_order]["order_time"] <= i):
                order = self.input_data[curr_order]
                order_time = order["order_time"]
                make_time = self.drinks_time[order["type"]]


                # Get the start time of the drinks the baristas are currently
                # making
                barista_one_start = barista_one["free_at"] - barista_one["make_time"]
                barista_two_start = barista_two["free_at"] - barista_two["make_time"]

                # A barista is free to take the order or should take this to make
                # more drinks
                if barista_one["free_at"] <= i:
                    self.output_data.append({
                        "order_id": order["order_id"],
                        "start_time": max(barista_one["free_at"], order_time),
                        "barista_id": 1
                    })

                    barista_one["make_time"] = make_time
                    barista_one["free_at"] = i + make_time
                    barista_one["index"] = len(self.output_data) - 1

                    # Look at the next order
                    curr_order += 1
                elif (barista_one["free_at"] > self.open_time and
                      barista_one_start < order_time):
                    barista_one["free_at"] = order_time + make_time
                    barista_one["make_time"] = make_time
                    index = barista_one["index"]
                    self.output_data[index] = {
                        "order_id": order["order_id"],
                        "start_time": order_time,
                        "barista_id": 1
                    }

                    # Look at the next order
                    curr_order += 1
                elif barista_two["free_at"] <= i:
                    self.output_data.append({
                        "order_id": order["order_id"],
                        "start_time": max(barista_two["free_at"], order_time),
                        "barista_id": 2
                    })

                    barista_two["make_time"] = make_time
                    barista_two["free_at"] = i + make_time
                    barista_two["index"] = len(self.output_data) - 1

                    # Look at the next order
                    curr_order += 1
                elif (barista_two["free_at"] > self.open_time and
                      barista_two_start < order_time):
                    barista_two["free_at"] = order_time + make_time
                    barista_two["make_time"] = make_time
                    index = barista_two["index"]
                    self.output_data[index] = {
                        "order_id": order["order_id"],
                        "start_time": order_time,
                        "barista_id": 1
                    }
                    # Look at the next order
                    curr_order += 1

                # No barista is currently free if they took the previous order
                else:

                    # A barista can finish this later order quicker than
                    # their previous order, so make this one first
                    if (order_time + make_time <= self.open_time and
                            order_time + make_time < barista_one["free_at"] and
                            order_time >= barista_one_start):
                        barista_one["free_at"] = order_time + make_time
                        barista_one["make_time"] = make_time
                        index = barista_one["index"]
                        self.output_data[index] = {
                            "order_id": order["order_id"],
                            "start_time": barista_one_start,
                            "barista_id": 1
                        }
                        # Look at the next order
                        curr_order += 1
                    elif (order_time + make_time <= self.open_time and
                          order_time + make_time < barista_two["free_at"] and
                          order_time >= barista_two_start):
                        barista_two["free_at"] = order_time + make_time
                        barista_two["make_time"] = make_time
                        index = barista_two["index"]
                        self.output_data[index] = {
                            "order_id": order["order_id"],
                            "start_time": barista_two_start,
                            "barista_id": 2
                        }
                        # Look at the next order
                        curr_order += 1


    def __drink_count_helper(self, order_id, barista_one, barista_two):
        """
        Helper method for using a greedy algorithm with dynamic programming to
        make the maximum number of drinks
        """




    def __write_output(self):
        """
        Writes the output data to the specified location
        @param output_data - a dictionary containing the cafe serving data
        @param output_location - the given output file name as a string
        return nothing
        """
        with open(self.output_file, 'w') as out:
            out.write(json.dumps(self.output_data, indent=4))


    def __check_input_validity(self):
        # Check if the input is valid
        for order in self.input_data:
            if order["order_time"] < 0:
                raise InvalidInputDataException("Order time is negative")
            if order["type"] not in self.drinks_time:
                raise InvalidInputDataException("Drink type is invalid")
            if order["order_id"] < 1:
                raise InvalidInputDataException("Order ID is negative")


class InvalidInputModeException(Exception):
    """ Exception class for an incorrectly specified mode """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InvalidInputDataException(Exception):
    """ Exception class for an incorrectly specified mode """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Run the program
if __name__ == "__main__":
    # Get the command line inputs
    mode = int(sys.argv[1])
    with open(sys.argv[2], 'r') as input_file:
        decoder = json.JSONDecoder()
        input_data = decoder.decode(input_file.read())
    output_file = sys.argv[3]

    cafe = Cafe(mode, input_data, output_file)
    cafe.open_for_business()
