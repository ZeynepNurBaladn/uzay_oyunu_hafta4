# Görev2

from functools import lru_cache

from uzay_oyunu.dekoratorler import say

@say
def fib_yalniz(n: int) -> int:
    
    return n if n < 2 else fib_yalniz(n - 1) + fib_yalniz(n - 2)

@say
@lru_cache(maxsize=None)
def fib_say_ustte(n: int) -> int:
    
    return n if n < 2 else fib_say_ustte(n - 1) + fib_say_ustte(n - 2)

@lru_cache(maxsize=None)
@say
def fib_lru_ustte(n: int) -> int:
   
    return n if n < 2 else fib_lru_ustte(n - 1) + fib_lru_ustte(n - 2)

def olc(n: int = 20) -> tuple[int, int, int]:
   
    fib_yalniz.cagri = 0
    fib_say_ustte.cagri = 0
    fib_say_ustte.__wrapped__.cache_clear()
    fib_lru_ustte.cache_clear()
    fib_lru_ustte.__wrapped__.cagri = 0

    fib_yalniz(n)
    fib_say_ustte(n)
    fib_lru_ustte(n)
    return (
        fib_yalniz.cagri,
        fib_say_ustte.cagri,
        fib_lru_ustte.__wrapped__.cagri,
    )
