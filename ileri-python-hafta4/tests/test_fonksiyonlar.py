import json
from pathlib import Path

import pytest

from uzay_oyunu.araclar import en_bagli_gezegenler, hamle_sayaci, sure_olc
from uzay_oyunu.kayit import gorev_kaydi
from uzay_oyunu.oyun import (
    envanter_metni,
    galaksi_kur,
    galaksi_yukle,
    hedef_menusu,
    travel,
)

GALAKSI_JSON = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"


def sahte_girdi(*secimler):

    it = iter(secimler)
    return lambda _istem="": next(it)


# Görev1
def test_envanter_metni():
    assert envanter_metni(True, False, True) == "Sende: bol kredi, yetenekli bir pilot"


def test_envanter_metni_bos():
    assert envanter_metni(False, False, False) == ""


def test_hedef_menusu():
    assert hedef_menusu(["centauri", "sirius"]) == (
        "Nereye gitmek istersin?\n[1] centauri\n[2] sirius"
    )


def test_saf_fonksiyonlar(capsys):
    envanter_metni(True, True, True)
    hedef_menusu(["a"])
    assert capsys.readouterr().out == ""


# Görev2
def test_gorev_kaydi():
    metin = gorev_kaydi(
        "Kara deliğe atla",
        "Kredi kazan",
        "Pilot bul",
        "Hiperdrive al",
        oncelik="yüksek",
        sorumlu="Zeynep",
    )
    assert metin == (
        "[YÜKSEK] Kara deliğe atla\n"
        " 1. Kredi kazan\n"
        " 2. Pilot bul\n"
        " 3. Hiperdrive al\n"
        " sorumlu: Zeynep"
    )


def test_oncelik():
    assert gorev_kaydi("X", "yüksek") == "[NORMAL] X\n 1. yüksek"


# Görev3 
def test_galaksi():
    with open(GALAKSI_JSON, encoding="utf-8") as f:
        veri = json.load(f)
    g = galaksi_kur(**veri)
    assert (g["konum"], g["yakit"]) == ("dünya", 100)

def test_varsayilan_yakit_50():
    assert galaksi_kur(["mars"], {"mars": []}, "mars")["yakit"] == 50


def test_value_error():
    with pytest.raises(ValueError):
        galaksi_kur(["mars"], {"mars": []}, "venüs")


def test_baglanti_sirasi():
    g = galaksi_yukle()
    assert g["baglantilar"]["dünya"] == ["centauri", "sirius"]
    assert g["baglantilar"]["sirius"] == ["dünya", "orion", "kara_delik"]


# Görev5 
def test_hamle_sayaci():
    say = hamle_sayaci()
    assert [say(), say(), say()] == [1, 2, 3]


def test_en_bagli_gezegenler():
    assert en_bagli_gezegenler(galaksi_yukle()) == [
        "sirius",
        "centauri",
        "dünya",
        "orion",
        "kara_delik",
    ]


def test_sure_olc(capsys):
    olculu = sure_olc(en_bagli_gezegenler)
    g = galaksi_yukle()
    assert olculu(g) == en_bagli_gezegenler(g)
    assert "en_bagli_gezegenler" in capsys.readouterr().out


# travel()
def test_travel():
    satirlar: list[str] = []
    sonuc = travel(
        galaksi_yukle(),
        girdi=sahte_girdi("1", "1", "2", "2", "2", "3"),
        cikti=satirlar.append,
    )
    assert sonuc == "kazandi"
    assert satirlar[-1] == "Oyunu 6 hamlede bitirdin!"


def test_travel_hedef():
    g = galaksi_kur(["a", "b"], {"a": ["b"], "b": ["a"]}, "a", yakit=100)
    menuler: list[str] = []
    with pytest.raises(StopIteration):  # sahte girdi biter; yalnızca ilk menüye bakıyoruz
        travel(g, girdi=sahte_girdi("1"), cikti=menuler.append)
    assert menuler[0] == "Nereye gitmek istersin?\n[1] b"
