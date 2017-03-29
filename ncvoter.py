# ncvoter data reader
# by Han Wang
# 03/29/2017

from gen import readzip
import csv

path = 'data/apr13/ncvoter100.zip'
output = 'data/apr13.csv'
data = readzip(path)

with open(output, 'wb') as f:
    w = csv.DictWriter(f, data[data.keys()[0]].keys())
    w.writeheader()
    for k in sorted(data.keys(), key=lambda x: int(x)):
        w.writerow(data[k])
