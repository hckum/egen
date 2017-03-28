# Functions for Error Generation Simulator v0.1
# by Han Wang
# 03/27/2017 first created, data preprocessing
# 03/28/2017 add typo generation

import csv
import zipfile
from datetime import date, datetime
import calendar
import random
import string
import copy


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
    title = []
    for i in reader:
        if i[2] == 'voter_reg_num':
            title = [x.strip() for x in i]
            break

    for i in reader:
        if i[2] != 'voter_reg_num':
            d[i[2]] = {}
            for n in range(len(i)):
                d[i[2]][title[n]] = i[n].strip()

            #d[i[2]] = [x.strip() for x in i] # [i[x].strip() for x in [9, 10, 25, 28]]
    return d


def field_filter(data, fields):
    """
    Select columns as needed.
    voter_reg_num, last_name, first_name, birth_age
    :param data: data dictionary
    :param fields: list of selected fields
    :return: data only with selected fields
    """
    d = {}
    for k in data.keys():
        d[k] = {}
        for f in fields:
            d[k][f] = data[k][f]
    return d


def dob(record):
    """
    Make up dob for a record
    :param record: a row of data
    :return: modified data by replacing age with dob.
    """
    tmp = record
    s = ' '.join(record.values())
    ymd = date.fromordinal(sum([ord(x) for x in s])).isoformat()
    year = 2017 - int(record['birth_age'])
    # leap year 02-29 validation
    while '02-29' in ymd and not calendar.isleap(year):
        year -= 1
    tmp['dob'] = ymd[5:] + '-' + str(year)
    return tmp

def swap_fields(record):
    """
    Swap first name and last name
    :param record:
    :return: modified record
    """
    tmp = record
    t = record['last_name']
    tmp['last_name'] = record['first_name']
    tmp['first_name'] = t
    return tmp


def swap_date(record):
    """
    Swap month and day in dob
    :param record:
    :return: modified record
    """
    tmp = record
    k = record['dob']
    try:
        l = [i for i in k.split('-')]
        k = '-'.join([l[1],l[0],l[2]])
        datetime.strptime(k,'%m-%d-%Y')
    except IndexError:
        return tmp
    except ValueError:
        return tmp
    tmp['dob'] = k
    return tmp


def del_field(record):
    """
    Deletion of a value
    :param record:
    :return: modified record
    """
    tmp = record
    f = random.randint(0,len(record.keys())-1)
    tmp[tmp.keys()[f]] = ''
    return tmp


def insert(record):
    """
    Perform an insertion
    :param record:
    :return: modified record
    """
    tmp = record
    pos = random.randint(0,len(tmp.keys())-1)
    field = tmp[tmp.keys()[pos]]
    if tmp.keys()[pos]=='dob':
        # valid insertion: months: 2 -> 12, days: 5->25
        mdy = tmp['dob'].split('-')
        type = 0
        if int(mdy[0])<=2:
            type+=1
        if int(mdy[1])<=9:
            type+=2
        if type == 0:
            insert(record)
        if type == 1:
            mdy[0] = str(int(mdy[0])+10)
        if type == 2:
            mdy[1] = str(int(mdy[1])+random.randint(1,2)*10)
        if type == 3:
            t = random.randint(0,2)
            if t==0:
                mdy[0] = str(int(mdy[0])+10)
            else:
                mdy[1] = str(int(mdy[1])+t*10)
        tmp['dob'] = '-'.join(mdy)
    elif field.isdigit():
        # voter_reg_num insertion
        p = random.randint(0, len(field))
        if p == len(field):
            tmp[tmp.keys()[pos]] += string.digits[random.randint(0,9)]
        else:
            tmp[tmp.keys()[pos]] = field[:p]+string.digits[random.randint(0,9)]+field[p:]
    elif field.isalpha():
        # last_name and first_name insertion
        p = random.randint(0,len(field))
        if p == len(field):
            tmp[tmp.keys()[pos]] += string.uppercase[random.randint(0,25)]
        else:
            tmp[tmp.keys()[pos]] = field[:p]+string.uppercase[random.randint(0,25)]+field[p:]
    return tmp


