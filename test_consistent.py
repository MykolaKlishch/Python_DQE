from hangman import consistent

expected_result = {
    ('',
     ''): True,
    ('-',
     ''): True,
    ('-ss-',
     ''): True,
    ('ssss',
     ''): True,
    ('--sa-',
     '--s--'): True,
    ('--ss-',
     '--s--'): False,
    ('--s--',
     '--ss-'): False,
    ('-ass-',
     '-as--'): False,
    ('-as--',
     '-ass-'): False,
    ('--',
     '---'): False,
    ('--',
     'sss'): False,
    ('ss',
     '---'): False,
    ('-sa',
     '-as'): False,
    ('a',
     's'): False,


}

for arguments in expected_result.keys():
    actual_result = consistent(*arguments)
    if actual_result != expected_result[arguments]:
        print(f'failed:   {arguments}')
        print(f'expected: {expected_result[arguments]}')
        print(f'got:      {actual_result}')
print('tests completed')
