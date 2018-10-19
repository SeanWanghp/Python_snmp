# coding=utf-8                                           #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-10-18
# coding=gbk                                             #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
import ConfigParser


def writeConfig(filename):
    config = ConfigParser.ConfigParser()
    # set db
    section_name = 'db'
    config.add_section(section_name)
    config.set(section_name, 'dbname', 'MySQL')
    config.set(section_name, 'host', '127.0.0.1')
    config.set(section_name, 'port', '80')
    config.set(section_name, 'password', '123456')
    config.set(section_name, 'databasename', 'test')

    # set app
    section_name = 'app'
    config.add_section(section_name)
    config.set(section_name, 'loggerapp', '192.168.20.2')
    config.set(section_name, 'reportapp', '192.168.20.3')

    # write to file
    config.write(open(filename, 'w'))


def updateConfig(filename, section, **keyv):
    config = ConfigParser.ConfigParser()
    config.read(filename)
    print config.sections()
    # for section in config.sections():
    #     print "[", section, "]"
    #     items = config.items(section)
    #     for item in items:
    #         print "\t", item[0], " = ", item[1]
    if config.has_option('db', "dbname"):
        print config.get('db', 'dbname')
    else:
        print config.set("db", "dbname", "MySQL_write")
    print "will start to re-write 'reportapp' value.........."
    for key in keyv:
        print "\t", key, " = ", keyv[key]
        config.set(section, key, keyv[key])
    config.write(open(filename, 'w'))


if __name__ == '__main__':
    file_name = 'test.ini'
    writeConfig(file_name)
    updateConfig(file_name, 'app', reportapp='192.168.100.100')
    print "end__"