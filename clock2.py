from apscheduler.schedulers.blocking import BlockingScheduler
import MovingAverage
import os
import logging
import sell
import storeRatios
import Median
import ScoreBuyStocks
import storeFinancials
logging.basicConfig()

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=10)
def timed_job():
	sell.main()
	print('This job is run every ten minutes.')


def scheduled_job3():
	storeFinancials.main()
	print 'This job is run every weekday at 18:00.'
	
print 'Job is running now'
sched.start()