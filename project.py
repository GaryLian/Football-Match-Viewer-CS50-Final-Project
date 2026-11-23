import csv

def normalize(name):
    return name.strip().lower()

def team_in_match(team, home, away):
    return team == normalize(home) or team == normalize(away)

def matches_teams(team1, team2, home, away):
    if team2 == "":
        return team_in_match(team1, home, away)
    return (team1 != team2) and team_in_match(team1, home, away) and team_in_match(team2, home, away)

def filter_squad(players, team, season):
    squad = []
    for player in players:
        if normalize(player["team"]) == team and player["season"] == season:
            squad.append(player)
    return squad

def main():
    team1 = normalize(input("Enter the first team: "))
    while team1 == "":
        print("The first team cannot be empty. Please enter a valid team name.")
        team1 = normalize(input("Enter the first team: "))
    team2 = normalize(input("Enter the second team: (press Enter to search for all matches) "))

    season = input("Enter the season (e.g., 2025-26): ").strip()

    with open("matches.csv", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        
        match_found = False

        for match in reader:

            if match["season"] == season:
                home = match["home_team"]
                away = match["away_team"]
            
        
        
                if  matches_teams(team1, team2, home, away):

                    match_found = True

                    date = match["date"]
                    home_goals = match["home_goals"]
                    away_goals = match["away_goals"]
                

                    if home_goals == "" and away_goals == "":
                        print(f"{date} | {home} vs {away} (scheduled)")
                    else:
                        print(f"{date} | {home} {home_goals} - {away_goals} {away}")

                

    if not match_found:
        print("No matches found.")
    elif team2 != "":
        answer = input("Show both teams' squads? (y/n): ")
        if answer.lower() == "y":


            with open("squads.csv", encoding="utf-8", newline="") as file:
                players = list(csv.DictReader(file))
            for team in [team1, team2]:
                print(f"\n{team.title()} Squad:")
                
                squad = filter_squad(players, team, season)

                for player in squad:
                    print(f"{player['player']} | {player['position']}")
                
                if not squad:
                    print(f"No squad data available.")

if __name__ == "__main__":
    main()