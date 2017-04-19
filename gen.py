# Functions for Error Generation Simulator v0.1
# by Han Wang
# 03/27/2017 first created, data preprocessing
# 03/28/2017 add typo generation, name variant generation
# 03/29/2017 add config file
# TODO : implement transpose and substitute for dob

import csv, zipfile, calendar, random, string, copy
from datetime import date, datetime


def readcsv(fpath):
    """

    :param fpath:
    :return:
    """
    d = {}
    b = open(fpath, 'r')
    title = []
    reader = csv.reader(b)
    for i in reader:
        if i[0] == 'voter_reg_num':
            title = [x.strip() for x in i]
            break

    for i in reader:
        if i[0] != 'voter_reg_num':
            d[i[0]] = {}
            for n in range(len(i)):
                d[i[0]][title[n]] = i[n].strip()
    return d


def readzip(fpath):
    """
    Read compressed txt files with title removed.
    :param fpath: path of the source data. zip, txt and csv formats are supported.
    :return: dict with reg_nums as keys and rows as values.
    """
    d = {}
    b = ''
    reader = None
    if fpath.split('.')[-1]=='zip':
        a = zipfile.ZipFile(fpath, 'r')
        b = a.open(fpath.split('/')[-1][:-4]+'.txt')
        reader = csv.reader(b, delimiter='\t')
    elif fpath.split('.')[-1] in ['csv', 'txt']:
        b = open(fpath, 'r')
        reader = csv.reader(b)
    print("Read in data from "+fpath)
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
    suffix = []
    for k in data.keys():
        d[k] = {}
        d[k]['original'] = {}
        d[k]['modified'] = {}
        d[k]['modifier'] = {'mod':[], 'field':[], 'pos':[]}
        for f in fields:
            d[k]['original'][f] = data[k][f]
        if(data[k]["name_sufx_cd"] != ""):
            suffix.append(k)

    return (d,suffix)


def load_config(fpath):
    """
    Load config
    :param fpath: path to config.txt
    :return: config dictionary
    """
    d = {}
    for line in open(fpath, 'r'):
        l = line.strip()
        if not l.startswith('#'):
            k = l.split('=')
            if k!=['']:
                if k[1].strip()[0].isdigit():
                    d[k[0].strip()] = float(k[1].strip())
                else:
                    d[k[0].strip()] = list([tuple(x.strip().split(':')) if ':' in x else x.strip() for x in k[1].split(',')])
    print d
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
    del tmp['birth_age']
    return tmp


def add_mod(record, mod, field, pos):
    """
    Add modifier information to record
    :param record:
    :param mod: modifier
    :param field: field name
    :param pos: position in fiels
    :return:
    """
    record['modifier']['mod'] += [mod]
    record['modifier']['field'] += [field]
    record['modifier']['pos'] += [pos]
    return record


def swap_fields(record):
    """
    Swap first name and last name
    :param record:
    :return: modified record
    """
    record['modified']['last_name'] = record['original']['first_name']
    record['modified']['first_name'] = record['original']['last_name']
    add_mod(record, 'field swap','last_name'+' first_name','')
    return record


def swap_date(record):
    """
    Swap month and day in dob
    :param record:
    :return: modified record
    """
    k = record['modified']['dob']
    try:
        l = [i for i in k.split('-')]
        k = '-'.join([l[1],l[0],l[2]])
        datetime.strptime(k,'%m-%d-%Y')
    except IndexError:
        return record
    except ValueError:
        return record
    record['modified']['dob'] = k
    add_mod(record, 'date swap','','')
    return record


def del_field(record):
    """
    Deletion of a value
    :param record:
    :return: modified record
    """
    f = random.randint(0,len(record['modified'].keys())-1)
    record['modified'][record['modified'].keys()[f]] = ''
    add_mod(record, 'missing', str(record['modified'].keys()[f]),'')
    return record


def insert(record):
    """
    Perform an insertion
    :param record:
    :return: modified record
    """
    tmp = record['modified']
    pos = random.randint(0,len(tmp.keys())-1)
    field = tmp[tmp.keys()[pos]]
    if tmp.keys()[pos]=='dob' and field!='':
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
        if tmp['dob']!=record['original']['dob']:
            add_mod(record, 'insertion', 'dob', '')
    elif field.isdigit():
        # voter_reg_num insertion
        p = random.randint(0, len(field))
        if p == len(field):
            tmp[tmp.keys()[pos]] += string.digits[random.randint(0,9)]
        else:
            tmp[tmp.keys()[pos]] = field[:p]+string.digits[random.randint(0,9)]+field[p:]
        add_mod(record, 'insertion', tmp.keys()[pos], str(p))
    elif field.isalpha():
        # last_name and first_name insertion
        p = random.randint(0,len(field))
        if p == len(field):
            tmp[tmp.keys()[pos]] += string.uppercase[random.randint(0,25)]
        else:
            tmp[tmp.keys()[pos]] = field[:p]+string.uppercase[random.randint(0,25)]+field[p:]
        add_mod(record, 'insertion', tmp.keys()[pos], str(p))
    return tmp


