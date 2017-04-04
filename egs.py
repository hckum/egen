# Migrating functions from main.py
# by Han Wang
# 4/4/2017

from gen import *
import random
import csv


def egs(config):
    """

    :param config: config file path
    :return: None
    """
    ##################################################
    # 1. CONFIGURATIONS

    cfg = load_config(config)
    fpath = cfg['input'][0]
    lookup = cfg['lookup'][0]
    print fpath
    output1 = cfg['original_data'][0]
    output2 = cfg['modified_data'][0]
    output3 = cfg['differences'][0]

    filter1, filter2 = cfg['field'], cfg['output']

    rate, rate_missing, rate_swap = cfg['rate'], cfg['rate_missing'], cfg['rate_swap']
    rate_typo, rate_vari = cfg['rate_typo'], cfg['rate_vari']
    typo_prob = [cfg['rate_insertion'], cfg['rate_deletion'], cfg['rate_transpose'], cfg['rate_substitution']]

    ##################################################
    # 2. DATA PREPARATION

    p = readzip(fpath)
    dat = field_filter(p, filter1)
    ks = sorted(dat.keys(), key=lambda x: int(x))
    for k in dat.keys():
        dat[k]['original'] = dob(dat[k]['original'])
        dat[k]['modified'] = copy.deepcopy(dat[k]['original'])
        dat[k]['ID'] = str(ks.index(k)+1)


    ##################################################
    # 3. LOOKUP TABLE PREPARATION

    v = {}
    with open(lookup,'r') as f:
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

    with open(output1, 'wb') as f:
        w = csv.DictWriter(f, ['ID']+filter2, extrasaction='ignore')
        w.writeheader()
        ks = sorted(dat.keys(),key=lambda x:int(x))
        for k in ks:
            dat[k]['original']['ID'] = dat[k]['ID']
            w.writerow(dat[k]['original'])

    with open(output2, 'wb') as f:
        w = csv.DictWriter(f, ['ID']+filter2, extrasaction='ignore')
        w.writeheader()
        ks = sorted(dat.keys(),key=lambda x:int(x))
        for k in ks:
            dat[k]['modified']['ID'] = dat[k]['ID']
            w.writerow(dat[k]['modified'])

    with open(output3, 'wb') as f:
        w = csv.writer(f)
        ks = sorted(dat.keys(),key=lambda x:int(x))
        for k in ks:
            if not match(dat[k]['original'], dat[k]['modified']):
                w.writerow([dat[k]['ID']]+[dat[k]['original'][i] for i in filter2]+[dat[k]['modified'][j] for j in filter2]+dat[k]['modifier'])

