# Error Generation Simulator v0.1
# by Han Wang
# 03/28/2017

from gen import *
import random
import csv, time
from copy import deepcopy

##################################################
# 1. CONFIGURATIONS

cfg = load_config('config.txt')

filter1, filter2 = cfg['field'], cfg['output']

rate, rate_missing, rate_swap = cfg['rate'], cfg['rate_missing'], cfg['rate_swap']
rate_typo, rate_vari = cfg['rate_typo'], cfg['rate_vari']
typo_prob = [cfg['rate_insertion'], cfg['rate_deletion'], cfg['rate_transpose'], cfg['rate_substitution']]

##################################################
# 2. DATA PREPARATION

p = readzip('data/apr13/ncvoter100.zip')
dat = field_filter(p, filter1)
for k in dat.keys():
    dat[k]['original'] = dob(dat[k]['original'])
    dat[k]['modified'] = copy.deepcopy(dat[k]['original'])


##################################################
# 3. LOOKUP TABLE PREPARATION

v = {}
with open('data/lookup.txt','r') as f:
    reader = csv.reader(f)
    for i in reader:
        v[i[0]] = [i[1]]

##################################################
# 4. ERROR RATEs PREPARATION

n = int(rate*len(dat.keys()))
prob = [rate_missing, rate_swap, rate_typo, rate_vari]
op = [x / float(sum(prob)) for x in prob]
q = [sum(op[:x]) for x in range(1, len(op) + 1)]

##################################################
# 5. ITERATIVELY ERROR GENERATION

d = {}
n_error = 0
while n_error <= n:
    t = random.randint(0, len(dat.keys())-1)
    k = dat.keys()[t]
    p = random.random()
    if p < q[0]:
        dat[k] = del_field(dat[k])
    elif p < q[1]:
        if match(swap_date(dat[k])['modified'], dat[k]['original']):
            dat[k] = swap_fields(dat[k])
        else:
            dat[k] = swap_date(dat[k])
    elif p < q[2]:
        dat[k] = add_typo(dat[k], typo_prob)
    elif p < q[3]:
        dat[k] = name_variant(dat[k], v)
    if not match(dat[k]['modified'], dat[k]['original']):
        d[k] = dat[k]['modified']
        n_error += 1

print len(d)/float(len(dat))

##################################################
# 6. WRITE OUTPUT TO FILES

with open('log/dict1.txt', 'wb') as f:
    w = csv.DictWriter(f, filter2, extrasaction='ignore')
    w.writeheader()
    for k in sorted(dat.keys(),key=lambda x:int(x)):
        w.writerow(dat[k]['original'])

with open('log/dict2.txt', 'wb') as f:
    w = csv.DictWriter(f, filter2, extrasaction='ignore')
    w.writeheader()
    for k in sorted(dat.keys(), key=lambda x:int(x)):
        w.writerow(dat[k]['modified'])

with open('log/changes.txt', 'wb') as f:
    w = csv.writer(f)
    for k in sorted(dat.keys(), key=lambda x:int(x)):
        if not match(dat[k]['original'], dat[k]['modified']):
            w.writerow([dat[k]['original'][i] for i in filter2]+[dat[k]['modified'][j] for j in filter2]+dat[k]['modifier'])

