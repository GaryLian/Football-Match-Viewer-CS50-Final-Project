import csv
from pathlib import Path
from tempfile import NamedTemporaryFile


DATA_DIR = Path(__file__).resolve().parent
COLUMNS = ["season", "competition", "date", "home_team", "away_team", "home_goals", "away_goals"]
COMPETITIONS = {
    "GB1": "Premier League",
    "ES1": "La Liga",
    "L1": "Bundesliga",
    "IT1": "Serie A",
    "FR1": "Ligue 1",
    "CL": "Champions League",
}


def read_matches(filename):
    matches = []
    with open(filename, encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            code = row["competition_id"]
            year = int(row["season"])
            if code in COMPETITIONS:
                matches.append({
                    "season": f"{year}-{str(year + 1)[-2:]}",
                    "competition": COMPETITIONS[code],
                    "date": row["date"],
                    "home_team": row["home_club_name"],
                    "away_team": row["away_club_name"],
                    "home_goals": row["home_club_goals"],
                    "away_goals": row["away_club_goals"],
                })
    return sorted(matches, key=lambda match: match["date"])


def write_matches(filename, matches):
    with NamedTemporaryFile(mode="w", dir=filename.parent, delete=False,
                            encoding="utf-8", newline="") as file:
        temporary = Path(file.name)
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(matches)
    temporary.replace(filename)


def main():
    matches = read_matches(DATA_DIR / "games.csv")
    write_matches(DATA_DIR / "matches_clean.csv", matches)
    print(f"Saved {len(matches)} matches to matches_clean.csv")


if __name__ == "__main__":
    main()
