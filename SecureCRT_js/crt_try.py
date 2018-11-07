# $language = "Python"
# $interface = "1.0"

import datetime
import time
import json
import re, string

'''
run this script in SecureCRT table, not with python method
'''

def CreateTab(host, tabName):
    objNewTab = crt.Session.ConnectInTab(host, True, failSilently=False)
    if objNewTab.Session.Connected != True:
        if crt.GetScriptTab().Index != objNewTab.Index:
            objNewTab.Close()
            return False
    objNewTab.Caption = tabName
    return objNewTab


def initTabSession(oneTab):
    usr      = 'exxxxxx\n'
    pwd      = 'admin\n'
    cfgCli   = 'set session pager disabled timeout disabled\n'
    disAlarm = 'set session alarm-notif disabled event-notif disabled tca-notif disabled\n'

    oneTab.Screen.Send(usr)
    oneTab.Screen.Send(pwd)
    crt.Sleep(200)
    oneTab.Screen.Send(cfgCli)
    crt.Sleep(200)

    oneTab.Screen.Send(disAlarm)
    crt.Sleep(200)

def cycleRestartTest(ctrlTabList, waitHint, waitSeconds, namePrefix, cycleIndex, vectEnable):
    keepTab = '/dbug/timeout\n'
    xdsl    = 'cd /xdsl\n'
    stop    = 'api stop all\n'
    start   = 'api start all\n'

    now   = datetime.datetime.now()

    fileName = "%s_TgtDetail_%s.txt" % (namePrefix, str(now).replace(' ', '_')[:-7])
    fileName = fileName.replace(':', '_')
    logFile  = open(fileName, 'a+')

    #debug console for each card in chasis
    i = 0
    for oneTab in ctrlTabList:
        oneTab.Activate()
        ii       = i%4 #for chasis 2
        shelf    = ii/2 + 1
        card     = ii%2 + 1
        dbgCard  = 'debug card %d/%d\n' % (shelf, card)
        #if(i!=6):

        oneTab.Screen.Send(dbgCard)
        oneTab.Screen.WaitForString(waitHint)

        i += 1

    crt.CommandWindow.Visible = True
    crt.CommandWindow.SendToAllSessions = True

    crt.CommandWindow.Text = keepTab
    crt.CommandWindow.Send()
    time.sleep(1)

    crt.CommandWindow.Text = xdsl
    crt.CommandWindow.Send()
    time.sleep(1)

    crt.CommandWindow.Text = stop
    crt.CommandWindow.Send()

    stopTimeFile  = open('ApiStopAllTime.txt', 'w')
    stopTimeFile.write('%d' % int(time.time()))
    stopTimeFile.close()

    time.sleep(5)   #time between "api stop all" and "api start all"

    beginTime = int(time.time())
    crt.CommandWindow.Text = start
    crt.CommandWindow.Send()
    ##disableBadPorts(ctrlTabList, badPorts, waitHint)

    startTimeFile  = open('ApiStartAllTime.txt', 'w')
    startTimeFile.write('%d' % beginTime)
    startTimeFile.close()

    #crt.Dialog.MessageBox("Started!")

    now = datetime.datetime.now()
    nowStr = now.strftime("%Y-%m-%d %H:%M:%S")

    logFile.write('%s: begin\n\n\n' % nowStr)

    '''
    ctrlTabList[3].Screen.Send('api stop all\n')
    time.sleep(30)
    ctrlTabList[3].Screen.Send('api start all\n')
    '''

    #wait x seconds then check result
    time.sleep(waitSeconds)

    #get show dsl-port result one by one
    i = 0
    showPortResults  = []
    targetsEndTime   = []
    targetsShowDone  = []

    for oneTab in ctrlTabList:

        ii       = i%4 #for chasis 2
        shelf    = ii/2 + 1
        card     = ii%2 + 1

        #if(i == 6):
        #    i+=1
        #    continue

        oneTab.Activate()
        oneTab.Screen.Send("exit\n")
        oneTab.Screen.WaitForString(waitHint)

        endTime = int(time.time())
        targetsEndTime.append(endTime)

        oneTab.Screen.Send('show dsl-port %d/%d\n' % (shelf, card))
        oneTab.Screen.WaitForString(waitHint)

        endTime = int(time.time())
        targetsShowDone.append(endTime)


        oneTab.Close()


chasisIps = ['10.245.46.205']

waitHint  = 'wang1'

testCycleCnt = 1

tabList = []

waitSeconds = 5

i = 0
for ip in chasisIps:
    for index in range(1, 4):
        tabHost = '/telnet %s 23' % ip
        tabName = 'Target-%d'  % (i*4 + index)
        oneTab = CreateTab(tabHost, tabName)

        if(oneTab == False):
            crt.Dialog.MessageBox("Tab %s failed!" % tabName)
            exit()

        tabList.append(oneTab)
        initTabSession(oneTab)
    i += 1


namePrefix   = "CRTlog/1000ft_Vect"

i = 0
while i<testCycleCnt:
    cycleRestartTest(tabList, waitHint, waitSeconds, namePrefix, i, True)
    i += 1

