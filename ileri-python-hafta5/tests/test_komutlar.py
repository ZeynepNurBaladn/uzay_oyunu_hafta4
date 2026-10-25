"""Hafta 5 Görev 4: komut sistemi testleri."""

import pytest

from uzay_oyunu.komutlar import KOMUTLAR, envanter, harita, komut, yardim
from uzay_oyunu.oyun import galaksi_kur, travel


@pytest.fixture
def temiz_komutlar():
    """Testin eklediği komutları geri alır."""
    orijinal = dict(KOMUTLAR)
    yield
    KOMUTLAR.clear()
    KOMUTLAR.update(orijinal)


@pytest.fixture
def durum():
    d = galaksi_kur()
    d["konum"] = "sirius"
    return d


def girdiler(*satirlar):
    it = iter(satirlar)
    return lambda _: next(it)


def test_uc_komut_kayitli():
    assert set(KOMUTLAR) == {"yardim", "envanter", "harita"}


def test_komut_fonksiyonu_degistirmez(temiz_komutlar):
    def merhaba(durum):
        return "merhaba"

    assert komut("merhaba", "selam verir")(merhaba) is merhaba
    assert KOMUTLAR["merhaba"] == (merhaba, "selam verir")


def test_ayni_ad_iki_kez_value_error(temiz_komutlar):
    with pytest.raises(ValueError):
        komut("yardim")(lambda d: "")


def test_yardim_komutu(durum):
    assert yardim(durum) == (
        "envanter eşyalarını gösterir\n"
        "harita gidebileceğin gezegenleri gösterir\n"
        "yardim komutları listeler"
    )


def test_envanter_komutu(durum):
    assert envanter(durum) == "credits: 100, engines: 1, copilot: yok"
    durum["copilot"] = "Ada"
    assert envanter(durum).endswith("copilot: Ada")


def test_harita_komutu(durum):
    assert harita(durum) == "orion, dünya, kara_delik"


def test_travel_komut_calistirir_ve_menuyu_tekrar_gosterir(durum, capsys):
    sonuc = travel(durum, giris=girdiler("harita", "cik"))
    assert sonuc == "cikis"
    cikti = capsys.readouterr().out
    assert "orion, dünya, kara_delik" in cikti
    assert cikti.count("Nereye gitmek istersin?") == 2
    assert durum["konum"] == "sirius" and durum["yakit"] == 100


def test_travel_komut_degilse_gezegen_secimi(durum):
    travel(durum, giris=girdiler("1", "cik"))
    assert durum["konum"] == "orion"
    assert durum["yakit"] == 95


def test_travel_yakit_bitince_kaybeder(capsys):
    d = galaksi_kur()
    d["yakit"] = 10
    hamleler = ["1", "1", "1"]  # 5, 0, sonra StopIteration
    assert travel(d, giris=girdiler(*hamleler)) == "kayip"
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in capsys.readouterr().out
