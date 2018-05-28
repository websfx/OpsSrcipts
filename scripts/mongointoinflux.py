#!/usr/bin/env python
#encoding:utf=8

import json
import time
import urllib
import urllib2
import pymongo
import datetime

def post_json(Id,isfinal,exceptionCount):
        default_encoding = 'utf-8'
        if sys.getdefaultencoding() != default_encoding:
                reload(sys)
                sys.setdefaultencoding(default_encoding)
        a = {
                "touser": "",
                "toparty": "2",
                "totag": "",
                "agentid": "1",
                "msgtype": "text",
                "text": {
                        "content":"道具时间链存在异常\n请查看对应的交易记录\nTradeId：%s\nIsFianl：%s\nexceptionCount:%s" %(Id,isfinal,exceptionCount)
                },
            }
        #print a
        resp = requests.post("http://192.168.10.176:9095",json=a)
        print(resp.content.decode("utf8"))


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
                TradeId=res["TradeId"]
                fTime = long(time.mktime(res["FinalTime"].timetuple()) * 1000.0 + res["FinalTime"].microsecond / 1000.0)
                aTime = res["AsyncEventListTimeSpan"]
                isFinal = res["IsFinal"]
                exceptionCount = res["ExceptionCount"]
                if isFinal:
                        isFinal='0'
                else:
                        isFinal='1'
                        #post_json(TradeId,isFinal,exceptionCount)
                        print TradeId,isFinal,exceptionCount
                        dbreqdata =  "gifteventlog" + ",TradeId="+ str(TradeId) +",ConsumTime=" + str(cTime) + ",PostTime=" + str(pTime) + ",asynctime=" + str(aTime) + ",finaltime=" +str(fTime) +",isfinal=" + str(isFinal) + " exceptionCount="+ str(exceptionCount)
                        dbrequrl = "http://10.53.6.15:8086/write?db=stream_id_num"
                        print dbreqdata
                        dbreq= urllib2.Request(url = dbrequrl,data=dbreqdata)
                        #print(dbreq)
                        urllib2.urlopen(dbreq)

	
if __name__ == "__main__":
	coll=get_db()
	in_db(get_doc(coll))	
	
	
	
	
