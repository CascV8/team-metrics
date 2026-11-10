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


def test_roster_ratings_and_curve():
    """Forwards and defencemen weighted by ice time within their own group; categories blended 2:1; curved in a pool."""
    from team_metrics import teams
    row = lambda pid, pos, toi, ovr, cat: {"id": pid, "team": "VAN", "pos": pos, "gp": 10, "toi": toi,
                                          "modes": {"5v5": {"overall": [ovr, 0], "cats": {"Offence": [cat, 0]}}}}
    rows = [row(1, "C", 20, 80, 90), row(2, "L", 10, 20, 30), row(3, "D", 25, 50, 0)]
    r = teams.roster_ratings(rows)["VAN"]
    assert r == {"Forwards": 60.0, "Blueline": 50.0}       # (80*20 + 20*10) / 30; the lone defenceman
    by = teams._weighted(rows, "VAN", lambda x: x["modes"]["5v5"]["cats"]["Offence"][0])
    assert by == {"F": 70.0, "D": 0.0}
    assert abs(teams._blend(by) - 70 * 2 / 3) < 1e-9        # not swamped by the defenceman's ice time
    assert teams.curve(3, [1, 2, 3, 4]) == 62.5
    assert teams.curve(None, [1]) is None
