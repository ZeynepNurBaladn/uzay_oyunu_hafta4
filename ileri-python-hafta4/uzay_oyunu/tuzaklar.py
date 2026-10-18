
def yakit_ekle(miktar: int, depo: list[int] | None = None) -> list[int]:
    
    if depo is None:
        depo = []
    depo.append(miktar)
    return depo
