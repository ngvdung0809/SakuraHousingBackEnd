from datetime import datetime

from dateutil.relativedelta import relativedelta

start_date = datetime.strptime('2020-11-11', '%Y-%m-%d')
end_date = datetime.strptime('2022-11-11', '%Y-%m-%d')
ky_tt = 3
c = relativedelta(end_date, start_date)
d = c.months + 12 * c.years

z = round(d / ky_tt)

a = []
b = start_date

for i in range(0, z):
    time = b + relativedelta(months=ky_tt, days=2)
    b = time - relativedelta(days=2)
    a.append(time.strftime('%Y-%m-%d'))

print(a)
print(z)

# tach thanh func de tinh cho ca dich vu.
