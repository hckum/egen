# Lookup table generator
# by Han Wang
# 4/4/2017


import csv

variants = {}

for i in range(1,69):
    d = {}
    with open('lookup/'+str(i)+'.csv', 'r') as f:
        reader = csv.reader(f)
        k = 0
        for i in reader:
            d[k] = i[1:]
            k += 1

    names = {}
    for i in d.keys():
        for j in d[i]:
            if j not in names:
                names[j] = set([i])
            else:
                names[j].add(i)
    print len(names)
    for n in names:
        variants[n] = set([])
        for j in names[n]:
            variants[n] |= set(d[j])
        variants[n].remove(n)

with open('lookup.csv', 'wb') as f:
    writer = csv.writer(f)
    for v in sorted(variants.keys()):
        writer.writerow([v.upper()]+sorted(list(variants[v])))

