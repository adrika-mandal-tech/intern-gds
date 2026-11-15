# Setup

Fifteen minutes, once. Everything in this pack runs offline on your own laptop
after this — no accounts, no API keys, no server, no downloads.

---

## 1. Check your Python

You need **Python 3.10 or newer**.

```bash
python --version
```

If that says 3.9 or older, or "command not found", install Python from
[python.org/downloads](https://www.python.org/downloads/) first. On macOS and
Linux you may need to type `python3` rather than `python` — if so, use `python3`
everywhere below.

## 2. Make a virtual environment

This keeps the pack's libraries separate from anything else on your machine. Do
it from **inside the `00-base/` folder**.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell refuses with an execution-policy error, run this once and try again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt should now start with `(.venv)`. That is how you know it worked, and
you need to do this step in every new terminal window.

## 3. Install the libraries

```bash
python -m pip install -r 02-setup/requirements.txt
```

Every one of these ships as a prebuilt wheel for Windows, macOS (both Intel and
Apple Silicon) and Linux. **You do not need a C compiler.** If pip starts trying
to build something from source, stop and ask — that means it could not find a
wheel for your platform, and it is a real finding rather than something to fight
through.

## 4. Run the check

```bash
python 02-setup/check_setup.py
```

You should see something very close to this. The version numbers and the machine
details will differ — that is fine and expected, and section 4 of the output is
information you will actually need in Part 1.

```
======================================================================
  Setup check
======================================================================

1. Libraries
   python         3.13.4
   networkx       3.6.1
   igraph         1.0.0
   leidenalg      0.12.0
   numpy          2.2.6
   scipy          1.18.0
   pandas         2.3.0
   matplotlib     3.11.0

2. Data files
   all 11 files match their recorded SHA-256 (7 graphs + 4 sidecars)

3. Graphs
   name                    nodes     edges
   lesmis                     77       254  ok
   unicodelang               868      1255  ok
   crime                    1380      1476  ok
   email-Eu-core             986     24929  ok
   openflights              3214     36906  ok
   facebook_combined        4039     88234  ok
   ca-GrQc                  5241     14484  ok

4. This machine
   platform       Windows-11-10.0.26200-SP0
   machine        AMD64
   cpu_count      4
   ram_gb         7.65

   Write these down. Your colleague's numbers will differ from
   yours in absolute terms and that is expected - which is exactly
   what Part 1 asks you to measure.

5. Toolkit self-test
   77 passed in 7.04s

======================================================================
  ALL CHECKS PASSED - you are set up correctly.
======================================================================
```

**The node and edge counts must match exactly.** They are the same seven graphs
your colleague is working from, and if one of you has a different file, none of
your numbers can be compared. That is what section 2 is checking — every data
file has a recorded SHA-256, and the check re-computes it.

## 5. If something failed

| What you saw | What it means |
|---|---|
| `Python 3.x is too old` | Install Python 3.10+ and remake the venv |
| `<library> is not installed` | Step 3 did not complete — re-run it and read the output |
| `these data files do not match their recorded checksum` | A data file has been modified. Re-copy the pack. **Do not** carry on — every number you measure afterwards would be about a different graph, and nothing downstream would tell you |
| `<graph> loaded as N=… expected N=…` | Same as above |
| `the toolkit's own tests did not pass` | Send us the full output. This is a problem with the pack, not with you |
| pip tries to compile something | Stop. Tell us your OS and Python version |

**A setup problem is the one thing here that is never worth struggling with
quietly.** If you are stuck for more than twenty minutes, ask.

---

**Next:** [`../01-context/graphs-from-zero.md`](../01-context/graphs-from-zero.md)
