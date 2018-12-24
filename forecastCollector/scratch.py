from datetime import datetime,timedelta

now = datetime.now()
start = now + timedelta(days=-1)
later = now + timedelta(days=10)
d_from_date = datetime.strptime(start.strftime('%Y-%m-%d') , '%Y-%m-%d')
d_to_date = datetime.strptime(later.strftime('%Y-%m-%d') , '%Y-%m-%d')

print(d_from_date.strftime('%Y-%m-%d %H:%M:%S'))
print(d_to_date.strftime('%Y-%m-%d %H:%M:%S'))

