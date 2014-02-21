#!/bin/bash
rrd_path="/var/www/html/rrd/eth1.rrd"
font_path="/var/www/html/font/yahei.ttf"
image_path="/var/www/html"

rrd_data='xx.xx.xx.xx'
while [ 1 ]         
do
eth0_in=`snmpwalk -v 2c -c aodiansvr $rrd_data ifInOctets.2 | awk '{print $4}'`
eth0_out=`snmpwalk -v 2c -c aodiansvr $rrd_data ifOutOctets.2 | awk '{print $4}'`
now=`date +%s`
echo "rrdtool update $rrd_path $now:$eth0_in:$eth0_out" >> eth1.cmd  
rrdtool update $rrd_path $now:$eth0_in:$eth0_out


rrdtool graph $image_path/eth1.png -w 700 -h 200 \
-n TITLE:11:"$font_path" \
-n UNIT:8:"$font_path" \
-n LEGEND:8:"$font_path" \
-c SHADEA#DDDDDD \
-c SHADEB#808080 \
-c FRAME#006600 \
-c FONT#006699 \
-c ARROW#FF0000 \
-c AXIS#000000 \
-c BACK#FFFFFF \
-Y -X 6 \
-t "Pst Server(203.195.186.17) Trffic eth0" -v "bits per second 流量" \
--start -1d --end now \
--x-grid MINUTE:12:HOUR:1:HOUR:1:0:'%H' \
DEF:value1=$rrd_path:eth0_in:AVERAGE \
DEF:value2=$rrd_path:eth0_out:AVERAGE \
CDEF:eth0_in=value1,8,* \
CDEF:eth0_out=value2,8,* \
COMMENT:" \n" \
AREA:eth0_in#00ff00:In \
GPRINT:eth0_in:LAST:" Current\:%8.2lf %s"  \
GPRINT:eth0_in:AVERAGE:"Average\:%8.2lf %s"  \
GPRINT:eth0_in:MAX:"MAX\:%8.2lf %s"  \
GPRINT:eth0_in:MIN:"MIN\:%8.2lf %s"  \
COMMENT:" \n" \
LINE2:eth0_out#4433ff:Out \
GPRINT:eth0_out:LAST:"Current\:%8.2lf %s"  \
GPRINT:eth0_out:AVERAGE:"Average\:%8.2lf %s"  \
GPRINT:eth0_out:MAX:"MAX\:%8.2lf %s"  \
GPRINT:eth0_out:MIN:"Min\:%8.2lf %s"  \
COMMENT:" \n" \
COMMENT:"─────────────────────────────────────────────\n" \
COMMENT:"\t\t\t\t\t\t\t\t\t\t\t\t\t\t  Last time\:$(date '+%Y-%m-%d %H\:%M')\n" -Y \
COMMENT:"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Aodian Soft Ops\n"

date
sleep 300
done