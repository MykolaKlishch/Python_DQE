def get_dash_pattern(
        prev_dash_pattern='',
        letter_to_disclose='',
        userinput) -> str:
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

expected_result = {
    ('',
     ''):
}

for arguments in expected_result.keys():
    actual_result = consistent(*arguments)
    if actual_result != expected_result[arguments]:
        print(f'failed:   {arguments}')
        print(f'expected: {expected_result[arguments]}')
        print(f'got:      {actual_result}')
print('tests completed')
