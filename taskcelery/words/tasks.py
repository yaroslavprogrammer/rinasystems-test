import collections

import nltk

from .lib import word_filter
from .celeryserver import app


@app.task
def find_most_common_words(
        file_list, count=10, preprocess=None, word_filter=word_filter):
    """Iterate over file list and find most used words in it."""
    counter = collections.Counter()

    print('RUNNED')

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
