#!/bin/pyithon
# -*- encoding:utf-8 -*-

import os
import datetime
import time
import sys
import MySQLdb
import socket

def insert_db(host,port,fsize,fexist,date):
        db = MySQLdb.connect(host="10.53.3.24",user="XX",passwd="xx",db="XX",port=3306,charset="utf8")
        cursor = db.cursor()
        sql = "insert into XX.dbbak_check values ('%s','%s','%s','%s','%s');" %(host,port,fsize,fexist,date)
        #print sql
        try:
                cursor.execute(sql)
                db.commit()
                #print "insert ok"
        except:
                db.rollback()
        db.close()

#get file
date = time.time()
def get_filesize(file):
        fsize = os.path.getsize(file)
        fsize = fsize/float(1024*1024)
        return round(fsize,2)

def whether_exist(file):
        fexist = os.path.exists(file)
        #print fexist
        return fexist

if __name__ == "__main__":
   #date = time.localtime()
   date = datetime.date.today()
   #print date
   date1 = datetime.datetime.now().strftime("%y%m%d")
   host = socket.gethostname()
   file = "" % date1
   #print file
   try:
        fsize = get_filesize(file)
        fexist = whether_exist(file)
        #print host,fsize,fexist,date
        insert_db(host,3306,fsize,fexist,date)
   except OSError,e:
        #print "0 \nfalse"
        insert_db(host,3306,0,'false',date)
