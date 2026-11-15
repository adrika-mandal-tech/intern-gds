# The graphs

Seven real graphs plus a synthetic generator. They ship with the pack, so
everything works offline and — more importantly — **you and your colleague are
provably working from identical files.** Every one has a recorded SHA-256, and
`check_setup.py` re-computes it.

Do not edit anything in this folder. If you open one of these in Excel and save
it, Excel will reformat a column, the checksum will stop matching, and every
number you measure afterwards will quietly be about a different graph.

---

## The zoo

Measured with `gdslab.profile`, not copied from anywhere:

| Graph | Nodes | Edges | Density | Median degree | Max degree | Skew | Components | Clustering |
|---|---|---|---|---|---|---|---|---|
| `lesmis` | 77 | 254 | 0.0868 | 6 | 36 | 6.0 | 1 | 0.573 |
| `unicodelang` | 868 | 1,255 | 0.0033 | 1 | 141 | 141.0 | 5 | **0.000** |
| `crime` | 1,380 | 1,476 | 0.0016 | 1 | 25 | 25.0 | 20 | **0.000** |
| `email-Eu-core` | 986 | 24,929 | 0.0257 | 33 | 544 | 16.5 | 1 | 0.407 |
| `openflights` | 3,214 | 36,906 | 0.0036 | 6 | 477 | 79.5 | 7 | 0.492 |
| `facebook_combined` | 4,039 | 88,234 | 0.0108 | 25 | 1,045 | 41.8 | 1 | 0.606 |
| `ca-GrQc` | 5,241 | 14,484 | 0.0011 | 3 | 81 | 27.0 | **354** | 0.530 |

**Skew** is `max degree ÷ median degree` — how many times more connected the
busiest node is than the typical one.

Two things in that table are worth staring at before you start.

**`ca-GrQc` and `facebook_combined` are roughly the same size and are not
remotely the same problem.** `ca-GrQc` has *more* nodes (5,241 vs 4,039) and
*six times fewer* edges, and it is shattered into 354 separate pieces while
`facebook_combined` is a single connected lump. Any statement of the form "this
algorithm handles graphs of about five thousand nodes" is close to meaningless
across those two.

**`unicodelang` and `crime` have a clustering coefficient of exactly zero.**
That is not a data problem. Clustering counts triangles, a triangle is a cycle
of length three, and a bipartite graph cannot contain an odd cycle at all — every
step crosses from one side to the other. Zero is the only value it could
possibly take. When a metric returns a suspiciously round number, the first
question is always whether it *could* have returned anything else.

---

## What each one is, and why it is here

### `lesmis` — 77 nodes, 254 edges, weighted
Characters in *Les Misérables*; an edge means two characters appear in a scene
together, and the weight is how many scenes. Small enough to print out and check
by hand, which is exactly what it is for: when a result surprises you on a big
graph, reproduce it here first.

**Note the weight means "how strongly related", not "how expensive".** Two
characters with weight 10 are *closer*, not further apart. Feeding this to a
shortest-path algorithm without thinking gives you the route through the
*weakest* relationships. That trap is deliberate.

- Source: <https://networks.skewed.de/net/lesmis>
- Origin: Knuth, *The Stanford GraphBase* (1993)

### `unicodelang` — 868 nodes, 1,255 edges, **bipartite**
Which languages are spoken in which territories. One side is territories, the
other is languages, and every edge crosses between them.

Its side labels are in `unicodelang.sides.csv`.

- Source: <https://networks.skewed.de/net/unicodelang>

### `crime` — 1,380 nodes, 1,476 edges, **bipartite**
People and crimes in St Louis in the 1990s; an edge means that person was
involved in that crime, as suspect, victim or witness. 829 people on one side,
551 crimes on the other.

This is the shape a graph takes when you build it out of documents: things on
one side, the places those things were mentioned on the other. Part 4 is
entirely about what that shape does to your answers.

Side labels in `crime.sides.csv`.

- Source: <https://networks.skewed.de/net/crime>

