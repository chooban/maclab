import csv
import sys
import ast
from operator import itemgetter


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


def build_rows(r):
    rows = []
    locations = ast.literal_eval(r[4])

    if len(locations) == 0:
        locations.append('NONE')

    for l in locations:
        rows.append((r[0], int(r[1]), float(r[2]), int(r[3]), l))
    return rows


if __name__ == '__main__':
    all_data = map(lambda x: x.split('\t'), read_in())
    all_data = sorted(all_data, key=lambda x: x[0])

    groupings = {}

    seed = all_data[0][0]
    groupings[seed] = []

    sortkeyfn = itemgetter(4)

    for r in all_data:
        if (r[0][:len(seed)] == seed):
            groupings[seed] = groupings[seed] + build_rows(r)
        else:
            seed = r[0]
            groupings[seed] = build_rows(r)

    row_count = len([item for sublist in groupings.values() for item in sublist])
    rows = []
    for seed, subsequences in groupings.iteritems():
        grouped = group_by(subsequences, idx=4)
        for location, elements in grouped.iteritems():
            count = reduce(lambda x, y: x + y[3], elements, 0)
            sequences = list(set(reduce(lambda x, y: x + [y[0]], elements, [])))
            sequences.sort()
            t = (seed, count, location, sequences)
            rows = rows + [t]
            progress(len(rows), row_count, status='Reticulating splines...')

    progress(row_count, row_count, status='Reticulating splines...')

    with open('output.tsv', 'w') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerows(rows)
