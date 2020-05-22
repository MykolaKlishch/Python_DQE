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
        word_list = [word.strip() for word in f.readlines()]
        return word_list


def filter_word_list(
        word_list: Iterable[str],
        pattern: str) -> List[str]:
    flags = re.IGNORECASE | re.UNICODE
    compiled_pattern = re.compile(pattern, flags=flags)
    return list(filter(compiled_pattern.match, word_list))


def guess_letter(
        word_list: Iterable[str],
        guessed: AbstractSet[str]) -> str:
    letters = Counter(itertools.chain.from_iterable(
        (set(word.lower()) - guessed for word in word_list)))
    print(letters)  # make proper statistical output
    return letters.most_common(1)[0][0]


def consistent(ndp: str, pdp='') -> bool:
    if not pdp:
        return True
    if len(ndp) != len(pdp):
        return False
    else:
        for index in range(len(ndp)):
            if pdp[index] != '-' and pdp[index] != ndp[index]:
                return False
    return True


def get_dash_pattern(prev_dash_pattern='', letter_to_disclose='') -> str:
    inp_msg = 'Enter the dash pattern of the word: '
    flags = re.IGNORECASE | re.UNICODE
    while True:
        dash_pattern = input(inp_msg).lower()
        new_letters = set(dash_pattern) - set(prev_dash_pattern)
        if not re.match(r'^[\w-]+$', dash_pattern, flags=flags):
            inp_msg = 'Input should contain only and letters. ' \
                      '\nPlease try again: '
            continue
        elif not consistent(dash_pattern, prev_dash_pattern):
            inp_msg = 'This dash pattern is inconsistent ' \
                      'with the previous one! \nPlease try again: '
            continue
        elif len(new_letters) > 1:
            inp_msg = 'You tried to disclose too many ' \
                      'new letters. \nPlease try again: '
            continue
        elif new_letters and letter_to_disclose not in str(new_letters):
            inp_msg = 'You tried to disclose the wrong letter. ' \
                      '\nPlease try again: '
            continue
        return dash_pattern


def convert_into_regex_pattern(dash_pattern: str) -> str:
    regex_pattern = dash_pattern.replace('-', r"[\w\']")
    final_regex_pattern = fr"^{regex_pattern}$"
    return final_regex_pattern


def _main():
    word_list = get_word_list()
    prev_dash_pattern = ''
    letter = ''  # letter to disclose
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
        if len(word_list) == 1:
            print(f"""I guessed! It's "{word_list.pop()}"!""")
            break
        elif len(word_list) == 0:
            print("I don't know any word that matches your pattern"
                  "\nMaybe you didn't pick your word from "
                  "words.txt, did you?")
            break
        letter = guess_letter(word_list, guessed_letters)
        print(f'Does the word contain letter "{letter}"?')
        prev_dash_pattern = dash_pattern


if __name__ == '__main__':
    _main()
