import pandas as pd


def test_team_lineup_matching():
    """Team pages: Daily Faceoff's slugs from the NHL's names, and its names matched to NHL ids by position."""
    from team_metrics import teams
    assert teams.slug("Montréal Canadiens") == "montreal-canadiens"
    assert teams.slug("St. Louis Blues") == "st-louis-blues"
    roster = [["Elias Pettersson", 1, "C"], ["Elias Pettersson", 2, "D"], ["Brock Boeser", 3, "R"], ["Thatcher Demko", 4, "G"]]
    match = teams._matcher(roster)
    assert match("Elias Pettersson", "C") == 1
    assert match("Elias Nils Pettersson", "LD") == 2       # Daily Faceoff's name for the defenceman: last name, in the D
    assert match("Elias Pettersson", "sk1") is None        # special teams: no position, two of them
    assert match("Brock Boeser", "sk2") == 3
    assert match("Thatcher Demko", "ir1") == 4
    assert match("Nobody Here", "C") is None


def test_deadline_lineup_picking():
    """Past seasons' lineups: the most-used combinations that share no player, and each stretch with nobody changing."""
    from collections import Counter

    from team_metrics import deadline
    usage = Counter({(1, 2, 3): 500, (1, 4, 5): 400, (4, 5, 6): 300, (7, 8, 9): 100})
    assert deadline._top(usage, 2) == [(1, 2, 3), (4, 5, 6)]       # (1, 4, 5) shares player 1 with the top line
    shifts = pd.DataFrame({"player_id": [1, 2, 3], "team_abbrev": ["A", "A", "B"],
                           "start_seconds": [0, 0, 10], "end_seconds": [30, 20, 30]})
    got = [(secs, sorted(ids.tolist())) for secs, ids, _ in deadline._stretches(shifts)]
    assert got == [(10, [1, 2]), (10, [1, 2, 3]), (10, [1, 3])]
