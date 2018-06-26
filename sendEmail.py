# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(),addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_email(info,text_msg,img_file,dayNow):
    [from_addr,password,to_addr,smtp_server]=info
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'南山天气Python自动查询程序 <%s>' % from_addr)
    msg['To'] = _format_addr(u'戴辉 <%s>' % to_addr)
    msg['Subject'] = Header(u'南山天气预报%s'%dayNow, 'utf-8').encode()
    msg.attach(MIMEText('%s' % text_msg, 'plain', 'utf-8'))
    with open(img_file,'rb')as f:
        mime = MIMEBase('weather_report', 'png', filename='%s weather_report.png'%dayNow)
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='%s weather_report.png'%dayNow)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
    server = smtplib.SMTP(smtp_server,  25)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print 'have send weather report to email: %s'%to_addr

if __name__=='__main__':
    info = ['daihui@mail.ustc.edu.cn', 'XXX', 'levitan@msn.cn', 'mail.ustc.edu.cn']
    msg_text='this is a text!\nYes,it\'s a test.'
    img_file='C:\Users\Levit\PycharmProjects\weather\\2017_11_29\\2017_11_29weatheReport.png'
    dayNow='2017_11_29'
    send_email(info, msg_text, img_file, dayNow)