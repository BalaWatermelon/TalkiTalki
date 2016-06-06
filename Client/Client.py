import socket
import threading
import time
import sys
import select
import os

from getpass import getpass

myFolder = os.path.dirname(os.path.abspath(__file__))

test_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
test_data.connect(('0.0.0.0',9999))

read_list = [test_data,sys.stdin]


while True:
    ready_to_read,ready_to_write,in_error = select.select(read_list , [], [])

    for recieve in ready_to_read:
        if recieve == test_data:
            #recieve data
            msg = test_data.recv(1024).decode()
            if msg == 'close':
                exit()
            if msg == 'Password: \n':
                msg=''
                pw = getpass()
                test_data.send(pw.encode())
            if msg == 'frequest':
                msg = test_data.recv(1024).decode()
                sys.stdout.write(msg)
                sys.stdout.flush()

            if msg == 'fstart':
                fname = test_data.recv(1024).decode()
                print('[*]Start recving...')
                f = open(myFolder+'/'+fname,'wb+')
                l = test_data.recv(1024)
                while (l!=b'eof'):
                    print('>Recieve packet')
                    f.write(l)
                    l = test_data.recv(1024)
                    if l == b'eof':
                        break
                f.close()
                print('>Recieve complete')

            if msg == 'fprep':
                sys.stdout.write(msg+'\n')
                sys.stdout.flush()
                fname = test_data.recv(1024).decode()
                f = open('/Users/Jackson/Desktop/Client1/'+fname,'rb')
                packet = f.read(1024)
                while(packet):
                    print('[*]Sending to server...')
                    test_data.send(packet)
                    packet = f.read(1024)
                f.close()
                test_data.send(b'eof')
                msg ='done\n'

            sys.stdout.write(msg)
            sys.stdout.flush()

        else:
            #typein data
            msg = sys.stdin.readline()
            test_data.send(msg.encode())

test_data.close()


'''
def reciever():
        message = test_data.recv(1024).decode()
        print(message)


recieveThread = threading.Thread(target=reciever)
recieveThread.run()

while True:
    cmd = input('>')
    sys.stdout.flush()
    test.send(cmd.encode())
    '''
