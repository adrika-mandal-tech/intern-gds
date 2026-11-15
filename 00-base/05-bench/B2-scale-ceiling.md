# B2 — Where does each algorithm stop being usable?

**Output:** `your-work/<your-name>/bench/B2/`

---

## The question

Every mature graph library has an **estimate** mode: before running anything, it
tells you what the job would need, so an impossible request becomes a sentence
rather than a crash.

To build that you need to know how each algorithm's cost actually grows.

> **For each algorithm, at what graph size does it stop being usable on your
> laptop — and could you have predicted that before running it?**

## Method

Use `03-data/make_synthetic.py` to generate graphs of increasing size **with the
same shape**, so size is the only thing changing. That is the point: the real
graphs in the pack differ in shape *and* size at once, which is exactly why Part
1 could not settle this.

For each algorithm — degree, PageRank, Louvain, closeness, betweenness,
similarity — time it at increasing sizes until either it exceeds a limit you set
in advance (say 60 seconds) or you run out of patience.

**Set that limit before you start**, and write it in your log. Deciding what
counts as "too slow" after seeing the numbers is how you talk yourself into a
conclusion.

## The deliverable

A table someone could actually use:

| Algorithm | Growth looks like | Usable to about | At which it takes |
|---|---|---|---|
| degree | | | |
| PageRank | | | |
| Louvain | | | |
| closeness | | | |
| betweenness | | | |
| node similarity | | | |

Plus the raw timings, one row per run.

## Questions to answer

1. **Fit the growth.** For each algorithm, does cost grow roughly linearly with
   nodes? With edges? Quadratically? Say how you decided — a log-log plot with a
   fitted slope is the standard way and it is worth learning.
2. **Extrapolate, then check.** Predict the time at a size you have not run.
   Then run it. How close were you? An extrapolation you have tested is worth ten
   you have not.
3. Which algorithm hits the wall first, and by how much of a margin over the next?
4. **Does holding shape constant change the answer from Part 1?** Part 1 found
   node count did not predict cost across the seven real graphs. Here shape is
   fixed. Does size predict cost now? This is the interesting question in B2 and
   it is worth most of your write-up.
5. Now vary the *shape* at fixed size — `planted_partition` with different
   `p_in`/`p_out`, or LFR with different `mu`. How much does cost move when size
   does not move at all?

## Why this matters

If you can answer (2) reliably, you can refuse a job before starting it. If you
cannot, then nobody can promise anything about a graph they have not already run
— which is itself a finding, and an important one to state plainly.
