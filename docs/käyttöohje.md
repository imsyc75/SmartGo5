## Asennus ja käynnistys
Kloonaa tämä repositorio koneellesi ja siirry sen kansioon. Aktivoi virtuaaliympäristö komennoilla
```bash
poetry shell
```
Asenna riippuvuudet komennolla
```bash
poetry install
```
Sovelluksen voi tämän jälkeen käynnistää komennolla
```bash
poetry run python3 src/ui.py
```

## Sovelluksen käyttö
Napsauta painiketta aloittaaksesi pelin. Pelaaja (musta) menee ensin. Voit aloittaa pelin uudelleen oikeasta alakulmasta. Voittaja on, kun 5 samanväristä palaa liitetään linjaan vaakasuunnassa, pystysuunnassa ja vinottain. Kun peli on ohi, voit lopettaa tai aloittaa alusta.

## Testit
Suorita testit komennolla
```bash
poetry run pytest
```
Testikattavuusraportin voi muodostaa komennolla
```bash
poetry run coverage html
```