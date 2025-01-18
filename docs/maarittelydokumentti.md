Tietojenkäsittelytieteen kandidaatti (TKT)
# Aihe ja toteutus
Kehitä tekoälyjärjestelmä, joka voi pelata Gomokua 20x20-laudalla. Tekoälyn täytyy pystyä valitsemaan tehokkaasti paras siirto ja tehdä päätöksiä kohtuullisessa ajassa. Järjestelmän on saavutettava tehokas voiton tunnistus ja tilanteen arviointi. Siksi projektin ydinpainotuksena on toteuttaa tehokas Minimax-hakualgoritmi. Lisäksi on tarpeen suunnitella tehokas tilanteen arviointifunktio. Myös siirtojen valintastrategia on optimoitava.

Pelin syötteinä ovat pelilaudan nykyinen tila ja pelaajan siirron sijainti. Järjestelmä käsittelee nämä syötteet. Esimerkiksi mahdollisten siirtojen luettelon päivittäminen, nykyisen tilanteen arvioiminen ja tekoälyn optimaalisen siirron laskeminen.

Minimax-haun (alfa-beta-karsinnalla) aikavaativuus on O(b^d), missä b on keskimääräinen haarojen lukumäärä solmua kohti ja d on hakusyvyys. Koska vain olemassa olevien nappuloiden kahden ruudun etäisyydellä olevat paikat otetaan huomioon, b-arvo pienenee merkittävästi. Voiton tunnistuksen aikavaativuus on O(1), koska meidän tarvitsee tarkistaa vain kiinteä määrä naapureita neljään suuntaan viimeisestä siirrosta. 

Tilavaativuuden osalta, laudan tilan vaatima tila on O(n^2), missä n = 20. Mahdollisten siirtojen lista on O(k), missä k on mahdollisten siirtojen lukumäärä, joka on yleensä paljon pienempi kuin n^2.

# Projektin kieli ja Ohjelmointikielet
Projektien ohjelmointikieli on python, ja kaikki dokumentaatio kirjoitetaan suomeksi. Mutta koodi ja kommentit tulevat olemaan englanniksi. Vertaisarvioinnissa voin arvioida ainakin pythonilla toteutettuja harjoitustöitä.

# Lähteet
Projektissa käytetaan seuraavia lähteitä:
- [Minimax Algorithm in Game Theory](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/)
- [Alpha–beta pruning(Wikipedia)](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
- [Gomoku(Wikipedia)](https://en.wikipedia.org/wiki/Gomoku)