"""Counts words in a Unicode text file

Longer version.
Has several features that were removed from shorter version:
 * default filename assignment;
 * word column width changes to fit the longest words;
 * filename provided in error output;
 * file is being closed.
"""

from collections import Counter
import re

filename = input('Enter the file name: ')
if not filename:
    filename = 'Book.txt'
try:
    f_handle = open(filename, 'rt', encoding='UTF-8')
except OSError as e:
    print(f'Could not open the file: {filename}\n{e.args[1]}')
    exit()
else:
    content = f_handle.read()
    content = content.lower()
    word_list = re.findall(r'\w+', content)
    word_counter = Counter(word_list)
    word_column_width = len(max(word_list, key=len))
    for word, count in sorted(word_counter.items()):
        print(f'{word:<{word_column_width}} {count} time' + 's' * (count > 1))
        # print('{:<25} {} times'.format(word, count))  # alternative
    f_handle.close()
