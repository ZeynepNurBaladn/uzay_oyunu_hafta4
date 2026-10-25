# Dekoratör sırası: `@say` ve `@lru_cache`

`say`, her çağrıda `cagri` niteliğini artıran bir dekoratördür. Üç sürümde `fib(20)` çağrıldığında sayaç şu değerleri verdi:

| Tanım | `fib(20)` çağrı sayısı |
|---|---|
| Yalnızca `@say` | **21891** |
| `@say` üstte, `@lru_cache` altta | **39** |
| `@lru_cache` üstte, `@say` altta | **21** |

Dekoratörler alttan üste uygulanır, yani en üstteki dekoratör dışarıdan görünen fonksiyondur. Özyineleme `fib(n-1)` gibi **genel adı** çağırdığı için her iç çağrı da en üstteki dekoratörden geçer. Üç sonucun farkı buradan gelir.

## 1) Yalnızca `@say` → 21891
Önbellek yok. `fib(n)` her seferinde `fib(n-1)` ve `fib(n-2)` çağırır, aynı alt problemler defalarca hesaplanır. Çağrı ağacının düğüm sayısı `2·F(21) − 1 = 2·10946 − 1 = 21891` olur. Sayı üstel büyür.

## 2) `@say` üstte, `@lru_cache` altta → 39
`say` en dışta olduğu için **her çağrıyı** sayar, önbellekten dönenleri de. Önbellek yalnızca asıl hesaplamayı kısaltır:

- `fib(2) … fib(20)` için 19 kez önbellek ıskalanır; her ıskalamada iki alt çağrı yapılır.
- `fib(0)` ve `fib(1)` birer kez hesaplanır, geri kalan alt çağrılar önbellekten gelir ama yine sayılır.

Toplam: 1 (ilk çağrı) + 2·19 = **39**. Sayaç, önbelleğin **isabetlerini de** gördüğü için 21'den büyüktür.

## 3) `@lru_cache` üstte, `@say` altta → 21
Önbellek en dışta. Argümanı daha önce görülmüş çağrılar `say`'e hiç ulaşmaz, `say` yalnızca **gerçek hesaplamaları** sayar. Her `n` (0…20) tam bir kez hesaplanır: 21 farklı değer, **21** çağrı.

`lru_cache` nesnesi `functools.wraps` ile asıl fonksiyonu `__wrapped__` olarak sakladığından sayaca `fib.__wrapped__.cagri` ile ulaşılır.

## Sonuç
- **Önbellek dışta** olursa sayaç yalnızca gerçek hesapları sayar (21).
- **Sayaç dışta** olursa önbellek isabetleri de sayılır (39).
- İkisi de önbelleksiz sürümden (21891) çok küçüktür; önbellek üstel maliyeti doğrusala indirir.
- Genel kural: dekoratör sırası davranışı değiştirir. Önce hangisinin çağrıyı "göreceğine" göre dizilmelidir.
