from operator import itemgetter
import random
from TaliaKart import TaliaKart
import time

def ilosc_danej_karty(karta):
    return karta.count(1)

def kolorKarty(karta):
    if(karta[0] == [0, 0, 0, 1]):#dzownek
        return 1
    elif(karta[0] == [0, 0, 1, 0]):#czerwo
        return 2
    elif(karta[0] == [0, 1, 0, 0]):#wino
        return 4
    elif(karta[0] == [1, 0, 0, 0]):#trefl
        return 8

def zapis_koloru_karty(kolor_str):
    if(kolor_str == 'dzownek'):#dzownek
        return [0, 0, 0, 1]
    elif(kolor_str == 'czerwo'):#czerwo
        return [0, 0, 1, 0]
    elif(kolor_str == 'wino'):#wino
        return [0, 1, 0, 0]
    elif(kolor_str == 'trefl'):#trefl
        return [1, 0, 0, 0]

def kolorKarty2(karta):
    kolor = ''
    ilosc_wystapien = karta[0].count(1)
    i = 0
    if(karta[0][3] == 1):#dzownek
        kolor += 'dzwonek '
        i += 1
        if ilosc_wystapien > i:
            kolor += (znak_karty(karta[1])) + ' '
    if(karta[0][2] == 1):#czerwo
        kolor += 'czerwo '
        i += 1
        if ilosc_wystapien > i:
            kolor += (znak_karty(karta[1])) + ' '
    if(karta[0][1] == 1):#wino
        kolor += 'wino '
        i += 1
        if ilosc_wystapien > i:
            kolor += (znak_karty(karta[1])) + ' '
    if(karta[0][0] == 1):#trefl
        kolor += 'trefl '
        i += 1
    kolor = kolor.replace('  ', ' ')
    return kolor

def kolor_str_to_int(kolor_str):
    if kolor_str == 'trefl':
        return 0
    elif kolor_str == 'wino':
        return 1
    elif kolor_str == 'czerwo':
        return 2
    elif kolor_str == 'dzwonek':
        return 3

def czy_ilosc_kart_do_wymiany_w_zakresie(ilosc_kart_do_wymiany_int):
    if isinstance(ilosc_kart_do_wymiany_int, int) and ilosc_kart_do_wymiany_int in range(0, 6):
        return True
    else:
        return False

def znak_karty(wartoscKarty):
    return{
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A'
        }[wartoscKarty]+' '

def wartosc_karty(znak_karty):
    return{
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
        }[znak_karty]

def uklad2(kartyGracza):
    uklad = ''
    for i in kartyGracza:
        uklad += znak_karty(i[1]) + str(kolorKarty2(i))
    uklad = uklad.replace('  ', '')
    return uklad

def przygotuj_reke(reka):
    kartyGracza = []
    wartoscKarty = 2
    for i in reka:
        iloscKarty = ilosc_danej_karty(i)
        if iloscKarty > 0:
            kartyGracza.append((i, wartoscKarty))
        wartoscKarty += 1
    return kartyGracza

def wysoka_karta(wartoscKarty):
    return wartoscKarty*0.1

def para(wartoscKarty):
    return 32+wartoscKarty

def trojka(wartoscKarty):
    return 96+(wartoscKarty)

def strit(wartoscNajwyszejKarty):
    return 128+(wartoscNajwyszejKarty)

def kolor(wartoscNajwyzszejKarty):
    return 160+(wartoscNajwyzszejKarty)#max 174

def full(wartoscKartyDwojka, wartoscKartyTrojka):
    return 192+(wartoscKartyTrojka+(wartoscKartyTrojka-wartoscKartyDwojka))#min 182

def kareta(wartoscKarty):
    return 224+(wartoscKarty)

def poker(wartoscNajwyzszejKarty):
    return 256+(wartoscNajwyzszejKarty)

