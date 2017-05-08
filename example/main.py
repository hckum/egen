# Error Generation Simulator v0.1
# by Han Wang
# 03/28/2017

from egs.table import Table

if __name__ == "__main__":
    t = Table()
    t.load_config('./config.txt')
    t.load_data('data/apr13.csv')
    t.load_lookup('data/lookup.csv')
    t.generate()
    t.write()
