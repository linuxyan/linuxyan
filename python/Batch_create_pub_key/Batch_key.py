#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sys
import paramiko

#注意，此处不能用～来代替家目录
home_dir = '/home/yan'
id_rsa_pub = '%s/.ssh/id_rsa.pub' %home_dir

if not  id_rsa_pub:
    print 'id_rsa.pub Does not exist!'
    sys.exit(0)

file_object = open('%s/.ssh/config' %home_dir ,'w')
file_object.write('StrictHostKeyChecking no\n')
file_object.write('UserKnownHostsFile /dev/null')
file_object.close()

def up_key(host,port,user,passwd):
    try:
        s = paramiko.SSHClient()
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	s.connect(host, port, user, passwd)

        t = paramiko.Transport((host, port))
        t.connect(username=user, password=passwd)
        sftp =paramiko.SFTPClient.from_transport(t)

        print 'create Host:%s .ssh dir......' %host
        stdin,stdout,stderr=s.exec_command('mkdir ~/.ssh/')
        print 'upload id_rsa.pub to Host:%s......' %host
        sftp.put(id_rsa_pub, "/tmp/temp_key")
        stdin,stdout,stderr=s.exec_command('cat /tmp/temp_key >> ~/.ssh/authorized_keys && rm -rf /tmp/temp_key')
        print 'host:%s@%s auth success!\n' %(user, host)
        s.close()
        t.close()
    except Exception, e:
        import traceback
        traceback.print_exc()
        try:
            s.close()
            t.close()
        except:
            pass

def run():
    for line in open('host.list'):
        line = line.strip('\n')
        host,port,user,passwd = line.split(':')
        up_key(host, int(port), user, passwd)

if __name__ == '__main__':
    run()
