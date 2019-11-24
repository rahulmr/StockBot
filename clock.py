from apscheduler.schedulers.blocking import BlockingScheduler
import MovingAverage
import os
import logging
import sell
import storeRatios
import Median
import ScoreBuyStocks
logging.basicConfig()

sched = BlockingScheduler()


#@sched.scheduled_job('interval', minutes=10)
#def timed_job():
#	sell.main()
#	print('This job is run every ten minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=4, minute=55)
def scheduled_job():
	sell.main()
	print 'This job is run every weekday at 10:25 am.'


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=3, minute=45)
def scheduled_job1():
	ScoreBuyStocks.main()
	print 'This job is run every weekday at 9:15 am.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=7, minute=40)
def scheduled_job2():
	ScoreBuyStocks.main()
	print 'This job is run every weekday at 1:10 pm.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=18, minute=30)
def scheduled_job3():
	storeRatios.main()
	print 'This job is run every weekday at 00:00.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=20, minute=00)
def scheduled_job4():
	Median.main()
	print 'This job is run every weekday at 1:30 am.'

print 'Job is running now'
sched.start()