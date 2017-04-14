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

    output1 = cfg['original_data'][0]
    output2 = cfg['modified_data'][0]
    output3 = cfg['differences'][0]

    filter2 = cfg['output']

    rate, rate_missing, rate_swap = cfg['rate'], cfg['rate_missing'], cfg['rate_swap']
    rate_suffix = cfg['rate_suffix']
    rate_typo, rate_vari = cfg['rate_typo'], cfg['rate_vari']
    typo_prob = [cfg['rate_insertion'], cfg['rate_deletion'], cfg['rate_transpose'], cfg['rate_substitution']]

    ##################################################
    # 2. DATA PREPARATION

    p = readcsv(fpath)

    dat,suffix = field_filter(p, p[p.keys()[0]].keys())
    print p[p.keys()[0]].keys()
    ks = sorted(dat.keys(), key=lambda x: int(x))
    for k in dat.keys():
        dat[k]['original'] = dob(dat[k]['original'])
        dat[k]['modified'] = copy.deepcopy(dat[k]['original'])
        dat[k]['ID'] = str(ks.index(k)+1)
    #print(suffix)

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
    prob = [rate_missing, rate_swap, rate_typo, rate_vari,rate_suffix]
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
        elif p < q[4]:
            t = random.randint(0, len(suffix) - 1)
            k = suffix[t]
            dat[k] = add_suffix(dat[k])
            del suffix[t]
        if not match(dat[k]['modified'], dat[k]['original']):
            d[k] = dat[k]['modified']
            n_error += 1

    print(len(d)/float(len(dat)))

    ##################################################
    # 6. WRITE OUTPUT TO FILES

    with open(output1, 'wb') as f:
        w = csv.DictWriter(f, ['ID']+filter2, extrasaction='ignore')
        w.writeheader()
        ks = sorted(dat.keys(), key=lambda x : int(x))
        for k in ks:
            dat[k]['original']['ID'] = dat[k]['ID']
            w.writerow(dat[k]['original'])

    with open(output2, 'wb') as f:
        w = csv.DictWriter(f, ['ID']+filter2, extrasaction='ignore')
        w.writeheader()
        ks = sorted(dat.keys(), key=lambda x : int(x))
        for k in ks:
            dat[k]['modified']['ID'] = dat[k]['ID']
            w.writerow(dat[k]['modified'])

    with open(output3, 'wb') as f:
        w = csv.writer(f)
        ks = sorted(dat.keys(), key=lambda x : int(x))
        for k in ks:
            if not match(dat[k]['original'], dat[k]['modified']):
                w.writerow([dat[k]['ID']]+[dat[k]['original'][i] for i in filter2]
                           +[dat[k]['modified'][j] for j in filter2]
                           +[';'.join(dat[k]['modifier']['mod']),
                             ';'.join(dat[k]['modifier']['field']),
                             ';'.join(dat[k]['modifier']['pos'])])

