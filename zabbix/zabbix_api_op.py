#!/usr/bin/python
#coding:utf-8

import json
import urllib2
from urllib2 import URLError
import sys, argparse

class zabbix_api:
    def __init__(self):
        self.url = 'http://zabbix_ip/api_jsonrpc.php' #zabbix url
        self.header = {"Content-Type": "application/json"}

    def user_login(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "username", #username
                "password": "password" #password
            },
            "id": 0
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "\033[041m 用户认证失败，请检查 !\033[0m", e.code
        else:
            response = json.loads(result.read())
            result.close()
            #print response['result']
            self.authID = response['result']
            return self.authID

    def host_get(self, hostName=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {"host": hostName}
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            #print response
            result.close()
            #print "主机数量: \033[31m%s\033[0m"%(len(response['result']))
            #print response['result']
            for host in response['result']:
                status = {"0": "OK", "1": "Disabled"}
                available = {"0": "Unknown", "1": "available", "2": "Unavailable"}
                #print host
                if len(hostName) == 0:
                    print "HostID : %s\tHostName : %s\tStatus : \033[32m%s\033[0m \tAvailable : \033[31m%s\033[0m" % (host['hostid'], host['name'], status[host['status']], available[host['available']])
                else:
                    print "HostID : %s\tHostName : %s\tStatus : \033[32m%s\033[0m \tAvailable : \033[31m%s\033[0m" % (host['hostid'], host['name'], status[host['status']], available[host['available']])
                return host['hostid']

    def hostgroup_get(self, hostgroupName=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": hostgroupName
                }
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            #print result.read()
            response = json.loads(result.read())
            result.close()
            #print response['result']
            for group in response['result']:
                if len(hostgroupName) == 0:
                    print "hostgroup : \033[31m%s\033[0m\tgroupid : %s" % (group['name'], group['groupid'])
                else:
                    print "hostgroup : \033[31m%s\033[0m\tgroupid : %s" % (group['name'], group['groupid'])
                    self.hostgroupID = group['groupid']
                    return group['groupid']

    def template_get(self, templateName=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": templateName
                }
            },
            "auth": self.user_login(),
            "id": 1
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
        #print response
        for template in response['result']:
            if len(templateName) == 0:
                print "template : \033[31m%s\033[0m\t  id : %s" % (template['name'], template['templateid'])
            else:
                self.templateID = response['result'][0]['templateid']
                print "Template Name :  \033[31m%s\033[0m " %templateName
                return response['result'][0]['templateid']

    def hostgroup_create(self, hostgroupName):

        """
        create host group from hostgroupName args
        :Yan hostgroupName: host group name
        """
        if self.hostgroup_get(hostgroupName):
            print "hostgroup  \033[42m%s\033[0m is exist !" %hostgroupName
            sys.exit(1)

        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": hostgroupName
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            #print response['result']
            print "添加主机组: \033[042m%s\033[0m  hostgroupID : %s" %(hostgroupName, response['result']['groupids'])

    def host_create(self, hostip, hostgroupName, templateName):
        """
        create host form args
        :Yan hostip: host ip
        :Yan hostgroupName: host_group list name
        :Yan templateName: host_template list name
        """
        if self.host_get(hostip):
            print "\033[041m该主机已经添加!\033[0m"
            sys.exit(1)
        group_list = []
        template_list = []
        for i in hostgroupName.split(','):
            var = dict()
            var['groupid'] = self.hostgroup_get(i)
            group_list.append(var)
        for i in templateName.split(','):
            var = dict()
            var['templateid'] = self.template_get(i)
            template_list.append(var)
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": hostip,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": hostip,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": group_list,
                "templates": template_list,
            },
            "auth": self.user_login(),
            "id": 1
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print "添加主机 : \033[42m %s \033[0m \t id : \033[31m %s \033[0m" % (hostip, response['result']['hostids'])

    def host_disable(self, hostip):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": self.host_get(hostip),
                "status": 1
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print '----主机现在状态------------'
            print self.host_get(hostip)

    def host_delete(self, hostid):
        hostid_list = []
        #print type(hostid)
        for i in hostid.split(','):
            var = dict()
            var['hostid'] = self.host_get(i)
            hostid_list.append(var)
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": hostid_list,
            "auth": self.user_login(),
            "id": 1
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except Exception, e:
            print e
        else:
            response = json.loads(result.read())
            result.close()
            for id in response['result']['hostids']:
                print "ID为\033[041m%s\033[0m的主机已经删除 !" %str(id)
            return 0

if __name__ == "__main__":
    zabbix = zabbix_api()
    #print zabbix.user_login()
    #print zabbix.host_get("10.0.0.205")
    #print zabbix.hostgroup_get("")
    #print zabbix.template_get("")
    #print zabbix.hostgroup_create("test3")
    #print zabbix.host_create('1.1.1.1', 'Zabbix servers,网上课堂', 'template')
    #print zabbix.host_create('2.2.2.2', 'Zabbix servers,网上课堂', 'template')
    #print zabbix.host_disable('1.1.1.1')
    #print zabbix.host_delete('1.1.1.1,2.2.2.2')
    parser = argparse.ArgumentParser(description='zabbix  api', usage='%(prog)s [options]')
    parser.add_argument('-H', '--host', nargs='?', dest='listhost',  help='查询主机')
    parser.add_argument('-G', '--group', nargs='?', dest='listgroup', help='查询主机组')
    parser.add_argument('-T', '--template', nargs='?', dest='listtemp', help='查询模板信息')
    parser.add_argument('-A', '--add-group', nargs=1, dest='addgroup', help='添加主机组')
    parser.add_argument('-C', '--add-host', dest='addhost', nargs=3, metavar=('192.168.2.1', 'test01,test02', 'Template01,Template02'), help='添加主机,多个主机组或模板使用分号')
    parser.add_argument('-d', '--disable', dest='disablehost', nargs=1, metavar=('192.168.2.1'), help='禁用主机')
    parser.add_argument('-D', '--delete', dest='deletehost', nargs='+', metavar=('192.168.2.1'), help='删除主机,多个主机之间用分号')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        print parser.print_help()
    else:
        args = parser.parse_args()
        #print args

        if args.listhost:
            zabbix.host_get(args.listhost)

        if args.listgroup:
            zabbix.hostgroup_get(args.listgroup)

        if args.listtemp:
                zabbix.template_get(args.listtemp)

        if args.addgroup:
            zabbix.hostgroup_create(args.addgroup[0])
        if args.addhost:
            zabbix.host_create(args.addhost[0], args.addhost[1], args.addhost[2])
        if args.disablehost:
            zabbix.host_disable(args.disablehost)
        if args.deletehost:
            zabbix.host_delete(args.deletehost[0])
