import scheduler_utility as su
from datetime import datetime

a = su.getSchedule()


b = a[0]['SchedulerDailyStopTime']

c = datetime.strptime(b, '%H:%M:%S').time()
print(c)
print(datetime.now().time())

print(c > datetime.now().time())

print(a[0]['ScheduleID'].__hash__())
a = a[0]['ScheduleID']
print(a.__hash__())

