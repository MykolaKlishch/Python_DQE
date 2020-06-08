"""This script tests two ways to guess next letter in
Hangman game and creates a csv report with obtained dataset:

===:Approaches/methods/ways:===
 1. Return the the MOST FREQUENT LETTER
    among the words from the word list.
    Implemented in guess_letter_by_letter_count()
    (defined in the current module)

 2. Return the letter that appears in
    the THE LARGEST NUMBER OF WORDS from the word list.
    Implemented in guess_letter_by_word_count()
    (imported from 'hangman' module)

===:Example of different choice:===
    Words:
    'element', 'torch', 'today', 'especially'

    Approach 1: choose letter 'E' because it appears 5 times in these words:
    'ElEmEnt', 'torch', 'today', 'EspEcially'
    Do not choose letter 't' - it appears only 3 times.

    Approach 2: choose letter 'T' because it appears in 3 of 4 words:
    'ELEMENT', 'TORCH', 'TODAY', 'especially'
    Do not choose letter 'e' - despite it is more frequent in general,
    it appears only in 2 words. Choosing 't' is safer than choosing 'e'.

===:Testing sample:===
    102305 words from words.txt file (must reside in current directory).

===:Metrics collected:===
    Successful, unsuccessful and total attempts to guess a letter
    before the word is guessed * for 2 approaches * for each of 102305 words.

===:Report:===
    Numbers of all attempts are recorded and saved as
    'attempts_by_approach.csv' file in current directory.
"""

import collections
import itertools
import csv
import os
import datetime
from typing import AbstractSet, Callable, Dict, Sequence
from hangman import get_word_list, filter_word_list, \
    disclosed_letters, convert_into_regex_pattern, \
    guess_letter as guess_letter_by_word_count


def guess_letter_by_letter_count(
        word_list: Sequence[str],
        disclosed: AbstractSet[str]) -> str:
    """Returns the most frequent letter
    among the words from the word list.
    Alternative to guess_letter_by_letter_count().

    The counter counts the total occurrences of the letter in all
    words. Letters that already have been disclosed are ignored.

    :param word_list: a list of words
    :param disclosed: letters to ignore (already guessed)
    :return: a single letter; if the word list is empty, returns None
    """
    letters = collections.Counter(itertools.chain.from_iterable(
        (word.lower() for word in word_list)))
    for letter in disclosed:
        if letter in letters.keys():
            del letters[letter]
    assert set(letters.keys()).isdisjoint(disclosed)
    if letters:
        return letters.most_common(1)[0][0]


def play_game(word_to_guess: str,
              guess_letter_function: Callable,
              word_list: Sequence[str]) -> Dict[str, int]:
    """Implements the game process (i.e. single iteration).

    A simplified version of '_main()' from the 'hangman' module.
    The word list is filtered after each attempt to guess a letter,
    both successful and unsuccessful. So each next guess is based on
    the recalculated probabilities. Check guess_letter.__doc__ and
    convert_into_regex_pattern.__doc__ for more details.

    :param word_to_guess: a word to guess in this iteration
    :param guess_letter_function: one of two functions to guess a letter
    :param word_list: a full list of words (already retrieved)
    :return: number of attempts
    """
    word_to_guess = word_to_guess.lower()
    print(word_to_guess, (
        "by_word_count", "by_letter_count"
    )["by_letter_count" in str(guess_letter_function)])
    dash_pattern = "-" * len(word_to_guess)
    regex_pattern = convert_into_regex_pattern(dash_pattern)
    word_list = filter_word_list(word_list, regex_pattern)
    attempts = {'successful': 0, 'unsuccessful': 0}
    while True:
        letter = guess_letter_function(
            word_list, disclosed_letters(dash_pattern))
        if letter not in word_to_guess:
            attempts['unsuccessful'] += 1
            word_list = filter_word_list(word_list, fr'^[^{letter}]+$')
        elif letter in word_to_guess:
            attempts['successful'] += 1
            dash_pattern = "".join([
                (dash_pattern[i], letter)[word_to_guess[i] == letter]
                for i in range(len(word_to_guess))])
            regex_pattern = convert_into_regex_pattern(dash_pattern)
            word_list = filter_word_list(word_list, regex_pattern)
        print(letter + "? -> " + dash_pattern)
        if (len(word_list) == 1
                or len(set(word.lower() for word in word_list)) == 1):
            print("guessed: " + word_list.pop())
            print()
            return attempts


def try_two_methods(word: str,
                    word_list: Sequence[str]) -> Dict[str, int]:
    """Plays 2 games using two different functions to guess letters
    in the same word. Returns a single entry for the dataset.
    The entry contains the number of attempts to guess the letters
    in the word by using two different methods.

    :param word: word to guess
    :param word_list: a full list of words (already retrieved)
    :return: entry for the dataset
    """
    attempts_by_word_count = play_game(
        word_to_guess=word,
        guess_letter_function=guess_letter_by_word_count,
        word_list=word_list)
    attempts_by_letter_count = play_game(
        word_to_guess=word,
        guess_letter_function=guess_letter_by_letter_count,
        word_list=word_list)
    record = {
        'word': word,
        'word_length': len(word),
        'by_word_count_guessed': attempts_by_word_count['successful'],
        'by_word_count_missed': attempts_by_word_count['unsuccessful'],
        'by_word_count_total': sum(attempts_by_word_count.values()),
        'by_letter_count_guessed': attempts_by_letter_count['successful'],
        'by_letter_count_missed': attempts_by_letter_count['unsuccessful'],
        'by_letter_count_total': sum(attempts_by_letter_count.values())
    }
    return record


def create_abs_filename():
    """Generates absolute filename for the report file.
    Filename contains timestamp to avoid accidental overwriting.
    """
    timestamp = str(datetime.datetime.today())
    timestamp = timestamp.replace(" ", "_").replace(":", "-")
    filename = f'report_{timestamp}.csv'
    abs_filename = os.path.join(os.getcwd(), filename)
    return abs_filename


def play_iterated_game(start=0, stop=102305) -> None:
    """Guess every word from the word list
    and record the numbers of all attempts in the csv report.
    If start and/or stop parameters are be specified,
    only part of it may be used.

    :param start: index to start.
    :param stop: index to stop.
    :return: None - collected data are dumped as csv
    """
    word_list = get_word_list()[start:stop]
    first_record = try_two_methods(word_list[0], word_list)
    csv_file = open(create_abs_filename(), 'w',
                    encoding='utf-8', newline='')
    writer = csv.DictWriter(csv_file, dialect='excel',
                            fieldnames=first_record.keys())
    writer.writeheader()
    writer.writerow(first_record)
    try:
        for word in word_list[1:]:
            writer.writerow(try_two_methods(word, word_list))
    except KeyboardInterrupt:
        pass
    else:
        print("csv file generated successfully")
    finally:
        csv_file.close()
        print("csv file successfully closed")


# If 'print_statistics(word_list, letters)' line
# in 'hangman' module remain uncommented, the log is printed with
# additional information which might be unnecessary for this test.
# However, csv report is not affected by this in any way.
if __name__ == "__main__":
    play_iterated_game()
