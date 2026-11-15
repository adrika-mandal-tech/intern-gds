# Part 3A — What betweenness costs, and what you lose by cutting corners

**Your track; your colleague has a different one.**
**Deliverable:** `your-work/<your-name>/part3/`

---

## 1. Two questions

You established in Part 2A that betweenness is by far the most expensive
centrality measure and that it sometimes disagrees sharply with the cheap ones.
So you cannot always avoid it. Which raises the obvious question:

> **1. Can you approximate it? Betweenness can be computed from a sample of
> starting points instead of all of them. How big does the sample need to be
> before the answer is trustworthy — and is "trustworthy" even the right word?**

And a second, separate question, about a different way of quietly getting the
wrong answer:

> **2. If you ignore edge weights, how wrong are you, and how often?**

## 2. Run it

From the pack root:

```bash
python part-3/run_part3a.py --who <your-name>
```

**Eight to ten minutes** (measured at 447 s and 534 s on the reference machine).
Start it, then read the rest of this brief while it runs — it is doing exact
betweenness on three graphs and then 150 sampled runs.

There is a `--full` flag that adds `facebook_combined`. It roughly triples the
runtime. Optional; see §9.

Three files land: `betweenness_exact.csv`, `betweenness_approx.csv`,
`weights_effect.csv`.

## 3. The approximation question

`betweenness_approx.csv` has, for each graph, five sample sizes (1%, 2%, 5%, 10%,
25% of nodes) × 10 seeds, each compared against the exact answer by:

- `top10_overlap` — do you find the same top ten?
- `top50_overlap` — the same top fifty?
- `spearman` — do you rank *everything* the same?

**Work out:**

1. **How much sampling do you need for a reliable top ten?** Give a number, and
   say what "reliable" means in your answer — you have 10 seeds per setting, so
   you can talk about the worst case and not just the average.
2. **Compare `top10_overlap` against `spearman` at the same sample size.** They
   will not tell the same story. Which one matters depends on what you are going
   to do with the result — explain when each is the right thing to look at.
3. **Is `top50_overlap` easier or harder to get right than `top10_overlap`?**
   Think about why before you look.
4. **Does the answer differ between graphs?** If 10% is enough on one graph and
   not on another, say what distinguishes them. You have Part 1's `profiles.csv`.
5. **The verdict.** Someone asks you: *"can we just sample it?"* Answer them, in
   a sentence, with the condition attached.

**Watch out for the shape of the trade.** Look at what a given sample size costs
against what it buys. If 25% of the pivots gets you most of the way, that is a
4× saving; if you need 50% it is barely worth the complexity. Put the cost and
the quality in one table so the trade is visible.

## 4. The weights question

`weights_effect.csv` has 500 random airport pairs. For each, two routes were
computed on the same graph:

- the **fewest-hops** route (ignoring distance entirely)
- the **shortest-distance** route (using the km weights)

and then the **true distance of both** was measured. So `cost_ratio` is: how much
further you actually fly if you ignore the weights.

**Work out:**

1. **How often do the two routes differ at all?** State it as a rate over 500.
2. **When they differ, by how much?** Do not report a mean. Report the
   distribution — median, upper percentiles, worst case. This matters because
   the shape is not symmetric.
3. **The specific question:** you will find a worst case somewhere around 5×.
   You will also find a median far lower than that. So: **is a 5× error typical,
   or is it the tail?** Answer precisely, and say which number you would quote to
   somebody deciding whether weights matter — and why.
4. **`paths_differ` is true even for some routes with the same number of hops.**
   Find those. You are flying further for *no saving in stops at all*. What
   fraction of the differing routes are like that, and what does it tell you
   about what the unweighted algorithm was actually optimising?
5. Nothing warned you. No error, no flag. **How would you catch this in a system
   you did not write?** Propose something concrete and checkable.

## 5. A caution about `lesmis`

The `openflights` weights are distances — a genuine cost, where bigger is worse.
`lesmis` weights are scene counts — a *strength*, where bigger means closer.

If you are tempted to repeat the weights experiment on `lesmis`, work out first
what "the shortest path" would even mean there. This is a good half-hour and a
very good paragraph in the memo. It is also the reason §4 uses only one graph:
**there is only one graph in this pack whose weights are a cost.** Say so in your
sample-size section — a rate measured on one graph is a rate about one graph.

## 6. What to hand in

```
your-work/<your-name>/part3/
├── part3-memo.md
├── betweenness_exact.csv
├── betweenness_approx.csv
├── weights_effect.csv
├── *.provenance.json
└── charts/
```

## 7. Check your work

```bash
python part-3/check_part3.py --who <your-name> --track A
```

## 8. Definition of done

- [ ] All three CSVs with provenance
- [ ] Memo answers §3.1–3.5 and §4.1–4.5
- [ ] The approximation verdict states a **condition**, not just a number
- [ ] The weights section reports a **distribution**, not a mean
- [ ] §5 addressed — you have one cost-weighted graph, and the memo says so
- [ ] Every rate carries its sample size in the same sentence
- [ ] `check_part3.py --track A` passes
- [ ] **Claims strand: C03, C04, C05 done this part** — the industrial
      deployment claims, where the grading matters most
      (`python 06-claims/check_claims.py --who <your-name> --min-done 9`)

## 9. If you finish early

Go deeper here:

- **Run `--full`.** It adds `facebook_combined`, the densest graph. Does the
  sampling answer hold on it? That is a real test of your §3.5 verdict, and if
  it does not hold you should say so loudly.
- Does the sample size you need scale with node count, or with something else?
  You have three graphs; say what you would need to answer it properly.
- Take the single worst `cost_ratio` route and look at it. Which airports, which
  path, why so bad? A named example is worth a paragraph of statistics.
- Your colleague found that Louvain gives a different answer every run. Sampled
  betweenness also has a seed. **How do their variabilities compare?** You both
  have 10+ runs per setting; this is a comparison neither of you can make alone,
  and it belongs in Part 4.
