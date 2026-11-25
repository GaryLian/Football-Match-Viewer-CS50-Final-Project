import csv

class Match:
    def __init__(self, row):
        self.season = row["season"]
        self.date = row["date"]
        self.home_team = row["home_team"]
        self.away_team = row["away_team"]
        self.home_goals = row["home_goals"]
        self.away_goals = row["away_goals"]


def normalize(name):
    return name.strip().lower()

def team_in_match(team, home, away):
    return team == normalize(home) or team == normalize(away)

def matches_teams(team1, team2, home, away):
    if team2 == "":
        return team_in_match(team1, home, away)
    return (team1 != team2) and team_in_match(team1, home, away) and team_in_match(team2, home, away)

def filter_matches(matches, team1, team2, season):
    result = []
    for match in matches:
        if match["season"] == season:
            home = match["home_team"]
            away = match["away_team"]
            if matches_teams(team1, team2, home, away):
                result.append(match)
    return result

def filter_squad(players, team, season):
    squad = []
    for player in players:
        if normalize(player["team"]) == team and player["season"] == season:
            squad.append(player)
    return squad

def load_csv(filename):
    with open(filename, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))

def main():
    team1 = normalize(input("Enter the first team:\n"))
    while team1 == "":
        print("The first team cannot be empty. Please enter a valid team name.")
        team1 = normalize(input("Enter the first team: "))

    team2 = normalize(input("Enter the second team: (press Enter to search for all matches)\n"))

    season = input("Enter the season (e.g., 2025-26):\n").strip()

    matches = load_csv("matches.csv")
    results = filter_matches(matches, team1, team2, season)

    for match in results:
        date = match["date"]
        home = match["home_team"]
        away = match["away_team"]
        home_goals = match["home_goals"]
        away_goals = match["away_goals"]

        if home_goals == "" and away_goals == "":
            print(f"{date} | {home} vs {away} (scheduled)")
        else:
            print(f"{date} | {home} {home_goals} - {away_goals} {away}")

    if not results:
        print("No matches found.")
    elif team2 != "":
        answer = input("Show both teams' squads? (y/n): ")
        if answer.lower() == "y":

            players = load_csv("squads.csv")

            for team in [team1, team2]:
                print(f"\n{team.title()} Squad:")
                
                squad = filter_squad(players, team, season)

                for player in squad:
                    print(f"{player['player']} | {player['position']}")           

                if not squad:
                    print(f"No squad data available.")

if __name__ == "__main__":
    main()