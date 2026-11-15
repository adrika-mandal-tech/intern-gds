"""A file saved from Excel, or from PowerShell's Set-Content -Encoding UTF8,
starts with a byte-order mark. Without utf-8-sig the first column name comes
back as '﻿graph' and the checker reports a missing column that is plainly
there - which is a confusing error for someone whose only mistake was opening
their own results file.

Found by running the Part 1 checker against a PowerShell-truncated CSV."""

import csv

from gdslab import check


def _csv_with_bom(tmp_path, name, header, rows):
    path = tmp_path / name
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return str(path)


def test_columns_are_found_despite_a_bom(tmp_path):
    p = _csv_with_bom(tmp_path, "b.csv", ["graph", "seed"], [["crime", 1]])
    assert check.require_columns(p, ["graph", "seed"]) == []


def test_rows_are_counted_despite_a_bom(tmp_path):
    p = _csv_with_bom(tmp_path, "b.csv", ["graph"], [["x"] for _ in range(5)])
    assert check.require_min_rows(p, 5) == []


def test_distinct_works_despite_a_bom(tmp_path):
    p = _csv_with_bom(tmp_path, "b.csv", ["seed"], [[i] for i in range(10)])
    assert check.require_distinct(p, "seed", 10) == []


def test_nulls_detected_despite_a_bom(tmp_path):
    p = _csv_with_bom(tmp_path, "b.csv", ["a"], [[1], [""]])
    assert check.require_no_nulls(p, ["a"]) != []


def test_memo_sections_found_despite_a_bom(tmp_path):
    p = tmp_path / "m.md"
    p.write_text("# What I did\nstuff", encoding="utf-8-sig")
    assert check.require_sections(str(p), ["What I did"]) == []


def test_a_truncated_file_is_still_caught_when_it_has_a_bom(tmp_path):
    """The BOM fix must not accidentally make the row check permissive."""
    p = _csv_with_bom(tmp_path, "b.csv", ["graph"], [["x"] for _ in range(19)])
    assert check.require_min_rows(p, 70) != []
