from django.shortcuts import render
from django.http import HttpResponse
import json
import sys
from datetime import date
import calendar
from calendar import HTMLCalendar
from django.views.decorators.csrf import requires_csrf_token

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

'''create another blog for Django
    https://djangocentral.com/building-a-blog-application-with-django/'''


# Create your views here.
@requires_csrf_token
def Index(request):
    return render(request, 'index.html')


def Login(request):
    '''https://www.cnblogs.com/leffss/p/11271097.html   can useing web for telnet'''
    return render(request, 'login.html')


def Python_test(request):
    import os
    print(os.getcwd())
    from templates import tk1
    return render(request, 'python_test.html')


def getJson(request):
    resp = {'errorcode': 100, 'detail': 'Get success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def my_view(request):
    if request.method == 'POST':
        import os
        print(os.getcwd())
        # Do your stuff ,calling whatever you want from set_gpio.py

    return  # Something, normally a HTTPResponse, using django


def index(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    if year < 1900 or year > 2099:
        year = date.today().year
    month_name = calendar.month_name[month]
    title = "MyClub Event Calendar - %s %s" % (month_name, year)
    cal = HTMLCalendar().formatmonth(year, month)
    return HttpResponse("<h1>%s</h1><p>%s</p>" % (title, cal))
    # return HttpResponse(u"欢迎光临 Maojun website, please go Home page - http://192.168.37.101:8000/home !")


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


import telnetlib


class tel(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # self.Session = telnetlib.Telnet(self.host, self.port)
        # self.Session.write(str("e7support") + str("\r\n"))
        # self.Session.read_until(str(">"), 10)
        # self.Session.write(str("admin") + str("\r\n"))
        # self.Session.read_until(str(">"), 10)
        # self.Session.write(str("show card") + str("\r\n"))
        # self.cli_return = self.Session.read_until(str(">"), 10)


class run(object):
    def __init__(self, name):
        self.name = name
        self.run = tel('10.245.46.205', 23).host
        e7support = str(10)
        self.tel = tel('10.245.46.205', 23).host


class Test(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
        self.run = '10.245.46.208'
        e7support = str(10)
        self.tel = tel('10.245.46.205', 23).host


def add2(request, a, b):
    c = int(a) + int(b)
    r = run('Maojun').name
    t = str(c) + r
    return HttpResponse(str(t))


def movie(request):
    '''https://www.cnblogs.com/leffss/p/11271097.html   can useing web for telnet'''
    from os import startfile
    startfile('C:\\Python37\\Scripts\\DjangoDemo\\templates\\movie.ogv')

    return render(request, 'C:\\Python37\\Scripts\\DjangoDemo\\templates\\movie.ogv')


def home(request):
    TutorialList = ["HTML", "CSS", "Java", "Python", "Django"]
    info_dict = {'site': 'calix', 'content': 'E7&C7'}
    List = map(str, range(5))
    test = Test("Sean", 30, "Male")

    return render(request, 'home.html',
                  {'TutorialList': TutorialList, 'info_dict': info_dict, 'List': List, 'test': test})
    # return render(request, 'icon.png')


def index_html(request):
    TutorialList = ["HTML", "CSS", "Java", "Python", "Django"]
    info_dict = {'site': 'calix', 'content': 'E7&C7'}
    List = map(str, range(5))
    test = Test("sean", 30, "male")
    return render(request, 'index.html',
                  {'TutorialList': TutorialList, 'info_dict': info_dict, 'List': List, 'test': test})


def base(request):
    test = Test("sean", 30, "male")
    return render(request, 'base.html', {'test': test})


def navigate(request):
    test = Test("sean", 30, "male")
    return render(request, 'navigate.html', {'test': test})


def index_js(request):
    return render(request, 'index_js.html')


def e7(request):
    test = Test("sean", 30, "male")
    return render(request, 'e7.html', {'test': test})


address = [
    {'name': 'VDSLr2-35B', 'address': '10.245.47.10', 'type': 'AXOS', 'username': 'root', 'password': 'root'},
    {'name': 'NGPON2-4', 'address': '10.245.46.207/208', 'type': 'AXOS', 'username': 'root', 'password': 'root'},
    {'name': 'Traffic', 'address': '10.245.46.205', 'type': 'E7', 'username': 'e7support', 'password': 'admin'},
    {'name': 'SLV192', 'address': '10.245.59.210', 'type': 'E7', 'username': 'e7support', 'password': 'admin'},
    {'name': 'E3-VCP192', 'address': '10.245.47.231-235', 'type': 'E3', 'username': 'e3support', 'password': 'admin'}
]


# 这里的address不是字典列表，而是元组列表
def addressbook(request):
    return render(request, 'list.html', {'address': address})


from django.template import loader, Context


def output(request, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename =%s.csv' % filename
    t = loader.get_template('csv.html')
    c = Context({'data': address})
    response.write(t.render(c))
    return response
