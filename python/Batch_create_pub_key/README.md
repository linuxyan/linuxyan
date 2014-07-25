Batch create pub key 
===

require
===
python version > 2.5
model:
paramiko

===
easy_install paramiko  or  pip install paramiko


批量创建auth key

host.list
文件格式为：

ip:port:user:passwd

ps:默认id_rsa.pub创建在~/.ssh/id_rsa.pub
修改Batch_key.py
	home_dir = '/home/yan'
	修改为本地家目录

把host.list和Batch_key.py放在同一级目录下。执行

python Batch_key.py

如下：

	yan@yan:~$ python Batch_key.py 
	create Host:192.168.18.46 .ssh dir......
	upload id_rsa.pub to Host:192.168.18.46......
	host:root@192.168.18.46 auth success!

	create Host:192.168.18.13 .ssh dir......
	upload id_rsa.pub to Host:192.168.18.13......
	host:root@192.168.18.13 auth success!

