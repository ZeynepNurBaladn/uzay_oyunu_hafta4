

import time
from collections.abc import Callable, Iterable, Iterator
from functools import lru_cache
from itertools import islice


# Görev 1: Fibonacci üreteci
def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Görev 2: Yakıt göstergesi
def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:

    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit


# Görev 3: Seyir defteri boru hattı
def satirlari_oku(yol: str) -> Iterator[str]:

    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                yield satir


def ayristir(satirlar: Iterable[str]) -> Iterator[tuple[str, str, int]]:
    
    for satir in satirlar:
        kaynak, _, hedef, yakit = satir.split()
        yield kaynak, hedef, int(yakit)


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]], esik: int
) -> Iterator[tuple[str, str, int]]:
    
    for kayit in kayitlar:
        if kayit[2] > esik:
            yield kayit


# Görev 4: Önbellekli rota sayacı 
def rota_sayaci(baglantilar: dict[str, list[str]]) -> Callable[[str, int], int]:

    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """gezegen'den başlayan, tam `adim` yolculukluk farklı rotaların sayısı."""
        if adim == 0:
            return 1
        return sum(rota_sayisi(hedef, adim - 1) for hedef in baglantilar[gezegen])

    return rota_sayisi


def rota_sayaci_onbelleksiz(
    baglantilar: dict[str, list[str]],
) -> Callable[[str, int], int]:

    def rota_sayisi(gezegen: str, adim: int) -> int:
        if adim == 0:
            return 1
        return sum(rota_sayisi(hedef, adim - 1) for hedef in baglantilar[gezegen])

    return rota_sayisi


def zamanlayici(aralik:float) -> Iterator[bool]:
    son=time.time()
    while True:
        simdi=time.time()
        if simdi-son>=aralik:
            son=simdi
            yield True
        else:
            yield False
if __name__=="__main__":
    tik=zamanlayici(2.0)
    tak=zamanlayici(5.0)
    baslangic=time.time()
    while time.time()-baslangic<10:
        if next(tik):
            print("tik")
        if next(tak):
            print("tak")