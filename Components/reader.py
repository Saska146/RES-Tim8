import re

# from load_balancer import uzmiVrednsotiPoKodu, nadjiWorkera
from Model.models import CodeEnum
from database import readDataByCode, readByDateAndCode


def PrikaziPodatkeZaKod():  # pragma: no cover
    izabran_kod = IzaberiKod()
    # worker = nadjiWorkera()
    # TODO: Implement
    #  podaci = worker.uzmiVrednsotiPoKodu()
    podaci = readDataByCode(izabran_kod)
    IspisiPodatke(podaci, f'Podaci za kod {izabran_kod}:')
    for podatak in podaci:
        print(f'\t{podatak}')


def PrikaziPodatkePoIstoriji():  # pragma: no cover
    interval1, interval2, interval3, interval4, izabran_kod = UzmiIstorijeskeVrednsoti()
    # worker = nadjiWorkera()
    # TODO: Implement
    #  podaci = worker.UzmiIstorijeskeVrednsoti()
    podaci = readByDateAndCode(interval1, interval2, interval3, interval4, izabran_kod)
    for podatak in podaci:
        print(podatak)


def UzmiIstorijeskeVrednsoti():
    interval1 = UzmiInterval('pocetni')
    interval2 = UzmiInterval('krajnji')
    interval3 = UzmiSatnicu('pocetni')
    interval4 = UzmiSatnicu('krajnji')
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
        print(f'Unesite {tip_intervala} interval u formatu YYYY.MM.DD HH:MM:SS')
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
    # PrikaziPodatkePoIstoriji()
    PrikaziPodatkeZaKod()
