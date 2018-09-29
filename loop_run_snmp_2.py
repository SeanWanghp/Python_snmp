# coding=utf-8
from pysnmp.entity.rfc3413.oneliner import cmdgen
from os.path import exists
import sys
import os, datetime, time
import multiprocessing, telnetlib
import subprocess, string
import os, sys, logging, datetime
from time import sleep
import re as sre
from multiprocessing import Process
import random


def _run_walk(target_IP, target_port):
		'''
		snmp code from python source code
		'''
        # Turn on debugging
        # debug.setLogger(debug.Debug('msgproc', 'secmod'))
        # Check for already existing file
        # target_file_name = str(random.random()) + '.txt'
        target_file_name = '1.txt'
        # print "target_file_name:", target_file_name

        community_name = 'public'
        # oid_id = '1.3.6.1.2.1'
        oid_id = '1.3.6.1.'
        # print "target_IP", target_IP, target_port, target_file_name
        path = 'snmp_walk_result/'
        if not os.path.exists(path):
            os.makedirs(path)
        if exists(path + target_file_name):
            sys.exit("The file '%s' already exists. Try again." % target_file_name)
        else:
            # target_file = open(path + target_file_name, 'wb')
            pass

        # Initialize counter to zero
        counter = 0

        # Create command generator
        cmdGen = cmdgen.CommandGenerator()

        # Get data
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData(community_name),
            cmdgen.UdpTransportTarget((target_IP, target_port), timeout=30, retries=2),#SNMP timeout setting for E7-20
            oid_id,  # <----------------- doesn't seem perfect either
            lexicographicMode=True,
            maxRows=2500, # <----------can't leave it out, this will decide how many lines write to txt
            ignoreNonIncreasingOid=True,
            lookupNames=True,
            lookupValues=True
        )

        # Print errors and values to file
        if errorIndication:
            print(errorIndication)
        else:
            # Print error messages
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                # Print values
                snmp_content = []
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        counter += 1
                        # target_file.write("(%s)\t start_OID: %s\tvalue =\t%s\n" % (counter, name.prettyPrint(), val.prettyPrint()))
                        print ("(%s)\t start_OID: %s\tvalue =\t%s" % (counter, name.prettyPrint(), val.prettyPrint()))
                        snmp_content += [val.prettyPrint()]

                for snmp_con in snmp_content:
                    '''
                    snmp content with regular expression and showing up what you needed
                    '''
                    card_rule = sre.compile('7-2\s+')
                    # print "card_rule type:", type(card_rule)
                    card_type = card_rule.search(snmp_con)
                    if card_type:
                        print "card_type: %s"%card_type.group()
                        print "card line: '\033[0;31m%s\033[0m'"%snmp_con
                    else:
                        # print "snmp_content: %s"%snmp_con
                        continue

                    # Finish the operation
                # target_file.close()
                print('Writing to %s successful. %d lines have been written' % (target_file_name, counter))

                # sys.exit(0)
        return None


def func(ip, port):
    print "ip:", ip, port

if __name__ == '__main__':
    # Enter parameters
    # target_IP = raw_input('Please enter IP, Target IP (10.245.59.210): ') or '10.245.59.210'
    # target_port = raw_input('Target port (30161): ') or 30161
    # target_file_name = raw_input('Target filename (.txt is added): ') or str(time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())) + '.txt'
    target_IP = '10.245.59.210'
    target_port = '30161'

    for i in range(1, 2):
		'''
		multiprocesssing for running on more EQPTs
		'''
        msg = ['10.245.46.208', '10.245.46.208', '10.245.46.208', '10.245.46.215', '10.245.46.216']
        tel_port = ['161', '161', '161', '161', '161']
        wait_time = 1
        for wait in range(0, wait_time):
            # print "please wait %s seconds: %s" % (wait_time, wait)
            pool = multiprocessing.Pool(processes=len(msg))
            for (ip, port) in zip(msg, tel_port):
                pool.apply_async(_run_walk, args=(ip, port))    #thread running two E7 process
            pool.close()
            pool.join()
            # pool = multiprocessing.Pool(processes=len(msg))
            # for (i, port) in zip(msg, tel_port):
            #     pool.apply_async(func, args=(i, port))  # thread running two E7 process
            # pool.close()
            # pool.join()
        print "Sub-process(es) done."

