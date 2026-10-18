def gorev_kaydi(
    baslik: str, *adimlar: str, oncelik: str = "normal", **ekler: str
) -> str:

    satirlar = [f"[{oncelik.upper()}] {baslik}"]
    satirlar += [f" {no}. {adim}" for no, adim in enumerate(adimlar, start=1)]
    satirlar += [f" {anahtar}: {deger}" for anahtar, deger in ekler.items()]
    return "\n".join(satirlar)


if __name__ == "__main__":
    adimlar = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]

    print(gorev_kaydi("Kara deliğe atla", *adimlar, oncelik="yüksek", sorumlu="Zeynep"))

    print()

    ayrintilar = {"oncelik": "yüksek", "sorumlu": "Zeynep"}
    print(gorev_kaydi("Kara deliğe atla", *adimlar, **ayrintilar))
