#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib2
import urllib
import json
import sys

#roomid=sys.argv[1]
#lag=sys.argv[2]

def http_get():
        #url='http://10.53.6.13:9090/api/v1/query?query=kube_pod_container_status_restarts_total%3E0&time=1523950678.451&_=1523950678355'
        url='http://kibana.haplat.net:60007/kibana-intf/mts_api/get_online_num?username=mts&password=bqzI2PxkkVv3tZlMB9YB&channel=idc-third-ws.longzhu.com'
	response = urllib.urlopen(url)
        return response.read()

ret = http_get()
json_dict = json.loads(ret)

for item in json_dict['data']:
        #print '%s' % item
        roomid  = item['room_id']
        online_num = item['online_num']
	#print '%s %s'%(roomid,online_num)
	dbreqdata =  "wangsu_online_num," + "roomid=" + str(roomid) + " online_num=" + str(online_num)
	dbrequrl = "http://10.53.6.15:8086/write?db=wangsu_online_num"
	dbreq= urllib2.Request(url = dbrequrl,data =dbreqdata)
	urllib2.urlopen(dbreq)
