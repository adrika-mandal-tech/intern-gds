# Part 3B — Do the communities actually hold together?

**Your track; your colleague has a different one.**
**Deliverable:** `your-work/<your-name>/part3/`

---

## 1. The claim you are testing

In Part 2B you established that Louvain gives a different grouping nearly every
run, while the *quality* score barely moves. Now a harder question about whether
those groupings are any good at all.

There is a well-known published claim about Louvain. The paper that introduced
the Leiden algorithm reported that Louvain produces communities that are

- **internally disconnected** — members reported as belonging to the same group
  with *no path between them inside that group* — at rates up to **16%**, and
- **badly connected** — barely holding together — at rates up to **25%**.

That claim is the entire reason the Leiden algorithm exists.

**Your job is not to confirm it. Your job is to measure it on real graphs and
report what you find.** If your rate is nothing like the published one, that is a
result, and a genuinely useful one — say so with the number and the sample size.

An internally disconnected community matters practically: it is a group that does
not exist. Anything downstream that describes "this community" will produce a
confident description of something with no coherent membership.

## 2. Run it

From the pack root:

```bash
python part-3/run_part3b.py --who <your-name>
```

**About 100 seconds.** Louvain and Leiden, 50 seeds each, on five graphs, with
every community checked. Plus the similarity experiment in §5.

Three files: `community_quality.csv`, `ground_truth_scores.csv`,
`similarity_vs_bridges.csv`.

## 3. Read the metric definitions before the numbers

`gdslab/stats.py::community_connectivity` counts three things. Read its
docstring — the definitions matter more than the numbers here.

| Category | Meaning |
|---|---|
| **disconnected** | The community falls into more than one piece. The serious one |
| **fragile** | Connected, but one edge holds together two substantial halves |
| **pendant** | Connected, but some member is a leaf hanging off the side |

**And read the note in that docstring about why there are three.** An earlier
version of this function counted any community with a leaf as "badly connected"
and produced rates of 84–100% on every graph and every algorithm. That is not a
finding — it is a definition that cannot discriminate. If a metric returns nearly
the same number on every input, it is not measuring the input.

Every fraction is over `n_assessed`, not `n_communities`: communities of one or
two nodes cannot fail any of these tests and are excluded from the denominator.
**Check that this matters** — compare `n_communities` and `n_assessed` on
`ca-GrQc` and say what the rate would have been if you had divided by the wrong
one.

## 4. What to work out

### 4.1 The headline

**What fraction of communities are internally disconnected?** Per graph, per
algorithm, with the sample size.

Then compare with the published claim of up to 16%. State the comparison
plainly, and be careful about what your number does and does not license you to
say — five graphs is five graphs.

### 4.2 Louvain versus Leiden

Leiden exists specifically to prevent disconnected communities. **Does it?**

- Compare the disconnected rate between the two algorithms.
- Then compare `fragile` and `pendant` between them. Is the difference in the
  same place?
- And compare modularity. **If Leiden fixes something, does it cost anything?**

Be careful here: you know from Part 2B that these algorithms vary between runs.
Any difference you report between Louvain and Leiden has to be bigger than that
run-to-run noise to mean anything. **Use your Part 2B spread to say whether it
is.** This is the main reason 2B came first.

### 4.3 Which graphs, and why

The fragile rate varies a lot between graphs. Put it beside Part 1's
`profiles.csv` (density, degree skew, components) and see whether anything
explains it.

Five graphs. Hypothesis, not conclusion. Say which.

### 4.4 Are they *right*, though?

`ground_truth_scores.csv` compares every run on `email-Eu-core` against the 42
real departments — the only graph in the pack where correctness is knowable
rather than just agreement.

- How well does either algorithm recover the real departments?
- **Does the run with the highest modularity also score best against the truth?**
  Check this properly. If the answer is no, it is the most important sentence in
  your memo: it would mean the score being optimised is not the thing you want.
- How many communities does each algorithm find, against the real 42?

### 4.5 Does similarity find the edges that matter?

Separate experiment, same file set. `similarity_vs_bridges.csv` scores every edge
two ways: **edge betweenness** (how much traffic crosses it) and **Jaccard
similarity** (how many neighbours its two endpoints share).

Look at the top 1% of edges by betweenness — the ones carrying the most traffic —
and at their similarity scores.

- What fraction score **exactly zero**?
- Work out *why* that happens. It is not a bug, and the eight-node example in
  [`the-six-families.md`](../00-base/01-context/the-six-families.md) §6 is the
  same phenomenon.
- Then the consequence: **if you used similarity to suggest "related items",
  which relationships would you systematically never suggest?** Say it concretely.
- Does the effect differ between `crime` and `email-Eu-core`? What about those
  graphs would explain it?

## 5. What to hand in

```
your-work/<your-name>/part3/
├── part3-memo.md
├── community_quality.csv
├── ground_truth_scores.csv
├── similarity_vs_bridges.csv
├── *.provenance.json
└── charts/
```

## 6. Check your work

```bash
python part-3/check_part3.py --who <your-name> --track B
```

## 7. Definition of done

- [ ] All three CSVs with provenance
- [ ] Memo answers §4.1–4.5
- [ ] The headline rate is stated with its sample size and compared to the
      published claim **without overclaiming in either direction**
- [ ] §4.2 uses your Part 2B spread to decide whether a difference is real
- [ ] §4.4 explicitly answers whether best-modularity means best-against-truth
- [ ] `check_part3.py --track B` passes
- [ ] **Claims strand: C03, C04, C05 done this part** — the industrial
      deployment claims, where the grading matters most
      (`python 06-claims/check_claims.py --who <your-name> --min-done 9`)

**One note on C01.** You have just measured, on real graphs, the thing C01
claims. Do not resolve C01 from your own result — go to the source and read what
it actually says, on what data. The comparison between the two belongs in your
claims memo at Part 4, and it is the most interesting entry in the strand.

## 8. If you finish early

Go deeper here:

- **Raise the seed count** to 200 on the two fastest graphs. Does the
  disconnected rate change? With rates this low, how many runs would you need
  before you could distinguish "rare" from "never"? That is a real question and
  worth a paragraph.
- Find an actual disconnected community — there are a few — and look at it. What
  are its members, and why did the algorithm put them together?
- The synthetic generators in `03-data/make_synthetic.py` produce graphs with
  **known** communities. Run both algorithms on `planted_partition` and `lfr` and
  score against the truth. Do they recover what was planted? Turn `p_out` up
  until they stop.
- Try `leidenalg.CPMVertexPartition` instead of `ModularityVertexPartition`.
  Different objective, different answers — but is it better by your measures?
