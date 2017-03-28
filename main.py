# Error Generation Simulator
# by Han Wang
#
from gen import *
import random


p = readzip('data/apr13/ncvoter100.zip')
dat = field_filter(p, [2, 9, 10, 29])

rate = 0.03
rate_missing = 0.5
rate_swap = 0.5
n = int(rate*len(dat.keys()))
d = {}

for k in dat.keys():
    dat[k] = dob(dat[k])

while len(d.keys()) <= n:
    t = random.randint(0,len(dat.keys()))
    k = dat.keys()[t]
    if random.random() < rate_missing:
        tmp = del_field(dat[k])
    elif match(swap_date(dat[k]), dat[k]):
        tmp = swap_fields(dat[k])
    else:
        tmp = swap_date(dat[k])
    if not match(tmp,dat[k]):
        d[k] = tmp

for k in d.keys():
    print d[k],dat[k]
print float(len(d.keys()))/len(dat.keys())



fname = {}
lname = {}
for k in dat.keys():
    if dat[k][1] not in lname:
        lname[dat[k][1]] = 1
    else:
        lname[dat[k][1]] += 1
    if dat[k][2] not in fname:
        fname[dat[k][2]] = 1
    else:
        fname[dat[k][2]] += 1

with open('tmp3.txt','wb') as f:
    c = [[k,lname[k]] for k in lname.keys()]
    w = csv.writer(f)
    w.writerows(sorted(c, key=lambda x:x[0]))

with open('tmp4.txt','wb') as f:
    c = [[k,fname[k]] for k in fname.keys()]
    w = csv.writer(f)
    w.writerows(sorted(c, key=lambda x:x[0]))
