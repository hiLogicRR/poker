import pyodbc

class MyDatabase(object):
    
    def __init__(self):
        self.connection = pyodbc.connect('Driver={SQL Server}; Server=KOM-KOMPUTER; Database=poker; Trusted_Connection=yes;')

    def zamknijPolaczenie(self):
        self.connection.close()

    def sprawdz_czy_uzytkownik_o_podanym_loginie_istnieje(self, login):
        cursor = self.connection.cursor()
        row = cursor.execute("SELECT nazwa_uzytkownika FROM gracze WHERE nazwa_uzytkownika='"+login+"'").fetchone()
        if(row == None):
            return False
        else:
            return True

    def sprawdz_czy_haslo_pasuje_do_loginu(self, login, haslo):
        cursor = self.connection.cursor()
        row = cursor.execute("SELECT haslo FROM gracze WHERE nazwa_uzytkownika='"+login+"' AND haslo='"+haslo+"'").fetchone()
        if(row == None):
            return False
        else:
            return True

    def stan_konta(self, login):
        cursor = self.connection.cursor()
        row = cursor.execute("SELECT stan_konta FROM gracze WHERE nazwa_uzytkownika='"+login+"'").fetchone()
        return row.stan_konta

    #niby dziala, ale sie zacina w petli, do sprawdzenia
    def dodaj_uzytkownika(self, login, haslo):
        if self.sprawdz_czy_uzytkownik_o_podanym_loginie_istnieje(login) == True:
            return False
        else:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO gracze (nazwa_uzytkownika, haslo, stan_konta) VALUES ('"+login+"', '"+haslo+"', 0)")
            self.connection.commit()
            return True