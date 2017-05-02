from record import *
from collections import OrderedDict
import csv, random, copy
import config
class Table:
    """
    Class for a data set
    """
    def __init__(self):
        self.title = []
        self.original = []
        self.modified = []
        self.data = []
        self.config = {}
        self.formats = []
        self.length = 0
        self.n = 0
        self.error_registry = {}
        self.fields = {'d':0, 'v':0, 'f':0}

    def load_config(self, fpath=''):
        d = {}
        if fpath:
            tmp = open(fpath, 'r')
        else:
            tmp = config.c
        for line in tmp:
            l = line.strip()
            if not l.startswith('#'):
                k = l.split('=')
                if k != ['']:
                    if k[1].strip()[0].isdigit():
                        d[k[0].strip()] = float(k[1].strip())
                    else:
                        d[k[0].strip()] = list(
                            [tuple(x.strip().split(':')) if ':' in x else x.strip() for x in k[1].split(',')])
        self.config = d

    def load_data(self, fpath):
        """
        
        :param fpath: load csv data 
        :return: 
        """
        tmp = []
        f = open(fpath,'r')
        reader = csv.reader(f)
        for i in reader:
            tmp+=[i]
        self.title = tmp[0]
        self.n = len(self.title)
        for r in range(1,len(tmp)):
            self.original+=[OrderedDict([(tmp[0][i], tmp[r][i]) for i in range(len(tmp[0]))])]

        # generate format list
        config = OrderedDict(self.config['fields_formats'])
        for c in config:
            if 'f' == config[c]:
                self.fields['f'] += 1
            elif 'd' == config[c]:
                self.fields['d'] += 1
            elif 'v' == config[c]:
                self.fields['v'] += 1

        t = float(sum(self.fields.values()))
        for f in self.fields.keys():
            self.fields[f] /=t

        for i in self.original[0].keys():
            if i in config.keys():
                self.formats += [config[i]]
            else:
                self.formats += ['h']

        # load self.data
        for i in self.original:
            self.data += [Record(i, self.formats)]
        self.length = len(self.data)

    def select(self,n):
        """
        Select the Nth record
        :param n: 
        :return: the Nth record
        """
        return self.data[n]

    def random_select(self):
        """        
        :return: randomly selected record
        """
        n = random.randint(0, self.length-1)
        return self.data[n]

    def index_of(self, record):
        """
        :param record: 
        :return: index of record 
        """
        return self.data.index(record)

    @staticmethod
    def conditional_sample(a, b):
        return random.choice(list(set(a)-set(b)))

    def get_modified_data(self):
        self.modified = [x.get_modified() for x in self.data]
        return self.modified

    def get_original_data(self):
        self.original = [x.get_original() for x in self.data]
        return self.original

    #########################################
    # Field Errors
    #########################################

    def missing(self, n, repetitive=False):
        counter = 0
        while counter < n:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('d')
            if ind*self.n+f_index not in self.error_registry:
                record.data[f_index].missing()
                #record.collect_mod()

                self.error_registry[ind*self.n+f_index] = [-1]
                counter+=1

    def swap(self, n, repetitive=False):
        """
        This is a special error that at the moment 
        is only used between first_name and last_name. 
        :param n: 
        :param repetitive: 
        :return: 
        """
        counter = 0
        while counter < n:
            record = self.random_select()
            ind = self.index_of(record)
            f_index_1 = self.title.index('last_name')
            f_index_2 = self.title.index('first_name')
            if ind*self.n+f_index_1 not in self.error_registry:
                record.swap(f_index_1, f_index_2)
                #record.collect_mod()

                self.error_registry[ind*self.n+f_index_1] = []
                self.error_registry[ind*self.n+f_index_2] = []
                counter+=1

    def date_swap(self, n, repetitive=False):
        """
        This is a special error that at the moment only applied to dob.
        :param n: 
        :param repetitive: 
        :return: 
        """
        counter = 0
        while counter < n:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('d')
            if ind * self.n + f_index not in self.error_registry:
                record.date_swap(f_index)
                # record.collect_mod()

                self.error_registry[ind * self.n + f_index] = []
                counter += 1

    def variant(self, n, repetitive=False):
        """
        This is a special error that at the moment 
        is only applied to first_name. 
        :param n: 
        :param repetitive: 
        :return: 
        """
        counter = 0
        while counter < n:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = self.title.index('first_name')
            if ind*self.n+f_index not in self.error_registry:
                record.variant(f_index, 'NICKNAME')

                self.error_registry[ind*self.n+f_index] = []
                counter+=1

    def add_suffix(self, n, repetitive=False):
        """
        This is a special error that at the moment 
        is only used on last_name. 
        :param n: 
        :param repetitive: 
        :return: 
        """
        counter = 0
        while counter < n:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = self.title.index('last_name')
            if ind * self.n + f_index not in self.error_registry and record.data[-1].original:
                record.add_suffix(f_index, record.data[-1].original)

                self.error_registry[ind * self.n + f_index] = []
                counter += 1

    #########################################
    # Char Errors
    #########################################

    def typo(self, n, repetitive=False):
        """
        Add typos
        :param n: total number of typo errors
        :param repetitive: 
        :return:
        """
        # Calculate numbers of typo errors
        nv_insertion = int(self.config['v_rate_insertion'] * self.fields['v'] * n)
        nv_deletion = int(self.config['v_rate_deletion'] * self.fields['v'] * n)
        nv_transpose = int(self.config['v_rate_transpose'] * self.fields['v'] * n)
        nv_replace = int(self.config['v_rate_substitution'] * self.fields['v'] * n)

        nf_insertion = int(self.config['f_rate_insertion'] * self.fields['f'] * n)
        nf_transpose = int(self.config['f_rate_transpose'] * self.fields['f'] * n)
        nf_replace = int(self.config['f_rate_substitution'] * self.fields['f'] * n)

        nd_transpose = int(self.config['d_rate_transpose'] * self.fields['d'] * n)
        nd_replace = int(self.config['d_rate_substitution'] * self.fields['d'] * n)

        ####################################
        # Variable Length Typo
        ####################################

        counter = 0
        while counter < nv_insertion:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('v')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k]!=[-1] and record.data[f_index].length>len(self.error_registry[k]):
                pos = self.conditional_sample(range(record.data[f_index].length), self.error_registry[k])

                record.data[f_index].insert(pos)

                counter+=1
                self.error_registry[k] += [pos]
                print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

        counter = 0
        while counter < nv_deletion:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('v')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k]!=[-1] and record.data[f_index].length-1>len(self.error_registry[k]):
                pos = self.conditional_sample(range(record.data[f_index].length), self.error_registry[k])

                record.data[f_index].delete(pos)

                counter += 1
                print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

        counter = 0
        while counter < nv_transpose:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('v')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k]!=[-1] and record.data[f_index].length-2>len(self.error_registry[k]):
                pos = self.conditional_sample(range(record.data[f_index].length - 1), self.error_registry[k])
                if pos+1 not in self.error_registry[k]:

                    record.data[f_index].transpose(pos)

                    counter += 1
                    self.error_registry[k] += [pos, pos+1]
                    print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

        counter = 0
        while counter < nv_replace:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('v')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k] != [-1] and record.data[f_index].length-1>len(self.error_registry[k]):
                pos = self.conditional_sample(range(record.data[f_index].length), self.error_registry[k])
                if pos not in self.error_registry[k]:

                    record.data[f_index].replace(pos)

                    counter += 1
                    self.error_registry[k] += [pos]
                    print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

        ####################################
        # Fixed Length Typo
        ####################################

        counter = 0
        while counter < nf_insertion:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('f')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k] != [-1] and record.data[f_index].length-1>len(self.error_registry[k]):
                pos = self.conditional_sample(range(record.data[f_index].length), self.error_registry[k])

                record.data[f_index].insert(pos)

                counter += 1
                self.error_registry[k] += [pos]
                print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

        counter = 0
        while counter < nf_transpose:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('f')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k] != [-1] and record.data[f_index].length-1>len(self.error_registry[k]):
                pos = self.conditional_sample(range(record.data[f_index].length - 1), self.error_registry[k])
                if pos + 1 not in self.error_registry[k]:

                    record.data[f_index].transpose(pos)

                    counter += 1
                    self.error_registry[k] += [pos, pos + 1]
                    print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

        counter = 0
        while counter < nf_replace:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('f')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k] != [-1] and record.data[f_index].length-1>len(self.error_registry[k]):
                pos = self.conditional_sample(range(record.data[f_index].length), self.error_registry[k])
                if pos not in self.error_registry[k]:

                    record.data[f_index].replace(pos)

                    counter += 1
                    self.error_registry[k] += [pos]
                    print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

        ####################################
        # Date Typo
        ####################################

        counter = 0
        while counter < nd_transpose:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('d')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k] != [-1]:
                pos = self.conditional_sample(['y', 'm', 'd'], self.error_registry[k])
                if pos not in self.error_registry[k]:
                    tmp = copy.deepcopy(record.data[f_index].modified)

                    record.data[f_index].transpose(pos)

                    if tmp!=record.data[f_index].modified:
                        counter += 1
                        self.error_registry[k] += [pos]
                        print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

        counter = 0
        while counter < nd_replace:
            record = self.random_select()
            ind = self.index_of(record)
            f_index = record.random_select_by_format('d')
            k = ind * self.n + f_index
            if k not in self.error_registry:
                self.error_registry[k] = []
            if self.error_registry[k] != [-1]:
                pos = self.conditional_sample(['y','m','d'], self.error_registry[k])
                if pos not in self.error_registry[k]:
                    tmp = copy.deepcopy(record.data[f_index].modified)

                    record.data[f_index].replace(pos)

                    if tmp!=record.data[f_index].modified:
                        counter += 1
                        self.error_registry[k] += [pos]
                        print(record.data[f_index].original, record.data[f_index].modified, record.data[f_index].modifier)

    def generate(self):
        """
        The core function of error generation
        :return: 
        """
        n_missing = int(self.config['rate'] * self.config['rate_missing'] * self.length)
        n_swap = int(self.config['rate'] * self.config['rate_swap_name'] * self.length)
        n_date_swap = int(self.config['rate'] * self.config['rate_swap_dob'] * self.length)
        n_variant = int(self.config['rate'] * self.config['rate_vari'] * self.length)
        n_suffix = int(self.config['rate'] * self.config['rate_suffix'] * self.length)
        n_typo = int(self.config['rate'] * self.config['rate_typo'] * self.length)

        self.missing(n_missing)
        self.swap(n_swap)
        self.date_swap(n_date_swap)
        self.variant(n_variant)
        self.add_suffix(n_suffix)
        self.typo(n_typo)

        for d in self.data:
            d.collect_mod()

    #########################################
    # Output
    #########################################

    def write_original(self, fpath):
        with open(fpath, 'wb') as f:
            writer = csv.DictWriter(f, fieldnames=[x[0] for x in self.config['fields_formats']])
            writer.writeheader()
            writer.writerows(self.get_original_data())

    def write_modified(self, fpath):
        with open(fpath, 'wb') as f:
            writer = csv.DictWriter(f, fieldnames=[x[0] for x in self.config['fields_formats']])
            writer.writeheader()
            writer.writerows(self.get_modified_data())

    def write_difference(self,fpath):
        with open(fpath, 'wb') as f:
            writer = csv.writer(f)
            fieldnames = [x[0] for x in self.config['fields_formats']] * 2 + ['modif', 'field', 'pos']
            writer.writerow(fieldnames)
            for record in self.data:
                if record.modifier['modif']!=[]:
                    tmp = record.original.values()
                    tmp += record.modified.values()
                    tmp_mod = record.modifier.copy()
                    for k in tmp_mod.keys():
                        tmp_mod[k] = ';'.join([str(x) for x in tmp_mod[k]])
                    tmp += tmp_mod.values()
                    writer.writerow(tmp)

    def write(self):
        self.write_original(self.config['original_data'][0])
        self.write_modified(self.config['modified_data'][0])
        self.write_difference(self.config['differences'][0])


