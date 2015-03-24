from poplib import POP3, POP3_SSL
from imaplib import IMAP4, IMAP4_SSL
from smtplib import SMTP, SMTP_SSL

class EmailAuth(object):
    @staticmethod
    def try_auth(server_info, user_info):
        protocol = server_info['protocol']
        if (protocol == 'SMTP'):
            try_auth_smtp(server_info, user_info)
        elif (protocol == 'POP'):
            try_auth_pop(server_info, user_info)
        elif (protocol == 'IMAP'):
            try_auth_imap(server_info, user_info)

    @staticmethod
    def try_auth_pop(server_info, user_info):
        try:
            if (server_info['SSL'] == True):
                if not server_info['port']:
                    server_info['port'] = 993
                conn = POP3_SSL(server_info['addr'], server_info['port'])
            else:
                if not server_info['port']:
                    server_info['port'] = 143
                conn = POP3(server_info['addr'], server_info['port'])
            conn.set_debuglevel(2)
            conn.user(user_info['username'])
            conn.pass_(user_info['password'])
        except:
            print "Invalid credentials:"
        else:
            print "Valid credential"
        finally:
            conn.close()

    @staticmethod
    def try_auth_imap(server_info, user_info):
        try:
            if (server_info['SSL'] == True):
                if not server_info['port']:
                    server_info['port'] = 993
                conn = IMAP4_SSL(server_info['addr'], server_info['port'])
            else:
                if not server_info['port']:
                    server_info['port'] = 143
                conn = IMAP4(server_info['addr'], server_info['port'])
            conn.set_debuglevel(2)
            conn.user(user_info['username'])
            conn.pass_(user_info['password'])
        except:
            print "Invalid credentials:"
        else:
            print "Valid credential"

    @staticmethod
    def try_auth_smtp(server_info, user_info):
        try:
            if (server_info['SSL'] == True):
                if not server_info['port']:
                    server_info['port'] = 993
                conn = SMTP_SSL(server_info['addr'], server_info['port'])
            else:
                if not server_info['port']:
                    server_info['port'] = 143
                conn = SMTP(server_info['addr'], server_info['port'])
            conn.set_debuglevel(2)
            conn.login(user_info['username'], user_info['password'])
        except:
            print "Invalid credentials:"
        else:
            print "Valid credential"

if __name__ == '__main__':
    server_info = {
        'protocol': 'POP',
        'SSL': True,
        'addr': 'pop3.google.com',
        'port': '993'
    }
    user_info = {
        'username': 'hoanglatk26',
        'password': 'abc'
    }

    EmailAuth.try_auth(server_info, user_info)
