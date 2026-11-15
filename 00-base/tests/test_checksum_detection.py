"""verify_checksums() is the thing standing between you and measuring a graph
you cannot identify. So it gets tested by actually corrupting a file, not by
being trusted."""

import json
import shutil

from gdslab import loaders


def _clone_data(tmp_path):
    dest = tmp_path / "03-data"
    shutil.copytree(loaders.DATA_DIR, dest)
    return dest


def _point_at(monkeypatch, directory):
    monkeypatch.setattr(loaders, "DATA_DIR", str(directory))
    monkeypatch.setattr(loaders, "_MANIFEST_PATH", str(directory / "MANIFEST.json"))


def test_clean_copy_verifies(tmp_path, monkeypatch):
    _point_at(monkeypatch, _clone_data(tmp_path))
    assert loaders.verify_checksums() == []


def test_a_single_changed_byte_is_detected(tmp_path, monkeypatch):
    data = _clone_data(tmp_path)
    target = data / "lesmis.edges.csv"
    content = target.read_text(encoding="utf-8")
    target.write_text(content.replace("source,target", "source,target "), encoding="utf-8")
    _point_at(monkeypatch, data)
    assert "lesmis" in loaders.verify_checksums()


def test_a_deleted_file_is_detected(tmp_path, monkeypatch):
    data = _clone_data(tmp_path)
    (data / "crime.edges.csv").unlink()
    _point_at(monkeypatch, data)
    assert "crime" in loaders.verify_checksums()


def test_an_appended_row_is_detected(tmp_path, monkeypatch):
    data = _clone_data(tmp_path)
    with open(data / "ca-GrQc.edges.csv", "a", encoding="utf-8") as fh:
        fh.write("999999,888888\n")
    _point_at(monkeypatch, data)
    assert "ca-GrQc" in loaders.verify_checksums()


def test_only_the_touched_file_is_reported(tmp_path, monkeypatch):
    data = _clone_data(tmp_path)
    with open(data / "lesmis.edges.csv", "a", encoding="utf-8") as fh:
        fh.write("1,2\n")
    _point_at(monkeypatch, data)
    assert loaders.verify_checksums() == ["lesmis"]


def test_manifest_lists_every_data_file(tmp_path, monkeypatch):
    """A file on disk that the manifest does not know about would go unchecked."""
    data = _clone_data(tmp_path)
    _point_at(monkeypatch, data)
    listed = {e["file"] for e in json.load(
        open(data / "MANIFEST.json", encoding="utf-8"))["entries"]}
    on_disk = {p.name for p in data.iterdir() if p.suffix == ".csv"}
    assert on_disk == listed
