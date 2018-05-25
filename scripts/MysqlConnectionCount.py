#!/bin/python
import MySQLdb
from influxdb import InfluxDBClient
import json
import paramiko as pmk

"""connect source_mysql get login info"""
def con_mysql_info():
        db = MySQLdb.connect(host="10.53.3.24",user="pluops",passwd="db@plu",db="LongzhuCC",port=3306,charset="utf8")
        cursor = db.cursor()
        data = cursor.execute("SELECT IP,Port,userid,Passwd FROM all_config;")
        info = cursor.fetchmany(data)
        return  info

"""con influx and insert data for grafana"""
def con_influx_info(Host,Ip,Port,Counts):
        client = InfluxDBClient('10.53.6.15', 8086, '', '', 'mysql_clientlist')
        json_body = [{"measurement": "mysql_clientlist","tags": {"server": str(Host), "host": str(Ip), "port": str(Port)}, "fields": {"server": str(Host), "host": str(Ip), "port": str(Port), "count": int(Counts)}}]
        client.write_points(json_body,retention_policy="autogen")

"""through lgoin info get ip and counts"""
def con_ssh_info(host,port,uid,passwd):
    ssh_client = pmk.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(pmk.AutoAddPolicy())
    cmd='''echo "show processlist"|/app/pluops/mysql/bin/mysql  --user="%s" --password="%s" -P%s|awk -F ' ' '{print $3}'|awk -F':' '{print $1}'|sort -rn|uniq -c'''%(uid,passwd,port)
    try:
        ssh_client.connect(host,username='root', port='58422', timeout=2)
        stdin,stdout,stderr=ssh_client.exec_command(cmd)
        result = stdout.read()
        return result
    except BaseException as e:
        print 'failed to connect to host: %r: %r' % (host, e)
        return 0
    else:
        return 0

def main():
        for host1,port1,uid1,passwd1 in con_mysql_info():
                #print host1
                data=con_ssh_info(host1,port1,uid1,passwd1)
                if data != 0:
                        for i in  data.split('\n'):
                                List= i.split(' ',8)
                                #print "LIST",List
                                if len(List) > 3:
                                        #print List[-2],List[-1]
                                        #print "host:%s,port:%s,ip:%s,coutnts:%s"%(host1,port1,List[-1],List[-2])
                                        con_influx_info(host1,List[-1],port1,List[-2])

if __name__ == "__main__":
        main()
                   