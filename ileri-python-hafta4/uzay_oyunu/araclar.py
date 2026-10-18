import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def hamle_sayaci() -> Callable[[], int]:
    toplam = 0

    def say() -> int:
        nonlocal toplam
        toplam += 1
        return toplam

    return say

def en_bagli_gezegenler(galaksi: dict[str, Any]) -> list[str]:

    return sorted(
        galaksi["gezegenler"],
        key=lambda g: (-len(galaksi["baglantilar"][g]), g),
    )

def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    
    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        gecen = time.perf_counter() - baslangic
        print(f"{fonksiyon.__name__} {gecen:.6f} sn sürdü")
        return sonuc

    return sarmalayici


if __name__ == "__main__":
    import json
    from pathlib import Path

    veri = json.loads((Path(__file__).with_name("galaksi.json")).read_text("utf-8"))
    olculu = sure_olc(en_bagli_gezegenler)
    print(olculu(veri))
