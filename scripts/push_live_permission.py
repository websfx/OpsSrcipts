#!/app/pluops/python/bin/python2.7
# -*- coding: UTF-8 -*-
import time
import urllib2
import urllib
import json
import sys
import MySQLdb
#from influxdb import InfluxDBClient
import json

db = MySQLdb.connect(host="10.53.4.14",user="lz_read",passwd="909e8d463991b442e2b3816e712ad8e5",db="Report",port=3306,charset="utf8")
cursor = db.cursor()
data = cursor.execute("select * from (select StreamId,count(*) nub   from Report.StreamAuthLog where OpType=2 and Result=0 and CreateTime > date_sub(now(), interval 10 minute)  GROUP BY StreamId) b where b.nub >=0   order by b.nub desc;")
info = cursor.fetchmany(data)
#print info
#print(info)
for stream,nub in info:
        #print(stream,nub)
        dbreqdata =  "stream_id_num," + "streamid=" + str(stream) + " count=" + str(nub)
        #print(dbreqdata)
        dbrequrl = "http://10.53.6.15:8086/write?db=stream_id_num"
	user_agent = 'Mozilla/5.0'
	headers = { 'User-Agent' : user_agent }
	#print(dbreqdata)
        #dbreq= urllib2.Request(url = dbrequrl,data =dbreqdata,headers=headers)
        dbreq= urllib2.Request(url = dbrequrl,data =dbreqdata)
        #print(dbreq)
        urllib2.urlopen(dbreq)

