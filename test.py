# coding=utf-8
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-09-20
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word


class Borg:
    """borg class makeing class attributes global"""
    _shared_state = {}   #attribute dictionary

    def __init__(self):
        self.__dict__ = self._shared_state   #make it attribute dictionary

class Singleton(Borg):  #Inherits from the borg class
    """this class now shares all its attributes among its various instances"""
    #this essenstiaily makes the singleton objects an object-oriented global variable

    def __init__(self, **kwargs):
        Borg.__init__(self)
        #update the attribute dictionary by inserting a new key-value pair
        self._shared_state.update(kwargs)

    def __str__(self):
        #return the attribute dictionary for printing
        return str(self._shared_state)

x = Singleton(HTTP = "hyper text transfer protocol")

y = Singleton(SNMP = 'simple network management protocol')

z = Singleton(DHCP = 'dynamic host configuration protoclo')
print x, y, z