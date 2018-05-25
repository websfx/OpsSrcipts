#!/usr/bin/env python
#encoding:utf=8

import json
import time
import urllib
import urllib2
import pymongo
import datetime



#```connection mongo```
def get_db():
	client=pymongo.MongoClient('10.200.151.13',27017)
	db=client.collectproplog
	collection=db.ItemEventMonitorRecord
	#print collection
	return collection

#```get data from mongo```
def get_doc(coll):
	startdate = (datetime.datetime.now() - datetime.timedelta(minutes=300))
	enddate = datetime.datetime.now()
	results = coll.find({"ConsumTime":{"$gte":startdate,"lte":enddate}})
	#results = coll.find()
	return results


#```insert into influxdb```
def in_db(results):
	for res in results:
		cTime = long(time.mktime(res["ConsumTime"].timetuple()) * 1000.0 + res["ConsumTime"].microsecond / 1000.0) 
        	pTime = res["PostEventTimeSpan"]
        	fTime = time.mktime(res["FinalTime"].timetuple())
		fTime = long(time.mktime(res["FinalTime"].timetuple()) * 1000.0 + res["FinalTime"].microsecond / 1000.0)
        	aTime = res["AsyncEventListTimeSpan"]
        	isFinal = res["IsFinal"]
		dbreqdata =  "gifteventlog," +"ConsumTime=" + str(cTime) + ",PostTime=" + str(pTime) + ",asynctime=" + str(aTime) + ",finaltime=" +str(fTime) + " isfinal=" + str(isFinal)
        	dbrequrl = "http://10.153.6.15:8082/write?db=stream_id_num"
        	print(dbreqdata)
        	dbreq= urllib2.Request(url = dbrequrl,data =dbreqdata)
        	print(dbreq)
        	urllib2.urlopen(dbreq)
	
if __name__ == "__main__":
	coll=get_db()
	in_db(get_doc(coll))	
	
	
	
	
