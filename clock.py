from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from query_council import run_query_council
from produce_tweets import run_produce_tweets

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BlockingScheduler()

q = Queue(connection=conn)

def gather_threads():
    q.enqueue(run_gather_threads)

def gather_comments():
    q.enqueue(run_gather_comments)

# sched.add_job(run_query_council) #enqueue right away once
sched.add_job(run_query_council, 'interval', days=1, start_date='2017-01-07 23:00:00')
# sched.add_job(run_produce_tweets) #enqueue right away once
sched.add_job(run_produce_tweets, 'interval', days=1, start_date='2017-01-07 23:00:00')
sched.start()
