import re
import itertools

# Note1: Password generation structure
#--------------------------------------------------------------
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
    # Preserved dictionary keywords, userinfo must implement this
    DICT_NAMES = [
        'NAME',
        'DOB',
        'TEL'
    ]
    DICT_KEYS = [
        # Full name
        'FIRST',
        'LAST',
        'MIDDLE',
        # DoB
        'DD',
        'MM',
        'YY',
        'YYYY',
        # Tel
        'MOBILE',
        'WORK'
    ]

    # Predefined pattern, applied for all agent
    PP = {
        'DATE_0': "${DD}${MM}${YYYY}",
        'DATE_1': "${MM}${DD}${YYYY}",
        'NAME_0': "${FIRST}${LAST}",
        'NAME_1': "${FIRST}${MIDDLE}${LAST}"
    }

    # Password structure
    P = {
        'P1': "%{NAME_0}%{DATE_0}",
        'P2': "#{1234}#{___}%{DATE_0}"
    }
    def __init__(self, account_info):
        self.account_info = account_info
        self.password_space = []

    @staticmethod
    def parse(string):
        element_list = re.findall(r"(.*?)\{(\w+)\}", string)
        return element_list

    @staticmethod
    def stdpat(string):
        structure = PasswordSpace.parse(string)
        enumerated_structure = (i for i,x in enumerate(structure) if x[0] == '%')
        for i in enumerated_structure:
            pattern_str = PasswordSpace.PP[structure[i][1]]
            pattern = PasswordSpace.parse(pattern_str)
            del structure[i]
            structure[i:i] = pattern
        return structure

    def genpws(self):
        for p in PasswordSpace.P.items():

            structure = PasswordSpace.stdpat(p[1])

            element_list = []
            for element in structure:
                tmp = []
                if element[0] == '#':
                    tmp.append(element[1])
                    element_list.append(tmp)
                elif element[0] == '$':
                    element_list.append(self.account_info[element[1]])

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

        self.password_space = password_list


    def numpws(self, s):
        structure = PasswordSpace.stdpat(s)
        pws_size = 0
        for element in structure:
            if element[0] == '#':
                pws_size += 1
            elif element[0] == '$':
                pws_size += len(self.account_info[element[1]])
        return pws_size

    def genpws_pat_partial():
        pass

    def genpws_partial():
        pass


if __name__ == '__main__':
    account_info = {
        # Full name
        'FIRST': ['la', 'dung'],
        'LAST': ['nguyen', 'hoang'],
        'MIDDLE': ['thi', 'van'],
        # DoB
        'DD': ['2', '02'],
        'MM': ['10', '07'],
        'YYYY': ['1982', '82'],
        # Tel
        'MOBILE': ['xxxx'],
        'WORK': ['yyyy']
    }
    password_space = PasswordSpace(account_info)
    #PasswordSpace.stdpat(PasswordSpace.P['P2'])
    password_space.genpws()
    for password in password_space.password_space:
        print password