def delete(record):
    """
    Perform a deletion
    :param record:
    :return: modified record
    """
    tmp = record['modified']
    pos = random.randint(0, len(tmp.keys()) - 1)
    field = tmp[tmp.keys()[pos]]
    if tmp.keys()[pos]=='dob' and field!='':
        # valid deletion: 21->01, 21->02, 20->02
        mdy = tmp['dob'].split('-')
        t = random.randint(0,1)
        if int(mdy[t])>=10:
            mdy[t] = '0'+mdy[t][0] if int(mdy[t])%10==0 else '0'+mdy[t][random.randint(0,1)]
        tmp['dob'] = '-'.join(mdy)
        add_mod(record, 'deletion', 'dob', '')
    elif field!='':
        p = random.randint(0,len(field)-1)
        tmp[tmp.keys()[pos]] = field[:p]+field[p+1:]
        add_mod(record, 'deletion', tmp.keys()[pos], str(p))
    return tmp


def transpose(record):
    """
    Perform a transposition
    :param record:
    :return: modified record
    """
    tmp = record['modified']
    pos = random.randint(0, len(tmp.keys()) - 2)
    field = tmp[tmp.keys()[pos]]
    if tmp.keys()[pos]=='dob':
        pass
    else:
        if len(field)>2:
            p = random.randint(0, len(field)-2)
            tmp[tmp.keys()[pos]] = field[:p]+field[p+1]+field[p]+field[p+2:]
            add_mod(record, 'transposition', tmp.keys()[pos], str(p))
    return tmp


def substitute(record):
    """
    Perform a substitution
    :param record:
    :return: modified record
    """
    tmp = record['modified']
    pos = random.randint(0, len(tmp.keys()) - 2)
    field = tmp[tmp.keys()[pos]]
    if field!='':
        p = random.randint(0,len(field)-1)
        if tmp.keys()[pos]=='dob':
            pass
        elif field.isdigit():
            tmp[tmp.keys()[pos]] = tmp[tmp.keys()[pos]][:p]+string.digits[random.randint(0,9)]+tmp[tmp.keys()[pos]][p+1:]
        elif field.isalpha():
            tmp[tmp.keys()[pos]] = tmp[tmp.keys()[pos]][:p]+string.uppercase[random.randint(0,25)]+tmp[tmp.keys()[pos]][p+1:]
        add_mod(record, 'substitution', tmp.keys()[pos], str(p))
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

    tmp = record['modified']
    k = random.random()
    # insertion
    if k<=q[0]:
        tmp = insert(record)
    # deletion
    elif k<=q[1]:
        tmp = delete(record)
    # transpose
    elif k<=q[2]:
        tmp = transpose(record)
    # substitution
    elif k<=q[3]:
        tmp = substitute(record)
    record['modified'] = tmp
    return record


def add_prefix_suffix(record):
    """
    Add a prefix or suffix
    :param record:
    :return: modified record
    """
    tmp = record
    return tmp


def misspell(record):
    """
    Replace the name with a misspelled name
    :param record:
    :return: modified record
    """
    tmp = record
    return tmp


def name_variant(record, v):
    """
    replace a name with its variant
    :param record:
    :param v: variant dictionary
    :return: modified record
    """
    tmp = record['modified']
    t = random.randint(0,1)
    k = 'first_name' if t==0 else 'last_name'
    if tmp[k] in v.keys():
        #tmp[k] = v[tmp[k]][0]
        tmp[k] = v[tmp[k]][random.randint(0,len(v[tmp[k]])-1)]
        add_mod(record, 'name variation', k, '')
    record['modified'] = tmp
    return record


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


def add_suffix(record):
    """

    :param record: 
    :return: 
    """
    suffix = record['original']["name_sufx_cd"]
    record['modified']["last_name"] = record['modified']["last_name"] + ' ' + suffix
    #record["name_sufx_cd"] = None
    add_mod(record, 'add_suffix', 'last_name', '')
    return record
