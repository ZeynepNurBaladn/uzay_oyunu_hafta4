"""Hafta 5 dekoratör testleri."""

import re
from functools import lru_cache

import pytest

from uzay_oyunu.dekoratorler import hafiza, log_cagri, say, sinirla, sure_olc
from uzay_oyunu.fib_sirasi import olc
from uzay_oyunu.oyun import galaksi_kur, hedef_menusu, yakit_harca, yolculuk


# --- Görev 1: sure_olc -------------------------------------------------------
def test_sure_olc_sonuc_degismeden_doner(capsys):
    @sure_olc
    def topla(a, b):
        return a + b

    assert topla(2, 3) == 5
    assert re.fullmatch(r"topla: \d+\.\d{4} sn\n", capsys.readouterr().out)


def test_sure_olc_adli_argumanlar(capsys):
    @sure_olc
    def bol(a, b=1):
        return a / b

    assert bol(a=10, b=4) == 2.5
    assert bol(8, b=2) == 4


def test_sure_olc_ad_ve_belge_korunur():
    @sure_olc
    def ornek():
        """Örnek belge."""

    assert ornek.__name__ == "ornek"
    assert ornek.__doc__ == "Örnek belge."


# --- Görev 2: say ve sıra ----------------------------------------------------
def test_say_cagri_sayar():
    @say
    def f():
        return 1

    f(), f(), f()
    assert f.cagri == 3
    assert f.__name__ == "f"


def test_dekorator_sirasi_fib20():
    assert olc(20) == (21891, 39, 21)


# --- Görev 3: log_cagri ------------------------------------------------------
def test_log_cagri_ciktisi(capsys):
    sonuc = log_cagri(yolculuk)("orion", hiz=3)
    assert sonuc == "orion hiz=3"
    assert capsys.readouterr().out == (
        "-> yolculuk('orion', hiz=3)\n<- yolculuk = 'orion hiz=3'\n"
    )


def test_log_cagri_galaksi_kur_ve_hedef_menusu(capsys):
    galaksi = galaksi_kur()
    assert galaksi["konum"] == "dünya"
    secim = hedef_menusu(["orion", "dünya"], lambda _: "1")
    assert secim == "1"
    cikti = capsys.readouterr().out
    assert "-> galaksi_kur()" in cikti
    assert "-> hedef_menusu(['orion', 'dünya'], " in cikti
    assert galaksi_kur.__name__ == "galaksi_kur"


# --- Görev 5: sinirla --------------------------------------------------------
def test_yakit_harca_normal():
    assert yakit_harca(30) == 70


@pytest.mark.parametrize("sinir,beklenen", [(0, 100), (100, 0)])
def test_yakit_harca_sinir_degerleri(sinir, beklenen):
    assert yakit_harca(sinir) == beklenen


@pytest.mark.parametrize("deger", [-1, 101, 150])
def test_yakit_harca_aralik_disi(deger):
    with pytest.raises(ValueError) as hata:
        yakit_harca(deger)
    assert str(hata.value) == f"yakit_harca: {deger} değeri 0-100 aralığında değil"


def test_sinirla_adli_arguman_ve_ad_korunur():
    assert yakit_harca(miktar=10) == 90
    assert yakit_harca.__name__ == "yakit_harca"


# --- Bonus: hafiza -----------------------------------------------------------
def test_hafiza_lru_cache_ile_ayni_sonuc_ve_cagri_sayisi():
    @hafiza()
    @say
    def fib_h(n):
        return n if n < 2 else fib_h(n - 1) + fib_h(n - 2)

    @lru_cache(maxsize=None)
    @say
    def fib_l(n):
        return n if n < 2 else fib_l(n - 1) + fib_l(n - 2)

    assert fib_h(25) == fib_l(25) == 75025
    assert fib_h.__wrapped__.cagri == fib_l.__wrapped__.cagri == 26


def test_hafiza_maxsize_en_eski_girdiyi_siler():
    cagrilar = []

    @hafiza(maxsize=2)
    def kare(x):
        cagrilar.append(x)
        return x * x

    kare(1), kare(2), kare(3)  # 1 silinir
    assert kare.boyut() == 2
    kare(2)  # önbellekte
    assert cagrilar == [1, 2, 3]
    kare(1)  # silinmişti, yeniden hesaplanır
    assert cagrilar == [1, 2, 3, 1]


def test_hafiza_sonuclari_lru_cache_ile_ayni():
    def f(x, y=1):
        return x * 10 + y

    h, l = hafiza(maxsize=3)(f), lru_cache(maxsize=3)(f)
    girdiler = [(1,), (2,), (1,), (3,), (4,), (1,), (2,)]
    for g in girdiler:
        assert h(*g) == l(*g)
    assert h(5, y=2) == l(5, y=2)
