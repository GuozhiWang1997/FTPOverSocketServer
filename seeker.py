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
import os

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


def combine_chunks(filename, count):
    with open('Client ' + filename, 'ab') as file:
        for i in range(count):
            with open('Client ' + filename + '_chunk_' + str(i + 1) + '.fck', 'rb') as chunk:
                chunk_size = os.path.getsize('Client ' + filename + '_chunk_' + str(i+1) + '.fck')
                print(chunk_size)
                file.write(chunk.read(chunk_size))


def quitt():
    cmd = {"action": "quit"}
    command(cmd)


while True:
    inp = input("Select action:\n"
                + " 1> test\n"
                + " 2> get chunk list\n"
                + " 3> get one chunk\n"
                + " 4> combine chunks\n"
                + " 9> quit\n")
    if inp == '1':
        test()
    elif inp == '2':
        get_list();
    elif inp == '3':
        chunk_num = input("id:\n")
        get_chunk('Phase2.pdf_chunk_' + str(chunk_num) + '.fck')
    elif inp == '4':
        combine_chunks('Phase2.pdf', 9)
    elif inp == '9':
        quitt()
        break
    else:
        print("Illegal choice!")

exit();