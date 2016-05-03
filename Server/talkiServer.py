import socket
import threading
from enum import Enum

class cmd:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class talkiServer():
    server = ''
    clienthandler=[]
    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = 7777

    def Start(self,ip,port):
        if self.startListen(ip,port):
            self.startRecieve()
        else:
            return

    def startListen(self,ip,port):
        global server
        try:
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server.bind((ip,port))
            server.listen(5)
            self.sprint('suc','Start listening on '+ip+':'+str(port))
            return True
        except:
            self.sprint('err','Listen on '+ip+':'+str(port)+' failed.')
            return False

    def startRecieve(self):
        global server
        global clienthandler
        while True:
            client,addr = server.accept()
            c = threading.Thread(target=clientservice,args=(client))
            c.start()
            clienthandler.append(c)

    def clientservice(self,socket):
        client = client()
        client.socket = socket
        while client.login is not True:
            self.requestLogin(client)

        client.send('Login success')

    def requestLogin(self,client):
        #TODO:request client to login through socket


    def sprint(self,state,string):
        if state == 'err':
            print(cmd.FAIL+'[*]>>Fatal: '+string+cmd.ENDC)
        elif state == 'suc':
            print(cmd.GREEN+'[*]'+string+cmd.ENDC)
        elif state == 'warn':
            print(cmd.WARNING+'[*]'+string+cmd.ENDC)

class status(Enum):
    available = 1
    invisible = 2

class client:
    name = ''
    ip = ''
    login = False
    status = status.available
    socket=''
    sessions = []
    def __init__(self,sock):
        self.socket = sock

    def send(self, string):
        self.socket.send(string.encode())
