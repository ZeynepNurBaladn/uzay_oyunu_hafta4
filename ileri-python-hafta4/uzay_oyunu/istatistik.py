from functools import partial, reduce

Baglantilar = dict[str, list[str]]


# 1. yol: map, filter, reduce
def buyuk_harf(baglantilar: Baglantilar) -> list[str]:
    """map ile büyük harfli gezegen adları."""
    return list(map(str.upper, baglantilar))


def enaz_iki_baglanti(baglantilar: Baglantilar) -> list[str]:
    """filter ile en az iki bağlantısı olan gezegenler."""
    return list(filter(lambda g: len(baglantilar[g]) >= 2, baglantilar))


def toplam_baglanti(baglantilar: Baglantilar) -> int:
    """reduce ile toplam bağlantı sayısı."""
    return reduce(lambda toplam, g: toplam + len(baglantilar[g]), baglantilar, 0)


# 2. yol: liste üreteci, sum 
def harf_buyuk(baglantilar: Baglantilar) -> list[str]:
    return [g.upper() for g in baglantilar]


def iki_baglanti_enaz(baglantilar: Baglantilar) -> list[str]:
    return [g for g, komsular in baglantilar.items() if len(komsular) >= 2]


def baglanti_toplam(baglantilar: Baglantilar) -> int:
    return sum(len(komsular) for komsular in baglantilar.values())


# functools.partial
def yolculuk(hedef: str, hiz: int = 1) -> str:
    return f"{hedef} gezegenine hız {hiz} ile gidiliyor"

hizli_yolculuk = partial(yolculuk, hiz=3)