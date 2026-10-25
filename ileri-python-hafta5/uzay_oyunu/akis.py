# Hafta 4

from __future__ import annotations

from functools import lru_cache
from typing import Callable, Iterable, Iterator


def fibonacci() -> Iterator[int]:
    
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    
    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit


def satirlari_oku(yol: str) -> Iterator[str]:
    
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                yield satir


def ayristir(satirlar: Iterable[str]) -> Iterator[tuple[str, str, int]]:
    
    for satir in satirlar:
        kaynak, sag = satir.split("->")
        hedef, yakit = sag.split()
        yield kaynak.strip(), hedef, int(yakit)


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]], esik: int
) -> Iterator[tuple[str, str, int]]:
   
    return (kayit for kayit in kayitlar if kayit[2] > esik)


def rota_sayaci_onbelleksiz(
    baglantilar: dict[str, list[str]],
) -> Callable[[str, int], int]:
   
    def rota_sayisi(gezegen: str, adim: int) -> int:
        if adim == 0:
            return 1
        return sum(rota_sayisi(komsu, adim - 1) for komsu in baglantilar[gezegen])

    return rota_sayisi


def rota_sayaci(baglantilar: dict[str, list[str]]) -> Callable[[str, int], int]:
   
    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        if adim == 0:
            return 1
        return sum(rota_sayisi(komsu, adim - 1) for komsu in baglantilar[gezegen])

    return rota_sayisi
