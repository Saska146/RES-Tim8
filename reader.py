import re

from models2 import CodeEnum
from database import readDataByCode, readByDateAndCode


def PrikaziPodatkeZaKod():  # pragma: no cover
    izabran_kod = IzaberiKod()
    podaci = readDataByCode(izabran_kod)
    IspisiPodatke(podaci, f'Podaci za kod {izabran_kod}:')


def PrikaziPodatkePoIstoriji():  # pragma: no cover
    interval1, interval2, interval3, interval4, izabran_kod = UzmiIstorijeskeVrednsoti()
    podaci = readByDateAndCode(interval1, interval2, interval3, interval4, izabran_kod)
    for podatak in podaci:
        print(podatak)


def UzmiIstorijeskeVrednsoti():
    interval1 = UzmiInterval('pocetni datum')
    interval2 = UzmiInterval('krajnji datum')
    interval3 = UzmiSatnicu('pocetno vreme')
    interval4 = UzmiSatnicu('krajnjo vreme')
    izabran_kod = CodeEnum(PrikaziMeni(list(CodeEnum)))
    return interval1, interval2, interval3, interval4, izabran_kod


# TODO: Test
def IzaberiKod():
    izabran_kod_id = PrikaziMeni(list(CodeEnum))
    izabran_kod = CodeEnum(izabran_kod_id)
    return izabran_kod_id


# TODO: Test
def UzmiInterval(tip_intervala):
    while True:
        print(f'Unesite {tip_intervala} interval u formatu YYYY.MM.DD')
        interval = input()
        if not ValidirajInterval(interval):
            continue

        return interval


# TODO: Test
def UzmiSatnicu(tip_intervala):
    while True:
        print(f'Unesite {tip_intervala} interval u formatu HH:MM:SS')
        interval = input()
        if not ValidirajSatnicu(interval):
            continue

        return interval


# TODO: Test
def ValidirajInterval(interval):
    if re.match('^[0-9]{4}.[0-1]?[0-9].[0-1]?[0-9]$', interval):
        return True

    print('Pogresan format unet.')
    return False


# TODO: Test
def ValidirajSatnicu(interval):
    if re.match('[0-9]{2}:[0-9]{2}:[0-9]{2}', interval):
        return True

    print('Pogresan format unet.')
    return False


# TODO: Test
def PrikaziMeni(opcije: list[str]):
    while True:
        print('\n')
        index = 0
        for opcija in opcije:
            index += 1
            print(f'{index}. {opcija}')
        choice = input()
        if ValidirajOpciju(choice, index):
            return int(choice)


# TODO: Test
def ValidirajOpciju(opcija: str, broj_opcija: int):
    try:
        if 1 <= int(opcija) <= broj_opcija:
            return True
        return False
    except:
        return False


# TODO: Test
def IspisiPodatke(podaci, text):
    print(text)
    for podatak in podaci:
        print(f'\t{podatak}')


if __name__ == '__main__':
    # Pozivi za testiranje da li rade metode
    #PrikaziPodatkeZaKod()
    PrikaziPodatkePoIstoriji()

