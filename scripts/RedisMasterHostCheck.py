#! /usr/bin/env python
#-*- coding:utf-8 -*-
import socket
from influxdb import InfluxDBClient


def _get_host():
	localIP = socket.gethostbyname(socket.gethostname())
	#print localIP
def post_json(IP):
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
                        "content":"未添加redis监控脚本！\n未监控机器ip:%s" % IP
                },
            }
        #print a
        resp = requests.post("http://192.168.10.176:9095",json=a)
        print(resp.content.decode("utf8"))


def get_data(sql):
	dlist=[]
	client = InfluxDBClient('10.53.3.20', 8086, 'root', '', 'redis_lag')
	result = client.query(sql)
	cpu_points = list(result.get_points())
	for i in cpu_points:
        	#cpu = cpu_points[]
        	dlist.append(i['value'])
	return dlist
if __name__ == "__main__":
	_get_host()
	mcmd='SHOW TAG VALUES FROM "redislag" WITH KEY = "master"'
	get_data(mcmd)
	scmd='SHOW TAG VALUES FROM "redislag" WITH KEY = "slaveip"'
	get_data(scmd)
	for item in get_data(scmd):
		if item in get_data(mcmd):
			print "%s exist"%item
		else:
			print "%s error"%item
			post_json(item)