"""Check your Part 1 deliverables are complete and well-formed.

    python part-1/check_part1.py --who <your-name>

What this does and does not do
------------------------------
It checks your evidence is PRESENT and WELL-FORMED: the files exist, they have
the right columns, they have as many rows as the brief asked for, nothing is
blank, your memo has its sections and no leftover placeholders.

It cannot check whether your findings are TRUE. Nothing can do that for you.
"The checker passed" means "this is reviewable", not "this is right".
"""

from __future__ import annotations

import argparse
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

from gdslab import check  # noqa: E402

RUNS_PER_GRAPH = 10
N_GRAPHS = 7

MEMO_SECTIONS = ["What I did", "What I found", "What surprised me",
                 "What I could not determine", "Judgement calls",
                 "Sample sizes", "Collaboration record"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    args = ap.parse_args()

    d = os.path.join(BASE, "your-work", args.who, "part1")
    profiles = os.path.join(d, "profiles.csv")
    pageranks = os.path.join(d, "pagerank_runs.csv")
    memo = os.path.join(d, "part1-memo.md")
    calibration = os.path.join(d, "calibration.md")

    problems = []

    # --- the profile table -------------------------------------------------
    problems += check.require_columns(profiles, [
        "name", "nodes", "edges", "degree_skew", "components", "clustering"])
    problems += check.require_min_rows(profiles, N_GRAPHS)
    problems += check.require_no_nulls(profiles, ["name", "nodes", "edges",
                                                  "degree_skew"])
    problems += check.require_provenance(profiles)

    # --- the pagerank runs -------------------------------------------------
    problems += check.require_columns(pageranks, [
        "graph", "run", "n_nodes", "n_edges", "degree_skew", "load_s",
        "compute_s", "iterations"])
    problems += check.require_min_rows(pageranks, N_GRAPHS * RUNS_PER_GRAPH)
    problems += check.require_no_nulls(pageranks, ["graph", "run", "compute_s",
                                                   "iterations"])
    problems += check.require_distinct(pageranks, "run", RUNS_PER_GRAPH,
                                       group_by="graph")
    problems += check.require_provenance(pageranks)

    # --- the memo ----------------------------------------------------------
    problems += check.require_sections(memo, MEMO_SECTIONS)
    problems += check.require_no_placeholders(memo)
    problems += check.require_a_sample_size(memo)

    # --- the cross-machine comparison --------------------------------------
    problems += check.require_no_placeholders(calibration, what="calibration note")
    if os.path.exists(calibration):
        text = open(calibration, encoding="utf-8").read().lower()
        for word, why in [
                ("colleague", "name whose machine you compared against"),
                ("ratio", "the brief asks specifically about ratios"),
                ("iteration", "iteration counts are the third thing to compare")]:
            if word not in text:
                problems.append("%s never mentions %r - %s"
                                % (calibration, word, why))

    # --- first impressions -------------------------------------------------
    notes = os.path.join(BASE, "your-work", args.who, "first-impressions.md")
    problems += check.file_exists(notes, "first-impressions notes")
    log = os.path.join(BASE, "your-work", args.who, "research-log.md")
    problems += check.file_exists(log, "research log")

    sys.exit(check.report("Part 1 - %s" % args.who, problems))


if __name__ == "__main__":
    main()