### `email-Eu-core` — 986 nodes, 24,929 edges, directed, **has ground truth**
Email between members of a European research institution. Directed: an edge from
A to B means A emailed B.

**This is the only graph in the pack where you can find out whether an algorithm
is right rather than merely whether two algorithms agree.** Every person's real
department is recorded in `email-Eu-core.labels.csv` — 42 of them. When a
community-detection algorithm proposes a grouping, you can score it against
what the organisation actually is.

Guard that distinction carefully. On the other six graphs you can only measure
*agreement*. Agreement is not correctness: two algorithms can agree and both be
wrong.

- Source: <https://snap.stanford.edu/data/email-Eu-core.html>

### `openflights` — 3,214 nodes, 36,906 edges, directed, **weighted with a real cost**
Regularly scheduled flights between airports worldwide. **The weight is
great-circle distance in kilometres** — a genuine cost, where bigger means
further, which is what a shortest-path algorithm expects.

This is the graph for the weights work, and it is the honest version of the
textbook example: a direct flight is one hop and might be enormously far; two
hops via a hub might be much shorter. "Fewest stops" and "shortest distance" are
different questions with different answers.

- Source: <https://networks.skewed.de/net/openflights>

### `facebook_combined` — 4,039 nodes, 88,234 edges
Merged friend circles from Facebook. Dense, heavily clustered (0.606), one
connected piece. The most expensive graph in the pack to run anything on.

- Source: <https://snap.stanford.edu/data/ego-Facebook.html>

### `ca-GrQc` — 5,241 nodes, 14,484 edges
Co-authorship in arXiv's General Relativity section; an edge means two people
wrote a paper together. Sparse and **shattered into 354 components** — most
research groups never co-author with most other research groups.

Anything that assumes a connected graph will behave strangely here, which is why
it is in the pack.

- Source: <https://snap.stanford.edu/data/ca-GrQc.html>

### Synthetic graphs — generated, not shipped
`make_synthetic.py` builds graphs where **you already know the right answer**:
planted-partition and LFR benchmark graphs come with their true communities
built in, plus a two-triangles-and-a-bridge graph small enough to reason about
completely.

Generated from a fixed seed, so they are identical on your machine and your
colleague's.

---

## Why the counts differ from the source pages

If you look up these graphs online, three of them will report different numbers
from the table above. That is not an error, and you should be able to check the
explanation rather than take it on trust.

Every edge list here has been normalised the same way: **self-loops dropped**
(an edge from a node to itself), and for undirected graphs **reciprocal
duplicates collapsed** (a file listing both `A,B` and `B,A` describes one edge,
not two).

| Graph | Source says | Ships as | Why |
|---|---|---|---|
| `email-Eu-core` | 1,005 / 25,571 | 986 / 24,929 | 642 self-loops removed: 25,571 − 642 = **24,929**. 19 people appear *only* in emails to themselves, so they vanish with the loops |
| `ca-GrQc` | 5,242 / 14,496 | 5,241 / 14,484 | The file lists every undirected edge twice. (28,980 − 12 self-loops) ÷ 2 = **14,484**. The source counts the 12 loops as edges; we do not |
| `openflights` | 3,214 / 66,771 | 3,214 / 36,906 | It is a *multigraph*: several airlines fly the same route, so the same airport pair appears many times. 29,864 duplicates collapsed. **All 36,907 pairs were checked and every duplicate carries an identical distance**, so collapsing loses nothing |

The other four match their sources exactly.

That third row is worth a moment. "Every duplicate carries an identical
distance" is a claim that had to be *checked* — great-circle distance between
two fixed airports obviously cannot vary, but "obviously" is how wrong numbers
get into datasets. It was checked across all 36,907 pairs. It held.

---

## Provenance

`MANIFEST.json` records, for every file: source URL, licence, description,
node and edge counts, how many self-loops and duplicates were dropped, and the
SHA-256. `gdslab.loaders` reads it as the single source of truth — the loader
does not have the graph sizes hard-coded anywhere, it asks the manifest.

These are public research datasets, used here for research and education. Each
entry carries its own citation.
