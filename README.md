# NBA Statistics

This program was created during fall 2022 as an assigment for IN4110 at UiO. It fetches NBA player statistics (assists, points, rebounds) from Wikipedia for the 2022 NBA playoffs, visualizes the statistics in bar graphs, and stores the graphs as png-images in the "NBA_player_statistics" folder.

<img src="NBA_player_statistics/assists.png" height="300px"/>

## Run script

    python3 fetch_player_statistics.py

## Run all tests

    pytest -v tests

## Run singular test file

    pytest -v tests/<filename>

## Dependencies

- Pandas
- BeautifulSoup4
- Requests
- Matplotlib
