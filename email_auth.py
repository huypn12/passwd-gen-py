from poplib import POP3, POP3_SSL
from imaplib import IMAP4, IMAP4_SSL
from smtplib import SMTP, SMTP_SSL

class EmailAuth(object):
    @staticmethod
    def try_auth(creds):
        protocol = creds['protocol']
        result = False
        if (protocol == 'SMTP'):
            result = EmailAuth.try_auth_smtp(creds)
        elif (protocol == 'POP'):
            result = EmailAuth.try_auth_pop(creds)
        elif (protocol == 'IMAP'):
            result = EmailAuth.try_auth_imap(creds)
        return result

    @staticmethod
    def try_auth_pop(creds):
        try:
            if (creds['SSL'] == True):
                if not creds['port']:
                    creds['port'] = 993
                conn = POP3_SSL(creds['ip_addr'], creds['port'])
            else:
                if not creds['port']:
                    creds['port'] = 143
                conn = POP3(creds['ip_addr'], creds['port'])
            conn.set_debuglevel(2)
            conn.user(creds['username'])
            conn.pass_(creds['password'])
        except:
            print "Invalid credentials:"
            return False
        else:
            print "Valid credential"
            conn.close()
            return True

    @staticmethod
    def try_auth_imap(creds):
        try:
            if (creds['SSL'] == True):
                if not creds['port']:
                    creds['port'] = 993
                conn = IMAP4_SSL(creds['ip_addr'], creds['port'])
            else:
                if not creds['port']:
                    creds['port'] = 143
                conn = IMAP4(creds['ip_addr'], creds['port'])
            conn.set_debuglevel(2)
            conn.user(creds['username'])
            conn.pass_(creds['password'])
        except:
            print "Invalid credentials:"
            return False
        else:
            print "Valid credential"
            conn.close()
            return True

    @staticmethod
    def try_auth_smtp(creds):
        try:
            if (creds['SSL'] == True):
                if not creds['port']:
                    creds['port'] = 993
                conn = SMTP_SSL(creds['ip_addr'], creds['port'])
            else:
                if not creds['port']:
                    creds['port'] = 143
                conn = SMTP(creds['ip_addr'], creds['port'])
            conn.set_debuglevel(2)
            conn.login(creds['username'], creds['password'])
        except:
            print "Invalid credentials:"
            return True
        else:
            print "Valid credential"
            conn.close()
            return False

if __name__ == '__main__':
    creds = {
        'protocol': 'POP',
        'SSL': True,
        'ip_addr': 'pop3.google.com',
        'port': '993',
        'username': 'hoanglatk26',
        'password': 'abc'
    }

    EmailAuth.try_auth(creds)
