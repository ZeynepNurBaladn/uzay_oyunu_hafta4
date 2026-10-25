# Hafta 5
from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable

# Görev1
def sure_olc(fonk: Callable) -> Callable:
   
    @wraps(fonk)
    def sarmal(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonk(*args, **kwargs)
        sure = time.perf_counter() - baslangic
        print(f"{fonk.__name__}: {sure:.4f} sn")
        return sonuc

    return sarmal

# Görev2
def say(fonk: Callable) -> Callable:
    

    @wraps(fonk)
    def sarmal(*args: Any, **kwargs: Any) -> Any:
        sarmal.cagri += 1
        return fonk(*args, **kwargs)

    sarmal.cagri = 0
    return sarmal

# Görev3
def log_cagri(fonk: Callable) -> Callable:
   
    @wraps(fonk)
    def sarmal(*args: Any, **kwargs: Any) -> Any:
        parcalar = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        print(f"-> {fonk.__name__}({', '.join(parcalar)})")
        sonuc = fonk(*args, **kwargs)
        print(f"<- {fonk.__name__} = {sonuc!r}")
        return sonuc

    return sarmal

# Görev5
def sinirla(alt: float, ust: float) -> Callable[[Callable], Callable]:
    
    def dekorator(fonk: Callable) -> Callable:
        @wraps(fonk)
        def sarmal(*args: Any, **kwargs: Any) -> Any:
            if args:
                deger = args[0]
            elif kwargs:
                deger = next(iter(kwargs.values()))
            else:
                raise TypeError(f"{fonk.__name__}: argüman verilmedi")
            if not alt <= deger <= ust:
                raise ValueError(
                    f"{fonk.__name__}: {deger} değeri {alt}-{ust} aralığında değil"
                )
            return fonk(*args, **kwargs)

        return sarmal

    return dekorator

# Bonus
def hafiza(maxsize: int | None = None) -> Callable[[Callable], Callable]:

    def dekorator(fonk: Callable) -> Callable:
        onbellek: dict = {}

        @wraps(fonk)
        def sarmal(*args: Any, **kwargs: Any) -> Any:
            anahtar = (args, tuple(sorted(kwargs.items())))
            if anahtar in onbellek:
                return onbellek[anahtar]
            sonuc = fonk(*args, **kwargs)
            if maxsize is not None:
                if maxsize <= 0:
                    return sonuc
                while len(onbellek) >= maxsize:
                    onbellek.pop(next(iter(onbellek)))
            onbellek[anahtar] = sonuc
            return sonuc

        sarmal.boyut = lambda: len(onbellek)
        sarmal.temizle = onbellek.clear
        return sarmal

    return dekorator
