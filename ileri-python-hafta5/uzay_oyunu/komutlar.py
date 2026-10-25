# Görev4

from __future__ import annotations
from typing import Any, Callable

Durum = dict[str, Any]

KOMUTLAR: dict[str, tuple[Callable[[Durum], str], str]] = {}


def komut(ad: str, aciklama: str = "") -> Callable[[Callable], Callable]:
  
    def dekorator(fonk: Callable[[Durum], str]) -> Callable[[Durum], str]:
        if ad in KOMUTLAR:
            raise ValueError(f"'{ad}' komutu zaten kayıtlı")
        KOMUTLAR[ad] = (fonk, aciklama)
        return fonk

    return dekorator


@komut("yardim", "komutları listeler")
def yardim(durum: Durum) -> str:

    return "\n".join(f"{ad} {aciklama}" for ad, (_, aciklama) in sorted(KOMUTLAR.items()))


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: Durum) -> str:

    pilot = durum["copilot"] or "yok"
    return f"credits: {durum['credits']}, engines: {durum['engines']}, copilot: {pilot}"


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: Durum) -> str:

    return ", ".join(durum["baglantilar"][durum["konum"]])
