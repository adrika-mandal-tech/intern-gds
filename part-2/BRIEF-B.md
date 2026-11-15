# Part 2B — Is community detection repeatable?

**This is your track; your colleague has a different one.**
**Deliverable:** `your-work/<your-name>/part2/`

---

## 1. The question

Community detection finds groups nobody labelled. Louvain is the standard fast
method, and it works by making educated guesses seeded with randomness — because
finding the genuinely best grouping is a problem with no known efficient exact
solution.

So the algorithm may not give the same answer twice.

**How much does it vary with itself, on identical input?**

That is a prerequisite question. Until you know how much one algorithm wobbles on
its own, you cannot say anything at all about how it compares to another one —
you would be comparing two coin flips. Your Part 3 depends on this answer.

## 2. Run it

From the pack root:

```bash
python part-2/run_part2b.py --who <your-name>
```

**Three to four minutes.** 200 runs each on five graphs: `unicodelang`, `crime`,
`email-Eu-core`, `openflights`, `ca-GrQc`. Every run gets a different seed.

(Measured at 160 s and 201 s on the same reference machine on different
occasions. If yours is wildly outside that, say so — but a 25% swing between two
runs of identical code is ordinary, and it is one of the things §6 of your Part 1
brief was about.)

The shape of the output, first graph only — the rest is yours to find:

```
  unicodelang        N=868    E=1255
     communities   min=19   max=24    (6 distinct counts)
     modularity    min=0.7143 max=0.7238  spread=0.0095  sd=0.00146
     distinct partitions: 200 of 200 runs
     mean ARI vs run 1  : 0.7335    identical to run 1: 1/200
```

One file: `louvain_runs.csv`, 1,000 rows. **One row per run.** Every number in
your memo gets computed from it.

## 3. What to work out

### 3.1 How often does it give a different answer?

`partition_hash` fingerprints the grouping — same hash means byte-identical
grouping.

- On each graph, how many of the 200 runs produced a *distinct* partition?
- How many matched run 1 exactly?

State it as a rate with the sample size attached. Then say plainly what it means
for anyone writing a test of the form `assert result == expected`.

### 3.2 But is a different answer a *worse* answer?

**This is the real question, and it is not the same as §3.1.**

`modularity` scores each grouping on its own terms. Look at the spread —
min, max, standard deviation — for each graph.

Now put the two together:

> The algorithm gave a different grouping on nearly every run. Did the **quality**
> vary as much as the **grouping** did?

Answer it with both numbers side by side. This distinction is the single most
important thing in this part, and it is the reason "the results changed" is not
by itself a bug report.

### 3.3 How much do the groupings actually differ?

`ari_vs_run1` is the Adjusted Rand Index against the first run: 1.0 identical,
around 0.0 no better than chance. It ignores what groups are *called* and only
cares which nodes were put together.

- Which graph has the lowest mean ARI — that is, where does Louvain disagree with
  itself most about who belongs with whom?
- Look at that graph's row in `profiles.csv` from Part 1 (your colleague has it,
  or re-run the profiler). **Is there something about its shape that would
  explain it?** You have five graphs, so this is a hypothesis, not a conclusion —
  say which.

### 3.4 Does the number of groups move?

`n_communities` per run.

- What is the range on each graph? On one of them it is notably wide.
- If a report said "this corpus contains 28 themes", and re-running produced a
  different number, what should the report have said instead?

### 3.5 So what should you actually do?

Close with a recommendation someone could follow:

- If you need a *reproducible* answer, what do you do?
- If you need the *best* answer, what do you do?
- If you are comparing Louvain against another algorithm next week — which you
  are, in Part 3 — **how many runs do you need, and how would you decide whether
  a difference between them is real?**

Use your own measured spread to justify the number. This directly sets up your
Part 3, so it is worth getting right.

## 4. Two traps

**Do not average across graphs.** The five graphs behave differently, and a mean
over them describes none of them. Report per graph.

**Do not report `n=200` as though it settles everything.** 200 runs measures the
spread of *this algorithm on this graph on this machine*. It says nothing about a
sixth graph. Be precise about what your sample is a sample *of*.

## 5. What to hand in

```
your-work/<your-name>/part2/
├── part2-memo.md              from 04-templates/memo-template.md
├── louvain_runs.csv           1,000 rows
├── louvain_runs.provenance.json
└── charts/
    └── modularity_spread.png
```

## 6. Check your work

```bash
python part-2/check_part2.py --who <your-name> --track B
```

It requires 200 **distinct** seeds per graph. A repeated seed repeats the answer,
which would silently turn 200 runs into fewer while looking the same.

## 7. Definition of done

- [ ] `louvain_runs.csv` — 1,000 rows, 200 distinct seeds per graph
- [ ] Memo covers §3.1 to §3.5, every section of the template
- [ ] **§3.2 answered explicitly** — different vs worse, with both numbers
- [ ] Per-graph results, not a single average
- [ ] Every rate has its sample size in the same sentence
- [ ] `check_part2.py --track B` passes
- [ ] **Claims strand: C02, C06, C12 done this part**
      (`python 06-claims/check_claims.py --who <your-name> --min-done 6`)

## 8. If you finish early

Go deeper here. Options:

- **Does the spread shrink with more runs, or is it a property of the algorithm?**
  Run with `--runs 500` on the two fastest graphs and compare the standard
  deviation. Predict first.
- Take the best-scoring and worst-scoring partitions on one graph. How different
  are they by ARI? Is the highest-modularity grouping *unusual*, or one of many
  near-identical ones?
- `email-Eu-core` has real department labels (`loaders.ground_truth`). Score a
  few runs against the truth with `stats.nmi`. **Does the run with the best
  modularity also match reality best?** If not, that is a genuinely important
  finding and you should say so loudly.

That last one is worth doing if you have any time at all.
