# Error Generation Simulator v0.1
# by Han Wang
# 03/28/2017

from gen import *
import random
import csv
from copy import deepcopy

filter1 = ['voter_reg_num', 'last_name', 'first_name', 'birth_age']
filter2 = ['voter_reg_num', 'last_name', 'first_name', 'dob']

p = readzip('data/apr13/ncvoter100.zip')
dat = field_filter(p, filter1)
for k in dat.keys():
    dat[k] = dob(dat[k])
data = deepcopy(dat)


rate = 0.03
rate_missing = 0.3
rate_swap = 0.2
rate_typo = 0.5
typo_prob = [0.4, 0.3, 0.15, 0.15]
n = int(rate*len(dat.keys()))
d = {}
op = [rate_missing, rate_swap, rate_typo]
q = [sum(op[:x]) for x in range(1, len(op) + 1)]

while len(d.keys()) <= n:
    t = random.randint(0,len(data.keys())-1)
    k = data.keys()[t]
    p = random.random()
    if p < q[0]:
        tmp = del_field(data[k])
    elif p < q[1]:
        if match(swap_date(data[k]), data[k]):
            tmp = swap_fields(data[k])
        else:
            tmp = swap_date(data[k])
    elif p < q[2]:
        tmp = add_typo(data[k], typo_prob)
    if not match(tmp,dat[k]):
        d[k] = tmp

for k in d.keys():
    data[k] = d[k]

with open('log/dict1.txt', 'wb') as f:
    w = csv.DictWriter(f, filter2, extrasaction='ignore')
    w.writeheader()
    for k in sorted(dat.keys(),key=lambda x:int(x)):
        w.writerow(dat[k])

with open('log/dict2.txt', 'wb') as f:
    w = csv.DictWriter(f, filter2, extrasaction='ignore')
    w.writeheader()
    for k in sorted(data.keys(), key=lambda x:int(x)):
        w.writerow(data[k])
