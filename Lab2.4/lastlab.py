import ssl
import requests
# from pprint import pprint
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
import collections
# import json
from flask import Flask, url_for
from flask import jsonify
import re
import glob
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    outstr = "<h1>Main menu</h1><hr><a href='" + url_for("configs") + "'><b>Configs</b></a>"
    outstr += "<br><a href='" + url_for("ciscostat") + "'><b>Cisco process memory used</b></a>"
    return outstr


@app.route('/configs')
def configs():
    return hostnamerawlist(url_for("configs"))


@app.route('/configs/<hostname>')
def page(hostname):
    return hostnameIPlist(hostname)


@app.route('/ciscostat')
def ciscostat():
    outstr = "<h1>Cisco process memory used:</h1><hr>"
    outstr += ciscostats()
    outstr += '<hr><a href="' + url_for("index") + '">Go to main menu</a>'
    return outstr


if __name__ == '__main__':


    def hostnamerawlist(path):
        ddhn = list()
        for nm in glob.glob("config_files\*.txt"):
            with open(nm) as f:
                for sttr in f:
                    if re.match("^(hostname) ([a-zA-Z0-9].+)", sttr):
                        m = re.match("^(hostname) ([a-zA-Z0-9].+)", sttr)
                        ddhn.append(m.group(2))
        outstr = "<h1>Configs:</h1><hr>"
        outstr += "<ul>"
        for i in ddhn:
            outstr += '<li><a href="'+ path +'/'+ i +'"><b>' + i + '</b></a></li>'
        outstr += '</ul>'
        outstr +='<hr><a href="' + url_for("index") + '">Go to main menu</a>'
        return outstr


    def hostnameIPlist(hostname):
        ls = '<h1>' + hostname + '</h1><hr>'
        ddhn = list()
        for nm in glob.glob("config_files\*.txt"):
            lip = list()
            hstnamel = list()
            with open(nm) as f:
                for sttr in f:
                    if re.match("^(hostname) ([a-zA-Z0-9].+)", sttr):
                        m = re.match("^(hostname) ([a-zA-Z0-9].+)", sttr)
                        hstname = m.group(2)
                        hstnamel.append(hstname)
                f.seek(0, 0)
                for sttrn in f:
                    if re.match(".*(ip address) ([0-9.]+) ([0-9.]+)", sttrn):
                        mm = re.match(".*(ip address) ([0-9.]+) ([0-9.]+)", sttrn)
                        lip.append(mm.group(2))
                ddhn.append(hstnamel + lip)

        for i in ddhn:
            if i[0] == hostname:
                for j in i:
                    if j != hostname:
                        ls +=j + '<br>'
        ls += '<hr><a href="' + url_for("configs") + '">Go to configs</a>'
        return ls


    def ciscostats():
        class Ssl1HttpAdapter(HTTPAdapter):
            def init_poolmanager(self, connections, maxsize, block=False):
                self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                               ssl_version=ssl.PROTOCOL_TLSv1)

        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

        s = requests.Session()
        s.mount("https://10.31.70.210:55443", Ssl1HttpAdapter())

        name = "restapi"
        password = "j0sg1280-7@"
        host_url = "https://10.31.70.210:55443"

        r = s.post(host_url + '/api/v1/auth/token-services', auth=(name, password), verify=False)
        # print(r.status_code)
        token = r.json()['token-id']
        # print(token)
        header = {"content-type": "application/json", "X-Auth-Token": token}
        r = s.get(host_url + '/api/v1/global/memory/processes', headers=header, verify=False)
        # pprint(r.json())

        data = r.json()['processes']
        dataDict = {}
        for i in data:
            dataDict[i['process-name']] = i['memory-used']
        dataDict = sorted(dataDict.items(), key=lambda x: x[1], reverse=True)

        outlin = '<table cellspacing="2" border="1" cellpadding="5"><tr><th colspan="2">Top 10 cisco memory greedy process!</th></tr>'
        for i in range(10):
            prntitem = dataDict[i]
            outlin += "<tr><td>" + prntitem[0] + "</td><td>" + str(prntitem[1]) + "</td></tr>"
        outlin += "</table>"
        return outlin

    app.run(port=80, debug=True)
