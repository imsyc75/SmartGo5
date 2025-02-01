Tällä viikolla olen keskittynyt tekoälyominaisuuksien kehittämiseen. Minimax-algoritmiin on lisätty alfa-beta-karsinta, ja hakusyvyys on nostettu kahdesta neljään. Kaksi muuta shakkimuotoa on lisätty. Hakustrategiaa on optimoitu niin, että se etsii ensin viimeisen shakkinappulan ympäriltä. Jos sopivaa vapaata paikkaa ei löydy, hakualuetta laajennetaan. Naapurin arviointi otetaan käyttöön merkityksettömien paikkojen suodattamiseksi. Lisääntynyt vihollisen uhkien arviointi. Arvioinnin kannalta älykäs suodatus suoritetaan riveille/sarakkeille, joissa on shakkinappuloita ja niiden vierekkäisille riveille/sarakkeille. Vähennä tarpeettomia vektoreita ja tehottomia laskelmia.

Sairastumisen takia tällä viikolla ei ollut paljon aikaa kehitykseen.Lisätty kaksi uutta testitiedostoa ja tyhjä testitiedosto Ai:sta. Ensi viikolla testikoodi optimoidaan.

Tekoälyn ajatteluaika on nyt 1-5 sekuntia, maksimissaan 10 sekuntia. Vastustuskyky ja puolustustietoisuus ovat aiempaa vahvempia. AI:n suorituskykyä voidaan kuitenkin edelleen optimoida, esimerkiksi tallentaa jo lasketut tilanteet välimuistiin toistuvien laskelmien vähentämiseksi (?). Testauksessa on paljon vastustusta, mutta kun Ai:n koodi on valmis, testaus on selkeämpi. Kaksi uutta testitiedostoa lisättiin tällä viikolla, mutta ne eivät ole täydellisiä. Ensi viikolla keskityn enemmän testaukseen.


Työaikaa kului noin 9 tuntia tällä viikolla. Tuntikirjanpito on liitteenä.
| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 28.1.  | 1 h            | keskustelu Hannun kanssa|
| 31.1.  | 4 h            | AI kehitys |
| 1.2.  | 4 h            | AI kehitys + testaus |
| Yhteensä | 17 h         |  |