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


#@sched.scheduled_job('interval', minutes=60)
#def timed_job():
#	sell.main()
#	print('This job is run every sixty minutes.')

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=4, minute=55)
#def scheduled_job():
#	sell.main()
#	print 'This job is run every weekday at 10:25 am.'


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=4, minute=15)
def scheduled_job1():
	ScoreBuyStocks.main()
	print 'This job is run every weekday at 9:45 am IST.'
	
#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=8, minute=00)
#def scheduled_job2():
#	ScoreBuyStocks.main()
#	print 'This job is run every weekday at 13:30 pm.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=16, minute=30)
def scheduled_job3():
	storeRatios.main()
	print 'This job is run every weekday at 22:00.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=22, minute=00)
def scheduled_job4():
	Median.main()
	print 'This job is run every weekday at 3:30 am.'

print 'Job is running now'
sched.start()