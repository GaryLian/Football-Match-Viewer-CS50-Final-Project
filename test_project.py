from project import filter_matches, filter_squad

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
    matches = [madrid_home, barcelona_home, next_season_match]
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


def test_filter_squad_by_team_and_season():
    madrid_player = {
        "season": "2025-26",
        "team": "Real Madrid",
        "player": "Madrid Player A",
        "position": "Goalkeeper",
    }
    barcelona_player = {
        "season": "2025-26",
        "team": "Barcelona",
        "player": "Barcelona Player A",
        "position": "Midfielder",
    }
    next_season_player = {
        "season": "2026-27",
        "team": "Real Madrid",
        "player": "Madrid Player B",
        "position": "Defender",
    }

    players = [madrid_player, barcelona_player, next_season_player]
    results = filter_squad(players, "real madrid", "2025-26")

    assert results == [madrid_player]
