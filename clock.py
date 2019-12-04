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

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=4, minute=55)
#def scheduled_job():
#	sell.main()
#	print 'This job is run every weekday at 10:25 am.'


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=5, minute=00)
def scheduled_job1():
	ScoreBuyStocks.main()
	print 'This job is run every weekday at 10:30 am IST.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=22, minute=30)
def scheduled_job2():
	ScoreBuyStocks.main()
	print 'This job is run every weekday at 4:00 am.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=16, minute=30)
def scheduled_job3():
	storeRatios.main()
	print 'This job is run every weekday at 22:00.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=13, minute=20)
def scheduled_job3():
	storeFinancials.main()
	print 'This job is run every weekday at 18:50.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=22, minute=00)
def scheduled_job4():
	Median.main()
	print 'This job is run every weekday at 3:30 am.'

print 'Job is running now'
sched.start()