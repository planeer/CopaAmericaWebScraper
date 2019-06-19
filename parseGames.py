import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def main():
    URL = "https://en.wikipedia.org/wiki/{}_Copa_Am%C3%A9rica"
    # Format [year, number of teams, normal page]
    years = [[1993, 12, True], [1995, 12, True], [1997, 12, True], [1999, 12, True], [2001, 12, True], [2004, 12, True], [2007, 12, True], [2011, 12, False], [2015, 12, False], [2016, 16, True]]

    for year in years:
        print("Parsing year: {}".format(year[0]))
        r = requests.get(URL.format(year[0]))
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")

        # Get group data
        games = soup.find_all("div", {"class": "footballbox"})
        if year[2]: # Some pages differ from others and are harder to parse
            num_of_group_games = year[1] * 6 / 4
        else:
            num_of_group_games = 0
        data = []
        for i, game in enumerate(games):
            if i < num_of_group_games:
                stage = "Group"
            elif i < num_of_group_games + 4:
                stage = "Quarter-finals"
            elif i < num_of_group_games + 4 + 2:
                stage = "Semi-finals"
            elif i < num_of_group_games + 4 + 2 + 1:
                stage = "Match for third place"
            else:
                stage = "Final"

            home_team = game.find('th', {'class': 'fhome'}).findNext('a').get_text()
            away_team = game.find('th', {'class': 'faway'}).findNext('a').get_text()

            goals = game.find('th', {'class': 'fscore'}).get_text().split('–')
            home_team_goals = re.findall('\d+', goals[0])[0]
            away_team_goals = re.findall('\d+', goals[1])[0]

            ftr = "D" if home_team_goals == away_team_goals else ("H" if home_team_goals > away_team_goals else "A")
            
            data.append([stage, home_team, away_team, home_team_goals, away_team_goals, ftr])

        # Save current year
        df = pd.DataFrame(data, columns = ["Stage","HomeTeam","AwayTeam","FTHG","FTAG","FTR"])
        df.to_csv("output/copa_america_" + str(year[0]) + ".csv", index=None)


if __name__ == "__main__":
    main()
