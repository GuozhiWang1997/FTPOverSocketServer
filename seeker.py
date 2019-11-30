# ==============================================
#                  OrchardSeeker
#
# Author:   Guozhi Wang
# Date:     Jun 16 2019
# Verwion:  0.3.2
# This file is delivered within OrchardPackage.
# ==============================================

import socket
import json

obj = socket.socket()
address = input("Input server IP:")
port = input("Input server port:")
port = int(port)
obj.connect((address, port))


def command(command):
    req_bytes = bytes(json.dumps(command), encoding="utf-8")
    obj.sendall(req_bytes)
    ret_bytes = obj.recv(65535)
    ret_str = str(ret_bytes, encoding="utf-8")
    print(ret_str)


def test():
    cmd = {"action": "test",
           "data": "test_data"}
    command(cmd)


def get_list():
    cmd = {
        "action": "get_list"
    }
    command(cmd)


def get_chunk(filename):
    cmd = {
        "action": "get_chunk",
        "data": filename
    }
    req_bytes = bytes(json.dumps(cmd), encoding='utf-8')
    obj.sendall(req_bytes)
    ret_bytes = obj.recv(1000 * 100)
    with open('Client ' + filename, 'wb') as file:
        file.write(ret_bytes)
    print(filename + ' has received.')


def quitt():
    cmd = {"action": "quit"}
    command(cmd)


while True:
    inp = input("Select action:\n"
                + " 1> test\n"
                + " 2> get chunk list\n"
                + " 9> quit\n")
    if inp == '1':
        test()
    elif inp == '2':
        get_list();
    elif inp == '3':
        for i in range(9):
            get_chunk('Phase2.pdf_chunk_' + str(i+1) + '.fck')
    elif inp == '9':
        quitt()
        break;
    else:
        print("Illegal choice!")

exit();