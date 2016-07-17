import heapq
import operator
import multiprocessing

from celery import group as celery_group

from .lib import chunked_generator

# NOTE: simplified to functions, may be wrap in class will be more clear
# using manager and processing classes with same API

# NOTE: collections.Counter is overhead and slow update on big data


def process_results(results, most_common):
    counter = {}

    for result in results:
        for key in result:
            if key in counter:
                counter[key] += result[key]
            else:
                counter[key] = result[key]

    # NOTE: profiled mem, sorted will use additional memory x2
    # lambda will be overhead due to 2 func calls, operator only 1 call

    return heapq.nlargest(
        most_common, counter.items(), key=operator.itemgetter(1))


def linear_worker(
        file_list, processing_func=None, limit=None, chunks=500,
        most_common=10):

    results = (
        processing_func(file_list)
        for file_list in chunked_generator(file_list, chunks, limit=limit)
    )

    return process_results(results, most_common)


def multiprocessing_worker(
        file_list, processing_func=None, limit=None, chunks=500,
        most_common=10, pool_num=1):
    real_cpu_count = int(multiprocessing.cpu_count() * 1.5)
    pool_num = pool_num if pool_num > real_cpu_count else real_cpu_count
    print('Using {} processes to calculate words'.format(pool_num))

    pool = multiprocessing.Pool(pool_num)

    file_lists = chunked_generator(file_list, chunks, limit=limit)
    results = pool.imap_unordered(processing_func, file_lists)

    return process_results(results, most_common)


def celery_worker(
        file_list, processing_func=None, limit=None, chunks=2500,
        most_common=10):
    # TODO: spawn it using process just for shortcut
    print(
        "Please start Celery server by running "
        "'celery -A words.tasks worker' and provide any args as you want")

    # NOTE: for redis use "config set stop-writes-on-bgsave-error" no if
    # fails to save on disk

    # prepare args
    file_list = chunked_generator(file_list, chunks, limit=limit)
    results = celery_group(
        processing_func.subtask((file_list, )) for file_list in file_list)
    results = results.apply_async().iterate()

    return process_results(results, most_common)


registered = [
    linear_worker, multiprocessing_worker, celery_worker
]
