import Evaluator
from TaliaKart import TaliaKart

class Gracz(object):
    def __init__(self, client_sock,nazwa):
        self.karty = []
        self.folded = False
        self.called = [False, False]
        self.raised = False
        self.all_in = False
        self.kredyty = 100
        self.bet = 0
        self.is_playing = False
        self.name = nazwa
        self.client_sock = client_sock
        self.czy_zalogowany = False
        self.jaki_uklad = ''
        self.Czy_host = False
        self.sila = 0

    def wez_karty(self, karty):
        self.karty = karty

    def wymien_karty(self, talia_kart):
        otrzymane_karty = []
        ilosc_kart_do_wymiany = -1
        while not Evaluator.czy_ilosc_kart_do_wymiany_w_zakresie(ilosc_kart_do_wymiany):
            self.client_sock.sendall('1 ile kart chcesz wymienic: \r\n\r\n')
            ilosc_kart_do_wymiany = self.recv_all(self.client_sock,'\r\n\r\n')
            try:
                ilosc_kart_do_wymiany = int(ilosc_kart_do_wymiany)
                if not ilosc_kart_do_wymiany in range(0,6):
                     self.client_sock.sendall('0 niepoprawna ilosc kart do wymiany \r\n\r\n')
            except ValueError:
                self.client_sock.sendall('0 not a number \r\n\r\n')
        otrzymane_karty = []
        ilosc_wymian = 0
        for i in range(0,ilosc_kart_do_wymiany):
            while ilosc_kart_do_wymiany > ilosc_wymian:
                self.client_sock.sendall('1 podaj karte (wartosc, kolor): \r\n\r\n')
                karta_do_wymiany = self.recv_all(self.client_sock,'\r\n\r\n').split()
                if len(karta_do_wymiany) == 2 and Evaluator.ma_karte(karta_do_wymiany[0]+' '+karta_do_wymiany[1], Evaluator.uklad2(Evaluator.przygotuj_reke(self.karty))):
                    self.client_sock.sendall('0 wymieniam karte ... \r\n\r\n')
                    wyl = talia_kart.losujKarte()
                    otrzymane_karty.append(wyl)
                    self.karty[Evaluator.wartosc_karty(karta_do_wymiany[0])-2][Evaluator.kolor_str_to_int(karta_do_wymiany[1])] = 0
                    self.karty[wyl[1]-2][wyl[0].index(1)] = 1
                    ilosc_wymian += 1
                else:
                   self.client_sock.sendall('0 nie masz tej karty w rece lub zly format. poprawny format: wartosc_karty kolor_karty\r\n\r\n')
        self.client_sock.sendall('0 '+Evaluator.uklad2(otrzymane_karty) + '\r\n\r\n')
        self.client_sock.sendall('0 ' + Evaluator.ladne_karty(Evaluator.przygotuj_reke(self.karty)) + '\r\n\r\n')

    def recv_all(self,socket, crlf):
        data = ""
        while not data.endswith(crlf):
            data = data + socket.recv(1)
        return data.replace(crlf, '')
