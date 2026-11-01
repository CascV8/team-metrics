# team-metrics

NHL team metrics, built on [nhl-microstats](https://github.com/CascV8/nhl-microstats): the numbers behind the
team pages on [pattullometrics](https://pattullometrics.pages.dev). The website itself lives in its own repo;
this one is only the data and the maths.

- **Metrics**: points percentage, power play and penalty kill (NHL stats); each skater category's 5v5 percentile
  averaged over the team's skaters by ice time; goaltending, the team's goalies' ratings by games. Each is ranked
  among the 32 teams, and the overall is the average of a team's ranks, ranked again (`season_teams`).
- **Current lineups**: Daily Faceoff's line combinations matched to NHL player ids against the team's roster
  (`team-metrics lineups`).
- **Opening night and after the trade deadline**: lineups read from the NHL's shift charts. The twelve forwards
  and six defencemen with the most 5v5 time form the lineup, their most-used combinations first; the goalies
  are the two with the most starts (`team-metrics deadline-lineups 2023 2024 2025`, shipped in
  `src/team_metrics/team_seasons/`).

```
uv sync
uv run team-metrics lineups
uv run team-metrics deadline-lineups 2025
```

Data goes in `data/` under the folder it's run from, shared with nhl-microstats.
