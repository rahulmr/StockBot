from apscheduler.schedulers.blocking import BlockingScheduler
import MovingAverage

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=4)
def scheduled_job():
	MovingAverage.main()
	print 'This job is run every weekday at 5pm.'
	
sched.start()