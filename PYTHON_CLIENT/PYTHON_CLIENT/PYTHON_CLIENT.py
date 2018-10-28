import socket,time, sys,os
from threading import Timer

def recv_all(socket,crlf):
    data = ""
    while not data.endswith(crlf):
        data = data + socket.recv(1)
    return data.replace(crlf,'')

def Polaczenie():
    HOST = '25.54.23.54'
    PORT = 5555
    SERVER = (HOST,PORT)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if_connected = ''
    while True:
        try:
            sock.connect(SERVER)
            return sock
        except socket.error:
            print 'Nie polaczono'
            print if_connected
            data = raw_input('Aby ponowic polaczenie: Enter \nAby zakonczyc: q\n ')
            if(data =='q'):
                sys.exit(0)

def Polaczenie_przerwane():
    HOST = '25.54.23.54'
    PORT = 5555
    SERVER = (HOST,PORT)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if_connected = ''
    while True:
        try:
            sock.connect(SERVER)
            if_connected = recv_all(sock, '\r\n\r\n')
            if if_connected == 'Nie polaczono.':
                print 'Server jest pelny'
                time.sleep(2)
                sys.exit(0)
            else:
                return sock,if_connected
        except socket.error:
            print 'Server nie odpowiada...'
            print if_connected
            data = raw_input('Aby ponowic polaczenie: Enter \nAby zakonczyc: q: ')
            if(data =='q'):
                sys.exit(0)


sock = Polaczenie()
response = ['0']
while True:
    try:
        if response[0] == '1' :
            data = raw_input('>')
            sock.sendall(data+ '\r\n\r\n') 
        elif response[0] == '2':
            sock.close()
            time.sleep(10)
            sys.exit(0)
        response = recv_all(sock,'\r\n\r\n')
        response = response.split(' ')
        print ' '.join(str(e) for e in response[1::])
    except socket.error:
        sock,response= Polaczenie_przerwane()
        print response
        response = ['0']

