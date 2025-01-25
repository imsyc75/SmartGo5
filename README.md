# SmartGo5
This project is an implementation of Gomoku AI as part of the Data Structures and Algorithms Project course (TKT20010). The author is a BSc student in the Computer Science Program (TKT) in University of Helsinki.

## Documentation
[Määrittelydokumentti](docs/maarittelydokumentti.md)

## Week report
[Viikko 1](docs/viikkoraportit/viikko1.md)

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

Run the test
```bash
python -m unittest src/tests/test_board.py 
```