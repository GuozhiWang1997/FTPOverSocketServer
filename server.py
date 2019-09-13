# ==============================================
#                   SimpleFTP
#
# Author:   Guozhi Wang
# Date:     Sep 12 2019
# Verwion:  0.0.1
# This file is a course homework of CNT5106C.
# ==============================================

import time
import json
import socketserver
import os

BUFFER_SIZE = 4096


# 统一格式输出日志 action为动作标识 msg为日志信息 type为消息类型
# type默认为0 0:普通 蓝色 1:警告 红色 2:成功 绿色 3:小问题 黄色
def log(action, msg, type=0):
    print(time.asctime() + ' [' + action, end=']:\t')
    if type == 0:
        print('\033[1;34m', end='')
    elif type == 1:
        print('\033[1;35m', end='')
    elif type == 2:
        print('\033[1;32m', end='')
    elif type == 3:
        print('\033[1;33m', end='')
    print(msg + '\033[0m')


def check_file_name_legal(file_name):
    file_name = str(file_name)
    if file_name.count('.') != 1 or len(file_name.split('.')[1]) > 4 or len(file_name) > 128:
        return False
    elif file_name.__contains__('<') or file_name.__contains__('>') or file_name.__contains__(':') or file_name.__contains__('"') or file_name.__contains__('/') or file_name.__contains__('\\') or file_name.__contains__('*') or file_name.__contains__('|') or file_name.__contains__('?'):
        return False
    else:
        return True

# 用于收发Socket数据包的服务器
class Slaver(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        client_ip = self.client_address[0]
        client_port = self.client_address[1]
        log('CON_EST', 'Established connection with ' + client_ip + ':' + (str)(client_port))

        while True:
            ret_bytes = conn.recv(BUFFER_SIZE)
            try:
                ret_str = str(ret_bytes, encoding="utf-8")
                req = json.loads(ret_str)
            except:
                log('MSG_ERR', 'Illegal packet received from ' + (str)(client_ip))
                continue

            if req["action"] == "dir" or req["action"] == "ls":
                file_list = os.listdir('./files/')
                msg = ""
                for file_name in file_list:
                    msg = msg + file_name + "\n"
                conn.sendall(bytes(msg, encoding="utf-8"))

            elif req["action"] == "get":
                file_name = req["file_name"]
                with open("./files/" + file_name, 'rb') as file:
                    while True:
                        buffer = file.read(BUFFER_SIZE)
                        if buffer:
                            conn.sendall(buffer)
                        else:
                            break
                log('FLE_SND', 'File ' + file_name + ' has been sent to ' + (str)(client_ip))

            elif req["action"] == "upload":
                file_name = req["file_name"]
                if not check_file_name_legal(file_name):
                    conn.sendall('Illegal filename!')
                else:
                    with open("./files/" + file_name, 'wb') as file:
                        while True:
                            buffer = 


            elif req["action"] == "quit":
                log('CON_END', 'Connection closed with ' + (str)(client_ip))
                msg = ("Connection closed.")
                conn.sendall(bytes(msg, encoding="utf-8"))
                break
            elif req["action"] == "check":
                log('CON_CHK', 'Check request from' + (str)(client_ip))
                msg = ('OK')
                conn.sendall(bytes(msg, encoding='utf-8'))

            else:
                log('MSG_ERR', 'Illegal command received from ' + (str)(client_ip))
                conn.sendall((bytes("Illegal command!", encoding="utf-8")))


if __name__ == "__main__":
    # server = socketserver.ThreadingTCPServer(("0.0.0.0", 9070), Slaver)
    # server.serve_forever()
    print(getfiles())
