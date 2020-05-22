"""Hangman game implementation"""

from collections import Counter
import itertools
import re
from typing import AbstractSet, Iterable, List, Sequence


def get_word_list(filename='words.txt') -> List[str]:
    """Reads the word list from the file.
    In case of OSError, prints customized error message."""
    try:
        f = open(filename, 'rt', encoding='utf-8')
    except OSError as e:
        print(f'Could not open the file. {e.args[1]}.')
        exit()
    else:
        return [word.strip() for word in f.readlines()]


def filter_word_list(
        word_list: Iterable[str],
        pattern: str) -> List[str]:
    """Filters the list of words.
    Words that do not match the
    specified pattern are excluded.
    """
    flags = re.IGNORECASE | re.UNICODE
    compiled_pattern = re.compile(pattern, flags=flags)
    return list(filter(compiled_pattern.match, word_list))


def guess_letter(
        word_list: Sequence[str],
        guessed: AbstractSet[str]) -> str:
    """Returns the letter which appears
    in the largest number of words from word list.
    If the word list is empty, returns None.
    """
    letters = Counter(itertools.chain.from_iterable(
        (set(word.lower()) - guessed for word in word_list)))
    print_statistics(word_list, letters)
    if letters:
        return letters.most_common(1)[0][0]


def print_statistics(
        word_list: Sequence[str],
        letters,
        options=3) -> None:
    """Prints information that is used to guess the next letter."""
    total_words = len(word_list)
    print(f' ║ There are {total_words} suitable words in the word list.')
    count_field_width = len(str(letters.most_common(1)[0][1]))
    for letter in letters.most_common(options):
        counts = letter[1]
        probability = counts / total_words
        print(f' ║ Letter {letter[0]} '
              f'appears in {counts:<{count_field_width}} '
              f'of them ({probability:<5.2%})')


def consistent(
        dash_pattern: str,
        prev_dash_pattern='') -> bool:
    """Checks if the new dash pattern
    is consistent with the previous one.
    Takes part in the validation of user input.
    The new dash pattern is considered consistent if:
    1) it has the same length as the previous dash pattern;
    AND
    2) all letters disclosed in the previous pattern
       remain at the same positions in the new dash pattern.
    OR
    3) there is no previous dash pattern to compare with.
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


def get_dash_pattern(
        prev_dash_pattern='',
        letter_to_disclose='') -> str:
    """Takes dash pattern as an input from the user.
    Checks if the input it correct and provides hints if it is not.
    """
    inp_msg = 'Enter the dash pattern: '
    flags = re.IGNORECASE | re.UNICODE
    while True:
        dash_pattern = input(inp_msg).lower()
        new_chars = (set(dash_pattern) - set(prev_dash_pattern))
        if not dash_pattern:
            continue
        elif not (re.match(r"^[\w'\-]+$", dash_pattern, flags=flags)
                  and re.match(r'^[^\d_]+$', dash_pattern)):
            inp_msg = 'Input must contain only letters,' \
                      "dashes (-), and apostrophes ('). " \
                      '\nPlease try again: '
            continue
        elif not consistent(dash_pattern, prev_dash_pattern):
            inp_msg = 'This dash pattern is not consistent ' \
                      'with the previous one! \nPlease try again: '
            continue
        elif (len(new_chars) > 1
              or not prev_dash_pattern and '-' not in dash_pattern):
            inp_msg = 'You tried to disclose too many ' \
                      'new letters. \nPlease try again: '
            continue
        elif new_chars and letter_to_disclose not in str(new_chars):
            inp_msg = 'You tried to disclose the wrong letter. ' \
                      '\nPlease try again: '
            continue
        return dash_pattern


def convert_into_regex_pattern(dash_pattern: str) -> str:
    """Converts dash pattern into regular expression.
    Generated pattern matches any word which:
    1) has letters from the dash pattern in the respective positions;
    2) doesn't have these letters in any other position.
    """
    disclosed_letters = set(dash_pattern) - set('-')
    if not disclosed_letters:
        regex_pattern = dash_pattern.replace(
            '-', fr"[\w\']")
    else:
        disclosed_letters = ''.join(list(disclosed_letters))
        disclosed_letters.replace("'", r"\'")
        regex_pattern = dash_pattern.replace(
            '-', fr"[^{disclosed_letters}]")
    final_regex_pattern = fr"^{regex_pattern}$"
    return final_regex_pattern


def end_game(word_list, attempts) -> bool:
    """Checks for conditions when the game ends and prints
    the respective output if one of the conditions is True.
    """
    if len(word_list) == 0:
        print("I don't know any word that matches your pattern."
              "\nMaybe you didn't pick your word from "
              "words.txt, did you?")
    elif len(word_list) == 1:
        print(f"""I guessed! It's "{word_list.pop()}"!""")
    elif len(word_list) > 1 and len(
            set(word.lower() for word in word_list)) == 1:
        print(f'The word is among the following: {word_list}'
              ' - depending on the case.')
    else:
        return False
    print(f" ║ Attempts to guess the letter:"
          f"\n ║  * successful   : {attempts['successful']}"
          f"\n ║  * unsuccessful : {attempts['unsuccessful']}"
          f"\n ║  * total        : {sum(attempts.values())}")
    return True


def _main():
    print('Game rules:'
          '\n 1. Pick the word from words.txt file.'
          '\n 2. Show the numbers of letters in your word'
          '\n    by typing a dash pattern (e.g. --------).'
          '\n 3. If I guessed the letter, please show me the'
          '\n    position(s) of this letter (e.g. -ss-----).'
          "\n 4. If I didn't guess the letter, just enter"
          '\n    the same pattern again.\n')
    word_list = get_word_list()
    prev_dash_pattern, letter = '', ''
    guessed_letters = set()
    attempts = {'successful': 0, 'unsuccessful': 0}
    while True:
        dash_pattern = get_dash_pattern(prev_dash_pattern, letter)
        regex_pattern = convert_into_regex_pattern(dash_pattern)
        word_list = filter_word_list(word_list, regex_pattern)
        if prev_dash_pattern == '':
            print(f'\nOK, so your word is '
                  f'{len(dash_pattern)} characters long.')
        elif prev_dash_pattern == dash_pattern:
            print(f'\nOK, so there is no letter "{letter}" in your word.')
            attempts['unsuccessful'] += 1
            word_list = filter_word_list(word_list, fr'^[^{letter}]+$')
        else:
            print(f'\nOK, so your word contains letter "{letter}".')
            attempts['successful'] += 1
            guessed_letters.add(letter)
        if end_game(word_list, attempts):
            break
        letter = guess_letter(word_list, guessed_letters)
        print(f'Does the word contain letter "{letter}"?')
        prev_dash_pattern = dash_pattern


if __name__ == '__main__':
    _main()
