import csv
import json
import time

import pytest

from gdslab import runs


def test_provenance_records_the_machine():
    p = runs.provenance()
    for key in ("python", "platform", "machine", "cpu_count", "ram_gb",
                "networkx", "numpy", "utc"):
        assert p[key], key


def test_timed_excludes_first_call_cost():
    state = {"n": 0}

    def slow_first():
        state["n"] += 1
        time.sleep(0.20 if state["n"] == 1 else 0.01)

    elapsed, _ = runs.timed(slow_first, warmup=1)
    assert elapsed < 0.10, "warm-up call leaked into the timing"


def test_timed_returns_the_result():
    elapsed, result = runs.timed(lambda: 6 * 7)
    assert result == 42
    assert elapsed >= 0


def test_timed_with_no_warmup_includes_the_first_call():
    state = {"n": 0}

    def slow_first():
        state["n"] += 1
        time.sleep(0.20 if state["n"] == 1 else 0.01)

    elapsed, _ = runs.timed(slow_first, warmup=0)
    assert elapsed >= 0.19


def test_recorder_writes_one_row_per_call(tmp_path):
    path = tmp_path / "out.csv"
    rec = runs.Recorder(str(path), ["seed", "value"])
    for s in range(3):
        rec.row(seed=s, value=s * 2)
    rec.close()
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    assert len(rows) == 3
    assert rows[2]["value"] == "4"


def test_recorder_writes_a_provenance_sidecar(tmp_path):
    path = tmp_path / "out.csv"
    runs.Recorder(str(path), ["a"]).close()
    sidecar = tmp_path / "out.provenance.json"
    assert sidecar.exists()
    assert "networkx" in json.load(open(sidecar, encoding="utf-8"))


def test_recorder_rejects_an_unknown_field(tmp_path):
    rec = runs.Recorder(str(tmp_path / "o.csv"), ["a"])
    with pytest.raises(ValueError):
        rec.row(a=1, bogus=2)


def test_recorder_rejects_a_missing_field(tmp_path):
    rec = runs.Recorder(str(tmp_path / "o.csv"), ["a", "b"])
    with pytest.raises(ValueError):
        rec.row(a=1)


def test_recorder_works_as_a_context_manager(tmp_path):
    path = tmp_path / "ctx.csv"
    with runs.Recorder(str(path), ["a"]) as rec:
        rec.row(a=1)
    assert len(list(csv.DictReader(open(path, encoding="utf-8")))) == 1


def test_run_many_records_every_seed(tmp_path):
    path = tmp_path / "m.csv"
    with runs.Recorder(str(path), ["graph", "seed", "elapsed_s", "result"]) as rec:
        runs.run_many(lambda seed: seed + 1, seeds=range(5), recorder=rec,
                      extra={"graph": "g"})
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    assert len(rows) == 5
    assert [r["result"] for r in rows] == ["1", "2", "3", "4", "5"]
    assert {r["graph"] for r in rows} == {"g"}


def test_run_many_uses_distinct_seeds(tmp_path):
    path = tmp_path / "s.csv"
    with runs.Recorder(str(path), ["seed", "elapsed_s", "result"]) as rec:
        runs.run_many(lambda seed: seed, seeds=range(20), recorder=rec)
    seeds = [r["seed"] for r in csv.DictReader(open(path, encoding="utf-8"))]
    assert len(set(seeds)) == 20
