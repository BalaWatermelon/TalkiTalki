import socket
from threading import Thread
from enum import Enum
import threading
import time
import os

class cmd:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TalkiServer:

    serverFolder = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = 7777

    def Start(self,ip,port):
        if self.startListen(ip, port):
            self.startRecieve()
        else:
            return

    def startListen(self, ip, port):
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
            c = service(client)
            c.start()


    def sprint(self,state,string):
        if state == 'err':
            print(cmd.FAIL+'[*]>>Fatal: '+string+cmd.ENDC)
        elif state == 'suc':
            print(cmd.GREEN+'[*]'+string+cmd.ENDC)
        elif state == 'warn':
            print(cmd.WARNING+'[*]'+string+cmd.ENDC)

class service(Thread):

    ClientHandler = ['']
    offLineData = [['password','h','haha'],['password','b','fuck'],['password','mango','123'],['oMessage','b','mango','fuck you b!']]
    def __init__(self, sock):
        Thread.__init__(self)
        self.socket = sock
        self.client = client(sock)
        service.ClientHandler.append(self)
        for serv in service.ClientHandler[1:]:
            print(serv)

    def run(self):
        while self.client.login != True:
            self.requestLogin()

        self.client.send('Login success\n')
        while True:
            self.giveOffLineData()
            self.client.send('>')
            command = self.client.recieve()
            command = command.strip()
            print ('[*]>> '+command+' from ' + self.client.name)
            request = command.split(' ')
            print(request)

            #request process logic
            if request[0] == 'exit':
                service.ClientHandler.remove(self)
                self.client.drop()
                break

            elif request[0] == 'friend':
                self.client.friend(request[1],request[2:])

            elif request[0] == 'send':
                if self.isOffline(request[1]):
                    self.client.send(request[1] + ' is currently off line, we left a system message for you.\n')
                    service.offLineData.append(['oMessage',request[1],self.client.name,request[2]])
                else:
                    for serv in service.ClientHandler[1:]:
                        if serv.client.name == request[1]:
                            msg = ' '.join(request[2:])
                            serv.client.send('Message from '+ self.client.name + ' : ' +msg+'\n')

            elif request[0] == 'talk':
                if self.isOffline(request[1]):
                    self.client.send('The user is currently offline, use "send" to leave a message.\n')
                else:
                    for serv in service.ClientHandler[1:]:
                        if serv.client.name == request[1]:
                            self.client.send('>')
                            talki = self.client.recieve().strip()
                            serv.client.send(self.client.name+' : '+talki+'\n')
                            while talki != 'exit':
                                self.client.send('>')
                                talki = self.client.recieve().strip()
                                serv.client.send(self.client.name+' : '+talki+'\n')

            elif request[0] == 'sendfile':
                f = open('/Users/Jackson/Desktop/'+request[2],'wb+')
                self.client.send('fprep')
                time.sleep(1)
                self.client.send(request[2])
                l = self.client.recieveb()
                while (l!=b'eof'):
                    print('>Recieve packet')
                    f.write(l)
                    l = self.client.recieveb()
                f.close()
                #check file exicst
                for c in service.ClientHandler[1:]:
                    if c.client.name == request[1]:
                        c.client.send('frequest')
                        c.client.send('[SYSTEM]>Filerequest from ' + self.client.name +' sending ' + request[2]+ '(y/n)')
                        self.client.send('[SYSTEM]>waiting for '+c.client.name+' to response...')
                        c.client.pendfile = 'recv'
                        c.client.pendfname = request[2].strip()

            elif request[0] =='y':
                if self.client.pendfile:
                    self.client.send('fstart')
                    time.sleep(1)
                    self.client.send(self.client.pendfname)
                    f = open('/Users/Jackson/Desktop/'+self.client.pendfname,'rb')
                    print(self.client.pendfname)
                    packet = f.read(1024)
                    while(packet):
                        print('[*]Sending to client...')
                        self.client.sendb(packet)
                        packet = f.read(1024)
                    f.close()
                    self.client.sendb(b'eof')
                    print('done')

            elif request[0] == 'goinvisible':
                self.client.stat = client.status.invisible

            elif request[0] == 'goonline':
                self.client.stat = client.status.available

    def requestLogin(self):
        #TODO:request client to login through socket
        ha= 'sdf'
        self.client.send('LoginID: \n')
        ID = self.client.recieve()
        self.client.send('Password: \n')
        PW = self.client.recieve()
        for data in service.offLineData:
            if data[0]=='password':
                if ID.strip() == data[1]:
                    if PW.strip() != data[2]:
                        self.client.send('WrongPWID\n')
                    else:
                        self.client.name=ID.strip()
                        self.client.login=True

    def giveOffLineData(self):
        for data in service.offLineData:
            print (data)
            if data[0] == 'oMessage':
                if data[1] == self.client.name:
                    self.client.send('Message from ' + data[2] + ':' + data[3] +'\n')
                    print (data)
                    service.offLineData.remove(data)

    def isOffline(self,who):
        for serv in service.ClientHandler[1:]:
            if serv.client.name == who:
                if serv.client.stat == client.status.available:
                    return False
        return True

    def sprint(self,state,string):
        if state == 'err':
            print(cmd.FAIL+'[*]>>Fatal: '+string+cmd.ENDC)
        elif state == 'suc':
            print(cmd.GREEN+'[*]'+string+cmd.ENDC)
        elif state == 'warn':
            print(cmd.WARNING+'[*]'+string+cmd.ENDC)

class client:
    class status(Enum):
        available = 1
        invisible = 2
    pendfile = ''
    pendfname = ''
    name = ''
    ip = ''
    login = False
    stat = status.available
    sessions = []
    friendList = []
    ofLineMessage = []
    def __init__(self,sock):
        self.socket = sock
        self.send('Welcome to server\n')
        print('Client create')

    def send(self,message):
        message = message.encode()
        self.socket.send(message)

    def sendb(self,bina):
        self.socket.send(bina)

    def recieve(self):
        message = self.socket.recv(1024).decode()
        print('[Client]>>'+message)
        return message

    def recieveb(self):
        message = self.socket.recv(1024)
        print('[Client]>>data')
        return message

    def drop(self):
        self.send('close')
        self.socket.close()

    def friend(self,func,par):
        if func == 'add':
            for name in par:
                self.friendList.append(name)
                self.send('[SYSTEM]Add ' + name + ' as friend\n')
        elif func == 'list':
            self.send('Your Friend List\n')
            if not self.friendList:
                self.send('Empty\n')
            else:
                for name in self.friendList:
                    self.send(name+'\n')
        elif func == 'rm':
            for name in par:
                self.friendList.remove(name)
                self.send('[SYSTEM]Remove ' + name + ' from friend list\n')
            self.friend('list','')
        elif func == 'status':
            self.send('Friend Status\n')
            for name in self.friendList:
                self.send(name)
                if service.isOffline(super,name):
                    self.send(': offline\n')
                else:
                    self.send(': online\n')

    def addOffLineMessage(self,fromuser,msg):
        return
