import inspect
from functools import partial
from itertools import islice, takewhile
from pathlib import Path

import pytest

from uzay_oyunu.akis import (
    ayristir,
    fibonacci,
    rota_sayaci,
    rota_sayaci_onbelleksiz,
    satirlari_oku,
    uzun_yolculuklar,
    yakit_gostergesi,
)
from uzay_oyunu.istatistik import (
    baglanti_toplam,
    buyuk_harf,
    enaz_iki_baglanti,
    harf_buyuk,
    hizli_yolculuk,
    iki_baglanti_enaz,
    toplam_baglanti,
)

from uzay_oyunu.oyun import galaksi_yukle, travel

SEYIR = str(Path(__file__).parent.parent / "veri" / "seyir.txt")


# Görev 1: fibonacci
def test_fibonacci_next():
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice():
    assert list(islice(fibonacci(), 12)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


def test_fibonacci_takewhile():
    assert list(takewhile(lambda x: x < 100, fibonacci()))[-1] == 89


def test_uretec_tek_kullanimlik():
    g = fibonacci()
    ilk = list(islice(g, 5))
    ikinci = list(islice(g, 5))
    assert ilk == [0, 1, 1, 2, 3]
    assert ikinci == [5, 8, 13, 21, 34]
    assert ilk != ikinci


# Görev 2: yakıt göstergesi
def test_yakit_gostergesi():
    assert list(yakit_gostergesi(100, 30)) == [70, 40, 10, 0]


def test_yakit_gostergesi_stopiteration():
    g = yakit_gostergesi(10, 10)
    assert next(g) == 0
    with pytest.raises(StopIteration):
        next(g)


def test_travel_yakit_bitince_kaybeder():
    satirlar: list[str] = []
    it = iter(["1"] * 25)  # dünya <-> centauri gidip gelme
    sonuc = travel(
        galaksi_yukle(), girdi=lambda _="": next(it), cikti=satirlar.append
    )
    assert sonuc == "kaybetti"
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in satirlar
    assert satirlar[-1] == "Oyunu 20 hamlede bitirdin!"


# Görev 3: boru hattı
def test_toplam_yakit():
    assert sum(y for _, _, y in ayristir(satirlari_oku(SEYIR))) == 88


def test_uzun_yolculuklar():
    kayitlar = ayristir(satirlari_oku(SEYIR))
    assert [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)] == [
        "sirius",
        "centauri",
        "orion",
        "kara_delik",
    ]


def test_satirlari_oku_yorum_ve_bos_satir_atlar(tmp_path):
    dosya = tmp_path / "s.txt"
    dosya.write_text("a -> b 1\n\n# yorum\nb -> c 2\n", encoding="utf-8")
    assert list(satirlari_oku(str(dosya))) == ["a -> b 1", "b -> c 2"]


def test_boru_hatti_tembel(tmp_path):
    dosya = tmp_path / "s.txt"
    dosya.write_text("a -> b 1\nb -> c 2\n", encoding="utf-8")
    hat = ayristir(satirlari_oku(str(dosya)))
    assert inspect.isgenerator(hat)
    assert next(hat) == ("a", "b", 1)  # tüm dosya okunmadan ilk kayıt geldi


# Görev 4: önbellekli rota sayacı
    say = rota_sayaci(galaksi_yukle()["baglantilar"])
    assert (say("dünya", 3), say("dünya", 10), say("dünya", 40)) == (
        9,
        2185,
        16832258606399,
    )

def test_rota_sayisi():
    say = rota_sayaci(galaksi_yukle()["baglantilar"])
    assert (say("dünya", 3), say("dünya", 10), say("dünya", 40)) == (
        9,
        2185,
        16832258606399,
    )

def test_onbellekli_ve_onbelleksiz():
    b = galaksi_yukle()["baglantilar"]
    assert rota_sayaci(b)("dünya", 12) == rota_sayaci_onbelleksiz(b)("dünya", 12)


def test_onbellek():
    say = rota_sayaci(galaksi_yukle()["baglantilar"])
    say("dünya", 20)
    bilgi = say.cache_info()
    assert bilgi.hits > 0
    assert bilgi.misses == bilgi.currsize  # her (gezegen, adım) çifti bir kez hesaplandı
    assert bilgi.misses <= 5 * 21  # en fazla 5 gezegen x 0..20 adım


# Görev 5: istatistik 
def test_buyuk_harf():
    b = galaksi_yukle()["baglantilar"]
    beklenen = ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]
    assert buyuk_harf(b) == harf_buyuk(b) == beklenen


def test_enaz_iki_baglanti():
    b = galaksi_yukle()["baglantilar"]
    beklenen = ["dünya", "centauri", "sirius", "orion"]
    assert enaz_iki_baglanti(b) == iki_baglanti_enaz(b) == beklenen


def test_toplam_baglanti():
    b = galaksi_yukle()["baglantilar"]
    assert toplam_baglanti(b) == baglanti_toplam(b) == 10


def test_hizli_yolculuk_partial():
    assert isinstance(hizli_yolculuk, partial)
    assert hizli_yolculuk.keywords == {"hiz": 3}
    assert hizli_yolculuk("sirius") == "sirius gezegenine hız 3 ile gidiliyor"
