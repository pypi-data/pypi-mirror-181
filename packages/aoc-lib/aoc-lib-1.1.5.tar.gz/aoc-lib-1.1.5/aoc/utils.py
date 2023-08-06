import re
from itertools import chain, islice


def get_ints(s: str) -> [int]:
    """
    Get all int (including sign) values from the given string
    """
    return list(map(int, re.findall(r"((?:-|\+)?\d+)", s)))


def fetch(iterable, n: int, fillvalue=None) -> [any]:
    """
    fetches n values from iterable - filled with fillvalue if needed;
    great for destructuring data with different number of arguments etc
    e.g.: a, b = fetch(args, 2) - fetches 2 elements from args and fills with None if needed
    :param iterable: the iterable to fetch from
    :param n: the number of elements to fetch; align that with your destructuring
    :param fillvalue: optional fill value if less than n elements are available (None as default)
    :return: list with the n elements; filled with fillvalue if needed
    """
    if len(iterable) >= n:
        return iterable[0:n]
    fill = [fillvalue] * (n - len(iterable))
    return chain(iterable, fill)

def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := list(islice(it, n))):
        yield batch