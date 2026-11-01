"""NHL team metrics: every team's numbers and ranks for a season, and its lineups (current, opening night, after
the trade deadline). Built on nhl-microstats."""

import argparse
import logging
import os


def main() -> None:
    parser = argparse.ArgumentParser(prog="team-metrics", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    ln = sub.add_parser("lineups", help="refresh Daily Faceoff lineups and NHL rosters")
    ln.add_argument("--force", action="store_true", help="refetch even if fetched in the last few hours")
    dl = sub.add_parser("deadline-lineups", help="past seasons' lineups after the trade deadline, from shift charts")
    dl.add_argument("seasons", nargs="+", help="start years of complete seasons")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s  %(message)s", datefmt="%H:%M:%S")
    logging.getLogger("puckscrape").setLevel(logging.WARNING)

    if args.cmd == "lineups":
        # Tell a workflow when a lineup or roster changed since the last deploy (data/lineups_deployed), so its site
        # is rebuilt and deployed even on a day with no new games.
        from nhl_microstats.collect import DATA
        from .teams import refresh_lineups
        fingerprint, fetched = refresh_lineups(force=args.force)
        deployed = DATA / "lineups_deployed"
        changed = not deployed.exists() or deployed.read_text().strip() != fingerprint
        print(f"{fetched} teams fetched; lineups {'changed' if changed else 'unchanged'} ({fingerprint[:12]})")
        if os.environ.get("GITHUB_OUTPUT"):   # refreshed: save the cache, so the next run doesn't refetch them
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"fingerprint={fingerprint}\n" + ("changed=true\n" if changed else "")
                        + ("refreshed=true\n" if fetched else ""))
    elif args.cmd == "deadline-lineups":
        from .deadline import write
        for s in args.seasons:
            write(int(s))
