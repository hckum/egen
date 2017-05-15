# Error Generation Simulator v0.1
# by Han Wang
# 03/28/2017

from egen.table import Table

t = Table()
t.load_config('example/config.txt')
t.load_data('example/data/apr13.csv')
t.load_lookup('data/lookup.csv')
t.generate()
t.write()
