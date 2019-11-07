# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response

# 表单
def search_form(request):
	return render_to_response('search_form.html')

# 接收请求数据
def search(request):  
	request.encoding='utf-8'
	if 'q' in request.GET:
		message = 'your search content:  ' + request.GET['q'].encode('utf-8')
	else:
		message = 'your search empty, please re-enter!'
	return HttpResponse(message)