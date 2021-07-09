import sys


def print_log(message: str, margin=50):
    sys.stdout.write('\r')
    sys.stdout.write(message.ljust(margin))
    sys.stdout.flush()


def print_progress(division: int, length: int, i: int):
    unit = length // division
    if i % unit == 0:
        progress_bar = '*' * int(i / unit) + '-' * (100 - int(i / unit))
        print_log(f'Progress: {progress_bar} {int(i / unit)}/100')

