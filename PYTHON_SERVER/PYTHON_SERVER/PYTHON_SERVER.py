import socket, sys, threading,time
from BaseProtocol import BaseProtocol
from Gracz import Gracz
from TaliaKart import TaliaKart
from LogikaPokera import LogikaPokera
from StolDoGry import StolDoGry
import Evaluator
from threading import Timer

def recv_all(socket, crlf):
    data = ""
    while not data.endswith(crlf):
        data = data + socket.recv(1)
    return data.replace(crlf, '')

STOLY_DO_GRY = []
CZY_STOL_JEST_DOSTEPNY = True

def kolejka(stol):
    
    # zrobic kopie graczy do wyswietlania 
    while True:
        gracze = []
        for gracz in stol.Gracz:
            gracze.append(gracz)
    
        logikaPokera = LogikaPokera(gracze) # obsluga Komend graczy
        logikaPokera.start_gra()
        logikaPokera.resetuj_talie()
        stop_Gra = False
        for gracz in stol.Gracz:
            while True:
                gracz.client_sock.sendall('1 Aby grac jeszcze raz kazdy gracz musi grac! Czy chcesz grac dalej tak/nie?\r\n\r\n')
                dane = recv_all(gracz.client_sock,'\r\n\r\n').split()
                if len(dane) == 1:
                    if dane[0] == 'tak':
                        break
                    elif dane[0] == 'nie':
                        stop_Gra = True
                        for g in stol.Gracz:
                            if g is not gracz:
                                g.client_sock.sendall('0 gra przerwana gracz '+gracz.name+' nie moze grac dalej!\r\n\r\n')
                        break
                    else:
                        gracz.client_sock.sendall('0 Zla komenda !\r\n\r\n')
                else:
                        gracz.client_sock.sendall('0 Zla komenda !\r\n\r\n')
            if stop_Gra == True:
                break
        if stop_Gra == True:
            break


    #start CZat
    #while True:
    #    data = ''
    #    for gracz in stol.Gracz:
    #        gracz.client_sock.sendall('1 twoja kolej \r\n\r\n')
    #        data = recv_all(gracz.client_sock,'\r\n\r\n')
    #        if data =='EXIT':
    #            break
    #        for g in stol.Gracz:
    #            if g is not gracz:
    #                g.client_sock.sendall('0 Gracz: '+gracz.name+'- '+data+'\r\n\r\n')
    #    if data == 'EXIT':
    #        break
    #koniec CZat

    #start gry Tworzenie watkow menu START
    for i in stol.Gracz:
        ClientThread(i).start()
    STOLY_DO_GRY.remove(stol)
    #koniec gry Tworzenie watkow menu START

    return

class Poczekalnia(threading.Thread):
    def __init__(self,stol,gracz):
        threading.Thread.__init__(self)
        self.stol = stol
        self.gracz = gracz
    
    def run(self):

        def time_up():
            data= ''

        while True:
            time.sleep(5)
            for gracz in self.stol.Gracz:
                gracz.client_sock.sendall('0 oczekuje na '+str(self.stol.Dostepne_miejsca_przy_stole)+'\r\n\r\n')
                 
            if self.stol.Dostepne_miejsca_przy_stole == 0:
                    self.stol.Czy_Gra = True
                    kolejka(self.stol)
                    return 
        return

