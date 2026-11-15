# What a results file looks like

Every experiment writes a CSV through `gdslab.runs.Recorder`. This page explains
the shape and the two rules that go with it.

---

## Rule 1 — one row per run, never a summary

If you run something 200 times, the file has 200 rows. Averages, spreads, rates
and percentages are computed **afterwards**, from those rows.

This is the single most important convention in the pack, and it exists for one
reason: **a summary destroys the sample size.** A file containing
`mean_modularity, 0.4231` looks exactly the same whether it came from one run or
a thousand. A file containing 200 rows cannot lie about how many runs there were.

It also means anyone — you next week, your colleague, whoever reads the memo —
can recompute any number you quote without rerunning anything.

So: **never write a summary row into a results file.** Put summaries in your
memo, computed from the raw file, and say which file.

## Rule 2 — every results file carries its provenance

`Recorder` automatically writes a sidecar next to your CSV:

```
louvain_runs.csv
louvain_runs.provenance.json
```

The sidecar records the platform, CPU count, RAM, Python version, and the version
of every library involved, plus a UTC timestamp.

Keep them together. A timing without provenance cannot be interpreted by anybody,
including you, three weeks from now — and the whole of Part 1 depends on being
able to compare two machines.

---

## The standard columns

Most experiment files carry these. Individual briefs add their own.

| Column | Meaning |
|---|---|
| `graph` | which graph, by its name in `03-data/` |
| `algorithm` | what was run |
| `seed` | the seed for this run. **Must differ between runs** — a repeated seed repeats the answer, silently turning N runs into one run wearing a bigger sample size |
| `elapsed_s` | seconds for the compute step, warm (excludes the warm-up call) |
| `load_s` | seconds to load/prepare the graph, where the experiment separates it |
| `n_nodes`, `n_edges` | so the file is self-describing without a join |

Then whatever the experiment measures — `modularity`, `n_communities`,
`ari_vs_run1`, `top10_overlap`, and so on.

## Using one

```python
import pandas as pd

runs = pd.read_csv("your-work/intern-A/part2/louvain_runs.csv")

# the summary goes in your MEMO, computed here - not into the CSV
print(runs.groupby("graph")["modularity"].agg(["count", "mean", "std", "min", "max"]))
```

Note `count` in that aggregation. Always include it. It is your sample size, and
it belongs in the memo sentence alongside the number.

## Writing one

```python
from gdslab import runs

FIELDS = ["graph", "algorithm", "seed", "elapsed_s", "n_communities", "modularity"]

with runs.Recorder("your-work/intern-A/part2/louvain_runs.csv", FIELDS) as rec:
    for seed in range(200):
        ...
        rec.row(graph="crime", algorithm="louvain", seed=seed,
                elapsed_s=elapsed, n_communities=len(communities),
                modularity=q)
```

`Recorder` will raise if you pass a field it does not expect, or leave one out.
That is deliberate: a half-filled row that reaches the file is indistinguishable
later from a real measurement.

---

## Where your files go

```
your-work/<your-name>/
├── first-impressions.md
├── research-log.md
├── questions.md
├── part1/
│   ├── part1-memo.md
│   ├── profiles.csv
│   ├── pagerank_runs.csv
│   ├── *.provenance.json
│   └── charts/
├── part2/
└── ...
```

One folder per part. Keep the provenance sidecars. Keep the charts with the CSVs
they came from.
