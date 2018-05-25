#! /usr/bin/env python
#-*- coding:utf-8 -*-
import json
import urllib2
import urllib
from influxdb import InfluxDBClient

#get pod cpu rate
def get_use_rate(measurement,namespace_name,pod_name):
	client = InfluxDBClient('k8s-influxdb.longzhu.cn', 80, '', '', 'k8s') 
	#print client.get_list_database() 
	#sql = '''SELECT last(value) FROM "%s" WHERE type = pod_container AND namespace_name = %s AND pod_name = %s''' %(measurement,namespace_name,pod_name)
	sql = '''SELECT last(value) FROM "%s" where "type" =  'pod_container' AND "namespace_name" = '%s' AND "pod_name" = '%s' ''' %(measurement,namespace_name,pod_name)
	result = client.query(sql)
	cpu_points = list(result.get_points())
	if cpu_points:
		cpu = cpu_points[0]
		print cpu
		return cpu['last']
	else:
		return 0

#get % percent
def calculate(use,limit):
	#print use,limit
	a=float(use)
	if limit == int(0):
		b="6666.6"
		#print b
	else:
		b=float(limit)
		#print b
	return "%.2f" % (a/b*100)
	#print "%.2f")


def http_get():
	namespace_name=[]
	pod_name=[]
        url='http://10.53.6.13:9090/api/v1/query?query=kube_pod_labels'
        response = urllib.urlopen(url)
	ret = response.read()
	#print ret
	return ret
#	json_dict = json.loads(ret)
#	for item in json_dict['data']['result']:
 #      		namespace = item['metric']['namespace']
#		pod = item['metric']['pod']
#		print namespace,pod


#main
if __name__ == "__main__":
   #cpu_usage = get_use_rate("cpu/usage_rate","pluops","trace-exporter-7649c97fd4-cwcdk")
   #cpu_limit = get_use_rate("cpu/limit","pluops","trace-exporter-7649c97fd4-cwcdk")
   #url_sp='http://10.53.6.13:9090/api/v1/query?query=kube_namespace_labels'
   #url_pod='http://10.53.6.13:9090/api/v1/query?query=kube_pod_labels%7Bnamespace%3D%22default%22%7D'
   #http_get()
   json_dict = json.loads(http_get())
   for item in json_dict['data']['result']:
           namespace = item['metric']['namespace']
           pod = item['metric']['pod']
           #print namespace,pod
	   cpu_usage = get_use_rate("cpu/usage_rate",namespace,pod)
	   cpu_limit = get_use_rate("cpu/limit",namespace,pod)
	   if cpu_limit == 0:
	   	rate = calculate(cpu_usage,100)
	   else:
		rate = calculate(cpu_usage,cpu_limit)  
	  	#print namespace,pod,rate
		dbreqdata =  "cpu_usage," + "namespace=" + namespace + ",pod=" + pod + " value=" + rate
		dbrequrl = "http://k8s-influxdb.longzhu.cn:80/write?db=cpu_usage_alert"
		#print(dbreqdata)
		dbreq= urllib2.Request(url = dbrequrl,data =dbreqdata)
		#print(dbreq)
		urllib2.urlopen(dbreq)
    #print cpu_usage
   #print cpu_limit
   #print calculate(cpu_usage,cpu_limit)
   #print type(http_get())
   #for nname,pname in http_get():
#	print nname,pname
