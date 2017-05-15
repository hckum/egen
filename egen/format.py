import string, random, datetime


def match(a,b):
    return a == b


class FixedLength:
    """
    fixed length string
    """

    def __init__(self, v, field, id, u=True):
        self.original = v
        self.modified = v
        self.modifier = {'modif':[], 'field':[], 'pos':[]}
        self.mutable = u

        self.field = field
        self.id = id
        self.length = len(self.modified)
        self.format = 'fixed'
        self.type = 'alnum'

        k = KeyboardTypo()
        self.ref = k.layout

        if v.isalpha():
            self.type = 'alpha'
        if v.isdigit():
            self.type = 'digit'

    def add_mod(self, mod, field=None, pos=-1):
        self.modifier['modif'] += [mod]
        self.modifier['field'] += [field] if field else [self.field]
        self.modifier['pos'] += [pos]
        self.length = len(self.modified)

    def immutable(self):
        self.mutable = False

    def insert(self, pos):
        values = string.ascii_uppercase + string.digits
        if self.type == 'alpha':
            values = string.ascii_uppercase + self.ref[self.modified[pos]]
        if self.type == 'digit':
            values = string.digits + self.ref[self.modified[pos]]

        tmp = self.modified[pos]

        while tmp==self.modified[pos]:
            tmp = values[random.randint(0,len(values)-1)]

        self.modified = self.modified[:pos]+tmp+self.modified[pos:-1]
        self.add_mod('insertion',self.field,pos)

    def transpose(self, pos):
        tmp = self.modified[:pos]+self.modified[pos+1]+self.modified[pos]+self.modified[pos+2:]
        if not match(tmp, self.modified):
            self.modified = tmp
            self.add_mod('transpose', self.field, pos)

    def replace(self, pos):
        values = self.ref[self.modified[pos]]
        tmp = values[random.randint(0,len(values)-1)]
        self.modified = self.modified[:pos]+tmp+self.modified[pos+1:]
        self.add_mod('replace', self.field, pos)

    def missing(self):
        self.modified = ''
        self.add_mod('missing', self.field, -1)

    def variant(self, v):
        self.modified = v
        self.add_mod('variant', self.field, -1)


class VariableLength:
    """
    variable length string 
    """

    def __init__(self, v, field, id, u=True):
        self.original = v
        self.modified = v
        self.modifier = {'modif': [], 'field': [], 'pos': []}
        self.mutable = u

        self.field = field
        self.id = id
        self.length = len(self.modified)
        self.format = 'variable'
        self.type = 'alnum'

        k = KeyboardTypo()
        self.ref = k.layout

        if v.isalpha():
            self.type = 'alpha'
        if v.isdigit():
            self.type = 'digit'

    def add_mod(self, mod, field=None, pos=-1):
        self.modifier['modif'] += [mod]
        self.modifier['field'] += [field] if field else [self.field]
        self.modifier['pos'] += [pos]
        self.length = len(self.modified)

    def immutable(self):
        self.mutable = False

    def insert(self, pos):
        values = string.ascii_uppercase + string.digits
        if self.type == 'alpha':
            values = string.ascii_uppercase + self.ref[self.modified[pos]]
        if self.type == 'digit':
            values = string.digits + self.ref[self.modified[pos]]

        tmp = values[random.randint(0,len(values)-1)]

        self.modified = self.modified[:pos]+tmp+self.modified[pos:]
        self.add_mod('insertion', self.field, pos)

    def delete(self, pos):
        self.modified = self.modified[:pos]+self.modified[pos+1:]
        self.add_mod('deletion', self.field, pos)

    def transpose(self, pos):
        tmp = self.modified[:pos] + self.modified[pos + 1] + self.modified[pos] + self.modified[pos + 2:]
        if not match(tmp, self.modified):
            self.modified = tmp
            self.add_mod('transpose', self.field, pos)

    def replace(self, pos):
        values = self.ref[self.modified[pos]]
        tmp = values[random.randint(0,len(values)-1)]
        self.modified = self.modified[:pos]+tmp+self.modified[pos+1:]
        self.add_mod('replace', self.field, pos)

    def missing(self):
        self.modified = ''
        self.add_mod('missing', self.field, -1)

    def variant(self, v):
        self.modified = v
        self.add_mod('variant', self.field, -1)

    def add_suffix(self, v):
        self.modified += ' ' + v
        self.add_mod('add_suffix', self.field, -1)


