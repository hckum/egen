# Web Crawler to behindthename.com
# by Han Wang
# 04/03/2017

from bs4 import BeautifulSoup
import urllib2, csv

'''
names = []
for k in range(1, 22):
    url = 'https://surnames.behindthename.com/names/'+str(k)
    a,b = [],[]
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')

    for i in soup.findAll("div", { "class" : "browsename b0" }):
        a += [i.find('a')['href'].split('/')[-1]]
    for i in soup.findAll("div", { "class" : "browsename b1" }):
        b += [i.find('a')['href'].split('/')[-1]]
    name = ['']*(len(a)+len(b))
    for i in range(len(name)):
        name[i] = a[i/2] if i%2==0 else b[(i-1)/2]
    names += name
    #with open('surnames/'+str(k)+'.txt', 'wb') as f:
    #    w = csv.writer(f)
    #    w.writerows([[x] for x in name])


print 'Listing URLs, done.'
'''
for i in range(1,22):
    with open('surnames/'+str(i)+'.txt', 'r') as f:
        r = csv.reader(f)
        names = []
        for j in r:
            names += j
    d = {}
    for n in names:
        url='https://surnames.behindthename.com/name/'+n+'/related'

        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content,'lxml')
        rows = soup.findAll('a',{'class':'ngl'})
        print n
        d[n] = []
        for t in rows:
            try:
                t.string.decode('ascii')
                d[n] += [t.string.encode('ascii')]
            except UnicodeEncodeError:
                pass
        d[n] = sorted(list(set(d[n])))

    with open('lookup/s'+str(i)+'.csv', 'wb') as f:
        w = csv.writer(f)
        for k in d.keys():
            w.writerow([k]+d[k])

