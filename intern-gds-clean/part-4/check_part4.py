"""Check your Part 4 deliverables.

    python part-4/check_part4.py --who <your-name>

Part 4 has three deliverables, not one: the projection experiment, your
replication of your colleague's headline claim, and the joint synthesis.
"""

from __future__ import annotations

import argparse
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

from gdslab import check  # noqa: E402

GRAPHS = 2

MEMO_SECTIONS = ["What I did", "What I found", "What surprised me",
                 "What I could not determine", "Judgement calls",
                 "Sample sizes", "Collaboration record"]

REPLICATION_SECTIONS = ["The claim I tested", "What I ran", "What I got",
                        "Verdict", "What we shared"]

SYNTHESIS_SECTIONS = ["Every claim", "Replication status", "What we would do differently"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    args = ap.parse_args()

    d = os.path.join(BASE, "your-work", args.who, "part4")
    problems = []

    # --- the projection experiment ----------------------------------------
    shape = os.path.join(d, "projection_shape.csv")
    problems += check.require_columns(shape, ["graph", "view", "nodes", "edges",
                                              "blowup_vs_raw"])
    problems += check.require_min_rows(shape, GRAPHS * 3)  # raw + 2 projections
    problems += check.require_provenance(shape)

    mass = os.path.join(d, "projection_mass.csv")
    problems += check.require_columns(mass, ["graph", "side", "share_of_nodes",
                                             "share_of_pagerank", "mass_ratio"])
    problems += check.require_min_rows(mass, GRAPHS * 2)

    rankings = os.path.join(d, "projection_rankings.csv")
    problems += check.require_columns(rankings, [
        "graph", "node", "side", "raw_rank", "projected_rank", "rank_change"])
    problems += check.require_min_rows(rankings, 1000)

    effect = os.path.join(d, "projection_effect.csv")
    problems += check.require_columns(effect, [
        "graph", "side", "top10_overlap", "top20_overlap",
        "spearman_raw_vs_projected", "ari_raw_vs_projected"])
    problems += check.require_min_rows(effect, GRAPHS * 2)
    problems += check.require_no_nulls(effect, ["top10_overlap",
                                                "spearman_raw_vs_projected"])

    # --- the memo ----------------------------------------------------------
    memo = os.path.join(d, "part4-memo.md")
    problems += check.require_sections(memo, MEMO_SECTIONS)
    problems += check.require_no_placeholders(memo)
    problems += check.require_a_sample_size(memo)

    # --- the replication ---------------------------------------------------
    replication = os.path.join(d, "replication.md")
    problems += check.require_sections(replication, REPLICATION_SECTIONS,
                                       what="replication note")
    problems += check.require_no_placeholders(replication, what="replication note")
    problems += check.require_a_sample_size(replication, what="replication note")

    # --- the joint synthesis ----------------------------------------------
    synthesis = os.path.join(d, "synthesis.md")
    problems += check.require_sections(synthesis, SYNTHESIS_SECTIONS,
                                       what="synthesis")
    problems += check.require_no_placeholders(synthesis, what="synthesis")
    problems += check.require_a_sample_size(synthesis, what="synthesis")

    log = os.path.join(BASE, "your-work", args.who, "research-log.md")
    problems += check.file_exists(log, "research log")
    questions = os.path.join(BASE, "your-work", args.who, "questions.md")
    problems += check.file_exists(questions, "questions file")

    sys.exit(check.report("Part 4 - %s" % args.who, problems))


if __name__ == "__main__":
    main()
