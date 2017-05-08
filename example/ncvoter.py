# ncvoter data reader
# by Han Wang
# 03/29/2017
import csv, zipfile, calendar
from datetime import date, datetime


path = 'data/apr13/ncvoter100.zip'
output = 'data/apr13.csv'

field = ['voter_reg_num', 'last_name', 'first_name', 'birth_age','name_sufx_cd']


def readzip(fpath):
    """
    Read compressed txt files with title removed.
    :param fpath: path of the source data. zip, txt and csv formats are supported.
    :return: dict with reg_nums as keys and rows as values.
    """
    d = []
    a = zipfile.ZipFile(fpath, 'r')
    b = a.open(fpath.split('/')[-1][:-4]+'.txt')
    reader = csv.reader(b, delimiter='\t')
    for i in reader:
        tmp = []
        for j in i:
            tmp += [j.strip()]
        d+=[tmp]
    return d


def dob(record):
    """
    Make up dob for a record
    :param record: a row of data
    :return: modified data by replacing age with dob.
    """
    tmp = record
    s = ' '.join(record[:3])
    ymd = date.fromordinal(sum([ord(x) for x in s])).isoformat()
    year = 2017 - int(record[3])
    # leap year 02-29 validation
    while '02-29' in ymd and not calendar.isleap(year):
        year -= 1
    tmp[3] = ymd[5:] + '-' + str(year)
    return tmp

data = readzip(path)
indices = [data[0].index(x) for x in field]
filtered = [[data[i][j] for j in indices] for i in range(len(data))]
filtered[0][3] = 'dob'
filtered[0] = ['ID'] + filtered[0]
for i in range(1, len(filtered)):
    filtered[i] = [str(i)]+dob(filtered[i])

with open(output, 'wb') as f:
    w = csv.writer(f)
    w.writerows(filtered)

