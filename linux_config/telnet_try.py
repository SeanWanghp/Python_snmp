from telnetlib import Telnet
from time import sleep



class e7_telnet(object):
    def __init__(self):
        print "self:", self()
        pass

    def telnet_e7(self, host, port, type=None):
        self.Tel = Telnet(host, port)
        # self.Tel.debuglevel(0)
        res = self.Tel.read_until(": " or "# " or "~ ")
        return self.Tel

class cli(e7_telnet):
    def __init__(self, host, port, type):
        super(cli, self).__init__()

        self.enter = '\r\n'
        self.res = ''
        self.host = host
        self.port = port
        self.type = type
        self.session = self.telnet_e7(self.host, self.port, self.type)
        pass

    def __call__(self):
        print 'telnet is in process'

    def login(self):
        if self.type == None:
            self.session.write("root" + self.enter)
            self.res += self.session.read_until(": ")
            self.session.write("root" + self.enter)
            self.res += self.session.read_until("# ")
            self.session.write("cli" + self.enter)
            self.res += self.session.read_until("# ")

    def cli_command(self, command):
        for cli in command.split('\n'):
            if not cli.strip().startswith('#'):
                self.session.write(command.strip() + self.enter)
                self.res += self.session.read_until("# ")
                print self.res
                sleep(5)
            else:
                print "ignore one command"
        return self.res

    def run_command(self, cli):
        self.login()
        cli_result = self.cli_command(cli)
        return cli_result     #for decorator


    def cli_lines(self):
        cli = '''paginate false
                        show inter line sum
                        #show run inter line'''
        return self.run_command(cli)

    def function_judge(self):
        import inspect
        print inspect.ismethod(self.run_command)
        print inspect.isclass(cli)


b = cli('10.245.47.10', 23, None)
b.cli_lines()
b.function_judge()