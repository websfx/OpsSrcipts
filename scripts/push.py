#!/bin/python
import time
import os
import sys
from multiprocessing import Pool
import functools
import paramiko as pmk


#path='/cygdrive/d/website/'
dict ={'AdminSite':'admin',
        'mb':'mb.tga.plu.cn',
        'livemb.plu.cn':'livemb.plu.cn',
        'comments.plu.cn':'comments.plu.cn',
        'PLU.Home.SearchApi':'searchapi.plu.cn',
        'livestream':'LiveStream',
        'websetting':'setting.longzhu.com',
        'webapiroom':'roomapicdn.plu.cn',
        'webapiuser':'userapi.plu.cn',
        'webapiuser-info':'userapi.plu.cn-7888',
        'webapiuser-ticket':'userapi.plu.cn-ticket',
        'webapirank':'rankapi.longzhu.com',
        '':''
        }

#rsync copy to hosts
def command(serverId,webSite,path='/cygdrive/d/website/'):
  skip_file = '--exclude="DfsrPrivate" --exclude="vc_for_nzs" --exclude="vc_for_jmb" --exclude="video-conference" --exclude="mobile-game-cast" --exclude="WebSite-PLU.Home.RoomUploadImage" --exclude="res.plures.net" --exclude="iis.bat" --exclude="redisSettings.release.config" --exclude="connectionStrings.release.config"'
  sync_cmd = "/usr/bin/rsync -ac -e ssh -p58422"+" "+path+webSite+" "+"Administrator@"+serverId+":/cygdrive/d/website/"+"  "+skip_file
  print sync_cmd
  #os.system(sync_cmd)
  print "%s rsync %s successful!!!" % (serverId,webSite)

#connection hosts and restart iis
def con_ssh(host,web,status, user='Administrator', port='58422'):  
    key=pmk.RSAKey.from_private_key_file(filename='C:\cygwin64\home\Aadministrator')
    ssh_client = pmk.SSHClient()  
    ssh_client.load_system_host_keys()  
    ssh_client.set_missing_host_key_policy(pmk.AutoAddPolicy())  
    try:  
        ssh_client.connect(host, username=user, port=port,key=key, timeout=2)  
        #ssh_client.exec_command('cd /cygdrive/c/Windows/System32/inetsrv;./appcmd.exe'+" "+str(status)+" "+"site"+" "+web)
	#ssh_client.exec_command('')
  	print "%s iis %s is %s" % (host,web,status)
    except BaseException , e:  
        print 'failed to connect to host: %r: %r' % (host, e)  
        return False  
    else:  
        return True
    ssh_client.close()
#start more pool in handler rsync
def run_pool(*args):
  pool = Pool(10)
  pool.map(functools.partial(command,args[0]),[args[1]])
  pool.close()
  pool.join()

#web_mini[] host[] 
#1.website_mini 2.build_type 3.website 4.hosts
if __name__ == "__main__":
 count = sys.argv
 print "count:",count[3]
 startTime = time.time()
 for h in count[3].split(','): 
	  if count[2] == "true":
   		  for w in count[1].split(','): 
			w1 = dict.get(w)
			if w1 == None:
					con_ssh(h,w,'stop')
			else:
					con_ssh(h,w1,'stop')
  		  pool = Pool(10)
  		  pool.map(functools.partial(command,h),count[1].split(','))
  		  pool.close()
		  pool.join()
		  for w in count[1].split(','):
                        w1 = dict.get(w)
                        if w1 == None:
                                        con_ssh(h,w,'start')
                        else:
                                        con_ssh(h,w1,'start')
 	  else:
		  print "else"
	 	  pool = Pool(10)
   		  pool.map(functools.partial(command,h),count[1].split(','))
       		  pool.close()
     	   	  pool.join()
 endTime = time.time()
 print "time :",endTime - startTime
