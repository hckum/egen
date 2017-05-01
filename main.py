# Error Generation Simulator v0.1
# by Han Wang
# 03/28/2017

from core.table import Table

if __name__ == "__main__":
    t = Table()
    t.load_config('config.txt')
    t.load_data('data/apr13.csv')
    #print [x[0] for x in t.config['fields_formats']]
    #print t.get_original_data()[0]
    #print t.formats
    t.generate()
    t.write()
