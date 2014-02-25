#!/usr/bin/python
#coding=utf-8
import rrdtool
from rrdtool import update as rrd_update
import os, netsnmp, time

rrd_dir = '/var/www/html/rrd/'
img_dir = '/var/www/html/image/'

if not os.path.exists(rrd_dir):
    os.makedirs(rrd_dir)
if not os.path.exists(img_dir):
    os.makedirs(img_dir)


'''create rrd file'''
def create_rrd(rrd_path):
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
def update_rrd(Host, eth_in_oid, eth_out_oid, rrd_path, auth):
    eth_in_trffic = netsnmp.snmpget(eth_in_oid, Version=2, DestHost=Host, Community=auth)[0]
    eth_out_trffic = netsnmp.snmpget(eth_out_oid, Version=2, DestHost=Host, Community=auth)[0]
    ret = rrd_update(rrd_path, 'N:%s:%s' %(eth_in_trffic, eth_out_trffic))
    if not ret:
        print rrdtool.error()
    print "update %s  N:%s:%s" %(rrd_path, eth_in_trffic, eth_out_trffic)


'''
update image data
'''
def update_png(image_path, rrd_path, Host):
        ret = rrdtool.graph(image_path, '-w 700', '-h 200',
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
        if not ret:
            print rrdtool.error()



def main():
    for line in open('hosts.conf'):
        Host = line.split()[0]
        eth = int(line.split()[1][-1])+2
        if line.split()[2]:
            auth = line.split()[2]
        else:
            auth = 'public'

        image_path = img_dir+Host+'_trffic'+'.png'
        rrd_path = rrd_dir+Host+'_trffic.rrd'
        if not os.path.exists(rrd_path):
            create_rrd(rrd_path)

        eth_in_oid = netsnmp.Varbind('ifInOctets.%s' %(eth))
        eth_out_oid = netsnmp.Varbind('ifOutOctets.%s' %(eth))
        update_rrd(Host, eth_in_oid, eth_out_oid, rrd_path, auth)
        update_png(image_path, rrd_path, Host)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(300)
