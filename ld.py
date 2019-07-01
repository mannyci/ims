import sys, ldap

DN = ''
secret = ''
un = ''
# DN, secret, un = sys.argv[1:4]

server = "ldap://."
port = 389

base = "dc=,dc="
scope = ldap.SCOPE_SUBTREE
filter = "(&(objectClass=user)(sAMAccountName=" + un + "))"
attrs = ["*"]

l = ldap.initialize(server)
l.protocol_version = 3
l.set_option(ldap.OPT_REFERRALS, 0)

l.simple_bind_s(DN, secret)

r = l.search(base, scope, filter, attrs)
type, user = l.result(r, 60)
name, attrs = user[0]
print(attrs['userPrincipalName'])


sys.exit()