from format import *
from collections import OrderedDict


class Record:
    """
    Class of record
    """

    def __init__(self, record, format_list):
        """

        :param record: ordered-dict formatted record
        :param format_list: {d,f,v,i}
        # date: d
        # fixed length: f
        # viriable length: v

        """
        self.fields = record.keys()
        self.data = []
        self.id = record['ID']
        self.modifier = OrderedDict([('modif',[]), ('field',[]), ('pos',[])])
        self.original = record
        self.modified = record
        self.formats = format_list

        for k in range(len(record.keys())):
            # mutable?
            m = True
            if 'i' in format_list[k]:
                m = False
            if 'd' in format_list[k]:
                self.data += [Date(record[record.keys()[k]],record.keys()[k],self.id, m)]
            if 'f' in format_list[k]:
                self.data += [FixedLength(record[record.keys()[k]],record.keys()[k],self.id, m)]
            if 'v' in format_list[k]:
                self.data += [VariableLength(record[record.keys()[k]],record.keys()[k],self.id, m)]
            if 'h' in format_list[k]:
                self.data += [HiddenField(record[record.keys()[k]],record.keys()[k],self.id)]

        self.length = len(self.data)


    def add_mod(self, mod, field=None, pos=-1):
        self.modifier['modif'] += [mod]
        self.modifier['field'] += [field]
        self.modifier['pos'] += [pos]

    def swap(self, a, b):
        """
        :param a: field1 index 
        :param b: field2 index 
        :return: 
        """
        tmp = self.data[a].modified

        self.data[a].modified = self.data[b].modified
        self.data[b].modified = tmp

        self.add_mod('swap', self.fields[a]+' '+self.fields[b], -1)

    def date_swap(self, n):
        self.data[n].swap()
        self.add_mod('date_swap', self.fields[n], -1)

    def missing(self, i):
        self.data[i].missing()

    def variant(self, i, v):
        """
        
        :param i: position index 
        :param v: new value : 
        :return: 
        """
        self.data[i].variant(v)

    def add_suffix(self, i, v):
        """

        :param i: position index 
        :param v: new value : 
        :return: 
        """
        self.data[i].add_suffix(v)

    def typo(self, i, pos, t):
        """
        
        :param i: field index
        :param pos: position of typo
        :param t: type of typo : {i:insert, d:delete, t:transpose, r:replace} 
        :return: 
        """
        # possible typos:
        op = {'i':'insert', 'd':'delete', 't':'transpose', 'r':'replace'}
        if op[t] in dir(self.data[i]):
            if t == 'i':
                self.data[i].insert(pos)
            if t == 'd':
                self.data[i].delete(pos)
            if t == 't':
                self.data[i].transpose(pos)
            if t == 'r':
                self.data[i].replace(pos)

    def collect_mod(self):
        """
        Merge modifiers into one list
        :return: 
        """
        for d in self.data:
            self.modifier['modif'] += d.modifier['modif']
            self.modifier['field'] += d.modifier['field']
            self.modifier['pos'] += d.modifier['pos']

    def get_original(self):
        self.original = OrderedDict([(self.fields[i],self.data[i].original) for i in range(self.length) if 'h' not in self.formats[i]])
        return self.original

    def get_modified(self):
        self.modified = OrderedDict([(self.fields[i],self.data[i].modified) for i in range(self.length) if 'h' not in self.formats[i]])
        return self.modified

    def select_field_by_index(self, n):
        """
        
        :param n: 
        :return: selected field
        """
        return self.data[n]

    def select_field_by_name(self, name):
        """
        :param name:field name 
        :return: selected field
        """
        return self.data[self.fields.index(name)]

    def random_select_index(self):
        """
        Randomly select a mutable field
        :return: 
        """
        n = random.randint(0, self.length-1)
        while not self.data[n].mutable:
            n = random.randint(0, self.length - 1)
        return n

    def random_select_field(self):
        """
        Randomly select a mutable field
        :return: 
        """
        n = random.randint(0, self.length-1)
        while not self.data[n].mutable:
            n = random.randint(0, self.length - 1)
        return self.data[n]

    def random_select_by_format(self, f):
        """
        Randomly select a mutable field 
        :param f: 
        :return: 
        """
        k = [i for i in range(self.length) if self.formats[i]==f]
        n = random.sample(k,1)[0]
        return n

