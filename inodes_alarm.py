#!/usr/bin/python
# -*-encoding: utf8 -*-
"""
脚本调用加密后的静态、动态token，调用应用号接口，推送消息
"""
import requests
import json
import configparser
# import  ConfigParser as configparser
import re
import logging.handlers
import commands


# 设置日志分割,保留10份
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.handlers.TimedRotatingFileHandler("inode_alarm.log", when='s', interval=1, backupCount=3)
fh.suffix = "%Y-%m-%d_%H-%M-%S.log"
fh.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.log$"
fh.extMatch = re.compile(fh.extMatch)
fh.setFormatter(formatter)
logger.addHandler(fh)

# 配置配置文件
cf = configparser.ConfigParser()
cf.read("inode_alarm.ini")

# 调应用号发送消息
def push_starling(content, information):

    url = "接口"

    payload = {
        # body里面的
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': get_token("static_token.txt"),
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    # 将 Python 对象编码成 JSON 字符串,否则报错
    # print(response.text)

# 获取token
def get_token(file_name):
    static_token = cf.get("nas", "encrypted_token")
    # with open('./%s' % file_name, mode='r') as file_handle:
    #     static_token = file_handle.read()
    url = "接口"
    payload = {
        # body里面的
        }
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)["result"]

# 获取 nas 的值
def get_inodes():
    # rst = commands.getoutput("df -i |grep nas |awk '{print $3}'")
    # 在python3.0以上已经没有commands模块了，使用subprocess代替commands
    inodes = 3
    # inodes = os.system("df -i |grep nas |awk '{print $3}'") 这个无法获取到inodes ,赋值会为0
    inodes = commands.getoutput("df -i |grep nas |awk '{print $3}'")
    return inodes

# 设置告警逻辑，配置告警值，避免重复告警
def set_alarm():
    if int(cf.get("nas", "alarm_status")) == 0:
        if int(get_inodes()) >= 10:
            push_starling("The [inodes] value of the [eks] NAS application you are interested in is:", get_inodes())
            cf.set("nas", "alarm_status", "1")
            with open("inode_alarm.ini", "w+") as f:
                cf.write(f)
            logger.debug("Message pushed to application number successfully")
        else:
            logger.info("Low inodes usage")
            cf.set("nas", "alarm_status", "0")
            with open("inode_alarm.ini", "w+") as f:
                cf.write(f)
    elif int(cf.get("nas", "alarm_status")) == 1:
        logger.info("The system has given an alarm")
        if int(get_inodes()) < 10:
            cf.set("nas", "alarm_status", "0")
            with open("inode_alarm.ini", "w+") as f:
                cf.write(f)
            if int(cf.get("nas", "alarm_status")) == 0:
                logger.info("Alarm recovered")
                push_starling("Alarm recovered, inodes value: ", get_inodes())

if __name__ == '__main__':
    try:
        set_alarm()
    except Exception as e:
        logger.exception(e)




