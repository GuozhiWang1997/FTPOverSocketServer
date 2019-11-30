# =================================================
#               FTPOverSocket_Server
#               P2P Version
#
# Author:       Guozhi Wang
# Init Date:    Nov 19 2019
# Last Mod:     Nov 19 2019
# Version:      0.0.1
# This project is a course homework of CNT5106C@UF.
# =================================================
import time
import json
import socketserver
import os
import yaml
import hashlib

BUFFER_SIZE = 1000*100


# case: 0-Primary, 1-Error, 2-Success, 3-Warning
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


def generate_chunks(filename):
    file_size = os.path.getsize(filename)
    with open(filename, 'rb') as file:
        chunk = file.read(BUFFER_SIZE)
        chunk_list = []
        chunk_id = 1
        byte_count = 0
        while chunk:
            if byte_count >= file_size:
                break
            elif byte_count + BUFFER_SIZE > file_size:
                chunk_size = file_size - byte_count
            else:
                chunk_size = BUFFER_SIZE

            chunk_filename = filename + '_chunk_' + str(chunk_id) + '.fck'
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_hash = hashlib.md5(chunk)
            chunk_md5_hex = chunk_hash.hexdigest()
            chunk_list.append({
                'chunk_id': chunk_id,
                'chunk_size': chunk_size,
                'filename': chunk_filename,
                'md5': chunk_md5_hex
            })
            chunk_id += 1
            byte_count += chunk_size
            chunk = file.read(chunk_size)
        with open('chunk_list.yml', 'w') as yml_file:
            yaml.dump(chunk_list, yml_file)


class FTPOverSocketServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        client_ip = self.client_address[0]
        client_port = self.client_address[1]
        client_address = str(client_ip) + ':' + str(client_port)
        log('NEW_PEER', 'Established connection with ' + client_address, 2)
        while True:
            ret_bytes = conn.recv(BUFFER_SIZE)
            try:
                ret_str = str(ret_bytes, encoding="utf-8")
                req = json.loads(ret_str)
            except:
                continue

            if req["action"] == "test":
                data = req["data"]
                log('RCV_TEST', str(data) + ' received from ' + client_address)
                msg = 'This is a test message!'
                conn.sendall(bytes(msg, encoding="utf-8"))
                log('RSP_TEST', 'Test message sent to ' + client_address)

            elif req["action"] == "get_list":
                with open('chunk_list.yml') as file:
                    chunk_list = yaml.load(file, Loader=yaml.FullLoader)
                    msg = json.dumps(chunk_list)
                    conn.sendall(bytes(msg, encoding='utf-8'))
                log('RSP_LIST', 'Chunk list sent to ' + client_address)

            elif req["action"] == "get_chunk":
                filename = req["data"]
                file_size = os.path.getsize(filename)
                with open(filename, 'rb') as file:
                    file_b = file.read(file_size)
                    conn.sendall(file_b)
                log('SNT_FILE', 'Chunk file ' + filename + ' sent to ' + client_address)


            elif req["action"] == "quit":
                msg = "Bye bye!"
                conn.sendall(bytes(msg, encoding='utf-8'))
                log('RCV_QUIT', client_address + ' has quit!', 1)


if __name__ == "__main__":
    generate_chunks('Phase2.pdf')
    log('INITDONE', 'The file has been splited into chunks.', 2)
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 9070), FTPOverSocketServer)
    server.serve_forever()