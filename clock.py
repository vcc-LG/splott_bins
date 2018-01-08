from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from query_council import run_query_council
from produce_tweets import run_produce_tweets, run_one_off_tweet

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BlockingScheduler()

q = Queue(connection=conn)

def query_council():
    q.enqueue(run_query_council)

def produce_tweets():
    q.enqueue(run_produce_tweets)

def one_off_tweet():
    q.enqueue(run_one_off_tweet)

sched.add_job(one_off_tweet) #enqueue right away once
sched.add_job(query_council, 'interval', days=1, start_date='2018-01-08 20:45:00')
# sched.add_job(produce_tweets) #enqueue right away once
sched.add_job(produce_tweets, 'interval', days=1, start_date='2018-01-08 20:45:00')
sched.start()
