# coding=utf-8
#!/usr/bin/python
# Filename: lambda.py
def make_repeater(n):
	return lambda c: c*n
twice = make_repeater(2)
print twice('a')
print twice('word')
print twice(5)


print filter(lambda x:x%2!=0,range(1,11))

print filter(lambda x:len(x)!=0,'hello')

print sorted([1, 2, 3, 4, 5, 6, 7, 8, 9], key=lambda x: abs(5-x))    #按照元素与5距离从小到大进行排序

print map(lambda x: x+1, [1, 2, 3])

print reduce(lambda a, b: '{};;{}'.format(a, b), [1, 2, 3, 4, 5, 6, 7, 8, 9])

