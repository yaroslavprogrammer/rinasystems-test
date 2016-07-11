import os
import glob
import itertools


def emails_from_dir():
    """Return iterator for all finded txt files in db dir with emails."""
    db = os.path.join(os.path.dirname(__file__), '..', 'db')
    files = glob.iglob(os.path.join(db, '**', '*.txt'), recursive=True)

    return files


def word_filter(word):
    """Filter word by length params."""
    return len(word) > 1


def chunked_iterator(iterable, n, limit=None):
    """Collect data into chunks or blocks and limit iterations."""
    # chunked_iterator('ABCDEFG', 3) --> ABC DEF G"
    iterator = iter(iterable)
    index = 0

    while True:
        chunk = tuple(itertools.islice(iterator, n))

        if not chunk:
            return

        index += n
        if limit and index > limit:
            return

        yield chunk
