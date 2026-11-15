# Questions — Solo

Write things down here **the moment they are unclear**, even if you resolve them
yourself an hour later. Especially then.

The ones you resolved yourself are often the most valuable entries in this file,
because they mark exactly where the pack failed to explain something and somebody
had to work it out. We cannot see those unless you record them.

Bring this file to every check-in.

---

## Open

### Q1 — How do I verify claims C02–C12 without access to the primary sources?

**Context:** claims.jsonl has 12 claims requiring primary-source verification. I have direct measurement for C01, but C02–C12 need papers, blog posts, and documentation I don't have local copies of.

**What I've tried:** Looking for PDFs in the corpus directory. The life_science_corpus contains biomedical papers, not the CS papers needed for these claims.

**Why it matters:** Until these are filled, claims.jsonl is 1/12 complete and claims-memo.md is incomplete.

---

## Resolved myself

### Q2 — Why does scipy fail with Python 3.10.20?

**Context:** Setting up the environment in Phase 0, scipy import failed with system Python.

**Answer I found:** The system Python had a version conflict. Creating an isolated venv with Python 3.10.20 resolved it.

**Where I found it:** "Working with virtual environments" section of the brief.

**Should the pack have said this?** yes — the scipy compatibility issue is mentioned but the exact fix (create new venv) is not explicit.

---

### Q3 — Why can't I do cross-machine calibration?

**Context:** calibration.md says to compare hashes between two runs on two machines. Only one machine available.

**Answer I found:** Solo execution means no colleague machine to compare with. Documented this in calibration.md rather than pretending it was done.

**Where I found it:** planner.html header says "Solo Execution".

**Should the pack have said this?** it did and I missed it — the planner.html header clearly states solo execution, but the calibration.md instructions assume a pair.

---

## Things in this pack I think are wrong

### Q4 — check_part1.py passes blank template memos

**Where:** `gdslab/check.py` — `check_part1.py` and `require_no_placeholders`

**What it says:** The checker verifies "your memo has its sections and no leftover placeholders".

**What I measured / what I think is right:** The placeholder list in check.py:24 is `("TODO", "TBD", "FIXME", "XXX", "<fill in>", "lorem ipsum")`. The templates ship with `<your name>`, `<the question you were answering>`, and `<start> to <end>` — none match. The sample-size check looks for `\b\d+\s+runs?\b` and `sample size`, which the blank template satisfies by existing. The checker passes a 100% blank memo.

**How confident:** high — tested by appending TODO (failed as expected) and removing a heading (failed as expected), confirming the machinery works but cannot see the pack's own templates.

---

### Q5 — Part 3B §2.3 ground truth ARI range wrong

**Where:** `part3/part3b-memo.md` section 2.3

**What it says:** "~0.45–0.55" for mean ARI vs truth

**What I measured:** Recomputed from ground_truth_scores.csv: Louvain 0.308, Leiden 0.305. The spread is 0.217–0.371 — no single run falls inside the published band.

**How confident:** high — recomputed from the CSV in a fresh pass.

---

### Q6 — Part 4 §2.4 ARI values wrong

**Where:** `part4/part4-memo.md` section 2.4

**What it says:** "~0.3–0.4" for all four ARI values

**What I measured:** Recomputed from projection_effect.csv: crime side 0 = 0.5688, crime side 1 = 0.5751, unicodelang side 0 = 0.1702, unicodelang side 1 = 0.3506. The crime values are dramatically higher than stated.

**How confident:** high — recomputed from the CSV.

---

### Q7 — Part 2A §2.5 three direction rows reversed

**Where:** `part2/part2a-memo.md` section 2.5

**What it says:** lesmis node 60, crime node 1053, openflights node 815 all have "betweenness ranks it higher"

**What I measured:** Recomputed from disagreements.csv: all three have betweenness = 0.0 or near-zero, degree ranks them higher. The CSV direction column confirms "degree ranks it higher" for all three.

**How confident:** high — the zero betweenness value makes this unambiguous.

---

### Q8 — Part 2A §2.1 unicodelang claim contradicts §3.2

**Where:** `part2/part2a-memo.md` section 2.1 vs 3.2

**What it says:** §2.1: "they diverge in ranking despite high ρ" — §3.2 (same file, three paragraphs later): top-10 overlap is 1.00

**What I think is right:** §3.2 is correct. The top-10 overlap is 1.00 (perfect agreement) for degree vs PageRank on unicodelang. §2.1's wording should say they agree on the top-10.

**How confident:** high — the overlap value is computed from the data.

---

### Q9 — Part 2A §2.4 and Part 3A §3.3 reach opposite conclusions

**Where:** `part2/part2a-memo.md` §2.4 and `part3/part3a-memo.md` §3.3 (or §2.1)

**What it says:** §2.4: "edge count drives betweenness cost more than node count" — §3.3: "betweenness scales closer to V×E than E alone"

**What I measured:** Node count vs compute time Spearman = +0.964 (strongest). Degree skew = +0.357 (weakest). Betweenness scales closer to V×E than E alone — the V×E conclusion is right, the edge-count-only conclusion is wrong.

**How confident:** high — recomputed from profiles.csv and pagerank_runs.csv.

---

### Q10 — fetch_log.jsonl records 68 attempts, not 60

**Where:** `gds-workflow.html` ontology section and `gds-workflow.html` corpus structure table

**What it says:** "60 papers", "58 of 60 fetched", "58 OK, 2 failed"

**What I measured:** fetch_log.jsonl records 68 attempts, 62 successes. Six anchor papers (A07–A12) initially failed, all six later retrieved. The corpus is 62 PDFs (12 anchor + 50 bulk), not 60.

**How confident:** high — counted entries in fetch_log.jsonl.

---

### Q11 — 1% sampling speedup range wrong

**Where:** `gds-workflow.html` betweenness methodology section and `graph_analysis.html` Finding 4

**What it says:** "~95–104×" speedup at 1% sampling

**What I measured:** Recomputed from betweenness_approx.csv: the measured range is 86.8–104.5×. Quote the floor as measured.

**How confident:** high — recomputed from the CSV.

---

### Q12 — Colleague dependency is fictional

**Where:** `gds-workflow.html` and `planner.html`

**What it says:** "Phase 5 depends on colleague output", "P5 replication dependency", "If colleague output is delayed, Phase 5 slips"

**What I think is right:** There is no colleague — solo execution. The claims strand depends on neither a colleague nor any code. It is twelve published claims checked against primary sources. Change "blocked" to "outstanding".

**How confident:** high — planner.html header says "Solo Execution".

---

### Q13 — Part 3B §2.3 community count wrong

**Where:** `part3/part3b-memo.md` section 2.3

**What it says:** "6–9" communities

**What I measured:** Recomputed from ground_truth_scores.csv: Louvain min=6, max=8; Leiden min=6, max=8. Range is 6–8, not 6–9.

**How confident:** high — recomputed from the CSV.
