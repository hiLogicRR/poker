from MyDatabase import MyDatabase
class BaseProtocol(object):
    
    zalogowano = False
    db = MyDatabase()
    koniec = "\r\n\r\n"
    nazwa_uzytkownika = ""
    
    def GlownaMetoda(self,data):
        if data: 
                if data !='/n':
                    data = " ".join(data.split())
                    data = data.split(' ')
                if 'LOGIN' in data:
                    #LOGIN
                    if len(data) == 2:
                        return "1 " + self.Login(data[1])
                    elif len(data) == 1:
                        return "1 brak nazwy uzytkownika\r\n\r\n"
                    else:
                        return "1 niepoprawna ilosc parametrow\r\n\r\n"
                    #END LOGIN
                elif 'PASSWORD' in data:
                    #PASSWORD
                    if len(data) == 2:
                        return "1 " + self.Password(data[1])
                    elif len(data) == 1:
                        return "1 brak nazwy uzytkownika\r\n\r\n"
                    else:
                        return "1 niepoprawna ilosc parametrow\r\n\r\n"
                    #END PASSWORD
                elif 'CASH' in data:
                    #CASH
                    if len(data) == 1:
                        return "1 " + self.Cash()
                    else:
                        return "1 nie poprawna ilosc parametrow\r\n\r\n"
                    #END CASH
                elif 'LOGOUT' in data:
                    #LOGOUT
                    if len(data) == 1:
                        return "1 " + self.Logout()
                    else:
                        return "1 nie poprawna ilosc parametrow\r\n\r\n"
                    #END LOGOUT
                elif 'COMMANDS' in data:
                    #COMMANDS
                    return "1 " + self.Commands()
                    #END COMMANDS 
                elif 'JOIN' in data:
                    #JOIN
                    return self.Join()
                    #END JOIN
                elif 'REGISTER' in data:
                    if len(data) == 3:
                        return "1 " + self.Register(data[1],data[2])
                    else:
                        return "1 nie poprawna ilosc parametrow\r\n\r\n"
                elif 'EXIT' in data:
                    if len(data) == 1:
                        return "2 " + self.Exit()
                else:
                    return "1 Niepoprawna komenda\n" + self.Commands()
        else:
            return "1 Niepoprawna komenda\n\n" + self.Commands()

    def Join(self):
        #if self.zalogowano == True:
        return 'JOIN'
        #else:
            #return "1 komenda dostepna po zalogowaniu" + self.koniec
    
    def Exit(self):
        return 'GOOD BYE'+self.koniec

    def Login(self, login):
        if self.zalogowano == False:
            poprawny_login = self.db.sprawdz_czy_uzytkownik_o_podanym_loginie_istnieje(login)
            if poprawny_login == True:
                self.nazwa_uzytkownika = login
                return "podaj haslo dla uzytkownika " + self.nazwa_uzytkownika + self.koniec
            else:
                return "uzytkownik o podanej nazwie nie istnieje." + self.koniec
        else:
            return "jestes juz zalogowany jako " + self.nazwa_uzytkownika + " !\nkomenda niedostepna." + self.koniec
    def Password(self,password):
        if self.nazwa_uzytkownika == "":
            return "nie podano loginu "+ self.koniec
        elif self.zalogowano == True:
            return "jestes juz zalogowany jako " + self.nazwa_uzytkownika + " !\nkomenda niedostepna." + self.koniec
        else:
            poprawne_haslo = self.db.sprawdz_czy_haslo_pasuje_do_loginu(self.nazwa_uzytkownika, password)
            if poprawne_haslo == True:
                print 'flaga na zalogowano'
                self.zalogowano = True
                return "witaj " +self.nazwa_uzytkownika + self.koniec
            else:
                return "niepoprawne haslo." + self.koniec

    def Cash(self):
        if self.zalogowano == False:
            return "komenda dostepna po zalogowaniu" + self.koniec
        else:
            return "stan konta "+str(self.db.stan_konta(self.nazwa_uzytkownika)) + self.koniec
            
    def Logout(self):
        if self.zalogowano == False:
            return "komenda dostepna po zalogowaniu" + self.koniec
        else:
            login = self.nazwa_uzytkownika
            self.nazwa_uzytkownika = ""
            self.zalogowano = False
            return "do widzenia " + login + self.koniec

    def Commands(self):
        return "LOGIN nazwa_uzytkownika\nPASSWORD haslo\nCASH\nLOGOUT\nREGISTER login haslo\nEXIT\nJOIN" + self.koniec

    def Register(self, login, haslo):
        if self.zalogowano == False:
            if self.db.dodaj_uzytkownika(login,haslo) == True:
                return "dodano uzytkownika "+ login + self.koniec
            else:
                return "nazwa uzytkownika zajeta" + self.koniec
        else:
            return "komenda niedostepna" + self.koniec


