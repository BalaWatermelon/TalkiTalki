import socket
import threading

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
        while True:
            client,addr = server.accept()

    def sprint(self,state,string):
        if state == 'err':
            print(cmd.FAIL+'[*]>>Fatal: '+string+cmd.ENDC)
        elif state == 'suc':
            print(cmd.GREEN+'[*]'+string+cmd.ENDC)
        elif state == 'warn':
            print(cmd.WARNING+'[*]'+string+cmd.ENDC)
