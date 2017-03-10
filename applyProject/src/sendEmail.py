#!/usr/bin/env python3
#coding: utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import utils, encoders
import mimetypes, sys,smtplib
import os
Bin = os.path.abspath(os.path.dirname(__file__))
import getpass
import sqlite3

__author__='Yuan Zan'
__mail__= 'zanyuan@annoroad.com'



class SendMail:
    def __init__(self,smtp_server,from_name,from_addr,to_addr,cc_addr,user,passwd):
        self.mailserver=smtp_server
        self.from_addr=from_addr
        self.to_addr=to_addr
        self.cc_addr=cc_addr
        self.username=user
        self.password=passwd
        self.from_name=from_name
    def attachment(self,filename):
        fd=open(filename,'rb')
        filename=filename.split('/')
        mimetype,mimeencoding=mimetypes.guess_type(filename[-1])        
        if (mimeencoding is None) or (mimetype is None):
            mimetype='application/octet-stream'       
        maintype,subtype=mimetype.split('/')
        if maintype=='text':
            retval=MIMEText(fd.read(), _subtype=subtype, _charset='utf-8')          
        else:
            retval=MIMEBase(maintype,subtype)
            retval.set_payload(fd.read())
            encoders.encode_base64(retval)
            retval.add_header('Content-Disposition','attachment',filename=filename[-1])
            fd.close()
        return retval
    def msginfo(self,msg,subject,filename): 
        message=msg
        msg=MIMEMultipart()
        msg['To'] = self.to_addr
        msg['Cc'] = self.cc_addr
        msg['From'] = self.from_name + '<'+self.from_addr+'>'
        msg['Date'] = utils.formatdate(localtime=1)
        msg['Message-ID'] = utils.make_msgid()
        if subject:
            msg['Subject'] = subject
        if message:
            body=MIMEText(message,_subtype='plain')
            msg.attach(body)

        if filename:
            msg.attach(self.attachment(filename))
        return msg.as_string()
    def send(self,msg=None,subject=None,filename=None):
        try:
            s=smtplib.SMTP(self.mailserver)
            try:
                s.login(self.username,self.password)                
            except Exception as e:
                #print (e)
                print ("passworld is wrong")
                print ("Authentication failed:")
                sys.exit()
            to_addrs = self.to_addr + ';' + self.cc_addr
            s.sendmail(self.from_addr,to_addrs.split(';'),self.msginfo(msg,subject,filename))
        except Exception as e:
            print (e)
            print ("passworld is wrong")
            print ("*** Your message may not have been sent!")
            sys.exit()
        else:
            print ("Message successfully sent to %d recipient(s)" %len(self.to_addr))

def applyProjectEmail(name,mfrom,To,copy,subject,msg,pwd,files):
    try:
        test = SendMail('smtp.exmail.qq.com',name,mfrom,To,copy,mfrom,pwd)
        test.send(msg,subject,files)
        print ("Apply project email email send successfully!")
    except Exception as e:
        print (e)
        print ("passworld is wrong\n")
        sys.exit()
 
def main():
    conn = sqlite3.connect(os.path.join(Bin,'tmp/applyProject.db'))
    cur = conn.cursor()

    username = getpass.getuser()
    cursor = conn.execute("select name, groups, email from usrInfo where user = \'{0}\'".format(username))
    name, groups, email = cursor.fetchall()[0]
    cursor = conn.execute("select email from usrInfo where groups = \'{0}\'".format(groups))
    cc = ';'.join([i[0] for i in cursor.fetchall()])
    cur.close()
    conn.close()

    mfrom = email
    To = r'刘涛<taoliu@annoroad.com>'
    copy = cc
    subject = "【下单申请】{0}下单申请".format(groups)
    msg = '涛哥:\n\n\t\t附件是 {0}下单申请, 请下单!\n\n祝好!\n{1}'.format(groups,name)
    files = sys.argv[2]
    pwd = sys.argv[1]
#    while(1):
#        pwd = getpass.getpass(prompt='please input the password of {0}:'.format(email))
#        if pwd != '':break
#    print ("sending ...")
    applyProjectEmail(name,mfrom,To,copy,subject,msg,pwd,files)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ('\tUsage:\n\t\tpython3 {0} password file.xlsx'.format(sys.argv[0]))
        exit()
    main()
