# Lookup tables generation
# by Han Wang
# 03/28/2017

import os, sys, csv
import gen


path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)


def get_names(fpath):
    """
    Get name dictionary
    :param fpath: compressed data file path: /data/../*.zip
    :return: dict with first and last names as keys
    """
    d = {}
    p = gen.readzip(fpath)
    dat = gen.field_filter(p, [9, 10])
    for n in dat.values():
        if n[0] not in d:
            d[n[0]] = ['NICKNAME']
        if n[1] not in d:
            d[n[1]] = ['NICKNAME']
    return d


def write_table(d):
    """
    Write a lookup table
    :param d: dict of names
    :return: file output
    """
    with open(path + '/data/lookup.txt', 'wb') as f:
        w = csv.writer(f)
        for k in d.keys():
            w.writerow([k] + d[k])


d = get_names(path + '/data/apr13/ncvoter100.zip')
write_table(d)