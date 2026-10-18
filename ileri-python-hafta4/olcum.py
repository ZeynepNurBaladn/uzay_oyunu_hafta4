import time

from uzay_oyunu.akis import rota_sayaci, rota_sayaci_onbelleksiz
from uzay_oyunu.oyun import galaksi_yukle

ADIM = 20

baglantilar = galaksi_yukle()["baglantilar"]

onbelleksiz = rota_sayaci_onbelleksiz(baglantilar)
t0 = time.perf_counter()
sonuc_a = onbelleksiz("dünya", ADIM)
sure_a = time.perf_counter() - t0

onbellekli = rota_sayaci(baglantilar)
t0 = time.perf_counter()
sonuc_b = onbellekli("dünya", ADIM)
sure_b = time.perf_counter() - t0

assert sonuc_a == sonuc_b
print(f"rota_sayisi('dünya', {ADIM}) = {sonuc_a}")
print(f"Önbelleksiz: {sure_a:.6f} sn")
print(f"Önbellekli : {sure_b:.6f} sn")
print(f"cache_info(): {onbellekli.cache_info()}")
