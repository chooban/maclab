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


# given a sequence of tuples like [(3,'c',6),(7,'a',2),(88,'c',4),(45,'a',0)],
# returns a dict grouping tuples by idx-th element - with idx=1 we have:
# if merge is True {'c':(3,6,88,4),     'a':(7,2,45,0)}
# if merge is False {'c':((3,6),(88,4)), 'a':((7,2),(45,0))}
def group_by(seqs, idx=0, merge=False):
    d = dict()
    for seq in seqs:
        k = seq[idx]
        v = (d.get(k, tuple()) + (seq[:idx] + seq[idx + 1:]
             if merge
             else (seq[:idx] + seq[idx + 1:], )))
        d.update({k: v})
    return d


def build_rows(rows, r):
    locations = ast.literal_eval(r[4])

    if len(locations) == 0:
        locations.append('NaN')

    for l in locations:
        rows.append((r[0], int(r[1]), float(r[2]), int(r[3]), l))


def process_seed(seed, subsequences, cutoff):
    rows = list()
    grouped = group_by(subsequences, idx=4)

    for location, elements in grouped.items():
        count = reduce(lambda x, y: x + y[3], elements, 0)
        if (count > cutoff):
            sequences = list(set(reduce(lambda x, y: x + [y[0]], elements, [])))
            sequences.sort()
            t = (seed, count, location, sequences)
            rows.append(t)
    return rows


if __name__ == '__main__':
    COUNT_CUTOFF = 50
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
    for r in all_data:
        if (r[0][:len(seed)] == seed):
            build_rows(rows, r)
        else:
            processed = process_seed(seed, rows, COUNT_CUTOFF)

            with open('output.tsv', 'w' if first is True else 'a') as tsvfile:
                writer = csv.writer(tsvfile, delimiter='\t')
                writer.writerows(processed)
            first = False

            seed = r[0]
            rows[:] = []
            build_rows(rows, r)
            progress(i, len(all_data), status='finding locations')
        i = i + 1
