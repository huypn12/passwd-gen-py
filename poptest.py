import poplib

try:
	conn=poplib.POP3_SSL('pop.googlemail.com', '995')
	conn.user('lanhm7777')
	conn.pass_('Lanhm1977')
except Exception as e:
	print e

print "done"
