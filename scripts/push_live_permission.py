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


ID=""
def post_json(ID,Roomid,DET,Time):
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
                        "content":"推流异常流id:%s\n房间ID:%s\n原因:%s\n创建时间:%s" %(ID,Roomid,DET,Time)
                },
            }
        #print a
        resp = requests.post("http://192.168.10.176:9095",json=a)
        print(resp.content.decode("utf8"))

def get_use_rate():
        client = InfluxDBClient('10.53.6.15', 8086 ,'','','stream_id_num')
        #print client.get_list_database()
        #sql = '''SELECT last(value) FROM "%s" WHERE type = pod_container AND namespace_name = %s AND pod_name = %s''' %(measurement,namespace_name,pod_name)
        sql = '''SELECT last(count),streamid FROM stream_id_num '''
        result = client.query(sql)
        data = list(result.get_points())
        List = data[0]
        return List['streamid']

db = MySQLdb.connect(host="10.53.4.14",user="lz_read",passwd="909e8d463991b442e2b3816e712ad8e5",db="Report",port=3306,charset="utf8")
cursor = db.cursor()
data = cursor.execute("select * from (select StreamId,count(*) nub   from Report.StreamAuthLog where OpType=2 and Result=0 and CreateTime > date_sub(now(), interval 10 minute)  GROUP BY StreamId) b where b.nub >=0   order by b.nub desc;")
info = cursor.fetchmany(data)
for stream,nub in info:
        #print(stream,nub)
        dbreqdata =  "stream_id_num," + "streamid=" + str(stream) + " count=" + str(nub)
        #if stream != get_use_rate():
                #post_json(stream,roomid,det,Time)
        #print(dbreqdata)
        dbrequrl = "http://10.53.6.15:8086/write?db=stream_id_num"
	user_agent = 'Mozilla/5.0'
	headers = { 'User-Agent' : user_agent }
	#print(dbreqdata)
        #dbreq= urllib2.Request(url = dbrequrl,data =dbreqdata,headers=headers)
        dbreq= urllib2.Request(url = dbrequrl,data =dbreqdata)
        #print(dbreq)
        urllib2.urlopen(dbreq)

