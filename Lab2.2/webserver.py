from flask import Flask, url_for
from flask import jsonify
import re
import glob
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "<h1>Main menu</h1><hr><a href='" + url_for("configs") + "'><b>Configs</b></a>"


@app.route('/configs')
def configs():
    return hostnamerawlist(url_for("configs"))


@app.route('/configs/<hostname>')
def page(hostname):
    return hostnameIPlist(hostname)


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
                        # print(j)
                        ls +=j + '<br>'
        ls += '<hr><a href="' + url_for("configs") + '">Go to configs</a>'
        return ls


    app.run(port=80, debug=True)