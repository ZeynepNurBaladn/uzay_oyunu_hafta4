"""Hafta 5 gösterimi: Görev 1 süre ölçümü, Görev 2 sayaçlar, Görev 3/5 örnek çıktılar."""

from uzay_oyunu.akis import rota_sayaci  # Hafta 4 modülünüz
from uzay_oyunu.dekoratorler import log_cagri, sure_olc
from uzay_oyunu.fib_sirasi import olc
from uzay_oyunu.oyun import BAGLANTILAR, yakit_harca, yolculuk

def rota_sayaci_onbelleksiz(baglantilar):
    """Önbelleksiz sürüm: yalnızca süre karşılaştırması için."""

    def rota_sayisi(gezegen, adim):
        if adim == 0:
            return 1
        return sum(rota_sayisi(k, adim - 1) for k in baglantilar[gezegen])

    return rota_sayisi


print("== Görev 1: önbelleksiz rota sayacı, adim=20 ==")
sure_olc(rota_sayaci_onbelleksiz(BAGLANTILAR))("dünya", 20)
sayac = rota_sayaci(BAGLANTILAR)
sure_olc(sayac)("dünya", 20)
print(sayac.cache_info())

print("\n== Görev 2: fib(20) çağrı sayıları ==")
print(olc(20))

print("\n== Görev 3 ==")
log_cagri(yolculuk)("orion", hiz=3)

print("\n== Görev 5 ==")
print(yakit_harca(30))
try:
    yakit_harca(150)
except ValueError as hata:
    print("ValueError:", hata)
