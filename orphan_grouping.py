from __future__ import print_function
from functools import reduce, partial
from multiprocessing import Pool
import csv
import sys
import os


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def count_abundance_if_match(orphan, acc, curr):
    if orphan.startswith(curr[0]):
        acc = (acc[0] + [curr], acc[1] + curr[1])
    return acc


def read_in():
    """Read all lines from stdin
    Strips newline characters from each line
    """
    lines = [x.strip() for x in sys.stdin.readlines()]
    return lines


def write(orphan, filename, total):
    global PROGRESS
    PROGRESS = PROGRESS + 1
    with open('orphan_output.tsv', 'a') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerow(orphan)
    progress(PROGRESS, total, 'grouping orphans')


def process_orphan(idx, orphan, orphans):
    reducer = partial(count_abundance_if_match, orphan[0])
    orphan_data = reduce(reducer, orphans[idx:], ([], 0))
    return (orphan[0], orphan[1], orphan_data[1], orphan_data[0])


if __name__ == '__main__':
    filename = 'orphan_output.tsv'
    if os.path.isfile(filename):
        os.remove(filename)

    orphans = map(
        lambda x: (x[0], int(x[1])),
        map(lambda x: x.split('\t'), read_in())
    )
    orphans = sorted(orphans, key=lambda x: len(x[0]), reverse=True)
    p = partial(process_orphan, orphans=orphans)
    cb = partial(write, filename=filename, total=len(orphans))
    PROGRESS = 0

    pool = Pool(os.cpu_count() - 1)
    for i, x in enumerate(orphans):
        pool.apply_async(p, args=(i, x), callback=cb)

    print("Closing pool...")
    pool.close()

    print("Waiting for processes to end...")
    pool.join()

    print("Done")
