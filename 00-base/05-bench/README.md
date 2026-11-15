# The bench

Six self-contained, bite-sized experiments. They exist for when something
**stalls** — a run fails, you are waiting on your colleague, a direction turns
out to be a dead end.

## When to use these

**Not** when you finish a part early. If you finish early, **go deeper on the
part you are in** — the "if you finish early" section at the end of every brief
tells you how. Depth on a question you already understand is worth more than a
fresh shallow pass at a new one.

Use the bench when you are genuinely **blocked** and would otherwise be idle.

## Rules

Same as everywhere else. One row per run, sample size on every rate, provenance
sidecars kept, a short memo saying what you found and what you could not
determine.

Put results in `your-work/<your-name>/bench/<Bn>/`. There is no checker for these
— they are yours to design, which is part of the point.

## The six

| | Question | Size |
|---|---|---|
| [B1](B1-memory.md) | How much memory does the same graph take in three different representations? | small |
| [B2](B2-scale-ceiling.md) | At what size does each algorithm stop being usable on your laptop? | larger |
| [B3](B3-resolution-limit.md) | Can Louvain find small communities, or does it merge them regardless? | small |
| [B4](B4-split-inflation.md) | How much does a random train/test split inflate a link-prediction score? | larger |
| [B5](B5-pagerank-undirected.md) | On an undirected graph, does PageRank tell you anything degree does not? | small |
| [B6](B6-weighted-communities.md) | Do edge weights change community structure, or only paths? | small |

**B5 and B3 are the two most likely to produce something we did not know**, if
you are choosing.

## A note on these being open-ended

The four parts hand you a protocol. These do not — they give you a question and
leave the design to you.

That is deliberate, and it is harder than it looks. Before you run anything,
write down in your log: what you expect to see, and what result would change your
mind. A measurement you cannot be surprised by is not a measurement.
