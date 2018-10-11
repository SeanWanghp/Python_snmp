import os
from time import sleep

OID = '1.3.6.1.2.1.2'

for i in range(1):
	print os.popen(('snmpwalk -v2c -cpublic 10.245.46.208 %s')%OID).read()
	print 'SNMPWALK running, please wait........'
	sleep(10)

	print os.popen(('snmpwalk -v2c -cpublic 10.245.46.215 %s')%OID).read()
	print 'SNMPWALK running, please wait........'
	sleep(1)

print "SNMPWALK finished"