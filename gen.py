# Error Generation Simulator v0.1
# by Han Wang
# 03/27/2017

import csv
import zipfile
from datetime import date, datetime
import calendar
import random


def readzip(fpath):
    """
    Read compressed txt files with title removed.
    :param fpath: path of the zip file
    :return: dict with reg_nums as keys and rows as values.
    """
    d = {}
    a = zipfile.ZipFile(fpath, 'r')
    b = a.open(fpath.split('/')[-1][:-4]+'.txt')
    reader = csv.reader(b, delimiter='\t')
    for i in reader:
        if i[2]!='voter_reg_num':
            d[i[2]] = [x.strip() for x in i] # [i[x].strip() for x in [9, 10, 25, 28]]
    return d


def field_filter(data, fields):
    """
    Select columns as needed.
    reg number: 2, last name: 9, first name: 10, birth age: 29
    :param data: data dictionary
    :param fields: list of selected
    :return: data only with selected fields
    """
    d = {}
    for k in data.keys():
        d[k] = [data[k][x] for x in fields]
    return d


def dob(record):
    """
    Make up dob for a record
    :param record: a row of data
    :return: modified data by replacing age with dob.
    """
    s = ' '.join(record)
    ymd = date.fromordinal(sum([ord(x) for x in s])).isoformat()
    year = 2017 - int(record[-1])
    # leap year 02-29 validation
    while '02-29' in ymd and not calendar.isleap(year):
        year -= 1
    return record[:-1] + [ymd[5:] + '-' + str(year)]


def swap_fields(record):
    """
    Swap first name and last name
    :param record:
    :return: modified record
    """
    return [record[i] for i in [0, 2, 1, 3]]


def swap_date(record):
    """
    Swap month and day in dob
    :param record:
    :return: modified record
    """
    k = record[-1]
    try:
        l = [i for i in k.split('-')]
        k = '-'.join([l[1],l[0],l[2]])
        datetime.strptime(k,'%m-%d-%Y')
    except ValueError:
        return record
    return record[:-1] + [k]


def del_field(record):
    """
    Deletion of a value
    :param record:
    :return: modified record
    """
    f = random.randint(0,len(record))
    return [record[i] if i != f else '' for i in range(len(record))]


def match(x,y):
    for j in range(len(x)):
        if x[j]!=y[j]:
            return False
    return True


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


'''
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
'''

