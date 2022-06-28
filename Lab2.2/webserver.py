from flask import Flask
from flask import jsonify
import re
import ipaddress
import glob


def strtoip(sttr):
    if re.match("^(ip address) ([0-9.]+) ([0-9.]+)", sttr):
        m = re.match("^(ip address) ([0-9.]+) ([0-9.]+)", sttr)
        ip = ipaddress.IPv4Interface(m.group(2))
    else:
        ip = None
    return ip


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "Hell111!"


@app.route('/configs')
def configs():
    return jsonify(hostnamerawlist())


@app.route('/configs/<hostname>')
def page(hostname):
    return jsonify(hostnameIPlist(hostname))


if __name__ == '__main__':


    def hostnamerawlist():
        lhn = set()
        ddhn = {}
        listhostname = list()
        for nm in glob.glob("config_files\*.txt"):
            # print(nm)
            with open(nm) as f:
                for sttr in f:
                    if re.match("^(hostname) ([a-zA-Z0-9].+)", sttr):
                        m = re.match("^(hostname) ([a-zA-Z0-9].+)", sttr)
                        # print(m.group(2))
                        ddhn.update({m.group(2): ''})
                        lhn.add(m.group(2))
                    if re.match("(ip address) ([0-9.]+) ([0-9.]+)", sttr):
                        mm = re.match("(ip address) ([0-9.]+) ([0-9.]+)", sttr)
                        ddhn.update({m.group(2): mm.group(2)})
                    print(m.group(2), mm.group(2))
        for i in lhn:
           listhostname.append(i)
        return ddhn


    def hostnamerawIPlist(hostt):
        lip = set()
        urll = 'config_files\\' + hostt + '.txt'
        for nm in glob.glob(urll):
            with open(nm) as f:
                for sttr in f:
                    if sttr.find("ip address") == 1:
                        # l.add(sttr.replace("ip address", "").strip())
                        lip.add(sttr.strip())
        return lip


    def hostnameIPlist(hostname):
        step = 0
        ls = list()
        for i in hostnamerawIPlist(hostname):
            step = step + 1
            if strtoip(i) != None:
                # print(step, strtoip(i))
                ls.append(strtoip(i))
        return ls

    # print(hostnamerawlist())
    # print(hostnameIPlist('bee-catme3400_10.12.226.50'))
    # aaaa = jsonify(hostnameIPlist('bee-catme3400_10.12.226.50'))
    # print(aaaa)
    # print(hostnameIPlist('bee-catme3400_10.12.226.50'))
    print(hostnamerawlist)

    #app.run(port=80, debug=True)