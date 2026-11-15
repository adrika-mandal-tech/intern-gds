# Part 1 — Measure the graph before you measure the algorithm

**Both of you do this, on your own machines.**
**Deliverable:** `your-work/<your-name>/part1/`

---

## 1. The question

Everyone's instinct about algorithm cost is *"bigger graph, slower"*. Node count
is the number people quote, budget from, and put in documentation.

**Find out whether it is true.**

You have seven graphs ranging from 77 to 5,241 nodes. Measure what actually
predicts how long PageRank takes and how many rounds it needs, and report what
you find — whether or not it agrees with the instinct.

There is a second question underneath it, and it is the reason there are two of
you: **which of your numbers survive being carried to a different machine?**

## 2. Before you start

- [ ] Orientation reading done (`START_HERE.md` §3)
- [ ] `python 02-setup/check_setup.py` passes
- [ ] `first-impressions.md` written — **before you understand any of this**
- [ ] `research-log.md` and `questions.md` started from the templates

## 3. Run it

From the **pack root** (the folder containing `00-base/` and `part-1/`):

```bash
python part-1/run_part1.py --who <your-name>
```

Under a minute. Compare what you see against
[EXPECTED_OUTPUT.md](EXPECTED_OUTPUT.md) — it tells you which columns should
match ours exactly and which should not.

Then look at what it wrote: `profiles.csv` (7 rows) and `pagerank_runs.csv`
(70 rows — seven graphs, ten runs each). Open them. Everything below is analysis
of those two files.

## 4. Experiment 1.1 — What shape is each graph?

`profiles.csv` describes all seven. Your job is to read it and say what it means.

Questions to answer in your memo:

- **Which graphs are "about the same size" but not the same problem?** Find at
  least one pair and say precisely what differs.
- **`ca-GrQc` is in 354 separate components.** What does that break? Name a
  specific measurement that becomes ill-defined, and say what you would do.
- **Two graphs have clustering of exactly 0.000.** Not nearly zero — exactly.
  Work out why. Then answer the harder question: **could that number ever have
  come out differently on those graphs?** If not, what was it measuring?

That last one is the point of the whole experiment. Write down your reasoning
before you look anything up.

## 5. Experiment 1.2 — What predicts the cost?

`pagerank_runs.csv` has, for every graph and every run: node count, edge count,
degree skew, load time, compute time, and **rounds to converge**.

Four charts are drawn for you in `charts/`. Use them, but do the analysis from
the CSV — a chart shows you a shape, a number goes in the memo.

**Answer these, each with the numbers behind it:**

1. **Does node count predict compute time?** Give the counter-example if there is
   one, by name and by number.
2. **Does edge count do better?** Is it good enough to budget from?
3. **Rounds to converge** — this is the interesting column. Does it track size at
   all? Look carefully at `lesmis` (77 nodes) against `email-Eu-core` (986). Then
   at `unicodelang` (868) against `email-Eu-core` (986) — nearly identical size.
4. **Does degree skew predict rounds better than node count does?** Say how you
   decided, not just what you concluded. "It looks like it" is not an answer;
   a rank correlation is.
5. **Load time vs compute time** — for which graphs is loading the larger cost?
   Would you have noticed if the script reported one combined number?

**A caution on (4).** You have seven data points. Seven. Be careful about how
strong a claim that supports — and say so in the memo. A correlation over seven
points is a hint, not a law, and noticing that is worth more to us than a
confident number would be.

## 6. Experiment 1.3 — What survives a change of machine?

**This is the one you cannot do alone.**

Once you have both run it:

1. Put your two `pagerank_runs.csv` files side by side. Also open both
   `pagerank_runs.provenance.json` — that is what records whose machine is whose.
2. Compare three things:
   - **absolute compute times** — how different?
   - **ratios between graphs** on each machine (e.g. `facebook_combined` ÷
     `ca-GrQc`) — do those agree, even though the absolute times do not?
   - **rounds to converge** — should be identical. Are they?
3. Write `part1/calibration.md`. It must name whose machines you compared, and
   discuss **ratios** and **iteration counts** explicitly.

Then answer the question this was really about:

> Someone reports "this took 86 seconds". Someone else reports "this took twice
> as long as the other graph". **Six months from now, which of those two
> statements is still useful, and why?**

If your rounds do *not* match, stop and tell us. That would mean something in the
pack is not deterministic when it should be, and it matters more than the rest of
this part.

## 7. What to hand in

```
your-work/<your-name>/
├── first-impressions.md
├── research-log.md
├── questions.md
└── part1/
    ├── part1-memo.md          from 04-templates/memo-template.md
    ├── calibration.md         §6
    ├── profiles.csv
    ├── pagerank_runs.csv
    ├── *.provenance.json      keep these
    └── charts/
```

## 8. Check your work

```bash
python part-1/check_part1.py --who <your-name>
```

It verifies your files are present, complete and well-formed. **It cannot check
whether your findings are right** — read what it prints when it passes.

Run it before you say you are done, and before you open Part 2.

## 9. Definition of done

- [ ] `profiles.csv` — 7 rows
- [ ] `pagerank_runs.csv` — 70 rows, 10 distinct runs per graph
- [ ] `calibration.md` — names your colleague's machine, discusses ratios and
      iteration counts
- [ ] `part1-memo.md` — every section of the template, every rate with a sample
      size in the same sentence
- [ ] `first-impressions.md` — written before you understood any of this
- [ ] Research log covers this part
- [ ] `check_part1.py` passes
- [ ] **Claims C01, C09, C10 done** — see below

## 10. The claims strand starts now

Alongside every part there is a second, smaller task: checking twelve
widely-cited claims about graph algorithms against their original sources. No
code — just careful reading. Read
[`00-base/06-claims/BRIEF.md`](../00-base/06-claims/BRIEF.md).

**For Part 1, do C01, C09 and C10.** C01 is the one you will measure yourself
later, so it is worth meeting it early.

Copy `06-claims/claims.jsonl` into `your-work/<your-name>/` and fill it in there.
Check it with:

```bash
python 06-claims/check_claims.py --who <your-name> --min-done 3
```

**Do this as you go, not all at the end.** Saved up, it becomes twelve claims in
one sitting, which is how you end up marking things `confirmed` because they
sound right.

## 11. If you finish early

**Go deeper here rather than starting something new.** Good directions:

- Vary the tolerance (`algos.pagerank_iters(G, tol=...)`) and see how rounds
  respond. Does the ranking of graphs by rounds stay stable?
- Generate graphs of increasing size with the same shape
  (`03-data/make_synthetic.py`) and check whether *within one shape* size does
  predict cost. That is a genuinely different question from the one above and
  the answer may not be the same.
- Run 1.2 again and see how much your own timings move between two sittings on
  the same machine. If that spread is large, what does it do to your confidence
  in the between-machine comparison?

The overflow bench in `00-base/05-bench/` exists for when something **stalls**,
not for when something finishes.

---

**One more thing.** If any number in this brief or in `EXPECTED_OUTPUT.md` does
not reproduce on your machine, that is a finding and we want it in
`questions.md`. Several of the numbers in this pack were wrong the first time
they were written down, and were only caught by being re-run.
