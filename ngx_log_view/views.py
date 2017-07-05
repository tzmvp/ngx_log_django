#coding=UTF-8
# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
import time
import datetime
import types
import sys
from datetime import timedelta,date

reload(sys)
sys.setdefaultencoding( "utf-8" )

def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if(n<0):
        n = abs(n)
        return date.today()-timedelta(days=n)
    else:
        return date.today()+timedelta(days=n)


def get_time_list():
    file_log = "/home/tzmvp/ngx_logspider/unix.log"    # get unix timestamp list,each line record minute 
    open_file = open(file_log,'r+')
    read_file = open_file.readlines()
    time_list = []
    for d in read_file:
	      time = d.split('\n')[0]
	      time_list.append(time)
    return time_list

def get_info(request):
    domain = request.GET['domain']
    list = get_time_list()
    return HttpResponse(domain,list)


def get_pv_count(request):
    domain = request.GET['domain']
    time_list = get_time_list()
    today = str(get_day_of_day(0))
    date_1_ago = str(get_day_of_day(-1))
    date_2_ago = str(get_day_of_day(-2))
    date_6_ago = str(get_day_of_day(-6))

    file_log = "/home/tzmvp/ngx_logspider/log/%s_%s" %(domain,today)        # file record every domain's pv count,per line a value
    file_log_1_day_ago = "/home/tzmvp/ngx_logspider/log/%s_%s" %(domain,date_1_ago)
    file_log_6_day_ago = "/home/tzmvp/ngx_logspider/log/%s_%s" %(domain,date_6_ago)

    open_file = open(file_log,'r+')
    read_file = open_file.readlines()
    open_file_1day = open(file_log_1_day_ago,'r+')
    read_file_1day = open_file_1day.readlines()
    open_file_6day = open(file_log_6_day_ago,'r+')
    read_file_6day = open_file_6day.readlines()

    pv_list = []
    pv_list_1day = []
    pv_list_6day = []
    
    for p in read_file:
	      pv = p.split('\n')[0]
	      pv_int = int(pv)
	      pv_list.append(pv_int)

    for p1 in read_file_1day:
	      pv1 = p1.split('\n')[0]
	      pv1_int = int(pv1)
	      pv_list_1day.append(pv1_int)

    for p6 in read_file_6day:
	      pv6 = p6.split('\n')[0]
	      pv6_int = int(pv6)
	      pv_list_6day.append(pv6_int)

    return render(request,'line.html',{'domain':domain,'time_list':time_list,'pv_list':pv_list,'pv_list_1day':pv_list_1day,'pv_list_6day':pv_list_6day,'today':today,'date_1_ago':date_1_ago,'date_2_ago':date_2_ago})

def Index(request):

    pv_count_file = '/home/tzmvp/ngx_logspider/overwrite.log'     # recoder overview,per line a data,line:xx,xx,xx,xx,xx,xx,xx\n
    pv_file = open(pv_count_file,'r')
    read_pv = pv_file.readlines()
    day = str(get_day_of_day(-1))

    domain_list = []

    for i in read_pv:
	      res = i.split('\n')[0]
	      R = res.split(',')
	      domain_list.append(R)

    return render(request,'index.html',{'domain_list':domain_list,'day':day})
