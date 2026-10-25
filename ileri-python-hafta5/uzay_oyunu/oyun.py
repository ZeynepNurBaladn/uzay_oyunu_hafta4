
from __future__ import annotations

from typing import Any, Callable

from uzay_oyunu.akis import yakit_gostergesi
from uzay_oyunu.dekoratorler import log_cagri, sinirla
from uzay_oyunu.komutlar import KOMUTLAR

def yolculuk(gezegen: str, hiz: int = 1) -> str:
    """Yolculuğu betimler (kendi Hafta 1-3 `yolculuk` fonksiyonunuzla değiştirin)."""
    return f"{gezegen} hiz={hiz}"


BAGLANTILAR = {
    "dünya": ["centauri", "sirius"],
    "centauri": ["dünya", "orion"],
    "sirius": ["orion", "dünya", "kara_delik"],
    "orion": ["centauri", "sirius"],
    "kara_delik": ["sirius"],
}


@log_cagri
def galaksi_kur() -> dict[str, Any]:
   
    return {
        "konum": "dünya",
        "baglantilar": {g: list(k) for g, k in BAGLANTILAR.items()},
        "credits": 100,
        "engines": 1,
        "copilot": None,
        "yakit": 100,
    }


@log_cagri
def hedef_menusu(hedefler: list[str], giris: Callable[[str], str] = input) -> str:
    
    print("Nereye gitmek istersin?")
    for sira, hedef in enumerate(hedefler, start=1):
        print(f"[{sira}] {hedef}")
    return giris("> ")


@sinirla(0, 100)
def yakit_harca(miktar: int) -> int:
    
    return 100 - miktar


def _hedef_coz(secim: str, hedefler: list[str]) -> str | None:
   
    if secim.isdigit() and 1 <= int(secim) <= len(hedefler):
        return hedefler[int(secim) - 1]
    return secim if secim in hedefler else None


def travel(
    galaksi: dict[str, Any],
    giris: Callable[[str], str] = input,
    cikti: Callable[[str], None] = print,
    tuketim: int = 5,
) -> str:
    
    gosterge = yakit_gostergesi(galaksi["yakit"], tuketim)
    while True:
        hedefler = galaksi["baglantilar"][galaksi["konum"]]
        secim = hedef_menusu(hedefler, giris).strip()
        if secim in KOMUTLAR:
            fonk, _ = KOMUTLAR[secim]
            cikti(fonk(galaksi))
            continue
        if secim == "cik":
            return "cikis"
        hedef = _hedef_coz(secim, hedefler)
        if hedef is None:
            cikti("Geçersiz seçim.")
            continue
        try:
            galaksi["yakit"] = next(gosterge)
        except StopIteration:
            cikti("Yakıtın bitti, uzayda sürükleniyorsun…")
            return "kayip"
        galaksi["konum"] = hedef
        cikti(yolculuk(hedef))
