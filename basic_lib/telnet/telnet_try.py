
# from time import sleep
# time = __import__('time')
# time.sleep(5)
from telnet_ping.telnet_lib import *


class LazyImport:
    '''using for dynamic import python libs'''
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name)
        return getattr(self.module, name)


tim = LazyImport("time")


class E7Telnet(Tellib):
    def __init__(self, host, port):
        super(E7Telnet, self).__init__(host, port)
        print("self:", self)
        pass

    def telnet_e7(self, host, port, type=None):
        self.Tel = Tellib(host, port)
        # self.Tel.debuglevel(0)
        res = self.Tel.read_until(b": " or b"# " or b"~ ", 30)
        return self.Tel


class Cli(E7Telnet, TelBasic):
    def __init__(self, host, port, type, username, password):
        super(Cli, self).__init__(host, port)

        self.enter = b'\r\n'
        self.res = b''
        self.host = host
        self.port = port
        self.type = type
        self.username = username
        self.password = password
        self.session = self.telnet_e7(self.host, self.port, self.type)
        pass

    def __call__(self):
        print('telnet is in process')

    def login(self):
        if self.type is 'AXOS':
            self.session.write(self.username + self.enter)
            self.res += self.session.read_until(b": ")
            self.session.write(self.password + self.enter)
            self.res += self.session.read_until(b"# ")
            self.session.write(b"" + self.enter)
            self.res += self.session.read_until(b"# ")
        if self.type is 'EXA':
            self.session.write(self.username + self.enter)
            self.res += self.session.read_until(b": ")
            self.session.write(self.password + self.enter)
            self.res += self.session.read_until(b"> ")
            self.session.write(b"" + self.enter)
            self.res += self.session.read_until(b"> ")

    def cli_command(self, command=None):
        for cli in command.split(b'\n'):
            if not cli.strip().startswith(b'#'):
                self.session.write(command.strip() + self.enter)
                self.res += self.session.read_until(b"# ")
                for cli_print in self.res.splitlines():
                    print(cli_print.decode(encoding='utf-8'))
                tim.sleep(5)
            else:
                print ("ignore one command")
        return self.res

    @must_connected
    def run_command(self, cli):
        cli_result = self.cli_command(cli)
        return cli_result     #for decorator

    def cli_lines(self):
        '''cli_lines using for run cli command'''
        cli = b'''paginate false
                        show inter sum
                        show run inter ethernet'''
        return self.run_command(cli)

    def _is_some_method(obj):
        return inspect.ismethod(obj) or inspect.ismethoddescriptor(obj)

    def function_judge(self):
        import inspect
        print(inspect.ismethod(self.run_command))
        print(inspect.isclass(Cli))
        for key, method in inspect.getmembers(E7Telnet, inspect.ismethod):
            '''inspect.getmembers(object[, predicate]) Return all the members of an object in a list of (name, value) 
            pairs sorted by name. If the optional predicate argument is supplied, 
            only members for which the predicate returns a true value are included.'''
            print("key: %s, methond: %s"%(key, method))
            # for item in method:
            #     print "method: ", item
        print(inspect.getmodulename('C:\GitHub\python_lib\telnet_ping\telnet_try.py'))
        print(inspect.getdoc(self.cli_lines))


if __name__ == '__main__':
    b = Cli('10.245.46.208', 23, 'AXOS', username=b'sysadmin', password=b'seanwang')
    b.cli_lines()
    b.function_judge()
