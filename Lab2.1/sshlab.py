import paramiko, time
import re

BUF_SIZE = 20000
TIMEOUT = 1

# Создаем объект — соединение по ssh
ssh_connection = paramiko.SSHClient()
ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Инициируем соединение по ssh
ssh_connection.connect("10.31.70.209", username="restapi", password="j0sg1280-7@", look_for_keys=False, allow_agent=False)
session = ssh_connection.invoke_shell()

session.send("\n")
session.recv(BUF_SIZE)
session.send("terminal length 0\n")
time.sleep(TIMEOUT)

session.send("\n")
session.recv(BUF_SIZE)
session.send("\n\n\nshow interfaces\n")
time.sleep(TIMEOUT*2)
s = session.recv(BUF_SIZE).decode()
lint = list()
for strr in s.splitlines():
    lraw = list()
    if re.match("^(\w.*\d)(?= is)", strr):
        m = re.match("^(\w.*\d)(?= is)", strr)
        # print(m)
        lraw.append(m.group(1))
    if re.match(".*input, (\d* bytes)", strr):
        m = re.match(".*input, (\d* bytes)", strr)
        # print(m)
        lraw.append(m.group(1))
    if re.match(".*output, (\d* bytes)", strr):
        m = re.match(".*output, (\d* bytes)", strr)
        # print(m)
        lraw.append(m.group(1))
    if len(lraw) > 0:
        lint.append(lraw)
print(lint)
#print(s)

session.close()