# =================================================
#                   FTPOverSocket
#
# Author:   Guozhi Wang
# Date:     Sep 12 2019
# Version:  0.0.3
# This project is a course homework of CNT5106C@UF.
# =================================================
import time
import json
import socketserver
import os
import yaml

BUFFER_SIZE = 4096
FILE_NAME = ""


def log(action, msg, case=0):
    print(time.asctime() + ' [' + action, end=']:\t')
    if case == 0:
        print('\033[1;34m', end='')
    elif case == 1:
        print('\033[1;35m', end='')
    elif case == 2:
        print('\033[1;32m', end='')
    elif case == 3:
        print('\033[1;33m', end='')
    print(msg + '\033[0m')

def login(username, password):
    with open("./userlist.yml", "r") as file:
        lines = file.read()
        user_list = yaml.safe_load(lines)
        for user in user_list:
            if user["username"] == username and str(user["password"]) == str(password):
                return True
        return False


class FTPOverSocketServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        client_ip = self.client_address[0]
        client_port = self.client_address[1]
        receiving_upload = False
        log('CON_EST', 'Established connection with ' + client_ip + ':' + str(client_port))
        file = None
        is_logged_in = False
        while True:
            if not is_logged_in:
                ret_bytes = conn.recv(BUFFER_SIZE)
                try:
                    ret_str = str(ret_bytes, encoding="utf-8")
                    account = ret_str.split("??")
                    if login(account[0], account[1]):
                        is_logged_in = True
                        conn.sendall(bytes("LOGIN_SUCCESS", "utf-8"))
                    else:
                        conn.sendall(bytes("WRONG_ACCOUNT", "utf-8"))
                        continue
                except:
                    continue
            if receiving_upload:
                ret_bytes = conn.recv(BUFFER_SIZE)
                try:
                    ret_str = str(ret_bytes, encoding="utf-8")
                    if ret_str == "DONE":
                        file.close()
                        receiving_upload = False
                        log('FLE_REC', 'File ' + FILE_NAME + ' has been uploaded successfully from ' + str(client_ip))
                        continue;
                    else:
                        file.write(ret_str)
                except:
                    file.write(ret_bytes)
            else:
                ret_bytes = conn.recv(BUFFER_SIZE)
                try:
                    ret_str = str(ret_bytes, encoding="utf-8")
                    req = json.loads(ret_str)
                except:
                    continue

                if req["action"] == "dir":
                    file_list = os.listdir('./files/')
                    msg = ""
                    for file_name in file_list:
                        msg = msg + file_name + "\n"
                    conn.sendall(bytes(msg, encoding="utf-8"))

                elif req["action"] == "get":
                    file_name = req["filename"]
                    with open("./files/" + file_name, 'rb') as file:
                        isFirst = True
                        while True:
                            buffer = file.read(BUFFER_SIZE)
                            if isFirst:
                                if not buffer:
                                    log('EPT_FLE', 'The file is empty!')
                                    conn.sendall(bytes("EMPTY FILE", encoding="utf-8"))
                                    break;
                                isFirst = False
                            if not buffer:
                                break;
                            if buffer:
                                conn.sendall(buffer)
                    log('FLE_SND', 'File ' + file_name + ' has been sent to ' + str(client_ip))

                elif req["action"] == "upload":
                    FILE_NAME = req["filename"]
                    receiving_upload = True
                    file = open("./files/" + FILE_NAME, 'wb')
                    log('FLE_REC', 'Starting receiving ' + FILE_NAME + ' from ' + str(client_ip))

                elif req["action"] == "quit":
                    log('CON_END', 'Connection closed with ' + str(client_ip))
                    break
                elif req["action"] == "check":
                    log('CON_CHK', 'Check request from' + str(client_ip))
                    msg = 'OK'
                    conn.sendall(bytes(msg, encoding='utf-8'))


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 9070), FTPOverSocketServer)
    server.serve_forever()
