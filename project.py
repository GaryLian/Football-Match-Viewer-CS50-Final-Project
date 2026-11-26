import csv
    

class Match:
    def __init__(self, row):
        self.season = row["season"]
        self.date = row.get("date")
        self.home_team = row["home_team"]
        self.away_team = row["away_team"]
        self.home_goals = row.get("home_goals")
        self.away_goals = row.get("away_goals")

    def __str__(self):
        if self.is_upcoming():
            return f"{self.date} | {self.home_team} vs {self.away_team} (scheduled)"
        score = f"{self.home_goals} - {self.away_goals}"
        return f"{self.date} | {self.home_team} {score} {self.away_team}"

    def is_upcoming(self):
        """
        Check if the match is upcoming (no goals recorded).
        """
        return self.home_goals == "" and self.away_goals == ""

    def has_team(self, team):
        """
        Check if the match involves the specified team.

        The team argument should be normalized.
        """

        return team in (normalize(self.home_team), normalize(self.away_team))

    def matches_teams(self, team1, team2):
        """
        Check if the match involves the specified teams.

        If team2 is "", match any game involving team1.

        Both team1 and team2 should be normalized.
        """

        if team2 == "":
            return self.has_team(team1)
        return team1 != team2 and self.has_team(team1) and self.has_team(team2)


def normalize(name):
    name = name.strip().lower()
    for label in ("fc", "cf"):
        name = name.removeprefix(label + " ")
        name = name.removesuffix(" " + label)
    return name


def filter_matches(matches, team1, team2, season):
    """
    Return a list of CSV rows that involve the specified teams in the given season.

    If team2 is "", return all of team1's matches.

    Both team1 and team2 should be normalized.
    """

    result = []
    for row in matches:
        if row["season"] == season and Match(row).matches_teams(team1, team2):
            result.append(row)
    return result


def load_csv(filename):
    with open(filename, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def get_teams():
    """
    Prompt for teams and season. team2 is "" if the user skips it.
    """

    team1 = normalize(input("Enter the first team:\n"))
    while team1 == "":
        print("The first team cannot be empty. Please enter a valid team name.")
        team1 = normalize(input("Enter the first team:\n"))

    team2 = normalize(input("Enter the second team: (press Enter to search for all matches)\n"))

    season = input("Enter the season (e.g., 2025-26):\n").strip()

    return team1, team2, season


def print_matches(results):
    for row in results:
        print(Match(row))


def main():
    team1, team2, season = get_teams()
    results = filter_matches(load_csv("matches_clean.csv"), team1, team2, season)
    if not results:
        print("No matches found.")
        return
    print_matches(results)


if __name__ == "__main__":
    main()
