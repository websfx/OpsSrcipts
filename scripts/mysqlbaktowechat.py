#!/usr/bin/python  
# -*- coding: utf-8 -*-  
import smtplib
import requests
import sys
import sys,os
import datetime
import MySQLdb
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr

#获取备份失败主机信息
def insert_db():
        hostbak=[]
        Date = datetime.date.today()
        db = MySQLdb.connect(host="10.53.3.24",user="pluops",passwd="db@plu",db="mysql",port=3306,charset="utf8")
        cursor = db.cursor()
        sql  = "select host,fsize,fexist from LongzhuCC.dbbak_check where fsize <=1000 and date = '%s';" % Date
        try:
                data = cursor.execute(sql)
                info = cursor.fetchmany(data)
                db.commit()
        except:
                db.rollback()
        db.close()
        for host,fszie,fexist in info:
                hostbak.append(host)
        return hostbak

#推送报警至微信
def post_json(dbname):
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
                        "content":"数据库备份存在异常\n请检查备份策略\n备份失败数据库：%s\n" %dbname
                },
            }
        print a
        resp = requests.post("http://192.168.10.176:9095",json=a)
        print(resp.content.decode("utf8"))
# 格式化邮件地址  
def formatAddr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendMail(body):
    smtp_server = 'mail.pptv.com'
    from_mail = 'lz_sre@pptv.com'
    account = 'lz_sre'
    mail_pass = 'Longzhu#super^^.'
    to_mail = ['lzmonitor@pptv.com']
    # 构造一个MIMEMultipart对象代表邮件本身  
    msg = MIMEMultipart()
    # Header对中文进行转码  
    msg['From'] = formatAddr('管理员 <%s>' % from_mail).encode()
    msg['To'] = ','.join(to_mail)
    msg['Subject'] = Header(header, 'utf-8').encode()
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    try:
        s = smtplib.SMTP()
        s.connect(smtp_server, "587")
        s.login(account, mail_pass)
        s.sendmail(from_mail, to_mail, msg.as_string())  # as_string()把MIMEText对象变成str       
        s.quit()
    except smtplib.SMTPException as e:
        print "Error: %s" % e
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    dbname = insert_db()
    header = "数据库备份失败！请检查备份策略"
    if  dbname:
        body = "备份失败数据库:'%s'" % dbname
        print dbname
        post_json(dbname)
        sendMail(body)
