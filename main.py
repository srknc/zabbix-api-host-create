import requests
import json
import sys
from requests.auth import HTTPBasicAuth
import datetime
import time


if ( len(sys.argv) < 7 ):
        print '[hostname] [host_ip] [host_group_id] [zabbix_username] [zabbix_password] [http_auth_username] [http_auth_password] [templeate_id]'
        sys.exit(1)
else:
        hostname=sys.argv[1]
        host_ip=sys.argv[2]
        host_group_id=sys.argv[3]
        zabbix_username=sys.argv[4]
        zabbix_password=sys.argv[5]
        http_auth_username=sys.argv[6]
        http_auth_password=sys.argv[7]
        templeate_id=sys.argv[8]
        url=sys.argv[9]


headers = {'content-type': 'application/json'}
def get_aut_key():
        payload= {'jsonrpc': '2.0','method':'user.login','params':{'user':zabbix_username,'password':zabbix_password},'id':'1'}
        r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=HTTPBasicAuth(http_auth_username,http_auth_password))
        if  r.status_code != 200:
                print 'problem -key'
                print r.status_code
                print r.text
                sys.exit()
        else:
                result=r.json()
                auth_key=result['result']
                return auth_key


def create_host(auth_key):
        payload={
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": hostname,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": host_ip,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                    {
                        "groupid": host_group_id
                    }
                ],
                "templates": [
                    {
                        "templateid": templeate_id
                    }
                ],
            },
            "auth": auth_key,
            "id": 1
        }



        r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=HTTPBasicAuth(http_auth_username,http_auth_password))
        if  r.status_code != 200:
                print 'problem -request'
                sys.exit()
        else:
                try:
                        result=r.json()['result']
                        host_id=result['hostids'][0]
                        return host_id
                except:
                        result=r.json()['error']
                        print 'error'
                        print result
                        sys.exit()


def set_maintenance(auth_key, host_id):
        active_till=int(time.time()+600)

        payload={
            "jsonrpc": "2.0",
            "method": "maintenance.create",
            "params": {
                "name": 'new server initialization period_'+str(active_till),
                "hostids": [ host_id ],
                "active_till": active_till,
                "timeperiods": [
                    {
                        "timeperiod_type": 0,
                        "period": 1800
                    }
                ]
            },
            "auth": auth_key,
            "id": 1
        }



        r = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=HTTPBasicAuth(http_auth_username,http_auth_password))
        if  r.status_code != 200:
                print 'problem -request'
                sys.exit()
        else:
                try:
                        result=r.json()['result']
                        print result
                except:
                        result=r.json()['error']
                        print 'error'
                        print result
                        sys.exit()






auth_key=get_aut_key()
host_id=create_host(auth_key)
set_maintenance(auth_key,host_id)
