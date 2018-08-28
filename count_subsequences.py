from __future__ import print_function
from functools import reduce
import csv
import sys
import ast


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def read_in():
    """Read all lines from stdin
    Strips newline characters from each line
    """
    lines = [x.strip() for x in sys.stdin.readlines()]
    return lines


if __name__ == '__main__':
    print('Reading input file...', end='')
    all_data = map(lambda x: x.split('\t'), read_in())
    print('done')

    print('Sorting rows...', end='')
    all_data = sorted(all_data, key=lambda x: x[0])
    print('done')

    seed = all_data[0][0]

    i = 0
    first = True
    rows = list()
    total = 0
    for r in all_data:
        if (r[0][:len(seed)] == seed):
            rows.append(r[0])
            total = total + int(r[1])
        else:
            with open('output.tsv', 'w' if first is True else 'a') as tsvfile:
                writer = csv.writer(tsvfile, delimiter='\t')
                writer.writerow([seed, rows, total])
            first = False

            seed = r[0]
            rows[:] = [r[0]]
            total = int(r[1])
            progress(i, len(all_data), status='finding locations')
        i = i + 1
