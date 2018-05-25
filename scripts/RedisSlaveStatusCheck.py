#!/usr/bin/env python

import commands
import socket
import urllib2
import urllib
import json
import requests
import sys
import os

#'''get host redis port'''
def get_port():
	result=[]
	cmd1="""netstat -tlpn |grep redis-server|grep 0.0.0.0|awk '{print $4}'|awk -F ':' '{print $2}' """
        t=os.popen(cmd1)
        for port in t.readlines():
		r = os.path.basename(port.strip())
		result += [r]
	return result


#'''get local'''
def getmaster_status(port):
	cmd="""echo "info Replication"|/app/redis/bin/redis-cli -h localhost -p %s|grep ^slave[0-9]|awk -F ':' '{print $2}'|awk -F ',' '{print $1"="$2"="$3"="$4"="$5}'""" % port
	out= commands.getoutput(cmd)
	try:	
		for line in out.split("\n"):
			#print line
			data= (line.split("=")[1::2])   #list  data
			#insert_influxdb(data)
			slaveip=data[0]
        		port=data[1]
      	 		status=data[2]
        		offset=data[3]
        		lag=data[4].replace('\r','')
			insert_influxdb(slaveip,port,status,offset,lag)
	except IndexError:
			return 0
			#insert_influxdb(0,port,"online",0,0)

def insert_influxdb(slaveip,port,status,offset,lag):
	master=socket.gethostbyname(socket.gethostname())
	if status == "online":
		count=1
	else:
		count=6
	dbreqdata = "redislag,"  "master="+str(master)+  ",slaveip=" +str(slaveip)+ ",port="+str(port)+",status="+str(status)+",offset="+str(offset)+" count="+str(count)+",lag=" +str(lag) 
	dbrequrl = 'http://10.53.3.20:8086/write?db=redis_lag'
	#print(dbreqdata)
	dbreq= urllib2.Request(url = dbrequrl,data =dbreqdata)
	#print(dbreq)
	urllib2.urlopen(dbreq)
	
if __name__ == "__main__":		 
	#getslave_status()
	port=get_port()
	for p in port:
		#print p
		getmaster_status(p)
