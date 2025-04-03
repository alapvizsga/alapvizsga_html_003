import pytest, bs4, cssutils
def get_source():
    with open("szoveg.txt", "r") as f: #Szövegfájl beolvasása
        return f.read() #Visszadobás egyben

def get_html():
    with open("./index.html", encoding="utf-8") as f: #HTML fájl beolvasása
        return bs4.BeautifulSoup(f, 'html.parser') #Visszadobás egyben

#Fájlok beolvasása/átalakítása
html_soup = get_html() #bs4 html oldal

#Ha HTML-t kell ellenőrizni, akkor a html_soup.find-al lehet
#elementet keresni, első paramétere az element típusa.
#A második paramétere lehet class, id, stb.
#A class-okat (és gondolom az id-kat is) listaként dobja vissza,
#szóval az első elemre kell ellenőrizni, ha csak egy class van megadva.
#A .name tulajdonság az element típusát adja vissza.
#Az elementek pozícióját személy szerint én az előző/következő elementekkel ellenőrzöm,
#és ha kell akkor a parent/children-el is.

def test_feladat_1():
    target = html_soup.find("html")

    assert target.attrs["lang"] == "hu", "Nem magyar az oldal nyelve!"

def test_feladat_2():
    target = html_soup.find("title")

    assert target.text == "Szoliman", "Nem 'Szoliman' az oldal címe!"

def test_feladat_3():
    target = html_soup.find("h1")

    assert isinstance(target, bs4.Tag), "Nem létezik egyes című fejezetcím!"

    assert target.text == "Szoliman", "Az egyes című fejezetcím nem 'Szoliman' tartalmú!"

def test_feladat_4():
    szoveg = get_source()

    sorok = szoveg.strip().split('\n')

    targets = html_soup.find_all("p")

    assert len(targets) == 3, "Nem megfelelő számú bekezdés van!"

    # Ha nem létezik a h1 cím (előző tag)
    assert isinstance(targets[0].find_previous_sibling("h1"), bs4.Tag), "Nem megfelelő a bekezdések elhelyezése!"

    # Ha nem a jó tag van előtte (double check)
    assert targets[0].find_previous_sibling("h1").text == "Szoliman", "Nem megfelelő a bekezdések elhelyezése!"

    assert isinstance(targets[1].find_previous_sibling("p"), bs4.Tag), "Helytelen a bekezdések elhelyezése!"
    assert isinstance(targets[1].find_next_sibling("p"), bs4.Tag), "Helytelen a bekezdések elhelyezése!"

    for index in range(0, 3):
        assert targets[index].text == sorok[index].strip(), f"Helytelen az {index + 1}. bekezdés szövege!"

def test_feladat_5():
    targets = html_soup.find_all("h2")
    
    assert len(targets) == 3, "Nem megfelelő számú kettes fejezetcím van!"

    szoveg = ["A szemrehányás", "A szentkönyv", "A leborulás"]
    sorok = get_source()

    for index in range(0, 3):
        assert targets[index].text == szoveg[index].strip(), f"Helytelen az {index + 1}. bekezdés címe!"

    # Első cím ellenőrzése

    assert isinstance(targets[0].find_previous_sibling("h1"), bs4.Tag), "Helytelen az első cím elhelyezése!"
    assert targets[0].find_previous_sibling("h1").text == "Szoliman", "Helytelen az első cím elhelyezése!"

    assert isinstance(targets[0].find_next_sibling("p"), bs4.Tag), "Helytelen az első cím elhelyezése!"
    assert targets[0].find_next_sibling("p").text == sorok[0].strip(), "Helytelen az első cím elhelyezése!"