class HiddenField:
    """
    immutable field, does not appear in output files.
    """
    def __init__(self, v, field, id):
        self.original = v
        self.modified = v
        self.modifier = {'modif': [], 'field': [], 'pos': []}
        self.mutable = False

        self.field = field
        self.id = id
        self.length = len(v)
        self.format = ''
        self.type = ''


class Date:
    """
    Class of dates
    Format: MM-DD-YYYY
    """

    def __init__(self, v, field, id, u=True):
        """

        :param v: value 
        :param id: id of the parent record
        """
        t = v.split('-')
        self._month = t[0]
        self._day = t[1]
        self._year = t[2]
        self.month = t[0]
        self.day = t[1]
        self.year = t[2]
        self.parentID = id

        self.original = v
        self.modified = '-'.join([self.month, self.day, self.year])
        self.length = len(self.modified)
        self.modifier = {'modif': [], 'field': [], 'pos': []}
        self.field = field
        self.format = 'date'
        self.mutable = u

    def update(self, m, d, y):
        """
        Update everything 
        :param v: 
        :return: 
        """
        self.month, self.day, self.year = m, d, y
        self.modified = '-'.join([m, d, y])

    @staticmethod
    def validate(date):
        try:
            datetime.datetime.strptime(date, '%m-%d-%Y')
        except ValueError:
            return False
        return True

    def add_mod(self, mod, field, pos=-1):
        """
        Add a modifier
        :param mod: 
        :param field: 
        :param pos: 
        :return: 
        """
        self.modifier['modif'] += [mod]
        self.modifier['field'] += [field]
        self.modifier['pos'] += [pos]

    def immutable(self):
        self.mutable = False

    def setField(self, field):
        """

        :param field: field name
        :return: 
        """
        self.field = field

    # insert, delete, transpose, replace
    # pos options: M/D/Y
    # temporally disable insert and delete

    def transpose(self, pos):
        m, d, y = self.month, self.day, self.year
        if pos == 'y':
            y = self.year[:2] + self.year[3] + self.year[2]
        elif pos == 'm':
            m = self.month[::-1]
        elif pos == 'd':
            d = self.day[::-1]
        tmp = '-'.join([m, d, y])
        if self.validate(tmp):
            self.update(m, d, y)
            self.add_mod('transpose',self.field, pos)

    def replace(self, pos):
        p = random.randint(0, 1)
        if pos == 'y':
            tmp = self.year[:p + 2] + string.digits.replace(self.year[p + 2], '')[random.randint(0, 8)] + self.year[
                                                                                                          p + 3:]
            if self.validate('-'.join([self.month, self.day, tmp])):
                self.update(self.month, self.day, tmp)
                self.add_mod('replace', self.field, pos)
        elif pos == 'm':
            tmp = self.month[:p] + string.digits.replace(self.month[p], '')[random.randint(0, 8)] + self.month[p + 1:]
            if self.validate('-'.join([tmp, self.day, self.year])):
                self.update(tmp, self.day, self.year)
                self.add_mod('replace', self.field, pos)
        elif pos == 'd':
            tmp = self.day[:p] + string.digits.replace(self.day[p], '')[random.randint(0, 8)] + self.day[p + 1:]
            if self.validate('-'.join([self.month, tmp, self.year])):
                self.update(self.month, tmp, self.year)
                self.add_mod('replace', self.field, pos)

    def swap(self):
        if self.validate('-'.join([self.day, self.month, self.year])):
            self.update(self.day, self.month, self.year)

    def missing(self):
        self.modified = ''
        self.add_mod('missing', self.field, -1)


class KeyboardTypo:
    """
    Keyboard related typo 
    """
    def __init__(self):
        self.layout = {'A':'S',
                       'B':'VN',
                       'C':'XV',
                       'D':'SF',
                       'E':'WR',
                       'F':'DG',
                       'G':'FH',
                       'H':'GJ',
                       'I':'UO',
                       'J':'HK',
                       'K':'JL',
                       'L':'K',
                       'M':'N',
                       'N':'BM',
                       'O':'IP',
                       'P':'O',
                       'Q':'W',
                       'R':'ET',
                       'S':'AD',
                       'T':'RY',
                       'U':'YI',
                       'V':'CB',
                       'W':'QE',
                       'X':'ZC',
                       'Y':'TU',
                       'Z':'X',
                       '0':'9',
                       '1':'2',
                       '2':'13',
                       '3':'24',
                       '4':'35',
                       '5':'46',
                       '6':'57',
                       '7':'68',
                       '8':'79',
                       '9':'80'}

