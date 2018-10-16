# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-10-12
'''
yield 是一个类似 return 
的关键字，迭代一次遇到yield时就返回yield后面的值。重点是：下一次迭代时，从上一次迭代遇到的yield后面的代码开始执行。
简要理解：yield就是 return 返回一个值，并且记住这个返回的位置，下次迭代就从这个位置后开始。
'''

# def fab(max):
#     a, b = 0, 2
#     while a < max:
#         yield a     #返回调用函数，执行完再向下执行, 返回整个YIELD返回的值
#         print 'a: ', a
#         a, b = b, a+b
#
# for i in fab(20):
#     print i,",",


# def yield_test(n):
#     for i in range(n):
#         yield call(i)   #返回整个yield返回的值,最先执行的是yield调用的方法
#         print("i=", i)
#         # 做一些其它的事情
#     print("do something.")
#     print("end.")
#
#
# def call(i):
#     # print 'call i: ', i
#     return i * 3
#
#     # 使用for循环
#
#
# for i in yield_test(5):     #i的值是整个yield返回的值,yield将函数定义成可迭代的
#     print(i, ",")


def search(keyword, filename):
    '''
    可以选出文件中你需要的行或者文字输出
    :param keyword:
    :param filename:
    :return:
    '''
    print('generator started')
    f = open(filename, 'r')
    # Looping through the file line by line
    for line in f:
        if keyword in line:
            # If keyword found, return it
            yield line
    f.close()

for i in search('driver', 'selenium.txt'):      #可以选出带某个参数的命令，比如：所有的SHOW
    print i.decode('gbk').encode('utf-8')

# def add(s, x):
#     return s + x
#
# def gen():
#     for i in range(3):
#         pass
#         # yield i
#     print 'i is', i
#
# base = gen()
# base = [0 ,1, 2, 3]
#
# for n in [1, 20, 2]:
#     print "n is: ", n
#     print "base is: ", base
#     base = (add(i, n) for i in base)
#
#
# print list(base)