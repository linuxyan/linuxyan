#!/usr/bin/env python
import sys
import paramiko

id_rsa_pub = '/home/yan/.ssh/id_rsa.pub'

if not  id_rsa_pub:
    print 'id_rsa.pub Does not exist!'
    sys.exit(0)

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


for line in open('host.list'):
    line = line.strip('\n')
    host = line.split(':')[0]
    port = line.split(':')[1]
    user = line.split(':')[2]
    passwd = line.split(':')[3]
    up_key(host, int(port), user, passwd)

