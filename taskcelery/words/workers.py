import collections
import multiprocessing

from celery import group as group_celery_tasks

from .lib import chunked_iterator

# NOTE: simplified to functions, may be wrap in class will be more clear
# using manager and processing classes with same API


def linear_worker(
        file_list, processing_func=None, limit=None, chunks=100,
        most_common=10):
    counter = collections.Counter()
    for file_list in chunked_iterator(file_list, chunks, limit=limit):
        results = processing_func(file_list)
        counter.update(results)

    return dict(counter.most_common(most_common))


def multiprocessing_worker(
        file_list, processing_func=None, limit=None, chunks=100,
        most_common=10, pool_num=1):
    real_cpu_count = multiprocessing.cpu_count()
    counter = collections.Counter()
    pool = multiprocessing.Pool(
        pool_num if pool_num > real_cpu_count else real_cpu_count)

    file_lists = chunked_iterator(file_list, chunks, limit=limit)
    results = pool.map(processing_func, file_lists)

    for result in results:
        counter.update(result)

    return dict(counter.most_common(most_common))


def celery_worker(
        file_list, processing_func=None, limit=None, chunks=100,
        most_common=10, pool_num=1):
    counter = collections.Counter()
    results = []

    for file_list in chunked_iterator(file_list, chunks, limit=limit):
        results.append(processing_func.s(file_list))

    results = group_celery_tasks(results)()
    for result in results.get(timeout=2 * chunks):
        counter.update(result)

    return dict(counter.most_common(most_common))



default_worker = linear_worker
registered = [
    linear_worker, multiprocessing_worker, celery_worker
]
