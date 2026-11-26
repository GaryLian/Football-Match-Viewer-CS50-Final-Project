from project import Match, filter_matches, normalize


def test_normalize_strips_and_lowercases():
    assert normalize("  Real Madrid  ") == "real madrid"
    assert normalize("BARCELONA") == "barcelona"
    assert normalize("") == ""


def test_filter_matches_includes_both_home_orders():
    madrid_home = {
        "season": "2025-26",
        "home_team": "Real Madrid",
        "away_team": "Barcelona",
    }
    barcelona_home = {
        "season": "2025-26",
        "home_team": "Barcelona",
        "away_team": "Real Madrid",
    }

    next_season_match = {"season": "2026-27", "home_team": "Barcelona", "away_team": "Real Madrid"}
    madrid_sevilla = {"season": "2025-26", "home_team": "Real Madrid", "away_team": "Sevilla"}
    matches = [madrid_home, barcelona_home, next_season_match, madrid_sevilla]
    results = filter_matches(matches, "real madrid", "barcelona", "2025-26")

    assert results == [madrid_home, barcelona_home]


def test_filter_matches_rejects_same_team_twice():
    matches = [
        {
            "season": "2025-26",
            "home_team": "Real Madrid",
            "away_team": "Barcelona",
        }
    ]

    results = filter_matches(matches, "real madrid", "real madrid", "2025-26")

    assert results == []


def test_filter_matches_with_no_opponent():
    madrid_home = {
        "season": "2025-26",
        "home_team": "Real Madrid",
        "away_team": "Sevilla",
    }
    madrid_away = {
        "season": "2025-26",
        "home_team": "Barcelona",
        "away_team": "Real Madrid",
    }
    unrelated_match = {
        "season": "2025-26",
        "home_team": "Barcelona",
        "away_team": "Sevilla",
    }

    matches = [madrid_home, madrid_away, unrelated_match]
    results = filter_matches(matches, "real madrid", "", "2025-26")

    assert results == [madrid_home, madrid_away]


def test_match_displays_goalless_draw():
    row = {
        "season": "2025-26",
        "date": "2026-03-21",
        "home_team": "Barcelona",
        "away_team": "Real Madrid",
        "home_goals": "0",
        "away_goals": "0",
    }
    match = Match(row)
    assert str(match) == "2026-03-21 | Barcelona 0 - 0 Real Madrid"


def test_match_displays_scheduled_game():
    row = {
        "season": "2025-26",
        "date": "2026-03-21",
        "home_team": "Barcelona",
        "away_team": "Real Madrid",
        "home_goals": "",
        "away_goals": "",
    }
    match = Match(row)
    assert str(match) == "2026-03-21 | Barcelona vs Real Madrid (scheduled)"