def delete(record):
    """
    Perform a deletion
    :param record:
    :return: modified record
    """
    tmp = record
    pos = random.randint(0, len(tmp.keys()) - 1)
    field = tmp[tmp.keys()[pos]]
    if tmp.keys()[pos]=='dob':
        # valid deletion: 21->01, 21->02, 20->02
        mdy = tmp['dob'].split('-')
        t = random.randint(0,1)
        if int(mdy[t])>=10:
            mdy[t] = '0'+mdy[t][0] if int(mdy[t])%10==0 else '0'+mdy[t][random.randint(0,1)]
        tmp['dob'] = '-'.join(mdy)
    elif field!='':
        p = random.randint(0,len(field)-1)
        tmp[tmp.keys()[pos]] = field[:p]+field[p+1:]
    return tmp


def transpose(record):
    """
    Perform a transposition
    :param record:
    :return: modified record
    """
    tmp = record
    pos = random.randint(0, len(tmp.keys()) - 1)
    field = tmp[tmp.keys()[pos]]
    if tmp.keys()[pos]=='dob':
        pass
    else:
        p = random.randint(0, len(field)-2)
        tmp[tmp.keys()[pos]] = field[:p]+field[p+1]+field[p]+field[p+2:]
    return tmp


def substitute(record):
    """
    Perform a substitution
    :param record:
    :return: modified record
    """
    tmp = record
    pos = random.randint(0, len(tmp.keys()) - 1)
    field = tmp[tmp.keys()[pos]]
    if field!='':
        p = random.randint(0,len(field)-1)
        if tmp.keys()[pos]=='dob':
            pass
        elif field.isdigit():
            tmp[tmp.keys()[pos]] = tmp[tmp.keys()[pos]].replace(tmp[tmp.keys()[pos]][p], string.digits[random.randint(0,9)])
        elif field.isalpha():
            tmp[tmp.keys()[pos]] = tmp[tmp.keys()[pos]].replace(tmp[tmp.keys()[pos]][p], string.uppercase[random.randint(0,25)])
    return tmp


def add_typo(record, prob):
    """
    Add a typo error:
    1. insertion
    2. deletion (omission)
    3. transpose
    4. substitution (replace)
    :param record: a record
    :param prob: probabilities of each typo type (should be a list of 4 decimals)
    :return: modified record
    """
    # prob normalization
    p = [x/float(sum(prob)) for x in prob]
    # create intervals
    q = [sum(p[:x]) for x in range(1, len(p)+1)]

    tmp = copy.deepcopy(record)
    k = random.random()
    # insertion
    if k<=q[0]:
        print '===Insertion==='
        tmp = insert(tmp)
    # deletion
    elif k<=q[1]:
        print '===Deletion==='
        tmp = delete(tmp)
    # transpose
    elif k<=q[2]:
        print '===Transposition==='
        tmp = transpose(tmp)
    # substitution
    elif k<=q[3]:
        print '===Substitution==='
        tmp = substitute(tmp)
    if tmp==record:
        add_typo(record, prob)
    else:
        print tmp.values(), record.values()
        return tmp


def name_variant(record, v):
    """
    replace a name with its variant
    :param record:
    :param v: variant dictionary
    :return: modified record
    """
    tmp = record
    t = random.randint(0,1)
    k = 'first_name' if t==0 else 'last_name'
    tmp[k] = v[tmp[k]][random.randint(0,len(v[tmp[k]])-1)]
    return tmp


def match(x, y):
    """
    Match test
    :param x: record x
    :param y: record y
    :return: True if they match, otherwise false
    """
    try:
        for j in x.keys():
            if x[j] != y[j]:
                return False
    except AttributeError:
        pass
    return True



