from random import randint

from firemelon import passgen


def generate_pass_non_human(length: int, use_number: bool, separator: str, use_upper: bool, use_lower: bool) -> str:
    password = ''
    genstr = ''
    symbols = {
        'digits' : '1234567890',
        'lowercase' : 'qwertyuiopasdfghjklzxcvbnm',
        'uppercase' : 'QWERTYUIOPASDFGHJKLZXCVBNM'
    }

    for key in symbols:
        if (not use_upper and key == 'uppercase') or (not use_lower and key == 'lowercase') or (not use_number and key == 'digits'):
            continue
        elif separator:
            genstr += separator
        genstr += symbols[key]

    if not genstr:
        return 'You can\'t create password without any symbols!'

    while len(password) < length:
        password += genstr[randint(0, len(genstr) - 1)]

    return password


def generate_pass_human(complexity: int, separator: str, use_number: bool) -> str:
    return passgen(complexity=complexity, sep=separator, use_number=use_number)