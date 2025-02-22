Tällä viikolla korjasin minimax-algoritmin liikuntalistoja koskevan virheen, minkä jälkeen tekoälyn suorituskyky parani huomattavasti. Tekoäly kuitenkin valitsee edelleen näennäisesti merkityksettömän sijainnin tilanteessa, jossa sillä on neljä nappulaa rivissä eikä pelaaja estä voittoa.

Tein seuraavat debuggaukset:
Ensin tulostin tekoälyn arvioiman edellisen siirron（last_move）ja kaikki ehdokassijainnit arviointipisteineen. Jos neljän nappulan rivi löytyy, tulostetaan viesti: Vector content: .......OOOO......... Huomasin, että tekoälyn arvioima last_move oli päinvastainen todelliseen nappulan sijaintiin verrattuna. Korjasin tämän virheen, mutta se ei vaikuttanut ongelmaan.

Neljän nappulan rivin jälkeen, tekoälyn miettiessä, huomasin kaikkien ehdokassijaintien pisteiden olevan 9999999999, joten tekoäly palautti listan ensimmäisen sijainnin voittosijainnin sijaan. Tämän vuoksi tulostin pelilaudan tilan ennen check_win-funktion true-paluuarvoa.

Huomasin pelilaudalla ylimääräisen tekoälyn nappulan, joka muodosti viiden nappulan rivin. Uskon ongelman olevan siinä, että minimax-algoritmi simuloidessaan eri siirtoja ja mahdollisia siirtosarjoja ei poista simuloituja nappuloita. Tämä johti siihen, että pelilaudalla tekoälyllä oli jo voittorivi. En ole varma, onko päätelmäni oikea. Yritin korjata ongelmaa tästä näkökulmasta, mutta tuloksetta.

Koska pääkoodia ei ole vielä täysin korjattu, testikoodia ei voi tehdä valmiiksi.

Tällä viikolla lisäsin myös käyttöliittymäelementtejä, kuten pelin aloitus- ja lopetussivut sekä yksinkertaista pelaajan kanssa vuorovaikutusta. Käyttöliittymään ei pitäisi tarvita enää lisäyksiä.

Ensi viikko on viimeinen viikko ennen demoa, joten tämä suurin ongelma pitää korjata. Näin jää aikaa testaukselle. Minulla on vielä kaksi tiedostoa ja aikaa pitäisi olla riittävästi.

Työaikaa kului noin 14 tuntia tällä viikolla. Tuntikirjanpito on liitteenä.
| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 17.2.  | 2 h            |Keskustelu Ohjaajan kanssa|
| 19.2.  | 4 h            | debug |
| 20.2.  | 1 h            | debug |
| 21.2.  | 2 h            | debug|
| 22.2.  | 5 h            | debug|
| Yhteensä | 14 h         |  |
