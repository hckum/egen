# Error Generation Simulator v0.1
# by Han Wang
# 03/28/2017

from gen import *
import random
import csv
from copy import deepcopy

cfg = load_config('config.txt')

filter1, filter2 = cfg['field'], cfg['output']

rate, rate_missing, rate_swap = cfg['rate'], cfg['rate_missing'], cfg['rate_swap']
rate_typo, rate_vari = cfg['rate_typo'], cfg['rate_vari']
typo_prob = [cfg['prob_insertion'], cfg['prob_deletion'], cfg['prob_transpose'], cfg['prob_substitution']]

p = readzip('data/apr13/ncvoter100.zip')
dat = field_filter(p, filter1)
for k in dat.keys():
    dat[k] = dob(dat[k])
data = deepcopy(dat)

v = {}
with open('data/lookup.txt','r') as f:
    reader = csv.reader(f)
    for i in reader:
        v[i[0]] = [i[1]]

n = int(rate*len(dat.keys()))
d = {}
prob = [rate_missing, rate_swap, rate_typo, rate_vari]
op = [x / float(sum(prob)) for x in prob]
q = [sum(op[:x]) for x in range(1, len(op) + 1)]

n_error = 0
while n_error <= n:
    t = random.randint(0, len(data.keys())-1)
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
    elif p < q[3]:
        tmp = name_variant(data[k], v)
    if not match(tmp, dat[k]):
        d[k] = tmp
        n_error += 1

for k in d.keys():
    data[k] = d[k]

print len(d)/float(len(dat))


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

