from project import filter_matches


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

    matches = [madrid_home, barcelona_home]
    results = filter_matches(matches, "real madrid", "barcelona", "2025-26")

    assert results == [madrid_home, barcelona_home]