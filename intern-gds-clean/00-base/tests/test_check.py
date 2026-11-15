"""Every helper is tested BOTH ways: it must pass good input and, more
importantly, be seen to FAIL bad input. A checker never seen to fail is not
evidence that anything was checked."""

import csv

from gdslab import check


def _csv(tmp_path, name, header, rows):
    path = tmp_path / name
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return str(path)


def _md(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


# --- file_exists -----------------------------------------------------------

def test_file_exists_passes_a_real_file(tmp_path):
    p = _csv(tmp_path, "a.csv", ["x"], [[1]])
    assert check.file_exists(p) == []


def test_file_exists_FAILS_on_missing(tmp_path):
    assert check.file_exists(str(tmp_path / "nope.csv")) != []


def test_file_exists_FAILS_on_empty(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("", encoding="utf-8")
    assert check.file_exists(str(p)) != []


# --- require_columns -------------------------------------------------------

def test_require_columns_passes(tmp_path):
    p = _csv(tmp_path, "c.csv", ["a", "b"], [[1, 2]])
    assert check.require_columns(p, ["a", "b"]) == []


def test_require_columns_FAILS_on_missing_column(tmp_path):
    p = _csv(tmp_path, "c.csv", ["a"], [[1]])
    assert check.require_columns(p, ["a", "b"]) != []


# --- require_min_rows ------------------------------------------------------

def test_require_min_rows_passes(tmp_path):
    p = _csv(tmp_path, "r.csv", ["a"], [[i] for i in range(10)])
    assert check.require_min_rows(p, 10) == []


def test_require_min_rows_FAILS_on_truncated_file(tmp_path):
    p = _csv(tmp_path, "r.csv", ["a"], [[i] for i in range(3)])
    assert check.require_min_rows(p, 10) != []


# --- require_distinct ------------------------------------------------------

def test_require_distinct_passes(tmp_path):
    p = _csv(tmp_path, "s.csv", ["seed"], [[i] for i in range(20)])
    assert check.require_distinct(p, "seed", 20) == []


def test_require_distinct_FAILS_on_repeated_seeds(tmp_path):
    p = _csv(tmp_path, "s.csv", ["seed"], [[1] for _ in range(20)])
    assert check.require_distinct(p, "seed", 20) != []


def test_require_distinct_checks_each_group(tmp_path):
    rows = [["g1", i] for i in range(5)] + [["g2", 0] for _ in range(5)]
    p = _csv(tmp_path, "g.csv", ["graph", "seed"], rows)
    problems = check.require_distinct(p, "seed", 5, group_by="graph")
    assert len(problems) == 1 and "g2" in problems[0]


# --- require_no_nulls ------------------------------------------------------

def test_require_no_nulls_passes(tmp_path):
    p = _csv(tmp_path, "n.csv", ["a"], [[1], [2]])
    assert check.require_no_nulls(p, ["a"]) == []


def test_require_no_nulls_FAILS_on_blank_cell(tmp_path):
    p = _csv(tmp_path, "n.csv", ["a"], [[1], [""]])
    assert check.require_no_nulls(p, ["a"]) != []


# --- require_provenance ----------------------------------------------------

def test_require_provenance_FAILS_without_sidecar(tmp_path):
    p = _csv(tmp_path, "p.csv", ["a"], [[1]])
    assert check.require_provenance(p) != []


def test_require_provenance_passes_with_sidecar(tmp_path):
    p = _csv(tmp_path, "p.csv", ["a"], [[1]])
    (tmp_path / "p.provenance.json").write_text('{"networkx": "3.6.1"}',
                                                encoding="utf-8")
    assert check.require_provenance(p) == []


# --- memo helpers ----------------------------------------------------------

def test_require_sections_passes(tmp_path):
    p = _md(tmp_path, "m.md", "# What I did\nstuff\n# What I found\nmore")
    assert check.require_sections(p, ["What I did", "What I found"]) == []


def test_require_sections_FAILS_on_missing_heading(tmp_path):
    p = _md(tmp_path, "m.md", "# What I did\nstuff")
    assert check.require_sections(p, ["What I did", "What I found"]) != []


def test_require_no_placeholders_passes(tmp_path):
    assert check.require_no_placeholders(_md(tmp_path, "m.md", "a real memo")) == []


def test_require_no_placeholders_FAILS_on_todo(tmp_path):
    assert check.require_no_placeholders(_md(tmp_path, "m.md", "results: TODO")) != []


def test_require_no_placeholders_FAILS_on_tbd(tmp_path):
    assert check.require_no_placeholders(_md(tmp_path, "m.md", "value: TBD")) != []


def test_require_a_sample_size_passes_on_n_equals(tmp_path):
    assert check.require_a_sample_size(_md(tmp_path, "m.md", "12% (n=200)")) == []


def test_require_a_sample_size_passes_on_out_of(tmp_path):
    assert check.require_a_sample_size(_md(tmp_path, "m.md", "9 out of 12 runs")) == []


def test_require_a_sample_size_FAILS_on_a_bare_rate(tmp_path):
    assert check.require_a_sample_size(_md(tmp_path, "m.md", "about 12%")) != []


# --- report ----------------------------------------------------------------

def test_report_returns_zero_when_clean(capsys):
    assert check.report("x", []) == 0
    assert "PASS" in capsys.readouterr().out


def test_report_returns_one_when_problems(capsys):
    assert check.report("x", ["bad thing"]) == 1
    assert "bad thing" in capsys.readouterr().out
