#!/usr/bin/env python
#coding=utf8

import MySQLdb
import urllib
import urllib2

from bs4 import BeautifulSoup
from web_login_weibo import login
pro_attrs = ['昵称','性别','大学','高中','初中','小学','中专技校','公司','生日','所在地']

   
def web_prase(uid,html,cur):

        insert_sql = "insert ignore into user_profile values(%s,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)"
        param = (uid)
        n = cur.execute(insert_sql,param)

        bsoup = BeautifulSoup(html,fromEncoding="gb18030")
        data = bsoup.findAll("script")
        for i in range(0,len(data)):
            if data[i].text.find("profile_pinfo") > 0 :
                profile_info = data[i].text
            
                #profile = profile_info.encode("gbk","ignore")
                profile = profile_info.encode("utf8","ignore")
                profile = profile.replace("\\n","")
                profile = profile.replace("\\r","")
                profile = profile.replace("\\t","")
                profile = profile.replace("\\","")
                tag = profile.find("\"html\":\"")
                profile = profile[tag+8:-3]

                #print profile
        
                profile_soup = BeautifulSoup(profile,fromEncoding="gb18030")
                info = profile_soup.findAll("div","pf_item clearfix")

                in_attr = 0
        
                
        
                std = 0
                for num in range(0,len(info)):
                    m=info[num].contents
                    mylist= []
                    for i in range(0,len(m)):
                            if len( dict(m[i].attrs)['class'] ) >=2:
                                    mylist.append(i)

                    for i in range(0,len(m)):
                            if i in mylist:
                                attr =  m[i].text.encode("utf8","ignore")
                                if( attr in pro_attrs):
                                    std = 1
                                    print m[i].text
                                    sql = "update user_profile set "+attr+" = %s where uid = %s"
                            
                                    str = ""
                            
                            else:
                                if std == 1:
                                    str= str+m[i].text.encode("utf8","ignore")
                                    if i+1 in mylist:
                                        param = (str,uid)
                                        n = cur.execute(sql,param)
                                        #print str
                    if std == 1:
                        param = (str,uid)
                        n = cur.execute(sql,param)
                        #print str
                    std = 0
        




if __name__ == '__main__':

    username = 'your_username'
    pwd = 'your_password'
    cookie_file = 'weibo_login_cookies.dat'
    
    if login(username, pwd, cookie_file):
        print 'Login WEIBO succeeded'
        try:
            conn = MySQLdb.Connect(host='localhost', user='root', passwd='bupttqy10', db='weibo',charset='utf8')
            cur=conn.cursor()
            c_sql = "select count(*) from user"
            total_user = cur.execute(c_sql)
            s_sql = "select uid from user"
            b = cur.execute(s_sql)
            uids = cur.fetchall()
            while count <= total_user:   
                uid = uids[count][0].encode("utf8","ignore")
                print uid,count
                url = 'http://weibo.com/p/100505'+uid+'/info?from=page_100505&mod=TAB#place'
                try:
                        data = urllib2.urlopen(url,timeout=3)
                        html = data.read()
                        web_prase(uid,html,cur)
                        conn.commit()
                        count = count + 1
                except Exception,e:
                        print str(e)
                
                
        
        finally:
            cur.close()
            conn.close()
        

    else:
        print 'Login WEIBO failed'

    
