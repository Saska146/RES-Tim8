import re

# from load_balancer import uzmiVrednsotiPoKodu, nadjiWorkera
from models import code


def PrikaziPodatkeZaKod():  # pragma: no cover
    izabran_kod = IzaberiKod()
    # worker = nadjiWorkera()
    # TODO: Implement
    #  podaci = worker.uzmiVrednsotiPoKodu()
    podaci = []
    IspisiPodatke(podaci, f'Podaci za kod {izabran_kod}:')


def PrikaziPodatkePoIstoriji():  # pragma: no cover
    interval1, interval2, izabran_kod = UzmiIstorijeskeVrednsoti()
    # worker = nadjiWorkera()
    # TODO: Implement
    #  podaci = worker.UzmiIstorijeskeVrednsoti()
    podaci = []
    IspisiPodatke(podaci, f'Podaci za kod {izabran_kod} u intervalu {interval1} - {interval2}:')


# TODO: Test
def UzmiIstorijeskeVrednsoti():
    interval1 = UzmiInterval('pocetni')
    interval2 = UzmiInterval('krajnji')
    izabran_kod = code[PrikaziMeni(code) - 1]
    return interval1, interval2, izabran_kod


# TODO: Test
def IzaberiKod():
    izabran_kod_id = PrikaziMeni(code)
    izabran_kod = code[izabran_kod_id - 1]
    return izabran_kod


# TODO: Test
def UzmiInterval(tip_intervala):
    while True:
        print(f'Unesite {tip_intervala} interval u formatu YYYY.MM.DD HH:MM:SS')
        interval = input()
        if not ValidirajInterval(interval):
            continue

        return interval


# TODO: Test
def ValidirajInterval(interval):
    if re.match('^[0-9]{4}.[0-1]?[0-9].[0-1]?[0-9] [0-9]{2}:[0-9]{2}:[0-9]{2}$', interval):
        return True

    print('Pogresan format unet.')
    return False


# TODO: Test
def PrikaziMeni(opcije):
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
def ValidirajOpciju(opcija, broj_opcija):
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
    pass
    # Pozivi za testiranje da li rade metode
    # PrikaziPodatkePoIstoriji()
    # PrikaziPodatkeZaKod()
