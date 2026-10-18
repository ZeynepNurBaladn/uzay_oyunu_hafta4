import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from uzay_oyunu.akis import yakit_gostergesi
from uzay_oyunu.araclar import hamle_sayaci

GALAKSI_YOLU = Path(__file__).with_name("galaksi.json")
TUKETIM = 5


# Görev 1: saf fonksiyonlar
def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:

    esyalar = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("hiperdrive")
    if copilot:
        esyalar.append("yetenekli bir pilot")
    return ("Sende: " + ", ".join(esyalar)) if esyalar else ""


def hedef_menusu(hedefler: list[str]) -> str:
    
    satirlar = ["Nereye gitmek istersin?"]
    satirlar += [f"[{no}] {hedef}" for no, hedef in enumerate(hedefler, start=1)]
    return "\n".join(satirlar)


# Görev 3: galaksiyi veriden kur
def galaksi_kur(
    gezegenler: list[str],
    baglantilar: dict[str, list[str]],
    baslangic: str,
    **kwargs: Any,
) -> dict[str, Any]:
    
    if baslangic not in gezegenler:
        raise ValueError(f"Başlangıç gezegeni listede yok: {baslangic!r}")
    return {
        "gezegenler": gezegenler,
        "baglantilar": baglantilar,
        "konum": baslangic,
        "yakit": kwargs.get("yakit", 50),
    }


def galaksi_yukle(yol: Path = GALAKSI_YOLU) -> dict[str, Any]:
    
    with open(yol, encoding="utf-8") as dosya:
        veri = json.load(dosya)
    return galaksi_kur(**veri)



def gezegen_olayi(gezegen: str, durum: dict[str, bool]) -> str:
    
    if gezegen == "dünya" and not durum["credits"]:
        durum["credits"] = True
        return "Dünya'da kredi kazandın."
    if gezegen == "centauri" and not durum["copilot"]:
        durum["copilot"] = True
        return "Centauri'de yetenekli bir pilot buldun."
    if gezegen == "orion" and durum["credits"] and not durum["engines"]:
        durum["engines"] = True
        return "Orion'da kredinle hiperdrive aldın."
    return ""


def travel(
    galaksi: dict[str, Any],
    girdi: Callable[[str], str] = input,
    cikti: Callable[[str], None] = print,
) -> str:
    
    durum = {"credits": False, "engines": False, "copilot": False}
    hamle = hamle_sayaci()
    gosterge = yakit_gostergesi(galaksi["yakit"], TUKETIM)
    gezegen = galaksi["konum"]
    toplam = 0
    sonuc = ""

    while not sonuc:
        hedefler = galaksi["baglantilar"][gezegen]
        cikti(hedef_menusu(hedefler))
        secim = girdi("> ").strip()
        if not secim.isdigit() or not 1 <= int(secim) <= len(hedefler):
            cikti("Geçersiz seçim, tekrar dene.")
            continue

        try:
            kalan = next(gosterge)
        except StopIteration:
            cikti("Yakıtın bitti, uzayda sürükleniyorsun…")
            sonuc = "kaybetti"
            break

        toplam = hamle()
        gezegen = hedefler[int(secim) - 1]
        cikti(f"{gezegen} gezegenine vardın. Kalan yakıt: {kalan}")

        mesaj = gezegen_olayi(gezegen, durum)
        if mesaj:
            cikti(mesaj)
        envanter = envanter_metni(**durum)
        if envanter:
            cikti(envanter)

        if gezegen == "kara_delik":
            if all(durum.values()):
                cikti("Hiperdrive ve pilotunla kara delikten geçtin. Kazandın!")
                sonuc = "kazandi"
            else:
                cikti("Kara delik seni yuttu…")
                sonuc = "kaybetti"

    cikti(f"Oyunu {toplam} hamlede bitirdin!")
    return sonuc

if __name__ == "__main__":
    travel(galaksi_yukle())