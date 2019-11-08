from apscheduler.schedulers.blocking import BlockingScheduler
import MovingAverage

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=4, minute=45)
def scheduled_job():
	MovingAverage.main()
	print 'This job is run every weekday at 10:15 am.'
	
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=8, minute=40)
def scheduled_job2():
	MovingAverage.main()
	print 'This job is run every weekday at 1:30 pm.'

print 'Job is running now'
sched.start()