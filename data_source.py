from genpass import PasswordSpace
from data_loader import DataLoader

class DataSource(object):
    def __init__(self, acc_name):
        self.data_loader = DataLoader()
        self.data_loader.load()
        self.acc = self.data_loader.get_acc(acc_name)
        self.pp = self.data_loader.structure['PP']
        self.p = self.data_loader.structure['P']
        self.d = self.acc['DICT']
        self.pws_space = PasswordSpace(self.d,
                                       self.pp,
                                       self.p)
        self.email_creds = self.acc['ACCOUNT']

    def get_chunk(self):
        creds = self.email_creds
        result = []
        pws_chunk = self.pws_space.get_password_chunk()
        if pws_chunk == None:
            print "DataSource: out of data"
            return None
        else:
            for pws in pws_chunk:
                creds['password'] = pws
                result.append(creds.copy())
        return result

if __name__ == '__main__':
    data_source = DataSource("la_hoang")
    print data_source.get_chunk()
