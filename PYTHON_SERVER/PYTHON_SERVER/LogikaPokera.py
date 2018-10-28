from Gracz import Gracz
from TaliaKart import TaliaKart
import Evaluator
import socket

def recv_all(sock, crlf):
    data = ""
    while not data.endswith(crlf):
        data = data + sock.recv(1)
    return data.replace(crlf, '')

class LogikaPokera(object):
    def __init__(self,gracze):
        self.talia = TaliaKart()
        self.gracze = gracze
        self.najwyzszy_zaklad = 0
        self.pot = 0
        self.all_called = False
        self.czy_breake = False
        self.dali_folda = []
        self.gracze_wyswietl = []

    def runda(self):
        ilosc_graczy = len(self.gracze)-1
        self.najwyzszy_zaklad = 0
        winner = self.gracze[0]
        self.all_called = False
        self.czy_breake = False
        self.dali_folda = []
        for gracz in self.gracze:
            for g in self.gracze_wyswietl:
                if g is not self.gracze_wyswietl:
                    g.client_sock.sendall('0 ruch gracza: '+gracz.name+'\n\r\n\r\n')
            if not gracz in self.dali_folda:
                if gracz.is_playing and gracz.all_in == False:
                    gracz.client_sock.sendall('0 ###### self.pot = ' + str(self.pot) + ' ######\n\r\n\r\n')
                    gracz.client_sock.sendall('0 ruch ' + gracz.name + ' ' + str(gracz.kredyty)+'\n\r\n\r\n')
                    while True:
                        if len(self.gracze) == 1:
                            for g in self.gracze_wyswietl:
                                g.client_sock.sendall('0 tylko jeden gracz nie spasowal ...\n\r\n\r\n')
                            break
                        wartosc_call = '0'
                        if gracz.bet < self.najwyzszy_zaklad:
                            wartosc_call = str(self.najwyzszy_zaklad - gracz.bet)
                        gracz.client_sock.sendall('1 FOLD | CALL (x' + str(gracz.called.count(False)) + ', koszt: ' + wartosc_call + ') | RAISE ilosc_kredytow)\n' + gracz.name + '> \r\n\r\n')
                        ruch = recv_all(gracz.client_sock, '\r\n\r\n')
                        ruch = ruch.split()
                        if 'FOLD' in ruch and len(ruch) == 1:
                            for g in self.gracze_wyswietl:
                                    if g is not gracz:
                                        g.client_sock.sendall('0 '+gracz.name+': FOLD\n\r\n\r\n')
                            gracz.client_sock.sendall('0 spasowales, nie bierzesz juz udzialu w rozgrywce.\r\n\r\n')
                            gracz.folded = True
                            self.pot = int(self.pot)
                            gracz.is_playing = False
                            self.dali_folda.append(gracz)
                            self.gracze.remove(gracz)
                            if len(self.gracze) == 1:
                                #gracz.client_sock.sendall('0 tylko jeden gracz nie spasowal ...\r\n\r\n')
                                return self.pot
                            break
                        elif 'CALL' in ruch and len(ruch) == 1:
                            if gracz.kredyty < int(wartosc_call):
                                gracz.client_sock.sendall('1 > ALL IN ? tak/ nie\r\n\r\n')
                                all_in = recv_all(gracz.client_sock, '\r\n\r\n')
                                all_in = all_in.split()
                                if 'tak' in all_in:
                                    for g in self.gracze:
                                        for g in self.gracze_wyswietl:
                                            if g is not gracz:
                                                g.client_sock.sendall('0 '+gracz.name+': ALL-IN\n\r\n\r\n')
                                    self.pot += gracz.kredyty
                                    gracz.bet += gracz.kredyty
                                    gracz.kredyty = 0
                                    gracz.client_sock.sendall('0 wszedles za all in\r\n\r\n')
                                    gracz.all_in = True
                                else:
                                    for g in self.gracze:
                                        if g is not gracze_wyswietl:
                                            g.client_sock.sendall('0 '+gracz.name+': FOLD\n\r\n\r\n')
                                    gracz.folded = True
                                    self.pot = int(self.pot)
                                    for g in self.gracze:
                                        if g == gracz:
                                            self.gracze.remove(g)
                                    gracz.client_sock.sendall('0 '+ gracz.name + ' folded, nie bierze juz udzialu w rozgrywce.\r\n\r\n')
                            elif gracz.called[0] == False:
                                if gracz.raised == False:
                                    gracz.called[0] = True
                                    if gracz.bet < self.najwyzszy_zaklad:
                                        for g in self.gracze_wyswietl:
                                            if g is not gracz:
                                                g.client_sock.sendall('0 '+gracz.name+': CALL\n\r\n\r\n')
                                        gracz.client_sock.sendall('0 sprawdzasz, pobrano ' + str(self.najwyzszy_zaklad - gracz.bet) + ' kredytow\r\n\r\n')
                                        x = (self.najwyzszy_zaklad - gracz.bet)
                                        gracz.bet += x
                                        gracz.kredyty -= x
                                        if gracz.kredyty == 0:
                                            gracz.client_sock.sendall('0 wszedles za all in\r\n\r\n')
                                            gracz.all_in = True
                                        self.pot += x
                                        self.gracze.append(gracz)
                                    else:
                                        gracz.client_sock.sendall('0 czekasz ...\r\n\r\n')
                                        self.gracze.append(gracz)
                            else:
                                gracz.called[0] = True
                                if gracz.bet < self.najwyzszy_zaklad:
                                    for g in self.gracze_wyswietl:
                                        if g is not gracz:
                                            g.client_sock.sendall('0 '+gracz.name+': CALL\n\r\n\r\n')
                                    gracz.client_sock.sendall('0 sprawdzasz, pobrano ' + str(self.najwyzszy_zaklad - gracz.bet) + ' kredytow\r\n\r\n')
                                    x = (self.najwyzszy_zaklad - gracz.bet)
                                    gracz.bet += x
                                    gracz.kredyty -= x
                                    if gracz.kredyty == 0:
                                        for g in self.gracze_wyswietl:
                                            if g is not gracz:
                                                g.client_sock.sendall('0 '+gracz.name+': ALL-IN\n\r\n\r\n')
                                        gracz.client_sock.sendall('0 wszedles za all in\r\n\r\n')
                                        gracz.all_in = True
                                    self.pot += x
                                else:
                                    gracz.client_sock.sendall('0 sprawdzasz ...\r\n\r\n')
                            bets = gracz.bet
                            all_same = True
                            for gracz in self.gracze:
                                if gracz.is_playing == True:
                                    if gracz.bet != bets:
                                        all_same = False
                            if all_same and self.najwyzszy_zaklad != 0:
                                self.czy_breake = True
                                break
                            break
                        elif 'RAISE' in ruch:
                            if len(ruch) == 2:
                                try:
                                    ruch[1] = int(ruch[1])
                                except ValueError:
                                    gracz.client_sock.sendall('0 argument nie jest liczba\r\n\r\n')
                            else:
                                gracz.client_sock.sendall('0 brak argumentu 1\r\n\r\n')
                            while True:
                                if len(self.gracze) == 1:
                                    for g in self.gracze_wyswietl:
                                        g.client_sock.sendall('0 tylko jeden gracz nie spasowal ...\r\n\r\n')
                                    break
                                if len(ruch) == 2:
                                    try:
                                        ruch[1] = int(ruch[1])
                                    except ValueError:
                                        gracz.client_sock.sendall('0 argument nie jest liczba\r\n\r\n')
                                else:
                                    gracz.client_sock.sendall('0 brak argumentu 2\r\n\r\n')
                                if len(ruch) == 2 and ruch[1] < gracz.kredyty:
                                    if gracz.raised == False:
                                        for g in self.gracze_wyswietl:
                                            if g is not gracz:
                                                g.client_sock.sendall('0 '+gracz.name+': RAISE '+str(ruch[1])+'\n\r\n\r\n')
                                        gracz.client_sock.sendall('0 '+ gracz.name + ' podbijasz o ' + str(ruch[1]) +'\r\n\r\n')
                                        gracz.kredyty -= int(ruch[1]) + int(wartosc_call)
                                        gracz.raised = True
                                        gracz.bet += int(ruch[1])+int(wartosc_call)
                                        self.pot += int(ruch[1])+int(wartosc_call)
                                        self.najwyzszy_zaklad = int(ruch[1]) + int(wartosc_call)
                                        self.gracze.append(gracz)
                                        break
                                    else:
                                        while 'RAISE' in ruch:
                                            wartosc_call = '0'
                                            if gracz.bet < self.najwyzszy_zaklad:
                                                wartosc_call = str(self.najwyzszy_zaklad - gracz.bet)
                                                gracz.client_sock.sendall('1 FOLD | CALL (x' + str(gracz.called.count(False)) + ', koszt: ' + wartosc_call + ') | RAISE ilosc_kredytow)\n' + gracz.name + '> \r\n\r\n')
                                                ruch = recv_all(gracz.client_sock, '\r\n\r\n')
                                                ruch = ruch.split()
                                            if 'FOLD' in ruch:
                                                gracz.client_sock.sendall('0 spasowales, nie bierzesz juz udzialu w rozgrywce.\r\n\r\n')
                                                self.pot = int(self.pot)
                                                gracz.folded = True
                                                gracz.is_playing = False
                                                for g in self.gracze:
                                                    if g == gracz:
                                                        self.gracze.remove(g)
                                                if len(self.gracze) == 1:
                                                    gracz.client_sock.sendall('0 tylko jeden gracz nie spasowal ...\r\n\r\n')
                                                    break
                                            elif 'CALL' in ruch:
                                                if self.gracze.index(gracz) == ilosc_graczy:
                                                    gracz.client_sock.sendall('0 kazdy sprawdzil, za chwile nastapi wymiana kart ...\r\n\r\n')
                                                    break
                                                else:
                                                    if gracz.called[0] == False:
                                                        if gracz.raised == False:
                                                            gracz.called[0] = True
                                                            if gracz.bet < self.najwyzszy_zaklad:
                                                                gracz.client_sock.sendall('0 sprawdzasz, pobrano ' + str(self.najwyzszy_zaklad - gracz.bet) + ' kredytow\r\n\r\n')
                                                                x = (self.najwyzszy_zaklad - gracz.bet)
                                                                gracz.bet += x
                                                                gracz.kredyty -= x
                                                                self.pot += x
                                                                self.gracze.append(gracz)
                                                            else:
                                                                gracz.client_sock.sendall('0 czekasz ...\r\n\r\n')
                                                                self.gracze.append(gracz)
                                                        else:
                                                            gracz.called[0] = True
                                                            if gracz.bet < self.najwyzszy_zaklad:
                                                                gracz.client_sock.sendall('0 sprawdzasz, pobrano ' + str(self.najwyzszy_zaklad - gracz.bet) + ' kredytow\r\n\r\n')
                                                                x = (self.najwyzszy_zaklad - gracz.bet)
                                                                gracz.bet += x
                                                                gracz.kredyty -= x
                                                                self.pot += x
                                                            else:
                                                                gracz.client_sock.sendall('0 sprawdzasz ...\r\n\r\n')
                                                    else:
                                                        if gracz.called[1] == False:
                                                            gracz.called[1] = True
                                                            gracz.client_sock.sendall('0 sprawdzasz, pobrano ' + str(self.najwyzszy_zaklad - gracz.bet) + ' kredytow. kredyty: ' + str(gracz.kredyty)+'\r\n\r\n')
                                                            x = (self.najwyzszy_zaklad - gracz.bet)
                                                            gracz.bet += x
                                                            gracz.kredyty -= x
                                                            self.pot += x
                                                bets = gracz.bet
                                                all_same = True
                                                for gracz in self.gracze:
                                                    if gracz.is_playing == True:
                                                        if gracz.bet != bets:
                                                            all_same = False
                                                if all_same:
                                                    gracz.client_sock.sendall('0 przechodzmy do wylonienia zwyciezcy, kazdy postawil tyle samo ...\r\n\r\n')
                                                    break
                                    break
                                elif len(ruch) != 2:
                                    gracz.client_sock.sendall('0 RAISE musi posiadac argument liczba_kredytow.\r\n\r\n')
                                    gracz.client_sock.sendall('1 '+ gracz.name+'> \r\n\r\n')
                                    ruch = recv_all(gracz.client_sock, '\r\n\r\n')
                                    ruch = ruch.split()
                                else:
                                    gracz.client_sock.sendall('0 niewystarczajaca ilosc kredytow.\r\n\r\n')
                                    gracz.client_sock.sendall('1 '+ gracz.name+'> \r\n\r\n')
                                    ruch = recv_all(gracz.client_sock, '\r\n\r\n')
                                    ruch = ruch.split()
                            break
                        else:
                           gracz.client_sock.sendall('0 zla komenda\r\n\r\n')
                           continue
                    gracz.client_sock.sendall('0 kredyty = ' + str(gracz.kredyty)+'\r\n\r\n')
                    if self.czy_breake == True:
                        break
                else:
                    gracz.client_sock.sendall('0 czekaj na nastepne rozdanie\r\n\r\n')
        return self.pot
    
    def czy_biora_udzial(self):
        licznik = 0
        for gracz in self.gracze_wyswietl:
            gracz.client_sock.sendall('1 czy chcesz wziac udzial w rozdaniu, wejscie: 10 ? tak\ nie: ' + gracz.name + '> \r\n\r\n')
            data = recv_all(gracz.client_sock, '\r\n\r\n')
            #data = data.split()
            while True:
                if data == 'tak':
                    gracz.is_playing = True
                    gracz.client_sock.sendall('0 pobrano 10 kredytow.\r\n\r\n')
                    gracz.karty = self.talia.rozdajKarty()
                    gracz.client_sock.sendall('0 twoje karty: \n' + Evaluator.uklad2(Evaluator.przygotuj_reke(gracz.karty))+'\r\n\r\n')
                    gracz.client_sock.sendall('0 twoje karty: \n' + Evaluator.ladne_karty(Evaluator.przygotuj_reke(gracz.karty))+'\r\n\r\n')
                    gracz.kredyty -= 10
                    #gracz.bet += 10
                    #self.najwyzszy_zaklad = gracz.bet
                    self.pot += 10
                    break
                elif data == 'nie':
                    gracz.client_sock.sendall('0 nie bierzesz udzialu w tym rozdaniu.\r\n\r\n')
                    gracz.is_playing = False
                    licznik += 1
                    break
                else:
                    gracz.client_sock.sendall('0 zla odpowiedz, sprobuj ponownie.\r\n\r\n')
                    gracz.client_sock.sendall('1 czy chcesz wziac udzial w rozdaniu, wejscie: 10 ? tak\ nie: ' + gracz.name + '> \r\n\r\n')
                    data = recv_all(gracz.client_sock, '\r\n\r\n')
        if licznik == len(self.gracze):
            return 'stop'
        return self.pot

    def resetuj_talie(self):
        self.talia.noweRozdanie()

    def start_gra(self):
        for gracz in self.gracze:
            self.gracze_wyswietl.append(gracz)
        self.pot = 0
        winner = self.gracze[0]
        czy_biora_udzial = self.czy_biora_udzial()
            
        if czy_biora_udzial == 'stop':
            return
        else: 
            self.pot = czy_biora_udzial

        #for gracz in self.gracze:
        #    gracz.karty = self.talia.rozdajKarty()

        for gracz in self.gracze_wyswietl:
            gracz.client_sock.sendall('0 \nzaczynam gre...\n\r\n\r\n')

        self.pot = self.runda()
        pom = []
        for gracz in self.gracze:
            if gracz not in pom and gracz.is_playing == True:
                pom.append(gracz)
        self.gracze = pom
        if len(self.gracze) != 1:

            for gracz in self.gracze_wyswietl:
                gracz.client_sock.sendall('0 przechodzmy do wymiany kart, kazdy postawil tyle samo ...\r\n\r\n')

            pom = []
            for gracz in self.gracze:
                if gracz not in pom and gracz.is_playing == True:
                    pom.append(gracz)
            self.gracze = pom

            if len(self.gracze) == 1:
                winner = self.gracze.pop()
                for gracz in self.gracze_wyswietl:
                    gracz.client_sock.sendall('0 \n\nroztrzygniecie rozdania ...\r\n\r\n')
                    gracz.client_sock.sendall('0 zwyciezca: ' + winner.name + ' wygrywa kredytow' + str(self.pot) + ', stan konta: ' + str(winner.kredyty) + ' kredytow\r\n\r\n')

            #self.najwyzszy_zaklad = 0
            for gracz in self.gracze:
                gracz.client_sock.sendall('0 #### ' + gracz.name + ' ####\r\n\r\n')
                gracz.wymien_karty(self.talia)
                gracz.sila,gracz.jaki_uklad = Evaluator.sila_reki(Evaluator.przygotuj_reke(gracz.karty))
                gracz.bet = 0
                gracz.called = [False, False]
                gracz.folded = False
                gracz.raised = False

            self.czy_breake = False

            gracz.client_sock.sendall('0 \ndruga runda...\n\r\n\r\n')
            self.pot = self.runda()

            gracz.client_sock.sendall('0 self.pot = ' + str(self.pot)+'\r\n\r\n')
            gracz.client_sock.sendall('0 przechodzmy do wylonienia zwyciezcy, kazdy postawil tyle samo ...\r\n\r\n')

            pom = []
            for gracz in self.gracze:
                if gracz not in pom and gracz.is_playing == True:
                    pom.append(gracz)
            self.gracze = pom

            for gracz in self.gracze_wyswietl:
                gracz.client_sock.sendall('0 \n\nobliczam sile rak graczy ...\r\n\r\n')

            for gracz in self.gracze:
                gracz.sila,gracz.jaki_uklad = Evaluator.sila_reki(Evaluator.przygotuj_reke(gracz.karty))

            for gracz in self.gracze_wyswietl:
                gracz.client_sock.sendall('0 \n\nwylaniam zwyciezce ...\r\n\r\n')

        print type(self.pot)
        print self.pot

        winner = self.gracze[0]
        #self.pot  = 0
        for gracz in self.gracze:
            if gracz.sila > winner.sila:
                winner = gracz
                print type(self.pot)
            print winner.kredyty
            print type(winner.kredyty)
        winner.kredyty += self.pot

        for gracz in self.gracze_wyswietl:
            gracz.client_sock.sendall('0 \n\nroztrzygniecie rozdania ...\r\n\r\n')
            gracz.client_sock.sendall('0 zwyciezca: ' + winner.name + ' wygrywa kredytow ' + str(self.pot) + ', stan konta: ' + str(winner.kredyty) + ' kredytow\r\n\r\n')

        gracz.client_sock.sendall('0 \n\npodglad rak graczy ...\r\n\r\n')
        for gracz in self.gracze_wyswietl:
            for g in self.gracze:
                gracz.client_sock.sendall('0 '+g.name+': ' + Evaluator.uklad2(Evaluator.przygotuj_reke(g.karty)) + ' sila = ' + str(g.sila)+' ukad: '+g.jaki_uklad+'\r\n\r\n')