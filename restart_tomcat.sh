#!/bin/bash
#Desc : restart tomcat
#Time : 2018-01-02

cd /usr/local/tomcat/logs
filename=`ls -l *.gz | sed -n '1p'| awk '{print $NF}'`
#md5=`md5sum $filename | cut -d ' ' -f 1`
#echo  $md5
scp -P 26261 $filename root@10.26.1.11:/usr/local/vrlog
sleep 20
rm -rf $filename
