#!/usr/bin/env python
#coding: utf-8
import pexpect
import sys
import os
def putPublicKey(publicKey,user,servers,port):
    for server in servers:
        child = pexpect.spawn("/usr/bin/ssh-copy-id -p %s -i %s %s@%s" %(port,publicKey,user,server))
        index = child.expect(["yes/no","password","exist",pexpect.exceptions.EOF, pexpect.TIMEOUT])
        if index != 0 and index != 1:
            print ("未向%s上传公钥匙"%(server))
            child.close(force=True)
        else:
            print ("开始向%s上传公钥"%(server))
            child.sendline("yes")
            child.expect("password")
            child.sendline("123456")
            child.expect("added")
            print ("已向%s上传公钥"%(server))
            print 
    print ("任务执行完成")
if __name__ == '__main__':
    user = "root"     #指定远程主机用户名
    servers = ["192.168.200.150","192.168.200.131","192.168.200.151","192.168.200.157","192.168.200.164"]  #指定远程主机列表
    port = "22"  #指定远程主机的ssh端口
    publicKey = "/root/.ssh/id_rsa.pub"  #指定要上传的公钥
     #如果指定的公钥不存在，自动创建
    if not os.path.exists(publicKey):
         direname = os.path.dirname(publicKey)
         print("指定公钥不存在，将自动生成私钥和公钥，路径为：%s"%(direname))
         child = pexpect.spawn("ssh-keygen -t rsa -P '' -f %s/id_rsa" %(direname))
         child.expect(pexpect.exceptions.EOF)
         child.close(force=True)
         print ("已生成私钥和公钥")
         print 
    putPublicKey(publicKey,user,servers,port)
