from collections import Counter
import itertools
import re
from typing import AbstractSet, Iterable, List


def get_word_list(filename='words.txt') -> List[str]:
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
        word_list: Iterable[str],
        guessed: AbstractSet[str]) -> str:
    """Returns the letter which appears
    in the largest number of words from word list.
    If the word list is empty, returns None.
    """
    letters = Counter(itertools.chain.from_iterable(
        (set(word.lower()) - guessed for word in word_list)))
    print(letters)  # make proper statistical output
    if letters:
        return letters.most_common(1)[0][0]


def consistent(
        dash_pattern: str,
        prev_dash_pattern='') -> bool:
    """Checks if the new dash pattern
    is consistent with the previous one.
    The new dash pattern is considered consistent if and only if:
    1) it has the same length as the previous dash pattern;
    2) all letters disclosed in the previous pattern
       remain at the same positions in the new dash pattern.
    """

    if not prev_dash_pattern:
        return True
    if len(dash_pattern) != len(prev_dash_pattern):
        return False
    for index in range(len(dash_pattern)):
        if '-' != prev_dash_pattern[index] != dash_pattern[index]:
            return False
        elif (dash_pattern[index] in prev_dash_pattern
              and prev_dash_pattern[index] != dash_pattern[index]):
            return False
    return True


def get_dash_pattern(
        prev_dash_pattern='',
        letter_to_disclose='') -> str:
    """<documentation>"""
    inp_msg = 'Enter the dash pattern of the word: '
    flags = re.IGNORECASE | re.UNICODE
    while True:
        dash_pattern = input(inp_msg).lower()
        if not dash_pattern:
            continue
        new_letters = (set(dash_pattern) - set(prev_dash_pattern))
        if not (re.match(r'^[\w\-]+$', dash_pattern, flags=flags)
                and re.match(r'^[^\d_]+$', dash_pattern)):
            inp_msg = 'Input should contain only letters and dashes. ' \
                      '\nPlease try again: '
            continue
        elif not consistent(dash_pattern, prev_dash_pattern):
            inp_msg = 'This dash pattern is not consistent ' \
                      'with the previous one! \nPlease try again: '
            continue
        elif len(new_letters) > 1:
            inp_msg = 'You tried to disclose too many ' \
                      'new letters. \nPlease try again: '
            continue
        elif new_letters and (letter_to_disclose not in str(new_letters)):
            inp_msg = 'You tried to disclose the wrong letter. ' \
                      '\nPlease try again: '
            continue
        return dash_pattern


def convert_into_regex_pattern(dash_pattern: str) -> str:
    """Converts dash pattern into regular expression."""
    regex_pattern = dash_pattern.replace('-', r"[\w\']")
    final_regex_pattern = fr"^{regex_pattern}$"
    return final_regex_pattern


def _main():
    word_list = get_word_list()
    prev_dash_pattern, letter = '', ''
    guessed_letters = set()
    while True:
        dash_pattern = get_dash_pattern(
            prev_dash_pattern, letter)
        if dash_pattern == prev_dash_pattern:
            print(f'OK, so there is no letter "{letter}" in your word.')
            word_list = filter_word_list(word_list, fr'^[^{letter}]+$')
        else:
            guessed_letters.add(letter)
            regex_pattern = convert_into_regex_pattern(dash_pattern)
            word_list = filter_word_list(word_list, regex_pattern)
        if len(word_list) == 0:
            print("I don't know any word that matches your pattern"
                  "\nMaybe you didn't pick your word from "
                  "words.txt, did you?")
            break
        if len(word_list) == 1:
            print(f"""I guessed! It's "{word_list.pop()}"!""")
            break
        if len(word_list) > 1 and len(
                set(word.lower() for word in word_list)) == 1:
            print(f'The word is among the following: {word_list}' 
                  'depending on the case.')
            break
        letter = guess_letter(word_list, guessed_letters)
        print(f'Does the word contain letter "{letter}"?')
        prev_dash_pattern = dash_pattern


if __name__ == '__main__':
    _main()
