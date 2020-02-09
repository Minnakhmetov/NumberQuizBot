import random


def get_number(length, is_integer):
    number = ''

    if length == 1:
        is_integer = True

    for i in range(length):
        if i == 0:
            number += str(random.randint(1, 9))
        else:
            number += str(random.randint(0, 9))

    if not is_integer:
        digits_before_point = random.randint(1, length - 1)
        number = number[:digits_before_point] + '.' + number[digits_before_point:]

    return number



