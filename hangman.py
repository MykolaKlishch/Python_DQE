"""Hangman game implementation."""

import collections
import itertools
import re
from typing import AbstractSet, Counter, List, Sequence


def get_word_list(filename='words.txt') -> List[str]:
    """Reads the word list from the file.
    In case of OSError, prints customized error message.

    :param filename: name of the file with words
        (default is 'words.txt' from the same directory)
    :type filename: str
    :return: a list of words
    :rtype: List[str]
    """
    try:
        f = open(filename, 'rt', encoding='utf-8')
    except OSError as e:
        print(f'Could not open the file. {e.args[1]}.')
        exit()
    else:
        return [word.strip() for word in f.readlines()]


def filter_word_list(
        word_list: Sequence[str],
        pattern: str) -> List[str]:
    """Filters the list of words.
    Words that do not match the
    specified pattern are excluded.

    :param word_list: a list of words to filter
    :type word_list: Sequence[str]
    :param pattern: regular expression
    :type pattern: str
    :return: a list of words that match the pattern
    :rtype: List[str]
    """
    flags = re.IGNORECASE | re.UNICODE
    compiled_pattern = re.compile(pattern, flags=flags)
    return list(filter(compiled_pattern.match, word_list))


def guess_letter(
        word_list: Sequence[str],
        disclosed: AbstractSet[str]) -> str:
    """Returns the letter which appears in
    the largest number of words from word list.

    :param word_list: a list of words
    :type word_list: Sequence[str]
    :param disclosed: letters to ignore (already guessed)
    :type disclosed: AbstractSet[str]
    :return: a single letter
    :rtype: str
        if the word list is empty, returns None
    """
    letters = collections.Counter(itertools.chain.from_iterable(
        (set(word.lower()) - disclosed for word in word_list)))
    if letters:
        print_statistics(word_list, letters)
        return letters.most_common(1)[0][0]


def print_statistics(
        word_list: Sequence[str],
        letters: Counter,
        options=5) -> None:
    """Prints information that is used to guess the next letter.

    :param word_list: a list of words
    :type word_list: Sequence[str]
    :param letters: Counter {letter: number of words}
    :type letters: Counter
    :param options: number of the most common letters to display
        (default is 5)
    :type options: int
    :return: None
    """
    total_words = len(word_list)
    print(f' ║ I know {total_words} words that match your pattern.')
    count_field_width = len(str(letters.most_common(1)[0][1]))
    for letter in letters.most_common(options):
        counts = letter[1]
        probability = counts / total_words
        print(f' ║ Letter "{letter[0]}" '
              f'appears in {counts:<{count_field_width}} '
              f'of them ({probability:<5.2%})')


def get_dash_pattern(
        prev_dash_pattern='',
        letter_to_disclose='') -> str:
    """Returns dash pattern based on the input from the user.
    Validates the input it correct and provides hints if it is not correct.

    :param prev_dash_pattern: str
        (default is '')
    :type prev_dash_pattern: str
    :param letter_to_disclose: a letter that may be disclosed
        (default is '')
    :type letter_to_disclose: str
    :return: validated dash pattern
    :rtype: str
    """
    inp_msg = 'Enter the dash pattern: '
    flags = re.IGNORECASE | re.UNICODE
    while True:
        dash_pattern = input(inp_msg).lower()
        new_letters = (disclosed_letters(dash_pattern) -
                       disclosed_letters(prev_dash_pattern))
        if not dash_pattern:
            continue
        elif not (re.match(r"^[\w'-]+$", dash_pattern, flags=flags)
                  and re.match(r'^[^\d_]+$', dash_pattern, flags=flags)):
            inp_msg = 'Input must contain only letters, dashes (-), ' \
                      "and apostrophes ('). \nPlease try again: "
            continue
        elif not consistent(dash_pattern, prev_dash_pattern):
            inp_msg = 'This dash pattern is not consistent ' \
                      'with the previous one! \nPlease try again: '
            continue
        elif len(new_letters) > 1 - (not prev_dash_pattern):
            inp_msg = 'You tried to disclose too many ' \
                      'new letters. \nPlease try again: '
            continue
        elif new_letters and letter_to_disclose not in new_letters:
            inp_msg = 'You tried to disclose the wrong ' \
                      'letter. \nPlease try again: '
            continue
        return dash_pattern


