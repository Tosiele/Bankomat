import sys
import numpy as np

plik_in = 'kontaLimityWyplat.txt'
#do testu jest to osobny plik, w wersji ostatecznej byłby to ten sam plik
plik_out = 'kontaLimityWyplatPo.txt'

saldo_bankomatu = 10000

saldo = 0
ile_pieniedzy = 0
limit_wyplat = 0

#--------------------------------------------------------------------------------

def pobierz_dane_kont(plik_wejsciowy):
    """pobiera dane kont z pliku"""
    with open(plik_wejsciowy, encoding="utf-8") as plik:
        dane = plik.read()

    lista = dane.split('\n') # podziel po liniach
    konta = [item.split(' ') for item in lista] # podziel po kolumnach
    konta.pop()

    return konta


def indeks_konta(nr_karty_input):
    """pobiera indeks konta na podstawie numeru karty"""
    konta = pobierz_dane_kont(plik_in)

    lista_nr = []
    for konto in konta:
        lista_nr.append(int(konto[1])) #tworzę listę numerów kart

    if nr_karty_input in lista_nr: #szukamy numeru karty w liście numerów kart
        print("Poprawny numer karty. Można kontynuować",
              "\n------------------------------------------------------------")

        lista = np.array(konta)
        #bierzemy indeks linijki z kontem na którym pracujemy
        return np.argwhere(lista == str(nr_karty_input))[0][0]

    print("Niepoprawny numer karty. Odmowa dostępu.\n")
    sys.exit()


def dane_konta(lista_kont, indeks):
    """zapisuje dane konta w zmiennych globalnych"""
    global saldo
    global ile_pieniedzy
    global limit_wyplat

    saldo = int(lista_kont[indeks][2])
    ile_pieniedzy = int(lista_kont[indeks][3])
    limit_wyplat = int(lista_kont[indeks][4])

    return(saldo, ile_pieniedzy, limit_wyplat)


def wplata():
    """obsługuje operację wpłaty do bankomatu"""
    global saldo
    global ile_pieniedzy
    global saldo_bankomatu

    kwota = input("Jaką kwotę chcesz wpłacić na konto: ")
    if kwota.isdigit(): #sprawdzamy czy użytkownik podał liczbę

        kwota = int(kwota)
        ile_pieniedzy += kwota
        saldo += kwota
        saldo_bankomatu += kwota
        print("Wpłacenie powiodło się.")

    else:
        print("Wpłacenie nie powiodło się. Niepoprawna wartosć wejsciowa.")


def wyplata():
    """obsługuje operację wypłaty z bankomatu"""
    global saldo
    global ile_pieniedzy
    global saldo_bankomatu
    global limit_wyplat

    kwota = input("Jaką kwotę chcesz wypłacić z konta: ")
    if kwota.isdigit(): #sprawdzamy czy użytkownik podał liczbę
        kwota = int(kwota)
        if ile_pieniedzy - kwota >= 0: #możemy wypłacić tylko jak mamy pieniądze
            if saldo_bankomatu - kwota >= 0: #możemy wypłacić tylko jak bankomat ma pieniądze
                if limit_wyplat - kwota >= 0:
                    ile_pieniedzy -= kwota
                    saldo -= kwota
                    saldo_bankomatu -= kwota
                    limit_wyplat -= kwota
                    print("Wypłacenie powiodło się.")
                else: print("Wypłacenie nie powiodło się, osiągnięto limit wypłat.")
            else: print("Wypłacenie nie powiodło się, brak pieniędzy w bankomacie.")
        else: print("Wypłacenie nie powiodło się, za mało srodków na koncie.")
    else: print("Wypłacenie nie powiodło się. Niepoprawna wartosć wejsciowa.")


def stan_konta():
    """wypisuje saldo i ilosć pieniędzy konta"""
    print("Ilosc pieniędzy na twoim koncie wynosi: ", ile_pieniedzy)
    print("Saldo twojego konta wynosi: ", saldo)


def zapisz_do_pliku(plik_wyjsciowy, konta):
    """zapisuje zmienione dane w nowym pliku"""

    with open(plik_wyjsciowy, "w", encoding="utf-8") as plik:
        for konto in konta: #idziemy po kolei po kontach
            for element in konto:
                plik.write(str(element) + ' ')
            plik.write('\n')
#--------------------------------------------------------------------------------

def main():
    """główna pętla programu"""
    konta = pobierz_dane_kont(plik_in)

    nr_karty = int(input("\nPodaj numer karty do weryfikacji: "))
    index = indeks_konta(nr_karty)

    global saldo
    global ile_pieniedzy
    global limit_wyplat
    saldo, ile_pieniedzy, limit_wyplat = dane_konta(konta, index)

    while True:
        print("---------------------------------------------------------------")
        print("\nCo chcesz zrobić? \n1.Wpłata \n2.Wypłata \n3.Stan konta \n4.Wyjdź\n")
        opcja = int(input())
        print("---------------------------------------------------------------")

        if opcja == 1:
            wplata()
        elif opcja == 2:
            wyplata()
        elif opcja == 3:
            stan_konta()
        elif opcja == 4:
            break
        else:
            print("\nWybierz opcję z listy.")

    konta[index][2] = saldo
    konta[index][3] = ile_pieniedzy

    zapisz_do_pliku(plik_out, konta)

#--------------------------------------------------------------------------------
main()
