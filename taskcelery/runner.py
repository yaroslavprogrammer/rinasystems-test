import sys

from words import workers
from words.lib import emails_from_dir
from words.tasks import find_most_common_words


def run():
    """Get appropriate worker from workers module and run it"""
    # NOTE: argsparse module will be more prettier

    # get worker name from arg
    try:
        worker_name = sys.argv[1]
    except IndexError:
        worker_name = 'default'

    try:
        worker = getattr(workers, '{}_worker'.format(worker_name))
    except AttributeError:
        print('{} worker not available, choose one from {}'.format(
            worker_name,
            ', '.join(w.__name__ for w in workers.registered)
        ))

    # get list iterator of files
    file_list = emails_from_dir()

    # run worker and print results
    result = worker(file_list, find_most_common_words, limit=1000)

    print('Result is {}'.format(result))


if __name__ == '__main__':
    run()