def DolaczenieDoStolu(gracz):
    if len(STOLY_DO_GRY) == 0:
        while True:
            gracz.client_sock.sendall('1 Brak stolow. Aby grac musisz utworzyc stol\nAby zrezygnowac: q\nAby stwrzyc stol podaj liczbe graczy od 2 do 10\r\n\r\n')
            data = recv_all(gracz.client_sock,'\r\n\r\n')
            if data == 'q':
                return 'MENU','nic'
            else:
                try:
                    data = int(data)
                    #x = StolDoGry(Gracz(client_socket),data)
                    Stol = StolDoGry(gracz,data)
                    gracz.Czy_host = True
                    STOLY_DO_GRY.append(Stol)
                    gracz.client_sock.sendall('0 Stworzono stol '+str(data)+' osobowy\r\n\r\n')
                    print gracz.name +' stworzy stol' + str(data)+' osobowy'
                    return 'POCZEKALNIA1',Stol
                except ValueError:
                        gracz.client_sock.sendall('0 Za komenda\r\n\r\n')
    else:
        gracz.client_sock.sendall('0 Dostepne stoly do gry \r\n\r\n')
        index_stolu = 1
        index_dostepnych_stolow = []
        index_dostepnych_stolow_str =''
        for stoly in STOLY_DO_GRY:
            if stoly.Dostepne_miejsca_przy_stole != 0:
                gracz.client_sock.sendall('0 Stol '+str(index_stolu)+' Ilosc miejsc '+str(stoly.Ilosc_miejsc_przy_stole)+' dostepne miejsca '+str(stoly.Obecni_gracze_przy_Stole) +'\r\n\r\n')
                index_dostepnych_stolow.append(index_stolu)
                index_dostepnych_stolow_str += ' ' + str(index_stolu)
            index_stolu += 1
        while True:
            gracz.client_sock.sendall('1 Aby dolaczyc do istniejacego stolu: JOIN\nAby stowrzyc nowy stol: STOL\nAby wyjsc: WROC \r\n\r\n')
            data = recv_all(gracz.client_sock,'\r\n\r\n')
            if data == 'JOIN':
                while True:
                    gracz.client_sock.sendall('1 Wybierz Stol z dostepnych\nPowrot: q\nLista dostepnych stolow:\n'+index_dostepnych_stolow_str+'\r\n\r\n')
                    data = recv_all(gracz.client_sock,'\r\n\r\n')
                    if data == 'q':
                        break
                    try:
                        data = int(data)
                        if data not in index_dostepnych_stolow:
                            continue
                        STOLY_DO_GRY[data - 1].Dolacz_gracza(gracz)
                        gracz.client_sock.sendall('0 Dolaczyles do Stolu '+str(data)+'\r\n\r\n')
                        print gracz.name +' dolaczyl do stolu'
                        return 'POCZEKALNIA','nic'
                    except ValueError:
                        gracz.client_sock.sendall('0 Za komenda \r\n\r\n')

            elif data == 'STOL':
                while True:
                    gracz.client_sock.sendall('1 Brak stolow. Aby grac musisz utworzyc stol\nAby zrezygnowac: q\nAby stwrzyc stol podaj liczbe graczy od 2 do 10\r\n\r\n')
                    data = recv_all(gracz.client_sock,'\r\n\r\n')
                    if data == 'q':
                        return 'MENU','nic'
                    else:
                        try:
                            data = int(data)
                            Stol = StolDoGry(gracz,data)
                            gracz.Czy_host = True
                            STOLY_DO_GRY.append(Stol)
                            gracz.client_sock.sendall('0 Stworzono stol '+str(data)+' osobowy\r\n\r\n')
                            print gracz.name +' stworzy stol' + str(data)+' osobowy'
                            return 'POCZEKALNIA1',Stol
                        except ValueError:
                                gracz.client_sock.sendall('1 Za komenda\r\n\r\n')
            elif data == 'WROC':
                return 'MENU','nic'

                       
class ClientThread(threading.Thread):
    def __init__(self, gracz,):
        threading.Thread.__init__(self)
        self.gracz = gracz
        self.czy_oczekiwac = False

    def run(self):
        protocol = BaseProtocol()
        self.gracz.client_sock.sendall('1 MENU GLOWNE\r\n\r\n')

        if self.gracz.czy_zalogowany == True:
            protocol.nazwa_uzytkownika = self.gracz.name
            protocol.zalogowano = True

        while True:
            data = ''
            data = recv_all(self.gracz.client_sock, '\r\n\r\n')
            dane_otrzymane_z_protokolu_BaseProtocol = protocol.GlownaMetoda(data)

            if self.gracz.czy_zalogowany == False:
                if protocol.zalogowano == True:
                    self.gracz.name = protocol.nazwa_uzytkownika
                    self.gracz.czy_zalogowany = True
            if dane_otrzymane_z_protokolu_BaseProtocol == 'JOIN':
                data,stol = DolaczenieDoStolu(self.gracz)
                if data == 'MENU':
                    self.gracz.client_sock.sendall('1 MENU GLOWNE\r\n\r\n')
                    continue
                elif data == 'POCZEKALNIA':
                    return
                elif data == 'POCZEKALNIA1':
                    poczekalnia = Poczekalnia(stol,self.gracz)
                    poczekalnia.start()
                    return
            if dane_otrzymane_z_protokolu_BaseProtocol == 'EXIT':
                self.gracz.client_sock.sendall('1 MENU GLOWNE\r\n\r\n')
                break
            self.gracz.client_sock.sendall(dane_otrzymane_z_protokolu_BaseProtocol)      
        self.client_sock.close()

class Server(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def run_server(self):
        self.server_sock.bind(self.addr)
        self.server_sock.listen(1)
        print( 'Server is listening ...')

        try:
            while True:
                client_sock, addr = self.server_sock.accept()
                print( 'Client %s:%s ...') % (addr[0], addr[1]) 
                print ('client %s:%s connected!') % (addr[0], addr[1])
                client_sock.sendall('Polaczono.\r\n\r\n')
                print 'polaczono gracza' +str(client_sock)
                ClientThread(Gracz(client_sock,str(addr[0]))).start()
        except socket.error:
            if self.server_sock != None:
                self.server_sock.close()
            sys.exit(-1)

server = Server('25.54.23.54', 5555) # >1024
server.run_server()
