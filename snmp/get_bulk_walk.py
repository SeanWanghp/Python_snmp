# coding=utf-8
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2016-12-12
# coding=gbk
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word



from pysnmp.entity.rfc3413.oneliner import cmdgen


cg = cmdgen.CommandGenerator()                          ##获得CommandGenerator对象

def snmpgetwalk(*args):
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorindex, varBindTable = cmdGen.bulkCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(('10.245.59.210', 30161)),
        0, 2,
        args[0],
        args[1],
    )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%sat%s' % (
            errorStatus.prettyPrint(),
            errorindexandvarBinds[int(errorindex) - 1][0] or '?'
        )
              )
    for varBindTableRow in varBindTable:
        for name, val in varBindTableRow:
            print("WALK showing:", '%s=%s' % (name.prettyPrint(), val.prettyPrint()))

def snmpgetbulk(*args):
    errorIndication, errorStatus, errorIndex, varBinds = cg.nextCmd(\
        cmdgen.CommunityData('my-agent', 'public', 1), cmdgen.UdpTransportTarget(('10.245.59.210', 161)),\
        args[0])
    print(errorIndication, errorStatus, errorStatus)
    for content in varBinds:
        print("SNMP content:", content[0][1])


def snmpget(*args):
    errorIndication, errorStatus, errorIndex, varBinds = cg.getCmd( #0代表v1,1代表v2c
                                                    cmdgen.CommunityData('my-agent', 'public', 1),
        ##社区信息，my-agent ,public 表示社区名,1表示snmp v2c版本，0为v1版本
                                                    cmdgen.UdpTransportTarget(('10.245.59.210', 161)),
        ##这是传输的通道，传输到IP 192.168.70.237, 端口 161上(snmp标准默认161 UDP端口)
                                                     args[0])
        ##传送的OID,个人认为MIB值
    print("SNMPGET:", str(varBinds[0]))                  ##varBinds返回是一个stulp，含有MIB值和获得值

def runit(loop=None):
    OID_W = '.1.3.6.1'                                  #walk oid
    OID_N = '.1.3.6.1.2.1.1'                            #get bulk with oid
    # snmpgetbulk(OID_N)                                  #Can using for single OID get value
    # snmpgetwalk(OID_N, OID_W)                           #Can using for single OID get value
    for i in range(1, loop):
        OID = '.1.3.6.1.2.1.1.%s.0'%i
        snmpget(OID)                                    #Can using for single OID get value
        print("i:", i)


if __name__ == "__main__":
    runit(loop=8)

######################################################################################################################

#!/usr/bin/python3
#-*-coding=utf-8-*-
#本模块由乾颐堂陈家栋编写，用于乾颐盾Python课程！
#QQ:594284672
#亁颐堂官网www.qytang.com
#乾颐盾课程包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！
from pysnmp.entity.rfc3413.oneliner import cmdgen

def cmdgen_bulkcmd():
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget(('10.245.59.210', 161)),
            0, 25,
            '1.3.6.1.2.1.2.2.1.2',
            '1.3.6.1.2.1.2.2.1.7',
        )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%sat%s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex) - 1] or '?'
        ))
    elif varBindTable == []:
        print("OID has no value, please try available one!")
    elif varBindTable:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('SNMP WALK: %s=%s' % (name.prettyPrint(), val.prettyPrint()))

# cmdgen_bulkcmd()