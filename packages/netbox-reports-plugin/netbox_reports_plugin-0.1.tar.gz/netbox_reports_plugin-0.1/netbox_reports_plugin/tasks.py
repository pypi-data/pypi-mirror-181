from redis import Redis
from rq import Queue
from django_rq.queues import get_queue
from datetime import timedelta, datetime
from django_rq import job

def test():
    print('task выполнился')

@job
def test_task():
    q = get_queue('default')
    res_test = q.enqueue_at(datetime(2022, 11, 30, 11, 58), test)
