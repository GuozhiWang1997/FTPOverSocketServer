# FTPOverSocketServer
This project is a course homework of CNT5106C@UF. It's a socket server that allow file upload and download.
## Environment
Python 3 | PyYaml
## How to use
1. Make sure you have installed python3 and pyyaml.
2. Make sure you have allowed network through port 9070. (You can change it in the server.py)
3. $ python3 ./server.py
## Directory Structure
```
FTPOverSocketServer
  | -- server.py
  | -- userlist.yml
  | -- files
        | -- user1
        | -- user2
        | -- ...
```
Username and passwords are stored in "userlist.yml" and their files are stored at according subdirectory of "/files".
## Where is the client?
You can find it [here](https://github.com/JuiceW/FTPOverSocketClient).
