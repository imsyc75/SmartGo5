## Ohjelman rakenne
Tämä on Pythonissa toteutettu Gomoku-peliohjelma. Ohjelma koostuu neljästä päätiedostosta:
1. index.py: Aloita peli kutsumalla start()-metodia
2. app.py: Pääpeliohjain on vastuussa pelin tilan, kuten nykyisen pelaajan, pelilaudan ja siirtohistorian, ylläpitämisestä. Ohjaa vuorottelua pelaajan ja tekoälyn välillä. siirron tehdäminen ja voiton tarkistaminen.
3. gomoku.py: määrittää perustaulun ja sääntölogiikan.
4. gomoku_ai.py: vastaa tekoälyn päätöksenteosta. Osaa tunnistaa ja pisteyttää erilaisia ​​shakkikuvioita.
Peliprosessi on seuraava: Pelaaja (X) asettaa nappulan laudalle. Tarkista, voittaako pelaaja. Käytä Minimax-algoritmia valitaksesi paras paikka nappulan sijoittamiselle. Tarkista, voittaako AI. Toista yllä olevia vaiheita, kunnes toinen osapuoli voittaa tai tasapeli.
## Tila- ja aikavaativuudet
Tilanvaativuus on pääosin O(n^2), missä n on shakkilaudan koko( = 20). Vaikka ehdokassiirron lista on myös teoreettisesti O(n^2), todellinen suoritusaika on yleensä O(k), missä k on paljon pienempi kuin n^2. Koska vain viimeisimmän sirron ympärillä olevat tyhjät tilat huomioidaan. Aikavaativuuken kannalta ohjelman aikaa vievin osa on AI-päätöksenteossa Minimax-algoritmi, jonka monimutkaisuus on O(b^d), missä b on ehdokaspaikkojen lukumäärä ja d on hakusyvyys ( = 3). Alpha-Beta-leikkaustekniikan ansiosta paras tapaus voidaan vähentää arvoon O(√b^d ).
Alfa-beta-leikkausohjeet: Alfa edustaa maksimipelaajan (AI) löytämää parasta (maksimipistettä). Beta dustaa minimoivan pelaajan (ihmisen) löytämää parasta (minimipistettä). Leikkausehto on kun Beta ≤ Alfa, se tarkoittaa, että nykyinen hakupolku ei vaikuta lopulliseen päätökseen ja haku voidaan lopettaa.
## Puutteet ja jatkokehitysmahdollisuudet
Nykyinen tekoälyalgoritmi optimoi suorituskykyä tarkistamalla vain nappulan ympärillä olevan yhden ruudun tyhjät paikat. Tämä menetelmä parantaa laskentatehokkuutta, mutta saattaa johtaa siihen, että algoritmi jättää huomiotta vastustajan mahdolliset voittopolut.
Toinen suorituskyvyn parantamisvaihtoehto on uudelleensuunnitella evaluate_board-funktio. Nykyinen funktio suorittaa koko pelilaudan tilan arvioinnin, mikä on laskentaresurssien kannalta tehotonta. Tehokkaampi suunnittelu hyödyntäisi paikallista arviointia, joka analysoi vain viimeisimmän siirron ympärillä tapahtuneet pelilaudan tilan muutokset, vähentäen näin merkittävästi tarpeetonta laskentakuormaa ja optimoiden aikavaativuutta.
## Laajojen kielimallien käyttö. 
Tätä projektia kehitettäessä käytin Clauden kielimallia apuvälineenä. Koska minulla ei ollut kokemusta pelien suunnittelusta itsenäisesti, Claude tarjosi apua seuraavilla: Projektin alussa se auttoi minua määrittämään projektin aikataulun ja tehtävät, jotka tulisi suorittaa kussakin vaiheessa, ja tarjosi minulle yleisen pelin kehitysprosessin. Se auttoi minua ajattelemaan pelin yleistä arkkitehtuuria.
Lisäksi tekoäly tekee kirjoittamilleni dokumentaatille kielioppitarkistuksia varmistaakseen niiden tarkkuuden ja säästäen samalla paljon aikaa.
## Viitteet
- [Alpha–beta pruning(Wikipedia)](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
- [Tournament-winning gomoku AI](https://sortingsearching.com/2020/05/18/gomoku.html)
- [Minimax Algorithm in Game Theory](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/)