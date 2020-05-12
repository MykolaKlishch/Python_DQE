"""Counts words in a Unicode text file"""

from collections import Counter
from re import findall

try:
    words = findall(r'\w+', open(input('Filename: ')).read().lower())
except OSError as e:
    print(f'Could not open the file. {e.args[1]}.')
    exit()
else:
    for w, c in sorted(Counter(words).items()):
        print(f'{w:<25} {c} time' + 's' * (c > 1))

# alternative ways to format the output:
# f'{w:<25} {c} time'
# '{:<25} {} time'.format(w, c)
