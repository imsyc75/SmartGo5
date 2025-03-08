# SmartGo5
This project is an implementation of Gomoku AI as part of the Data Structures and Algorithms Project course (TKT20010). The author is a BSc student in the Computer Science Program (TKT) in University of Helsinki.

[![GHA workflow badge](https://github.com/imsyc75/SmartGo5/workflows/CI/badge.svg)](https://github.com/imsyc75/SmartGo5/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/imsyc75/SmartGo5/graph/badge.svg?token=7Z7JGE8W6I)](https://codecov.io/gh/imsyc75/SmartGo5)

## Documentation
[Määrittelydokumentti](docs/maarittelydokumentti.md)
[Testausdokumentti](docs/testausdokumentti.md)
[Toteusdokumentti](docs/toteu6dokumentti.md)
[Käyttöohje](docs/käyttöohje.md)


## Week report
[Viikko 1](docs/viikkoraportit/viikko1.md)
[Viikko 2](docs/viikkoraportit/viikko2.md)
[Viikko 3](docs/viikkoraportit/viikko3.md)
[Viikko 4](docs/viikkoraportit/viikko4.md)
[Viikko 5](docs/viikkoraportit/viikko5.md)
[Viikko 6](docs/viikkoraportit/viikko6.md)

## User's instruction
After cloning the repository to your own machine, start poetry in the project root directory using the following command

```bash
poetry install
```

Activate virtual environment
```bash
poetry shell
```

Run the game
```bash
poetry run python3 src/ui.py
```

Test
```bash
poetry run pytest
```