def consistent(
        dash_pattern: str,
        prev_dash_pattern='') -> bool:
    """Checks if the new dash pattern
    is consistent with the previous one.

    Takes part in validation of the user input.
    The new dash pattern is considered consistent if:
    1) it has the same length as the previous dash pattern;
    AND 2) all letters disclosed in the previous pattern
    remain at the same positions in the new dash pattern.
    OR 3) there is no previous dash pattern to compare with.

    :param dash_pattern: a new dash pattern
    :type dash_pattern: str
    :param prev_dash_pattern: a previous dash pattern
        (default is '' - means there is no previous dash pattern)
    :type prev_dash_pattern: str
    :return: is the new dash pattern consistent with the previous one
    :rtype: bool
    """
    if not prev_dash_pattern:
        return True
    if len(dash_pattern) != len(prev_dash_pattern):
        return False
    for index in range(len(dash_pattern)):
        if dash_pattern[index] != prev_dash_pattern[index] != '-':
            return False
        if (dash_pattern[index] in prev_dash_pattern
                and prev_dash_pattern[index] != dash_pattern[index]):
            return False
    return True


def disclosed_letters(dash_pattern: str) -> AbstractSet[str]:
    """Returns a set of letters disclosed in the dash pattern.

    :param dash_pattern: dash pattern w/ or w/o letters
    :type dash_pattern: str
    :return: letters that occur in the dash pattern
    :rtype: AbstractSet[str]
    """
    return set(dash_pattern) - set("-")


def convert_into_regex_pattern(dash_pattern: str) -> str:
    """Converts dash pattern into regular expression.

    Generated pattern matches any word which:
    1) has the same length as the dash pattern;
    2) has letters from the dash pattern in the same positions;
    3) doesn't have these letters in any other position.

    :param dash_pattern: dash pattern to convert into regex
    :type: str
    :return: regular expression
    :rtype: str
    """
    disclosed = disclosed_letters(dash_pattern)
    if not disclosed:
        dash_replacement = r"[\w']"
    else:
        dash_replacement = fr"[^{''.join(list(disclosed))}]"
    regex_pattern = dash_pattern.replace("-", dash_replacement)
    final_regex_pattern = fr"^{regex_pattern}$"
    return final_regex_pattern


def the_end(
        word_list: Sequence[str],
        attempts: dict) -> bool:
    """Checks for conditions when the game ends and prints
    the respective output if one of the conditions is True.

    :param word_list: a list of words
    :type word_list: Sequence[str]
    :param attempts: number of attempts to guess a letter
        (successful and unsuccessful)
    :type attempts: dict
    :return: is it the en of the game
    :rtype: bool
    """
    words_left = len(word_list)
    if words_left == 0:
        print("I don't know any word that matches your pattern."
              "\nMaybe you didn't pick your word from "
              "words.txt, did you?")
    elif words_left == 1:
        print(f"""Your word is "{word_list[0]}"!""")
    elif words_left > 1 and len(
            set(word.lower() for word in word_list)) == 1:
        print(f"""Your word is{' either' * (words_left == 2)}"""
              f""" "{'", "'.join(word_list[:-1])}" """
              f"""or "{word_list[-1]}" - depending on the letter case.""")
    else:
        return False
    print(f" ║ Attempts to guess the letter:\n"
          f" ║ * successful   : {attempts['successful']}\n"
          f" ║ * unsuccessful : {attempts['unsuccessful']}\n"
          f" ║ * total        : {sum(attempts.values())}")
    return True


def main():
    """Implements the game process.

    :return: None
    """
    print('How to play:'
          '\n 1. Pick the word from words.txt file.'
          '\n 2. Show the number of letters in your word'
          '\n    by typing a dash pattern (e.g. ---------).'
          '\n 3. If I guessed the letter, please show me the'
          '\n    position(s) of this letter (e.g. -ss------).'
          "\n 4. If I didn't guess the letter, just enter"
          '\n    the same pattern again.\n')
    word_list = get_word_list()
    prev_dash_pattern, letter = '', ''
    attempts = {'successful': 0, 'unsuccessful': 0}
    while True:
        dash_pattern = get_dash_pattern(prev_dash_pattern, letter)
        if prev_dash_pattern == dash_pattern:
            print(f'\nOK, so there is no letter "{letter}" in your word.')
            attempts['unsuccessful'] += 1
            word_list = filter_word_list(word_list, fr'^[^{letter}]+$')
        else:
            if prev_dash_pattern == '':
                print(f'\nOK, so your word is '
                      f'{len(dash_pattern)} characters long.')
            else:
                print(f'\nOK, so your word contains letter "{letter}".')
                attempts['successful'] += 1
            regex_pattern = convert_into_regex_pattern(dash_pattern)
            word_list = filter_word_list(word_list, regex_pattern)
        if the_end(word_list, attempts):
            break
        letter = guess_letter(word_list, disclosed_letters(dash_pattern))
        print(f'Does the word contain letter "{letter}"?')
        prev_dash_pattern = dash_pattern


if __name__ == '__main__':
    main()
