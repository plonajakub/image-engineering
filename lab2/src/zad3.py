from math import *


def sigmoid(x):
    return 1 / (1 + exp(-x))


if __name__ == '__main__':
    with open('../misc/zad3_files/input.txt') as f_args:
        args = f_args.read().split('\n')

    str_out = ''
    for val in args:
        str_out += 'sigmoid({}) = {}\n'.format(val, sigmoid(float(val)))

    with open('../misc/zad3_files/output.txt', 'w') as f_values:
        f_values.write(str_out)
