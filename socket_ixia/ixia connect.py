import sys, socket, re, os, copy, time
srvhost = '10.245.69.200'
ixiaip = '10.245.252.54'
username = 'sean'
sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockobj.connect((srvhost, 4555))

sockobj.send('package require IxTclHal \r\n')
print sockobj.recv(4096).rstrip('\r\n')

sockobj.send('ixConnectToTclServer %s \r\n' % srvhost)
print sockobj.recv(4096).rstrip('\r\n')

sockobj.send('ixConnectToChassis %s \r\n' % ixiaip)
print sockobj.recv(4096).rstrip('\r\n')

sockobj.send('ixGetChassisID %s \r\n' % ixiaip)
print sockobj.recv(4096).rstrip('\r\n')

buffer = ''
print "*"*50

for line in open('ixia.txt'):
#    print line
    sockobj.send(line + "\r\n")
    ixiaoutput = sockobj.recv(4096).rstrip('\r\n')
    print ixiaoutput
    print 
    buffer += ixiaoutput
#    print buffer

print "*"*50

sockobj.send('ixLogout \r\n')
print sockobj.recv(4096).rstrip('\r\n')

sockobj.send('ixDisconnectFromChassis %s \r\n' % ixiaip)
print sockobj.recv(4096).rstrip('\r\n')

sockobj.send('ixDisconnectTclServer %s \r\n' % srvhost)
print sockobj.recv(4096).rstrip('\r\n')


