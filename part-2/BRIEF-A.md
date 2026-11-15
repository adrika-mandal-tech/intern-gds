# Part 2A — Do the four centrality measures agree?

**This is your track; your colleague has a different one.**
**Deliverable:** `your-work/<your-name>/part2/`

---

## 1. The question

"Which node is the most important?" has at least four answers:

| Measure | What it actually asks | Cost |
|---|---|---|
| **degree** | who has the most connections? | free |
| **PageRank** | who is endorsed by others who are endorsed? | cheap |
| **closeness** | who is nearest to everyone on average? | expensive |
| **betweenness** | who sits on the most routes between others? | very expensive |

The practical question behind them:

> **When can you use a cheap measure instead of an expensive one, and when would
> that be a serious mistake?**

That matters because on the graphs here, betweenness costs **thousands of times**
more than degree. If they mostly agree, you should nearly always use degree. If
they disagree in a way that matters, you cannot.

Your job is to find out which, and to be precise about *where* the answer changes.

## 2. Run it

From the pack root:

```bash
python part-2/run_part2a.py --who <your-name>
```

**One to two minutes**, nearly all of it exact betweenness and closeness on
`openflights`. It runs five graphs: `lesmis`, `unicodelang`, `crime`,
`email-Eu-core`, `openflights`.

(On the reference machine this took 50 s once and 123 s another time, with
nothing changed but what else the laptop was doing. That spread is worth
remembering when you come to compare timings with your colleague — it is a
floor on how precisely any wall-clock comparison can mean anything.)

You should see output shaped like this — the first graph only, so you can confirm
it is working. The rest is yours to discover:

```
  lesmis  (N=77, E=254)
     cost: degree 0.000s  pagerank 0.001s  closeness 0.003s  betweenness 0.011s
     agreement (Spearman / top-10 overlap):
       degree       vs pagerank      rho=+0.966  top10=0.54
       ...
     biggest degree-vs-betweenness disagreement: node 60 (degree rank 24, betweenness rank 69)
```

Four files land in `part2/`: `centrality_scores.csv` (every node's four scores),
`centrality_agreement.csv`, `centrality_cost.csv`, `disagreements.csv`.

## 3. What to work out

### 3.1 Which pairs agree, and which do not

`centrality_agreement.csv` has Spearman correlation and top-10 overlap for all
six pairs on all five graphs.

- Which pair agrees most across the graphs? Which least?
- **Does the answer change from graph to graph?** If a pair agrees strongly on
  one graph and weakly on another, that is more interesting than any average, and
  the memo should lead with it rather than bury it in a mean.

### 3.2 The trap in this data — do not miss it

Look at `unicodelang`, `degree` vs `betweenness`. You will find a Spearman
correlation of about **+0.98** — which sounds like near-perfect agreement — and a
top-10 overlap of about **0.43**.

Both numbers are correct. Work out how they can both be true.

Then answer the question that follows, because it is the practical one:

> If you are going to act on the **top ten** most important nodes, which of those
> two numbers should you have looked at? What would you have concluded from the
> correlation alone?

This generalises well beyond graphs and it is the most valuable thing in this
part. Give it room in the memo.

### 3.3 Name the nodes where they disagree

`disagreements.csv` lists, per graph, the five nodes with the largest gap between
their degree rank and their betweenness rank.

- Pick the most extreme one and **look at it**. What is it about that node's
  position that makes the two measures disagree so violently? Use
  `loaders.names("lesmis")` for readable names on that graph.
- The gaps run in both directions — some nodes are ranked far higher by
  betweenness, some far lower. Explain both.

A correlation is a summary. **A named node with an explanation is a finding.**
The memo needs at least one.

### 3.4 What it costs

`centrality_cost.csv` has the timings.

- How does the cost of each measure grow across the five graphs? Against nodes,
  or against edges?
- Betweenness on `openflights` takes about 31 seconds at 3,214 nodes. Using your
  own measurements, estimate what it would take at 30,000 nodes, and **say what
  assumption your estimate rests on.** Then say how much you trust it — you are
  extrapolating from five points.

### 3.5 The recommendation

Close with a direct answer:

> **When is degree an acceptable substitute for betweenness, and when is it not?**

Conditions, not vibes. "When the graph has property X" or "when you only need
Y" — something a person could actually apply.

## 4. A caution about closeness

Three of these graphs are disconnected (`unicodelang` 5 components, `crime` 20,
`ca-GrQc` 354). Closeness is defined as nearness to everyone else — and some
nodes cannot reach some others at all.

networkx handles this by working within each node's own component. **That is a
choice, and it has a consequence**: a node in a tiny isolated component can score
very well, because everyone it can reach is close by.

Check whether that happened in your data. If it did, it belongs in the memo, and
it is exactly the sort of thing that makes a number look healthy while measuring
something other than what you meant.

## 5. What to hand in

```
your-work/<your-name>/part2/
├── part2-memo.md              from 04-templates/memo-template.md
├── centrality_scores.csv
├── centrality_agreement.csv
├── centrality_cost.csv
├── disagreements.csv
├── *.provenance.json
└── charts/
```

## 6. Check your work

```bash
python part-2/check_part2.py --who <your-name> --track A
```

## 7. Definition of done

- [ ] All four CSVs present with provenance sidecars
- [ ] Memo covers §3.1 to §3.5, every section of the template
- [ ] **§3.2 answered explicitly** — this is the one we most want to read
- [ ] At least one named node, with an explanation of why the measures disagree
- [ ] Every rate or correlation has its sample size in the same sentence
- [ ] `check_part2.py --track A` passes
- [ ] **Claims strand: C02, C06, C12 done this part**
      (`python 06-claims/check_claims.py --who <your-name> --min-done 6`)

## 8. If you finish early

Go deeper here. Options:

- Add a fifth measure — eigenvector centrality, or harmonic centrality — and see
  where it lands relative to the four.
- `run_part2a.py` deliberately drops edge weights (`weighted=False`). Re-run
  weighted on `openflights` and see whether the rankings change. Note that
  `lesmis` weights are a *strength* and `openflights` weights are a *cost*, so
  think before you do it to both.
- Your colleague is measuring how much Louvain varies between runs. Everything
  you have computed is deterministic. **Is it?** Run `run_part2a.py` twice and
  diff the CSVs. Predict the answer before you look.
