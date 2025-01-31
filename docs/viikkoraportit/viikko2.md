Tällä viikolla kehitin Gomokun peruslogiikkaa ja tekoäly. Käytin pygamea UI:n toteuttamiseen. gomoku.py sisältää pelilogiikan, kuten laudan tilan hallinnan ja siirtojen validoinnin. App.py:n GomokuGame-luokka hoitaa pelitilan ja vuorot. Tämä vei paljon aikaa, mutta onneksi verkossa on paljon koodeja esimerkeiksi.

Tekoäly tunnistaa tällä hetkellä 5 perusmallia. Arviointifunktio ja hakukehikko kaipaavat parannusta. Huomasin, että tekoälyn nopeus hidastuu, kun nappuloita on paljon laudalla, sillä se lisää hakualgoritmin aikakompleksisuutta.

Testaus jäi vähälle ajanpuutteen vuoksi. Keskityin vain laudan toiminnan testaamiseen.

Ensi viikolla keskityn tekoälyn strategia-algoritmien optimointiin, kuten alpha-beta pruning ja heuristisen haun lisäämiseen. Laajennan myös testejä. Tällä hetkellä uskon, että lisättävät testit voivat olla voiton määrittämisen testejä ja tekoälytoimintojen testejä. Minulla ei ole tällä hetkellä vahvoja ajatuksia tästä. Toivon saavansa ohjetta.

Työaikaa kului noin 17 tuntia tällä viikolla. Tuntikirjanpito on liitteenä.
| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 19.1.  | 1 h            | Ymmärrä pelin logiikka ja löydä tietoa|
| 21.1.  | 3 h            | Pelilogiikan kehitys |
| 22.1.  | 3 h            | Pelilogiikan kehitys |
| 24.1.  | 5 h            | Pelilogiikan kehitys + tekoälykehitys |
| 25.1.  | 5 h            | AI kehitys + testi + viikoraportti |
| Yhteensä | 17 h         |  |