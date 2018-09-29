# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Maojun'
#data@:2018-03-22
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word


from telnetlib import Telnet
from time import sleep
import logging


class Para(object):         #property need 'object' for running
    '''
    # a = Para(5)
    # print a.host
    # a.host = 100
    # print a.host
    '''
    def __init__(self):
        self._port = None

    def get_port(self):
        return self._port

    def set_port(self, value):
        print "_port is 23"
        if not isinstance(value, int):
            raise ValueError('host must be an integer!')
        if value != 23:
            raise ValueError('host must between 23!')
        self._port = value

    def del_port(self):
        del self._port

    port = property(fget=get_port, fset=set_port, fdel=del_port, doc="I'm the property.")

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self._score = score


class e7_telnet(object):
    def __init__(self):
        print "self:", self()
        self.function_judge()
        pass

    def __call__(self):
        self.__dict__ = {'_host': 'x.x.x.x',
                            '_port': '23',
                            '_type': 'ssh'}
        return self.__dict__


    def telnet_e7(self, _host, _port, _type=None):
        '''
        Telent to _host and return the session
        '''
        self.Tel = Telnet(_host, _port)
        # self.Tel.debuglevel(0)
        res = self.Tel.read_until(": " or "# " or "~ ")
        return self.Tel



class cli(e7_telnet, Para):
    def __init__(self, _host, _port, _type):
        super(cli, self).__init__()

        # self.enter = '\r\n'
        self.res = ''
        self._host = _host
        Para().port = _port         #import property class to check parameter
        self._port = Para().port
        self._type = _type
        self.session = self.telnet_e7(self._host, self._port, self._type)
        self.score = 10
        print self.score
        self.login()

    def __new__(cls, *args, **kwargs):
        '''
        Give a prompt for user when system running start.
        '''
        logging.warn('SMX server2 upgrade in process, please waiting...................')
        return object.__new__(cls, *args, **kwargs)   #__init__will not running if no return

    def __del__(self):
        '''
        close the session
        '''
        self.session.write('exit' + self.enter)
        try:
            self.session.close()
            logging.warn("telnet session closed!")
        except BaseException, e:
            print e.message

    def login(self):
        '''
        login to the server
        '''
        if self._type == None:
            self.session.write("user" + self.enter)
            self.res += self.session.read_until(": ")
            self.session.write("password" + self.enter)
            self.res += self.session.read_until("$ ")
            self.session.write("pwd" + self.enter)
            self.res += self.session.read_until("$ ")

    def cli_command(self, command):
        '''
        :param command: CLI
        :return: output with the command
        '''
        for cli in command.split('\n'):
            if not cli.strip().startswith('#'):
                self.session.write(command.strip() + self.enter)
                self.res += self.session.read_until("$ " or ": ")
                print self.res
                sleep(5)
            else:
                print "ignore one command"
        return self.res

    def step_command(self, command, prompt):
        '''
        :param command:
        :param prompt:
        :return: output from the command
        '''
        self.session.write(command + self.enter)
        print self.session.read_until(prompt)


    def ftp_get_baseline(self, ftp_ip, ftp_user, ftp_password, baseline_version):
        '''
        using ftp server to get the baseline
        '''
        self.step_command('ftp %s'%ftp_ip, ": ")
        self.step_command('%s'%ftp_user, ":")
        self.step_command('%s'%ftp_password, "> ")
        self.step_command('ls', "> ")
        self.step_command('get %s'%baseline_version, "> ")
        self.step_command('bye', "# ")


    def run_command(self, cli, baseline_version):
        '''
        upgrade SMx server detail process
        :param cli:
        :param baseline_version:
        :return:
        '''
        ftp_ip = '10.245.46.201'
        ftp_user = 'sean'
        ftp_password = 'sean'
        ftp_path = 'cd \xxxxx\xxx\install'


        cli_result = self.cli_command(cli)
        #switch user and copy baseline
        self.step_command('sudo -i', "# ")
        self.step_command('cd /opt/pma/PMAPMAA/bin', "# ")
        '''
        cd /opt/pma/PMAPMAA/logs    check the log files and remove unused
        ./install-xxx.bin -n -c standalone -d /opt/pma -u
		mount -t cifs -o username=username,password=******* //your local windows ip/version /mnt/version/
        '''
        self.step_command('./shutdown.sh', "bin]# ")
        self.step_command('cp /mnt/version/%s /opt/' % (baseline_version), "# ")    #will take minutes
        self.step_command('cd /opt', "# ")
        self.step_command('ll', "# ")
        # self.ftp_get_baseline(ftp_ip, ftp_user, ftp_password, baseline_version)
        # self.step_command('ls', "# ")
        #install new baseline
        self.step_command('cd /opt', "# ")
        self.step_command('./%s -n -c standalone -d /opt/pma -u'%(baseline_version), "opt]# ")    #will take minutes...."yes(y)|no(n)): "
        # self.step_command('y', "version]# ")    #will take minutes
        #
        # # #install finished then startup SMX server
        self.step_command('cd /opt/pma/PMAPMAA/bin', "# ")
        self.step_command('./startup.sh', "bin]# ")
        self.step_command('./ver.sh', "# ")
        # # return cli_result     #for decorator
        self.step_command('exit', "$ ")


    def cli_lines(self, baseline_version):
        '''
        cli_lines using for run cli command
        '''
        cli = '''pwd
                cd /mnt/version
                ls -all'''
        print baseline_version
        return self.run_command(cli, baseline_version)

    def _is_some_method(obj):
        return inspect.ismethod(obj) or inspect.ismethoddescriptor(obj)


    def function_judge(self):
        '''
        # inspect.getmembers(object[, predicate]) Return all the members of an object in a list of (name, value) pairs sorted by name.
        If the optional predicate argument is supplied, only members for which the predicate returns a true value are included.
        :return:
        '''
        import inspect
        print "inspect process starting ---------------------------------"
        print inspect.ismethod(self.run_command)
        print inspect.isclass(cli)
        for key, method in inspect.getmembers(e7_telnet, inspect.ismethod):
            print "key: %s, methond: %s"%(key, method)
            # for item in method:
            #     print "method: ", item
        print inspect.getmodulename('C:\\Python27\\Doc\\telnet_ping\\telnet_try.py')
        print inspect.getdoc(self.cli_lines)
        print "inspect process stopped ---------------------------------"

if __name__ == "__main__":
    getattr(cli, 'enter', setattr(cli, 'enter', '\r\n'))
    # sleep(600)
    b = cli('10.245.x.x', 23, None)
    b.cli_lines('install-xxxx.bin')


