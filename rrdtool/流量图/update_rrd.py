#!/usr/bin/python
#coding=utf-8
import rrdtool
from rrdtool import update as rrd_update
import os, netsnmp, time

Host='xx.xx.xx.xx'
eth_in_oid = netsnmp.Varbind('ifInOctets.2')
eth_out_oid = netsnmp.Varbind('ifOutOctets.2')
image_path = '/var/www/html/image/'+Host+'/'
rrd_path = '/var/www/html/rrd/'+Host+'_trffic.rrd'
ISOTIMEFORMAT='%Y-%m-%d %X'
datetime = time.strftime(ISOTIMEFORMAT, time.localtime())

if not os.path.isdir(image_path):
    os.makedirs(image_path)

'''
create rrd file
'''
def create_rrd():
    ret = rrdtool.create(rrd_path,"--step","300","--start","0",
    "DS:eth_in:COUNTER:600:0:U",
    "DS:eth_out:COUNTER:600:0:U",
    "RRA:AVERAGE:0.5:1:600",
    "RRA:AVERAGE:0.5:6:700",
    "RRA:AVERAGE:0.5:24:775",
    "RRA:AVERAGE:0.5:288:797",
    "RRA:MAX:0.5:1:600",
    "RRA:MAX:0.5:6:700",
    "RRA:MAX:0.5:24:775",
    "RRA:MAX:0.5:444:797",
    "RRA:MIN:0.5:1:600",
    "RRA:MIN:0.5:6:700",
    "RRA:MIN:0.5:24:775",
    "RRA:MIN:0.5:444:797")

    if not ret:
        print rrdtool.error()



'''
update rrd data
'''
def update_rrd():
    eth_in_trffic = netsnmp.snmpget(eth_in_oid, Version=2, DestHost=Host, Community='aodiansvr')
    eth_out_trffic = netsnmp.snmpget(eth_out_oid, Version=2, DestHost=Host, Community='aodiansvr')
    ret = rrd_update(rrd_path,'N:%s:%s' %(eth_in_trffic[0], eth_out_trffic[0]))
    print "update %s  N:%s:%s" %(rrd_path,eth_in_trffic[0], eth_out_trffic[0])


'''
update image data
'''
date = time.strftime('%Y-%m-%d %H:%M:%S')
def update_png():
        image_name = image_path+Host+'_trffic'+'.png'
        print image_name
        ret = rrdtool.graph(image_name, '-w 700', '-h 200',
                      '-t Server(%s) 流量' %(Host),
                      '--color', 'BACK#FFFFFF',
                      '--color', 'SHADEA#DDDDDD',
                      '--color', 'SHADEB#808080',
                      '--color', 'FRAME#006600',
                      '--color', 'FONT#006699',
                      '--color', 'ARROW#FF0000',
                      '--color', 'AXIS#000000',
                      '-v 流量 Bytes/s',
                      '-s -1d',
                      '-e now',
                      '--x-grid','MINUTE:12:HOUR:1:HOUR:1:0:%H',
                      'DEF:value1=%s:eth_in:AVERAGE' %(rrd_path),
                      'DEF:value2=%s:eth_out:AVERAGE' %(rrd_path),
                      'CDEF:eth_in=value1,8,*',
                      'CDEF:eth_out=value2,8,*',
                      'COMMENT: \\n',
                      'AREA:eth_in#00ff00:流入',
                      'GPRINT:eth_in:LAST:Current\:%8.2lf %s',
                      'GPRINT:eth_in:AVERAGE:Average\:%8.2lf %s',
                      'GPRINT:eth_in:MAX:MAX\:%8.2lf %s',
                      'GPRINT:eth_in:MIN:MIN\:%8.2lf %s',
                      'COMMENT: \\n',
                      'LINE2:eth_out#4433ff:流出',
                      'GPRINT:eth_out:LAST:Current\:%8.2lf %s',
                      'GPRINT:eth_out:AVERAGE:Average\:%8.2lf %s',
                      'GPRINT:eth_out:MAX:MAX\:%8.2lf %s',
                      'GPRINT:eth_out:MIN:Min\:%8.2lf %s',
                      'COMMENT: \\n',
                      'COMMENT: \\n',
                      'COMMENT:─────────────────────────────────────────────\n',
                      'COMMENT: \\n',
                      "COMMENT:XXX运维部开发与维护\t\t\t最后更新 \:%s\n"  %(time.strftime("%Y-%m-%d %H\:%M\:%S", time.localtime())))
#create_rrd()
while True:
    update_rrd()
    update_png()
    time.sleep(300)
