Batch create pub key 
===
批量创建auth key

host.list
文件格式为：

ip:port:user:passwd


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

