#!/usr/bin/python

""" genre.py
Given a file with book titles and descriptions in JSON format and a csv file of
genre keywords and their respective point values, prints the title of each book
followed by the top-three matching genres with their scores (>0) to STDOUT.
"""

import sys
import csv
import json


def main():
    """
    The main function that runs the program, primarily gets the input from the
    command line and delegates program function to other functions
    Input: none
    Output: none
    """
    # Make sure the number of arguments is correct
    if len(sys.argv) < 3:
        sys.exit("Usage: ./genre.py <file of book list as json> " +
                 "<file of genre/keyword/value rows as csv>")

    # Get the list of book titles and descriptions
    with open(sys.argv[1], 'r') as book_file:
        decoder = json.JSONDecoder()
        book_list = decoder.decode(book_file.read())

    # Get the genre/keyword/value information and store as a dictionary, where
    # the key is the genre and the value is also a dictionary, where the key
    # is the keyword and the value is its points
    genre_data = {}
    with open(sys.argv[2], 'r') as genre_file:
        reader = csv.reader(genre_file)

        # Skip the row of table titles
        next(reader)

        # Store each row entry into genre_data
        for row in reader:
            genre = row[0]

            # There is a space in front of each keyword that we want to ignore
            keyword = row[1][1:]

            points = int(row[2])

            if genre in genre_data:
                genre_data[genre][keyword] = points
            else:
                genre_data[genre] = {keyword: points}

    # Call the function that contains the scoring and printing
    match_genres(book_list, genre_data)


def match_genres(book_list, genre_data):
    """
    Given a book list (each book as a dictionary of its title and description)
    and keywords/points that match to genres, determines the top three likely
    genres that each book in the book list belongs to
    Input: book_list - list of books as dictionaries
           genre_data - dictionary of genres and their keywords and points
    Output: none
    """
    # Match each book to its top three genres
    for book in book_list:

        # Print the book title
        print book["title"]

        # Get the scores for each genre
        genre_matching = score_book(book, genre_data)
        scores = calculate_genre_scores(genre_data, genre_matching)

        # Print the top three most likely genres
        print_most_likely_genre(scores)
        print_most_likely_genre(scores)
        print_most_likely_genre(scores)

        # Print a new line after each book
        print


def score_book(book, genre_data):
    """
    Given a book as a dictionary with its title and description, calculates its
    likelihood to belong in a genre based on the given genre_data
    Input: book - a dictionary representing one book
           genre_data - dictionary of genres and their keywords and points
    Output: genre_matching - dictionary of genres and their scores for the given book
    """
    # Construct a dictionary for this book where the keys are the genres and the
    # value is a list containing the number of keywords matched to this genre
    # and a set of keyword matches
    genre_matching = {}

    # Initialize each genre to have 0 matching keywords and an empty set
    for genre in genre_data:
        genre_matching[genre] = [0]
        genre_matching[genre].append(set())

    description = book["description"]
    for i in range(0, len(description)):
        # Check if each genre's keywords match with the current position in the
        # description
        for genre in genre_data:
            for keyword in genre_data[genre]:
                curr = description[i:i + len(keyword)]
                if curr == keyword:
                    # Increment total number of matching keywords for the genre
                    genre_matching[genre][0] += 1

                    # Add the keyword to the set of matching keywords
                    genre_matching[genre][1].add(keyword)

    return genre_matching


def calculate_genre_scores(genre_data, genre_matching):
    """
    Given a dictionary of one book's genre-matching results, calculate its score
    for matching each genre
    Input: genre_data - dictionary of genres and their keywords and points
           genre_matching - a dictionary of genres mapped to the total number of
           matching keywords and a set of unique matching keywords for one book
    Output: scores - a dictionary of genres mapped to their calculated scores for
            the current book
    """
    scores = {}
    for genre in genre_matching:
        # Initialize the score as 0
        scores[genre] = 0

        # If there were any matching keywords, update the score
        if genre_matching[genre][0] > 0:
            # Calculate the average point value of unique matching keywords
            total_unique_points = 0
            for keyword in genre_matching[genre][1]:
                total_unique_points += genre_data[genre][keyword]
            average_points = total_unique_points / len(genre_matching[genre][1])

            # Calculate the overall score for matching this genre
            scores[genre] = genre_matching[genre][0] * average_points

    return scores


def print_most_likely_genre(scores):
    """
    Given a dictionary of genres matched to their scores for one book, print the
    most likely genre with its scores
    Input: scores - a dictionary of genres mapped to their calculated scores
    Output: none
    """
    try:
        # Gets the genre with the maximum score
        most_likely_genre = max(scores.iterkeys(), key=(lambda key: scores[key]))
    # ValueError means that there are no more keys in the dictionary (there are
    # less than 3 genres that have a positive score for this book)
    except ValueError:
        return

    if scores[most_likely_genre] > 0:
        # Print the most likely genre with its score and delete the genre from
        # the dictionary so we don't keep printing the same genre
        print most_likely_genre + ",", scores.pop(most_likely_genre, 0)


if __name__ == "__main__":
    main()
