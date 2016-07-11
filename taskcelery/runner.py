import sys
import time

from words import workers
from words.lib import emails_from_dir
from words.tasks import find_most_common_words


def run(default_worker='linear'):
    """Get appropriate worker from workers module and run it"""
    # NOTE: argsparse module will be more prettier and robust

    # get worker name from arg
    try:
        worker_name = sys.argv[1]
    except IndexError:
        worker_name = default_worker

        print("You don't provided worker name using default: {}".format(
            worker_name))

    try:
        limit = int(sys.argv[2])
    except (IndexError, ValueError):
        print("You don't set correct limit, will be used all file list")
        limit = None

    start_time = time.time()

    # get worker func from module
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
    result = worker(file_list, find_most_common_words, limit=limit)

    time_spent = time.time() - start_time

    print('Result is {}'.format(result))
    print('Time spended to find it {}s'.format(round(time_spent, 2)))


if __name__ == '__main__':
    run()
