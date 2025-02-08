Tällä viikolla lisättiin siirtojen generointi. Toteutettiin dynaamisen kandidaattisiirtojen listan ylläpito, jossa priorisoidaan viimeisimmän siirron nappulan sijaintia. Voittotarkistuksissa vain viimeisimmän siirron rivien tarkistaminen paransi tekoälyn suorituskykyä. Kandidaattisiirtojen listan tila säilytettiin ja päivitettiin minimax-haussa.

Käytännössä huomasin tekoälyn keskittyvän vastustamiseen voittomahdollisuuksien etsimisen sijaan. Tämä johti tekoälyn heikkoon suorituskykyyn. Esimerkiksi, jos tekoälyllä on jo neljä nappulaa rivissä, se ei valitse voittoa vaan vastustaa minua. Kokeilin monia eri tapoja korjata tätä. Jotkut menetelmät tekivät koodista monimutkaisempaa ja heikensivät tekoälyn suorituskykyä. Suorituskyvyn säilyttämiseksi päätin säätää arviointifunktion painotuksia. Tästä oli apua, mutta apu oli silti vähäistä.

Ensi viikolla keskitytään testien kehittämiseen Ohjaustilaisuus Testauksesta -tilaisuuden jälkeen.

Työaikaa kului noin 10 tuntia tällä viikolla. Tuntikirjanpito on liitteenä.
| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 3.2.  | 1 h            | siirtojen generoinnin kehittäminen |
| 4.2.  | 2 h            | siirtojen generoinnin kehittäminen |
| 5.2.  | 2 h            | keskustelu Hannun kanssa |
| 7.2.  | 2 h            | AI kehitys |
| 8.2.  | 3 h            | AI kehitys |
| Yhteensä | 10 h         |  |