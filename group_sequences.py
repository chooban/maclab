import sys
import pprint


def read_in():
    """Read all lines from stdin
    Strips newline characters from each line, and removes the empty line at the
    end of the file
    """
    lines = [x.strip() for x in sys.stdin.readlines()]
    lines.pop()
    return lines


def next_sequence(list):
    """
    Generator function to allow for custom iteration through a list of
    strings.

    For use when you want to be able to skip certain elements. Elements to be
    skipped on subsequent iterations can be passed via the 'send' method.

    The indices of the elements to be skipped should be provided. This allows
    a very fast lookup on an array of booleans.

    https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/
    """
    i = 0
    j = len(list)
    all_seen = [False] * j
    # print("list is {0}".format(list))
    while(i < j):
        # print("all_seen is {0}".format(all_seen))
        if (not all_seen[i]):
            # print("yielding {0}".format(i))
            seen = yield i
            # print("Matched {0} for {1}".format(seen, i))
            for c in seen:
                all_seen[c] = True
        all_seen[i] = True
        i = i + 1


def read_and_sort():
    # Read all relevant strings from stdin, remove duplicates by passing
    # to a set, and then converting back to a list. Then use cmp to order
    # the list by string length.
    # https://docs.python.org/2/library/functions.html#cmp
    all_sequences = list(set(map(lambda x: x.split('\t')[0], read_in())))
    all_sequences.sort()
    return all_sequences


def find_super_sequences(seq, possibles):
    """
    Returns a list of tuples for matched supersequences. The tuples consist of
    the index in possibles, and the value itself.
    """
    found = list()
    i = 0
    while (i < len(possibles)):
        p = possibles[i]
        # This is against PEP-8, but does save time and since the main time
        # sink in this script is .startswith, then it's worth it
        if (p[:len(seq)] == seq):
            found.append((i, p))
        else:
            break
        i = i + 1
    return found


def validate_counts(all_sequences, groupings):
    count = reduce(lambda x, y: x + len(y), groupings.values(), 0)
    uniq = set(reduce(lambda x, y: x + y, groupings.values(), []))
    return count == len(uniq) and count == len(all_sequences)


if __name__ == '__main__':
    all_sequences = read_and_sort()
    groupings = {}

    # Process the first iterator value by calling next, as we don't currently
    # have any previously seen values to pass to it.
    iterator = next_sequence(all_sequences)
    idx = next(iterator, None)
    key = all_sequences[idx]
    children = find_super_sequences(key, all_sequences[idx:])
    groupings[key] = [x[1] for x in children]

    # Now go through all the values of the iterator until there are no more.
    while True:
        try:
            idx = iterator.send([x[0] + idx for x in children])
            key = all_sequences[idx]
            children = find_super_sequences(key, all_sequences[idx:])
            groupings[key] = [x[1] for x in children]
        except StopIteration:
            break

    if (validate_counts(all_sequences, groupings)):
        for k, v in groupings.items():
            v.sort()

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(groupings)
    else:
        print("Found {0} values for {1} rows".format(count, len(all_sequences)))
        print("There are {0} uniq supersequences".format(len(uniq_supersequences)))
        sys.exit(1)
