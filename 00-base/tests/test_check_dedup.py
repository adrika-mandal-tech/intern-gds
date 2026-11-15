"""report() collapses duplicates, and the memo helpers label the file they were
actually given. Both were real defects caught by running the Part 1 checker."""

from gdslab import check


def test_report_collapses_duplicates(capsys):
    code = check.report("x", ["same thing", "same thing", "same thing"])
    out = capsys.readouterr().out
    assert code == 1
    assert out.count("same thing") == 1
    assert "1 problem(s)" in out


def test_report_preserves_order(capsys):
    check.report("x", ["b", "a", "b", "c"])
    out = capsys.readouterr().out
    assert out.index("- b") < out.index("- a") < out.index("- c")


def test_missing_file_is_labelled_with_what_it_is(tmp_path):
    missing = str(tmp_path / "nope.md")
    assert "calibration note" in check.require_no_placeholders(
        missing, what="calibration note")[0]
    assert "memo" in check.require_no_placeholders(missing)[0]


def test_sections_helper_takes_a_label(tmp_path):
    missing = str(tmp_path / "nope.md")
    assert "synthesis" in check.require_sections(missing, ["A"], what="synthesis")[0]


def test_sample_size_helper_takes_a_label(tmp_path):
    missing = str(tmp_path / "nope.md")
    assert "replication note" in check.require_a_sample_size(
        missing, what="replication note")[0]
