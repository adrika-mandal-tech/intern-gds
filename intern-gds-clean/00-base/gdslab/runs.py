"""The measurement harness. Everything you measure should go through this.

Three ideas, each of which exists because skipping it produces confident wrong
numbers.

**One row per run, never a summary.** ``Recorder`` writes one line per
execution. Averages, spreads and rates are computed afterwards, from the rows.
This is deliberate: if the harness wrote summaries, a single run would look
exactly like two hundred runs in the output file, and nobody reading your
results later could tell the difference. Writing the rows makes the sample size
impossible to lose.

**Warm up before timing.** The first call into a library pays for imports,
lazily-built lookup tables and whatever else. Measured on the reference machine:
the first ``pagerank`` call on a 77-node graph took 0.3239 s and the next three
took 0.0012 s. That is a factor of 270, on a graph small enough to draw by hand.
If you time the first call you are timing Python's import machinery, not the
algorithm. ``timed()`` discards a warm-up call by default.

**Record the machine.** Every results file gets a ``.provenance.json``
sidecar naming the platform, the CPU count, the RAM and every library version.
Two people running the same script on different laptops will get different
absolute times and identical iteration counts; without the sidecar you cannot
tell which of those you are looking at.
"""

from __future__ import annotations

import csv
import datetime
import json
import os
import platform
import sys
import time


def _ram_gb() -> float:
    """Total physical RAM in GB, best effort across platforms. 0.0 if unknown."""
    try:  # Linux / most Unix
        return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2 ** 30, 2)
    except (ValueError, OSError, AttributeError):
        pass
    if sys.platform == "win32":
        try:
            import ctypes

            class _MemStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

            status = _MemStatus()
            status.dwLength = ctypes.sizeof(_MemStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return round(status.ullTotalPhys / 2 ** 30, 2)
        except Exception:
            pass
    if sys.platform == "darwin":
        try:
            import subprocess
            out = subprocess.check_output(["sysctl", "-n", "hw.memsize"])
            return round(int(out.strip()) / 2 ** 30, 2)
        except Exception:
            pass
    return 0.0


def _version(module_name: str) -> str:
    try:
        module = __import__(module_name)
    except ImportError:
        return "not installed"
    return str(getattr(module, "__version__", None)
               or getattr(module, "version", None) or "unknown")


def provenance() -> dict:
    """Everything needed to interpret a timing later. Written beside every CSV."""
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
        "cpu_count": os.cpu_count() or 0,
        "ram_gb": _ram_gb(),
        "networkx": _version("networkx"),
        "igraph": _version("igraph"),
        "leidenalg": _version("leidenalg"),
        "numpy": _version("numpy"),
        "scipy": _version("scipy"),
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }


def timed(fn, *args, warmup: int = 1, **kwargs):
    """Run ``fn`` and return ``(elapsed_seconds, result)``.

    Calls ``fn`` ``warmup`` times first and throws those results away. Pass
    ``warmup=0`` only when you specifically want to measure cold-start cost.
    """
    for _ in range(warmup):
        fn(*args, **kwargs)
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    return time.perf_counter() - start, result


class Recorder:
    """Writes one CSV row per run, plus a provenance sidecar.

    ``fields`` is fixed at construction. Passing an unexpected field, or
    omitting an expected one, raises - so a half-filled row cannot reach the
    file and be mistaken for a real measurement later.
    """

    def __init__(self, path: str, fields: list):
        self.path = path
        self.fields = list(fields)
        parent = os.path.dirname(os.path.abspath(path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        self._fh = open(path, "w", newline="", encoding="utf-8")
        self._writer = csv.DictWriter(self._fh, fieldnames=self.fields,
                                      lineterminator="\n")
        self._writer.writeheader()
        self.n_rows = 0

        stem = path[:-4] if path.endswith(".csv") else path
        with open(stem + ".provenance.json", "w", encoding="utf-8") as fh:
            json.dump(provenance(), fh, indent=2)

    def row(self, **kwargs):
        unknown = set(kwargs) - set(self.fields)
        if unknown:
            raise ValueError("unknown field(s) %s; expected %s"
                             % (sorted(unknown), self.fields))
        missing = set(self.fields) - set(kwargs)
        if missing:
            raise ValueError("missing field(s) %s; every row must be complete"
                             % sorted(missing))
        self._writer.writerow(kwargs)
        self.n_rows += 1

    def close(self):
        if not self._fh.closed:
            self._fh.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


def run_many(fn, seeds, recorder: Recorder, extra: dict | None = None,
             warmup: int = 1):
    """Run ``fn(seed=s)`` once per seed, timing each, recording one row each.

    ``fn`` must accept a ``seed`` keyword. The recorder must have at least the
    fields ``seed``, ``elapsed_s`` and ``result``, plus every key in ``extra``.
    """
    extra = extra or {}
    warmed = False
    for seed in seeds:
        if not warmed:
            for _ in range(warmup):
                fn(seed=seed)
            warmed = True
        start = time.perf_counter()
        result = fn(seed=seed)
        elapsed = time.perf_counter() - start
        recorder.row(seed=seed, elapsed_s=round(elapsed, 6), result=result, **extra)
