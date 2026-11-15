# B1 — The same graph, three ways of storing it

**Output:** `your-work/<your-name>/bench/B1/`

---

## The question

A graph is just nodes and edges, so it takes the space it takes. Except it does
not: the same graph stored three different ways can differ enormously in memory,
and there is a widely-repeated claim that a 260-million-edge graph occupies 9 GB
in one library, 14 GB in another and 93 GB in a third.

**Measure it yourself, at a scale your laptop can hold.**

## What to compare

The same graph, loaded three ways:

1. **networkx** — a dict of dicts of dicts. Flexible, every node can carry
   arbitrary attributes.
2. **igraph** — compact internal arrays, C under the hood.
3. **scipy sparse (CSR)** — `nx.to_scipy_sparse_array(G)`. Just the structure:
   two integer arrays and nothing else.

## How to measure memory honestly

This is the hard part, and getting it wrong is the main risk.

`sys.getsizeof` **does not work** on nested structures — it reports the size of
the outer container only, so a networkx graph will look tiny. If you use it and
report that networkx is efficient, you have measured the wrong thing.

Two approaches that do work:

- **`tracemalloc`** — start tracing, build the object, take a snapshot, compare.
  Measures what Python allocated.
- **Process RSS before and after** — via `resource` on Unix or a ctypes call on
  Windows. Cruder, includes interpreter noise, but catches allocations Python
  does not see.

Use one, say which, and say what it does not capture. If you can, use both and
report where they disagree — a disagreement between two measurement methods is
itself worth writing down.

## Suggested shape

- Measure across all seven graphs so you have a range of sizes.
- Report **bytes per edge** and **bytes per node** as well as totals, so the
  numbers survive being compared to a different graph.
- Report the **ratio** between representations, not just absolute bytes. Your
  laptop is not the interesting variable.

## Questions to answer

1. What is the ratio between the largest and smallest representation?
2. Does the ratio hold constant across graph sizes, or does it change?
3. What is networkx actually spending the memory *on*? (Consider: what can a
   networkx graph do that a CSR array cannot?)
4. The claimed ratio is about tenfold. What do you measure, and does your number
   support or contradict it? **Be careful about scale** — you are measuring at
   thousands of edges and the claim is at 260 million. Say what that gap does to
   your confidence.
5. If you had to hold a graph a hundred times larger than `facebook_combined`,
   which representation would you choose, and what would you give up?

## The trap

Do not measure the memory of a graph you have already built in another form.
Building the networkx graph and then converting to CSR measures the *conversion*,
not the CSR representation — and the networkx object is still in memory while you
do it. Measure each in isolation, in a fresh process if you have to.
