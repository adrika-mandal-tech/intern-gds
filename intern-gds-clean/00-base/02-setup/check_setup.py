"""Run this once, before anything else.

It checks four things, in order, and stops at the first one that fails:

  1. every library imports
  2. every shipped data file is byte-for-byte what it should be
  3. every graph loads at exactly the size it is documented at
  4. the toolkit's own test suite passes

If all four pass you are set up correctly, and step 3 in particular means the
seven graphs on your disk are the same seven graphs everybody else is working
from - which is what makes your numbers comparable to your colleague's.

    python 02-setup/check_setup.py
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, BASE)

EXPECTED_SIZES = {
    "lesmis": (77, 254),
    "unicodelang": (868, 1255),
    "crime": (1380, 1476),
    "email-Eu-core": (986, 24929),
    "openflights": (3214, 36906),
    "facebook_combined": (4039, 88234),
    "ca-GrQc": (5241, 14484),
}


def fail(message: str) -> None:
    print("\n  FAILED: %s" % message)
    print("\n  Do not start the work until this is fixed. If you are stuck for")
    print("  more than twenty minutes, ask - a setup problem is the one thing")
    print("  here that is never worth struggling with quietly.")
    sys.exit(1)


def main() -> None:
    print("=" * 70)
    print("  Setup check")
    print("=" * 70)

    # 1. libraries -----------------------------------------------------------
    print("\n1. Libraries")
    if sys.version_info < (3, 10):
        fail("Python %d.%d is too old; this pack needs 3.10 or newer."
             % sys.version_info[:2])
    print("   %-14s %s" % ("python", sys.version.split()[0]))
    for module_name in ("networkx", "igraph", "leidenalg", "numpy", "scipy",
                        "pandas", "matplotlib"):
        try:
            module = __import__(module_name)
        except ImportError:
            fail("%s is not installed. Run:\n"
                 "       python -m pip install -r 02-setup/requirements.txt"
                 % module_name)
        version = (getattr(module, "__version__", None)
                   or getattr(module, "version", None) or "unknown")
        print("   %-14s %s" % (module_name, version))

    # 2. data integrity ------------------------------------------------------
    print("\n2. Data files")
    from gdslab import loaders, runs

    bad = loaders.verify_checksums()
    if bad:
        fail("these data files do not match their recorded checksum: %s\n"
             "       Something has modified them. Re-copy the pack; do not\n"
             "       measure anything against a file you cannot identify." % bad)
    n_files = len(loaders._manifest()["entries"])
    print("   all %d files match their recorded SHA-256 "
          "(%d graphs + %d sidecars)"
          % (n_files, len(EXPECTED_SIZES), n_files - len(EXPECTED_SIZES)))

    # 3. graphs load ---------------------------------------------------------
    print("\n3. Graphs")
    print("   %-20s %8s %9s" % ("name", "nodes", "edges"))
    for name, (nodes, edges) in EXPECTED_SIZES.items():
        G = loaders.load(name)
        got = (G.number_of_nodes(), G.number_of_edges())
        if got != (nodes, edges):
            fail("%s loaded as N=%d E=%d, expected N=%d E=%d"
                 % (name, got[0], got[1], nodes, edges))
        print("   %-20s %8d %9d  ok" % (name, nodes, edges))

    # 4. this machine --------------------------------------------------------
    print("\n4. This machine")
    info = runs.provenance()
    for key in ("platform", "machine", "cpu_count", "ram_gb"):
        print("   %-14s %s" % (key, info[key]))
    print("\n   Write these down. Your colleague's numbers will differ from")
    print("   yours in absolute terms and that is expected - which is exactly")
    print("   what Part 1 asks you to measure.")

    # 5. toolkit tests -------------------------------------------------------
    print("\n5. Toolkit self-test")
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"],
                            cwd=BASE, capture_output=True, text=True)
    tail = [line for line in result.stdout.strip().splitlines() if line.strip()]
    print("   %s" % (tail[-1] if tail else "(no output)"))
    if result.returncode != 0:
        fail("the toolkit's own tests did not pass. Full output:\n\n%s"
             % result.stdout)

    print("\n" + "=" * 70)
    print("  ALL CHECKS PASSED - you are set up correctly.")
    print("=" * 70)
    print("\n  Next: read 01-context/graphs-from-zero.md")


if __name__ == "__main__":
    main()
