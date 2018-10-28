from Gracz import Gracz

class StolDoGry(object):
    def __init__(self,gracz,ilosc_miejsc_przy_stole):
        self.Gracz = [gracz]
        self.Ilosc_miejsc_przy_stole = ilosc_miejsc_przy_stole
        self.Dostepne_miejsca_przy_stole = self.Ilosc_miejsc_przy_stole - 1
        self.Obecni_gracze_przy_Stole = 1
        self.Czy_Gra = False

    def Dolacz_gracza(self,gracz):
        self.Gracz.append(gracz)
        self.Dostepne_miejsca_przy_stole -= 1
        self.Obecni_gracze_przy_Stole += 1


