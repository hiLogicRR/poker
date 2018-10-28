import random

class TaliaKart(object):
    talia = []
    wylosowane = []

    def __init__(self):
        for i in range(2,15):
            self.talia.append(([0,0,0,1], i))
            self.talia.append(([0,0,1,0], i))
            self.talia.append(([0,1,0,0], i))
            self.talia.append(([1,0,0,0], i))

    def losujKarte(self):
        i = random.randint(0,51)
        while i in self.wylosowane:
            i = random.randint(0,51)
        self.wylosowane.append(i)
        return self.talia[i]

    def rozdajKarty(self):
        rozdanie = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for i in range(0,5):
            karta = self.losujKarte()
            kolor = karta[0].index(1)
            rozdanie[karta[1]-2][kolor] = 1
        #self.noweRozdanie()
        return rozdanie

    def wymienKarty(self, iloscKarty):
        i = 0
        while i < iloscKarty:
            self.losujKarte()

    def noweRozdanie(self):
        self.wylosowane = []

##rozdaj_karty()->wymienKarty()->noweRozdanie()