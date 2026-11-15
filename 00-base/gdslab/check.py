"""The building blocks the per-part checkers are made of.

What a checker is, and is not
-----------------------------
A checker verifies that your evidence is **present and well-formed**: the file
exists, it has the columns it should, it has as many rows as the brief asked
for, the seeds really are distinct, your memo has the sections it needs and no
leftover placeholders.

A checker cannot tell you whether your finding is **true**. Nothing can do that
for you. "The checker passed" means "this is reviewable", not "this is right" -
and if you ever catch yourself reporting the former as though it were the
latter, that is exactly the mistake this pack is about.

Every helper returns a list of problem strings. Empty list means fine.
"""

from __future__ import annotations

import csv
import os
import re

PLACEHOLDERS = ("TODO", "TBD", "FIXME", "XXX", "<fill in>", "lorem ipsum")


def _read(path: str):
    with open(path, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def file_exists(path: str, what: str = "file") -> list:
    if not os.path.exists(path):
        return ["missing %s: %s" % (what, path)]
    if os.path.getsize(path) == 0:
        return ["empty %s: %s" % (what, path)]
    return []


def require_columns(path: str, columns) -> list:
    problems = file_exists(path, "results file")
    if problems:
        return problems
    with open(path, encoding="utf-8-sig") as fh:
        header = next(csv.reader(fh), [])
    missing = [c for c in columns if c not in header]
    if missing:
        return ["%s is missing column(s) %s (has %s)" % (path, missing, header)]
    return []


def require_min_rows(path: str, minimum: int) -> list:
    problems = file_exists(path, "results file")
    if problems:
        return problems
    rows = _read(path)
    if len(rows) < minimum:
        return ["%s has %d rows, expected at least %d - did the run finish?"
                % (path, len(rows), minimum)]
    return []


def require_distinct(path: str, column: str, expected: int,
                     group_by: str | None = None) -> list:
    """Every run must use a different seed. Repeating a seed repeats the answer,
    which silently turns N runs into 1 run wearing a bigger sample size."""
    problems = require_columns(path, [column] + ([group_by] if group_by else []))
    if problems:
        return problems
    rows = _read(path)
    groups = {}
    for row in rows:
        groups.setdefault(row.get(group_by, "") if group_by else "", []).append(row[column])
    out = []
    for key, values in sorted(groups.items()):
        if len(set(values)) < expected:
            where = " for %s=%s" % (group_by, key) if group_by else ""
            out.append("%s has %d distinct %s%s, expected %d"
                       % (path, len(set(values)), column, where, expected))
    return out


def require_no_nulls(path: str, columns) -> list:
    problems = require_columns(path, columns)
    if problems:
        return problems
    out = []
    for i, row in enumerate(_read(path), start=2):
        for column in columns:
            if row.get(column) in (None, "", "nan", "None"):
                out.append("%s line %d: column %r is empty" % (path, i, column))
    return out[:10]


def require_provenance(path: str) -> list:
    """Every results file needs its sidecar, or the numbers cannot be interpreted."""
    stem = path[:-4] if path.endswith(".csv") else path
    sidecar = stem + ".provenance.json"
    problems = file_exists(sidecar, "provenance sidecar")
    if problems:
        return problems + ["  (write results through gdslab.runs.Recorder "
                           "and this appears automatically)"]
    return []


def require_sections(md_path: str, headings, what: str = "memo") -> list:
    problems = file_exists(md_path, what)
    if problems:
        return problems
    text = open(md_path, encoding="utf-8-sig").read().lower()
    missing = [h for h in headings if h.lower() not in text]
    if missing:
        return ["%s is missing required section(s): %s" % (md_path, missing)]
    return []


def require_no_placeholders(md_path: str, what: str = "memo") -> list:
    problems = file_exists(md_path, what)
    if problems:
        return problems
    text = open(md_path, encoding="utf-8-sig").read()
    found = [p for p in PLACEHOLDERS if p.lower() in text.lower()]
    if found:
        return ["%s still contains placeholder text: %s" % (md_path, found)]
    return []


def require_a_sample_size(md_path: str, what: str = "memo") -> list:
    """A memo that states a rate without a sample size is not yet a finding.

    Looks for an explicit n=..., 'sample size', 'runs', or 'out of' construction.
    Crude on purpose - it is a prompt to check yourself, not a proof.
    """
    problems = file_exists(md_path, what)
    if problems:
        return problems
    text = open(md_path, encoding="utf-8-sig").read().lower()
    patterns = [r"\bn\s*=\s*\d+", r"sample size", r"\b\d+\s+runs?\b",
                r"\bout of\s+\d+", r"\b\d+\s+of\s+\d+\b", r"\bacross\s+\d+\b"]
    if not any(re.search(p, text) for p in patterns):
        return ["%s states no sample size anywhere - every rate needs one" % md_path]
    return []


def report(name: str, problems) -> int:
    """Print the outcome. Returns a process exit code: 0 clean, 1 problems.

    Duplicates are collapsed - several checks touch the same file, and one
    missing file should be reported once, not five times.
    """
    seen, unique = set(), []
    for problem in problems:
        if problem not in seen:
            seen.add(problem)
            unique.append(problem)
    problems = unique

    print("=" * 70)
    print("  %s" % name)
    print("=" * 70)
    if not problems:
        print("  PASS - everything the checker can see is present and well-formed.")
        print()
        print("  Note: this says your evidence is reviewable. It does NOT say")
        print("  your finding is correct. Nothing can check that but you.")
        return 0
    print("  %d problem(s):\n" % len(problems))
    for problem in problems:
        print("   - %s" % problem)
    print()
    print("  Nothing here is a telling-off. A checker catching something is the")
    print("  checker doing its job - much better now than after you reported it.")
    return 1
