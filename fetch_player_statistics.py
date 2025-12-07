from binascii import a2b_base64
import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html
from pathlib import Path



try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"



def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players)
    all_players = {}
    for item in teams:
        temp = []
        for key in item:
            temp.append(item[key])
        all_players[temp[0]] = get_players(temp[1])

    # get player statistics for each player,
    # using get_player_stats
    for team, players in all_players.items():
        for p in players:
            temp = (get_player_stats(p["url"], team))
            if temp:
                p["points"] = temp["points"]
                p["assists"] = temp["assists"]
                p["rebounds"] = temp["rebounds"]
            else:
                p["points"] = 0.0
                p["assists"] = 0.0
                p["rebounds"] = 0.0

    # Select top 3 for each team by points:
    best = {}
    for team, players in all_players.items():
        top_3 = []
        for p in players:
            if len(top_3) != 3:
                top_3.append({
                    "name": p["name"],
                    "points": p["points"],
                    "assists": p["assists"],
                    "rebounds": p["rebounds"]
                })
            else:
                # Sorts the top 3 so that the worst out of the 3 is first in the list.
                top_3 = sorted(top_3, key=lambda d: d["points"])
                if p["points"] > top_3[0]["points"]:
                    top_3[0]["name"] = p["name"]
                    top_3[0]["points"] = p["points"]
                    top_3[0]["assists"] = p["assists"]
                    top_3[0]["rebounds"] = p["rebounds"]
        best[team] = top_3

    stats_to_plot = ["points", "assists", "rebounds"]
    for stat in stats_to_plot:
        plot_best(best, stat=stat)



def plot_best(best: Dict[str, List[Dict]], stat: str) -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    stats_dir = "results_graphs"
    # Make new directory.
    current_dir = os.getcwd()
    final_dir = os.path.join(current_dir, stats_dir)
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    # Clears plot so old doesn't overlap with new
    plt.clf()
    colors = ["red", "green", "purple"]
    counter = 0
    all_teams = []

    for team, players in best.items():
        # Sorts player from best stat to worst.
        players = sorted(players, key=lambda d: d[stat], reverse=True)
        all_teams.extend(["", team, "", ""])
        # Gets player names and stats
        stats = []
        names = []
        for p in players:
            stats.append(p[stat])
            names.append(p["name"])
        # Adds the bars for the stats
        for i in range(len(players)):
            plt.bar(counter+i, stats[i], 1, color=colors[i], label=names[i])
            plt.text(counter+i-0.4, 0, names[i], rotation=90)
        counter += len(players)+1

    plt.xticks(range(len(all_teams)), all_teams, rotation=90)
    plt.title(f"{stat} per game for top 3 players in all teams")
    filename = f"{stats_dir}/{stat}.png"
    print(f"Creating {filename}")
    plt.tight_layout()
    plt.savefig(filename)
        


def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]



def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Get the table
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    roster = soup.find(id="Roster")
    table = roster.find_next("table")

    players = []
    # Loop over every row and get the names from roster
    rows = table.find_all("tr")
    rows = rows[3:]
    for row in rows:
        # Get the columns
        cols = row.find_all("td")
        # find name links (a tags)
        # and add to players a dict with
        # {'name':, 'url':}
        name_col = cols[2] # Name and player link are at column 3
        name = [td.text.strip() for td in cols][2]
        # Cleaning up names with a legend attached to them (ex: (TW))
        name = re.sub("\xa0", "", name)
        a = name_col.find("a")
        url = a.attrs["href"]

        players.append({"name": name, "url": f"{base_url}{url}"})

    # return list of players
    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    if soup.find(id="Regular_season"):
        nba = soup.find(id="Regular_season")
    elif soup.find(id="NBA"):
        nba = soup.find(id="NBA")
    table = nba.find_next("table")

    # Normally these are the indices for the wanted stats.
    ppg_index = 12
    apg_index = 9
    rpg_index = 8

    stats = {}
    rows = table.find_all("tr")
    rows = rows[1:]
    # Loop over rows and extract the stats
    index = 1
    rowspan = 0
    for row in rows:
        cols = row.find_all("td")
        # Some fixes if there are fewer columns than expected because of a colspan.
        if len(cols) < 13:
            ppg_index = ppg_index - (13 - len(cols))
            apg_index = apg_index - (13 - len(cols))
            rpg_index = rpg_index - (13 - len(cols))

        if not cols[index].find("a"):
            break

        title = cols[index].find("a").attrs["title"]

        # Check correct team (some players change team within season)
        if cols[0].has_attr("rowspan"):
            index = 0
        else:
            index = 1

        try:
            if "2021" in title and team in title:
                # load stats from columns
                # keys should be 'points', 'assists', etc.
                stats = {
                    "points": float(cols[ppg_index].text.strip("*\n")),
                    "assists": float(cols[apg_index].text.strip("*")),
                    "rebounds": float(cols[rpg_index].text.strip("*"))
                }
                break
        except ValueError as e:
            print(f"ValueError: {e}")
            

    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
