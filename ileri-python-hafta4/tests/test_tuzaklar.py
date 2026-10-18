from uzay_oyunu.tuzaklar import yakit_ekle

def test_yakit():
    
    ilk = yakit_ekle(10)
    ikinci = yakit_ekle(20)
    assert ilk == [10]
    assert ikinci == [20]

def test_depo():
    depo = [1]
    assert yakit_ekle(2, depo) == [1, 2]
    assert depo == [1, 2]

def test_yakit_ekle_depo():
    assert yakit_ekle(5) is not yakit_ekle(5)
