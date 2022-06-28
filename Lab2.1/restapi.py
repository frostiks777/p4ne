import paramiko
import time
import ssl
import requests
import pprint
import urllib3

from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter

class Ssl1HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl.PROTOCOL_TLSv1)

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

s = requests.Session()
s.mount("https://10.31.70.210:55443", Ssl1HttpAdapter())

name = "restapi"
password = "j0sg1280-7@"
host_url = "https://10.31.70.210:55443"

r = s.post(host_url + '/api/v1/auth/token-services', auth=(name, password), verify=False)
#print(r.status_code)
token = r.json()['token-id']
#print(token)
header = {"content-type": "application/json", "X-Auth-Token": token}
r = s.get(host_url + '/api/v1/interfaces', headers=header, verify=False)
#pprint.pprint(r.json())

ddd = []

for i in range(len(r.json()['items'])):
    ddd.append(r.json()['items'][i]['if-name'])

#print(ddd)
outl = []
for i in ddd:
    #print('/api/v1/interfaces/'+i+'/statistics')
    st = s.get(host_url + '/api/v1/interfaces/'+i+'/statistics', headers=header, verify=False)
    #st.json()
    outl.append('if: '+ i +' | out-total-packets: '+str(st.json()['out-total-packets'])+' | in-total-packets: '+str(st.json()['in-total-packets']))
    #print('if: '+ i +' | out-total-packets: '+str(st.json()['out-total-packets'])+' | in-total-packets: '+str(st.json()['in-total-packets']))

for i in range(len(outl)):
    print(outl[i])