def sila_reki(kartyGracza):
    #print uklad(kartyGracza)
    kartyGracza.sort(key=itemgetter(1), reverse=True)
    iloscRoznychKart = len(kartyGracza)
    if iloscRoznychKart == 5:
        i = 1
        czyKolor = True
        for i in range(1,5):
            if kolorKarty(kartyGracza[i]) != kolorKarty(kartyGracza[i-1]):
                czyKolor = False
                break
        if czyKolor is False:
            if kartyGracza[0][1] == 14 and kartyGracza[4][1] == 2 and kartyGracza[1][1]-kartyGracza[4][1] == 3:
                #print 'strit ' + uklad(kartyGracza)
                return strit(kartyGracza[1][1]),'strit'
            elif kartyGracza[0][1] - kartyGracza[4][1] == 4:
                #print 'strit ' + uklad(kartyGracza)
                return strit(kartyGracza[0][1]),'strit'
            else:
                print 'wysoka karta ' + znak_karty(kartyGracza[0][1])
                return wysoka_karta(kartyGracza[0][1]),'wysoka karta'
        else:
            if kartyGracza[0][1] - kartyGracza[4][1] != 4:
                #print 'kolor ' + uklad(kartyGracza)
                return kolor(kartyGracza[0][1]),'kolor'
            else:
                print 'poker ' + uklad(kartyGracza)
                if kartyGracza[0][1] == 14 and kartyGracza[4][1] == 2:
                    return poker(kartyGracza[1][1])
                return poker(kartyGracza[0][1]),'poker'
    elif iloscRoznychKart == 2:
        kartyGracza.sort(key=s, reverse=True)
        if kartyGracza[0][0].count(1) == 3:
            #print 'full ( trojka '+znak_karty(kartyGracza[0][1])+" para "+znak_karty(kartyGracza[1][1])+" )"
            return full(kartyGracza[1][1], kartyGracza[0][1]),'full'
        else:
            #print 'kareta '+znak_karty(kartyGracza[0][1])+" wysoka karta "+znak_karty(kartyGracza[1][1])
            return kareta(kartyGracza[0][1]) + wysoka_karta(kartyGracza[1][1]),'kareta'
    else:
        sila = 0
        for i in kartyGracza:
            if i[0].count(1) == 2:
                #print 'para '+znak_karty((i[1]))
                sila += para(i[1])
            elif i[0].count(1) == 3:
                #print 'trojka '+znak_karty((i[1]))
                sila += trojka(i[1])
        for i in kartyGracza:
            if i[0].count(1) == 1:
                #print 'wysoka karta '+znak_karty((i[1]))
                sila += wysoka_karta(i[1])
                break
        return sila ,'para,trojka'
def ma_karte(karta_str, reka_str):
    if karta_str in reka_str:
        return True
    return False

def ladne_karty(przygotowane_karty):
    gora = '.---------.'
    bok = '|        |' # 1 + 7 + 1
    dol =  '.---------.'
    linia1 = '\t'
    linia2 = '\t'
    linia3 = '\t'
    linia4 = '\t'
    linia5 = '\t'
    linia6 = '\t'
    linia7 = '\t'
    for karta in przygotowane_karty:
        kolor = str(kolorKarty2(karta))
        wartosc = str(znak_karty(karta[1]))
        start = int((10 - len(kolor))/2)+1
        koniec = 10-start
        if len(kolor) % 2 == 0:
            koniec += 1
        if wartosc != '10 ':
            linia1 += gora + '\t'
            linia2 += bok[:1] + wartosc + bok[2:] + '\t'
            linia3 += bok[:1] + ' ' + bok[1:] + '\t'
            linia4 += bok[:start] + kolor + bok[koniec:] + '\t'
            linia5 += bok[:1] + ' ' + bok[1:] + '\t'
            linia6 += bok[:7] + wartosc + bok[8:] + '\t'
            linia7 += dol + '\t'

        else:
            linia1 += gora + '\t'
            linia2 += bok[:1] + wartosc + bok[3:] + '\t'
            linia3 += bok[:1] + ' ' + bok[1:] + '\t'
            linia4 += bok[:start] + kolor + bok[koniec:] + '\t'
            linia5 += bok[:1] + ' ' + bok[1:] + '\t'
            linia6 += bok[:6] + wartosc + bok[8:] + '\t'
            linia7 += dol + '\t'
        #print str(linia1 + '\n' + linia2 + '\n' + linia3 + '\n' + linia4 + '\n' + linia5 + '\n' + linia6 + '\n' + linia7)

    return str(linia1 + '\n' + linia2 + '\n' + linia3 + '\n' + linia4 + '\n' + linia5 + '\n' + linia6 + '\n' + linia7)



reka = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1], [0, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

reka2 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 1], [0, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

pustaReka = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


