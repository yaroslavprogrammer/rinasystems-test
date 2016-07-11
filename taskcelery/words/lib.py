import os
import glob
import itertools
import collections

import nltk


def emails_from_dir():
    """Return iterator for all finded txt files in db dir with emails."""
    db = os.path.join(os.path.dirname(__file__), '..', 'db')
    files = glob.iglob(os.path.join(db, '**', '*.txt'), recursive=True)

    return files


def length_word_filter(word):
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


def find_most_common_words(
        file_list, count=10, preprocess=None, word_filter=length_word_filter):
    """Iterate over file list and find most used words in it."""
    counter = collections.Counter()

    for index, filetosearch in enumerate(file_list):
        with open(filetosearch, 'r') as f:
            content = f.read()
            if preprocess:
                content = preprocess(content)
            counter.update(
                word
                for word in nltk.word_tokenize(content) # slow func
                if word_filter(word)
            )

    return dict(counter.most_common(count))
