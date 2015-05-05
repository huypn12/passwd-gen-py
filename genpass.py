import re
import itertools

# Note1: Password generation structure
#--------------------------------------------------------------
# List utilities function: flatten nested list
def nested_item(depth, value):
    if depth <= 1:
        return [value]
    else:
        return [nested_item(depth - 1, value)]

def nested_list(n):
    """Generate a nested list where the i'th item is at depth i."""
    lis = []
    for i in range(n):
        if i == 0:
            lis.append(i)
        else:
            lis.append(nested_item(i, i))
    return lis

def flatten(lis):
    """Given a list, possibly nested to any level, return it flattened."""
    new_lis = []
    for item in lis:
        if type(item) == type([]):
            new_lis.extend(flatten(item))
        else:
            new_lis.append(item)
    return new_lis


class PasswordSpace(object):
    def __init__(self, dictionary, predefined_pattern, pattern):
        self.P = pattern
        self.PP = predefined_pattern
        self.D = dictionary
        self.password_space = []
        self.space_size = 0
        self.space_index = 0
        self.space_offset = 128
        print "PasswordSpace generator created"
        print "Rule set: ", self.P
        print "Pattern set: ", self.PP
        print "User dictionary: ", self.D
        for p in self.P:
            self.space_size += self.numpws(p[1])
        print "Password space size: ", self.space_size
        print "Password space offset: ", self.space_offset

    def parse(self, string):
        element_list = re.findall(r"(.*?)\{(\w+)\}", string)
        return element_list

    def stdpat(self, string):
        structure = self.parse(string)
        enumerated_structure = (i for i,x in enumerate(structure) if x[0] == '%')
        for i in enumerated_structure:
            pattern_str = self.PP[structure[i][1]]
            pattern = self.parse(pattern_str)
            del structure[i]
            structure[i:i] = pattern
        return structure

    def get_elems_by_key(self, tuple_list, key):
        result = [v for i, v in enumerate(tuple_list) if v[0] == key]
        return result[0][1]

    ###################################################################
    ###################################################################
    def genpws(self):
        for p in self.P:
            structure = self.stdpat(p[1])
            element_list = []
            for element in structure:
                tmp = []
                if element[0] == '#':
                    tmp.append(element[1])
                    element_list.append(tmp)
                elif element[0] == '$':
                    element_list.append(self.get_elems_by_key(self.D, element[1]))

            product_list = []
            for dict_elem in element_list:
                if product_list == []:
                    product_list = dict_elem
                    continue
                else:
                    product_list = [list(item) for item in itertools.product(product_list, dict_elem)]

            password_list = []
            for nested_product in product_list:
                flat_product = flatten(nested_product)
                password = ''.join(flat_product)
                password_list.append(password)
            self.password_space.extend(password_list)

    ###################################################################
    ###################################################################
    ###################################################################
    def numpws(self, s):
        structure = self.stdpat(s)
        if len(structure) == 0:
            return 0
        else:
            pws_size = 1
            for element in structure:
                if element[0] == '#':
                    pws_size *= 1
                elif element[0] == '$':
                    if len(self.get_elems_by_key(self.D, element[1])) > 0:
                        #pws_size *= len(self.account_info[element[1]])
                        pws_size *= len(self.get_elems_by_key(self.D, element[1]))
        return pws_size

    def genpws_pat_partial(self, pindex, start, count):
        p = self.P[pindex]
        structure = self.stdpat(p[1])
        I = len(self.D) - 1
        pos = [0] * len(self.D)
        pos[I] = start % len(self.D[I])
        i = I - 1
        while i>=0:
            start = start / len(self.D[i+1])
            pos[i] = start % len(self.D[i])
            i = i - 1
        c = 0
        result = []
        while c < count:
            element_list = []
            for element in structure:
                tmp = []
                if element[0] == '#':
                    tmp.append(element[1])
                    element_list.append(tmp)
                elif element[0] == '$':
                    # Find the dictionary which has
                    D_idx_l = [idx for idx, v in enumerate(self.D) if v[0] == element[1]]
                    D_idx = D_idx_l[0]
                    D_dict = self.D[D_idx][1]
                    element_list.append(D_dict[pos[D_idx]])
            result.append(''.join(flatten(element_list)))

            c += 1
            j = I-2#
            while j>=0:
                pos[j] = pos[j] + 1
                if pos[j] > len(self.D[j]) - 1:
                    pos[j] = 0
                    j = j - 1
                else:
                    break
        return result

    def calc_start(self, idx):
        start = 0
        for i in range(idx):
            start += self.numpws(self.P[i][1])
        return start

    def calc_count(self, idx):
        return self.numpws(self.P[idx][1])

    def genpws_partial(self, start, count):
        i = 0
        while self.calc_start(i) + self.calc_count(i) < start:
            i += 1
        s = start - self.calc_start(i)
        c = min(count, self.calc_count(i))
        result = []
        while (True):
            new_passwd = self.genpws_pat_partial(i,s,c)
            #print new_passwd, ".."
            result.extend(new_passwd)
            #c = len(new_passwd)
            count = count - c
            i += 1
            if (i >= len(self.P)):
                break
            s = 0
            c = min(count, self.calc_count(i))
            if c == 0:
                break
        return result

    def get_password_chunk(self):
        if self.space_index > self.space_size:
            return None
        stop_idx = self.space_index + self.space_offset
        chunk = self.genpws_partial(self.space_index, self.space_offset)
        self.space_index = stop_idx
        return chunk


if __name__ == '__main__':
    # Predefined pattern, applied for all agent
    PP = {
        'DATE_0': "${DD}${MM}${YYYY}",
        'DATE_1': "${MM}${DD}${YYYY}",
        'NAME_0': "${FIRST}${LAST}",
        'NAME_1': "${FIRST}${MIDDLE}${LAST}"
    }

    # Password structure

    P = [
        ['P1', "%{NAME_0}%{DATE_0}"],
        ['P2', "#{1234}#{___}%{DATE_0}"],
        ['P3', "%{DATE_0}%{NAME_0}"],
        ['P4', "%{NAME_1}%{DATE_0}%{DATE_1}"],
        ['P5', "%{NAME_0}"]
    ]

    D = [
        # Full name
        ('FIRST', ['la', 'dung']),
        ('LAST', ['nguyen', 'hoang']),
        ('MIDDLE', ['thi', 'van']),
        # DoB
        ('DD', ['2', '02']),
        ('MM', ['10', '07']),
        ('YYYY', ['1982', '82', '92']),
        # Tel
        ('MOBILE', ['xxxx']),
        ('WORK', ['yyyy'])
    ]

    print "User dictionary: "
    print D
    password_space = PasswordSpace(D, PP, P)
    print "\n"

    print "Pattern list: "
    print password_space.PP
    print "\n"

    print "Password pattern list: "
    print password_space.P
    print "\n"

    print (password_space.space_size)

    pat = password_space.genpws_partial(1260,100)
    print pat
