from pathlib import Path

from flask import Flask, render_template, request

from project import Match, filter_matches, load_csv, normalize


app = Flask(__name__, static_folder="Logo")
DATA_DIR = Path(__file__).resolve().parent


def load_archive():
    seasons = {}
    for row in load_csv(DATA_DIR / "matches_clean.csv"):
        season = row["season"]
        if season not in seasons:
            seasons[season] = []
        seasons[season].append(row)
    return seasons


def get_search_options(archive):
    names = set()
    competitions = set()
    for matches in archive.values():
        for match in matches:
            names.add(match["home_team"])
            names.add(match["away_team"])
            competitions.add(match["competition"])
    return sorted(names), sorted(competitions)


ARCHIVE = load_archive()
TEAM_NAMES, COMPETITIONS = get_search_options(ARCHIVE)


@app.route("/")
def home():
    seasons = sorted(ARCHIVE, reverse=True)

    team = request.args.get("team", "").strip()
    opponent = request.args.get("opponent", "").strip()
    season = request.args.get("season", "2024-25")

    competition = request.args.get("competition", "any")

    matches = []
    message = ""

    if team:
        team1 = normalize(team)
        team2 = normalize(opponent)
        search_seasons = [season]
        if season == "any":
            search_seasons = seasons

        for year in search_seasons:
            rows = ARCHIVE.get(year, [])
            for row in filter_matches(rows, team1, team2, year):
                if competition != "any" and row["competition"] != competition:
                    continue
                line = f"{row['competition']} | {Match(row)}"
                if season == "any":
                    line = f"{year} | {line}"
                matches.append(line)

        if not matches:
            message = "No matches found."
    elif "team" in request.args:
        # The form was submitted with an empty team name.
        message = "Please enter a team name."

    return render_template(
        "home.html",
        team_names=TEAM_NAMES,
        team=team,
        opponent=opponent,
        season=season,
        seasons=seasons,
        competitions=COMPETITIONS,
        competition=competition,
        matches=matches,
        message=message,
    )
