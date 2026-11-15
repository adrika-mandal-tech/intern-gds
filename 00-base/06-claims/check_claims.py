"""Check your claim-verification rows are complete and well-formed.

    python 06-claims/check_claims.py --who <your-name>

Reads your-work/<your-name>/claims.jsonl.

It checks the SHAPE of your verdicts, not whether you graded correctly. Nothing
can check that but a second reader.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, BASE)

from gdslab import check  # noqa: E402

VERDICTS = {"confirmed", "partly-confirmed", "misstated", "unverifiable"}
GRADES = {"production", "research", "product", "marketing"}
MIN_QUOTE = 25
EXPECTED_IDS = {"C%02d" % i for i in range(1, 13)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    ap.add_argument("--min-done", type=int, default=1,
                    help="how many rows must be filled in (default 1)")
    args = ap.parse_args()

    path = os.path.join(BASE, "your-work", args.who, "claims.jsonl")
    problems = check.file_exists(path, "claims file")
    if problems:
        problems.append("  copy 06-claims/claims.jsonl to your-work/%s/ and fill "
                        "it in there" % args.who)
        sys.exit(check.report("Claims - %s" % args.who, problems))

    rows, seen, done = [], set(), 0
    with open(path, encoding="utf-8-sig") as fh:
        for i, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                problems.append("line %d is not valid JSON: %s" % (i, exc))
                continue
            rows.append((i, row))

    for i, row in rows:
        cid = row.get("claim_id", "?")
        if cid in seen:
            problems.append("line %d: duplicate claim_id %s" % (i, cid))
        seen.add(cid)

        verdict = (row.get("verdict") or "").strip()
        if not verdict:
            continue  # not attempted yet - that is allowed
        done += 1

        if verdict not in VERDICTS:
            problems.append("%s: verdict %r is not one of %s"
                            % (cid, verdict, sorted(VERDICTS)))

        grade = (row.get("grade") or "").strip()
        if grade and grade not in GRADES:
            problems.append("%s: grade %r is not one of %s"
                            % (cid, grade, sorted(GRADES)))

        notes = (row.get("notes") or "").strip()
        if not notes:
            problems.append("%s: has a verdict but no notes - the reasoning is "
                            "the point, not the verdict" % cid)

        if verdict == "unverifiable":
            if not notes or len(notes) < 40:
                problems.append("%s: 'unverifiable' needs notes saying what you "
                                "tried, so nobody repeats it" % cid)
        else:
            source = (row.get("primary_source") or "").strip()
            quote = (row.get("quote") or "").strip()
            if not source:
                problems.append("%s: verdict %r needs a primary_source"
                                % (cid, verdict))
            if len(quote) < MIN_QUOTE:
                problems.append("%s: quote is %d characters, needs at least %d - "
                                "a short quote could match almost anything"
                                % (cid, len(quote), MIN_QUOTE))
            if not grade:
                problems.append("%s: verdict %r needs a grade" % (cid, verdict))

    missing = EXPECTED_IDS - seen
    if missing:
        problems.append("claims missing from your file entirely: %s"
                        % sorted(missing))

    if done < args.min_done:
        problems.append("only %d row(s) filled in, expected at least %d"
                        % (done, args.min_done))

    print("  %d of %d claims attempted" % (done, len(EXPECTED_IDS)))
    sys.exit(check.report("Claims - %s" % args.who, problems))


if __name__ == "__main__":
    main()
