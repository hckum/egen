# ncvoter data reader
# by Han Wang
# 03/29/2017
import csv, zipfile

path = 'data/apr13/ncvoter100.zip'
output = 'data/apr13.csv'

field = ['voter_reg_num', 'last_name', 'first_name', 'birth_age']


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

data = readzip(path)
indices = [data[0].index(x) for x in field]
filtered = [[data[i][j] for j in indices] for i in range(len(data))]

with open(output, 'wb') as f:
    w = csv.writer(f)
    w.writerows(filtered)

