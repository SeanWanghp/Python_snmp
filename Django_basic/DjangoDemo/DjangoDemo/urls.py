"""DjangoDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from demoapp import views, search


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index),
    path('login/', views.Login),
    path('python/', views.Python_test),
    path(r'json/', views.getJson),
    path(r'my_view/', views.my_view),

    # path(r'', views.index),  # new
    path('<int:year>/<str:month>/', views.index, name='index'),
    path(r'add', views.add, name='add'),  # add calc
    path(r'add/(\d+)/(\d+)', views.add2, name='add2'),

    path(r'home', views.home, name='home'),
    path(r'navigate.html', views.navigate, name='navigate'),
    path(r'e7.html', views.e7, name='e7'),
    path(r'movie.ogv', views.movie, name='movie'),
    path(r'index_js.html', views.index_js, name='index_js'),
    path(r'base.html', views.base, name='base'),
    path(r'list.html', views.addressbook, name='addressbook'),
    path(r'csv/(<filename>\w+)', views.output),
    path(r'base.html', views.index_html, name='index'),

    path(r'search-form', search.search_form),
    path(r'search', search.search),
]
