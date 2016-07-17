import nltk

from .lib import word_filter
from .celeryserver import app


@app.task
def find_most_common_words(
        file_list, preprocess=None, word_filter=word_filter):
    """Iterate over file list and find most used words in it."""
    counter = {}

    for index, filetosearch in enumerate(file_list):
        with open(filetosearch, 'r') as f:
            content = f.read()
            if preprocess:
                content = preprocess(content)
            words = (
                word
                for word in nltk.word_tokenize(content) # slow func
                # for word in content.split() fast simple for test
                if word_filter(word)
            )
            for word in words:
                if word in counter:
                    counter[word] += 1
                else:
                    counter[word] = 1

    # NOTE: using print as logging message for celery and other runners
    # if we use only celery logger we need to use 'self' and redirect to std
    # just showing debug messages in celery or multiprocessing is we calc
    print('Calculated top words per {} files.'.format(len(file_list)))

    # NOTE: fixed math issue with top 10
    return counter
