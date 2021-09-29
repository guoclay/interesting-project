import socket
import fcntl
import struct
import smtplib
import time
import threading as thd

from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
# 用于构建邮件头

# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '1620285208@qq.com'  
password = 'ycrrqxkzlbbabggc'
 
# 收信方邮箱
to_addr_list = ['xy_guoclay@163.com','2937046279@qq.com','873746953@qq.com','1137416958@qq.com','1084083934@qq.com']
 
# 发信服务器
smtp_server = 'smtp.qq.com'
# 当前ip地址
now_ip='171.88.141.153'
#选择查看的网卡
eth=b'pppoe-wan'
#统计开始时间
begin_time=0.0
#时间标志位
flag_time=1

#连接smtp函数
def connect_smtp():
    try:
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server,465)
        server.login(from_addr, password)
        return server
    except Exception:
        print("connect smtp server failed!")

#发送邮件函数
def send_msg(to_addr_list,subject,content):
    now_time=time.strftime('%Y-%m-%d %H:%M:%S')
    msg = MIMEText(str(content),'plain','utf-8')
    msg['From'] = Header("Nas_gxy")
    
    msg['Subject'] = Header(subject)
    try:
        server=connect_smtp()
        for to_addr in to_addr_list:
            msg['To'] = Header(to_addr)
            server.sendmail(from_addr,to_addr,msg.as_string())
        server.quit()
    except:
        print("[%s]Error:Email send Faild"%(now_time))

#获取网卡ip地址函数
def get_ip_address(ifname):
        s =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])

#检查当前网卡ip是否有变化
def check_ip():
    global flag_time,begin_time,now_ip,eth
    thd.Timer(10,check_ip).start()
    new_ip=get_ip_address(eth)
    if new_ip!=now_ip:
        end_time=time.time()
        spend_time=(end_time-begin_time)//3600
        now_ip=new_ip
        send_msg(to_addr_list,"IP is changed",("经过%d小时后IP发生改变，现在的IP地址为%s")%(spend_time,new_ip))
        flag_time=1
    elif flag_time==1:
        begin_time=time.time()
        flag_time=0
    else:
        pass


if __name__=="__main__":
    
    check_ip()

