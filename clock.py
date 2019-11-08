from apscheduler.schedulers.blocking import BlockingScheduler
import MovingAverage

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=4, minute=15)
def scheduled_job():
	MovingAverage.main()
	print 'This job is run every weekday at 5pm.'

print 'Job is running now'
sched.start()