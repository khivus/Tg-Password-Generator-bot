from random import randint

from firemelon import passgen


def generate_pass_numbers_only(length: int):
    password = ''
    while len(password) < length:
        num = randint(0, 10)
        password += str(num)
    return password


def generate_pass_non_human(length: int, use_number: bool):
    password = ''
    if use_number:
        template = '1234567890' + \
                   'qwertyuiopasdfghjklzxcvbnm' + \
                   'QWERTYUIOPASDFGHJKLZXCVBNM' + \
                   '!@#$%^&*()_+-=\\\'\";:`~|/?.,'
    else:
        template = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    while len(password) < length:
        num = randint(0, len(template) - 1)
        password += template[num]
    return password


def generate_pass_human(complexity: int, separator: str, use_number: bool):
    return passgen(complexity=complexity, sep=separator, use_number=use_number)
