# What Part 1 actually printed

Real output from a real run, not an illustration. **Your numbers will differ**
in the timing columns and that is the entire point of experiment 1.3 — but the
node counts, edge counts, skew, components, clustering and **iteration counts**
should match exactly. If any of those differ, stop and ask.

Reference machine: Windows 11, 4 logical cores, 7.65 GB RAM, Python 3.13.4,
networkx 3.6.1. Whole run takes well under a minute.

```
==========================================================================
  Part 1 - measuring the graphs before measuring the algorithms
==========================================================================
  machine : Windows-11-10.0.26200-SP0 | 4 cores | 7.65 GB RAM
  writing : ...\00-base\your-work\intern-A\part1

1.1  Profiling every graph
     graph                  nodes    edges    skew   comps   clust
     lesmis                    77      254     6.0       1   0.573
     unicodelang              868     1255   141.0       5   0.000
     email-Eu-core            986    24929    16.5       1   0.407
     crime                   1380     1476    25.0      20   0.000
     openflights             3214    36906    79.5       7   0.492
     facebook_combined       4039    88234    41.8       1   0.606
     ca-GrQc                 5241    14484    27.0     354   0.530

1.2  PageRank on each graph, 10 runs each
     graph                   load_s compute_s  rounds identical?
     lesmis                  0.0007    0.0020      37       yes
     unicodelang             0.0019    0.0271      67       yes
     email-Eu-core           0.0260    0.0353      14       yes
     crime                   0.0027    0.0335      54       yes
     openflights             0.1736    0.1704      40       yes
     facebook_combined       0.0913    0.3573      21       yes
     ca-GrQc                 0.0158    0.1729      41       yes

==========================================================================
  Done. Now go and interpret it - that part is yours.
==========================================================================

  Most nodes  : ca-GrQc              (5241 nodes)
  Slowest     : facebook_combined    (4039 nodes)

  Those are not the same graph. Section 2 of your memo should
  explain why, and say what DOES predict the cost.

  PageRank gave identical scores across all 10 runs on 7 of 7 graphs.
  Worth remembering when you meet an algorithm that does not.
```

## Which columns should match, and which should not

| Column | Should match ours? | Why |
|---|---|---|
| nodes, edges, skew, comps, clust | **exactly** | Properties of the data. Different means something is wrong |
| rounds | **exactly** | The algorithm is deterministic — same input, same number of rounds, on any machine |
| load_s, compute_s | **no** | Your hardware |
| identical? | should be `yes` throughout | If any says `NO`, that is a genuine finding — write it up |

That table is most of experiment 1.3. Three kinds of number, and only two of them
survive being carried to another machine.

## Files it writes

```
your-work/<your-name>/part1/
├── profiles.csv                    7 rows, one per graph
├── profiles.provenance.json
├── pagerank_runs.csv               70 rows, 7 graphs x 10 runs
├── pagerank_runs.provenance.json
└── charts/
    ├── degree_<graph>.png          x7
    ├── cost_vs_nodes.png
    ├── cost_vs_edges.png
    ├── rounds_vs_skew.png
    └── rounds_vs_nodes.png
```

## If it fails

**`data files do not match their checksums`** — a file in `03-data/` has been
modified. Re-copy the pack. Do not proceed.

**`ModuleNotFoundError`** — run from the pack root
(`python part-1/run_part1.py --who yourname`), not from inside `part-1/`.

**A `RuntimeError` about PageRank not settling** — that would be a genuine
finding on one of these graphs. Record which graph, and tell us.
