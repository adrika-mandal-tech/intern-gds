# Part 4 — Projection, replication, and what you actually learned

**Both of you, together again.**
**Deliverable:** `your-work/<your-name>/part4/`

---

Three things this part, and the first one is the capstone.

---

## Part A — Projection changes the answer

### A1. The idea

Every experiment so far ran on a graph somebody had already decided the shape of.
This one is about that decision.

Some graphs have **two kinds of node**, with every edge crossing between them:

- people ↔ crimes they were involved in (`crime`)
- territories ↔ languages spoken there (`unicodelang`)

You cannot sensibly ask "which person is most central among people" on such a
graph, because **no two people are connected at all**. Every path between two
people goes through a crime.

So you *derive* a graph: connect two people when they were involved in the same
crime. Those person-to-person edges exist in no data file. You invented them —
correctly, usefully, but you invented them, and the algorithm now sees a world
you constructed.

**The question: how much does that choice change the answer?**

### A2. Run it

```bash
python part-4/run_part4.py --who <your-name>
```

**About 30 seconds.** It runs PageRank and community detection three ways on each
of the two graphs: on the raw two-sided graph, on the side-0 projection, and on
the side-1 projection.

Four files: `projection_shape.csv`, `projection_mass.csv`,
`projection_rankings.csv`, `projection_effect.csv`.

### A3. What to work out

**1. Does score pile up on one side?** `projection_mass.csv` gives each side's
share of the nodes and its share of the total PageRank. A `mass_ratio` of 1.0
means the side gets exactly the score its size warrants.

- Which side accumulates score, on each graph?
- **Why?** It is not random, and the answer is about how the two sides differ
  structurally.
- If you ran PageRank on the raw graph and reported "the top ten most important
  things", what would actually be in that list?

**2. What does projection do to the size?** `projection_shape.csv`.

- The blow-up ratio differs a lot between the two graphs, and between the two
  sides of the same graph. `away_side_max_degree` and
  `biggest_single_contribution` are your explanation — work out the relationship.
- **Predict, before you look:** if the away side had one node connected to 1,000
  things, how many edges would that one node contribute?
- What does this tell you about when projecting a graph is safe and when it is
  not? Give the rule.

**3. Does the ranking survive?** `projection_effect.csv` compares each entity's
rank in the raw graph against its rank in the projection: top-10 overlap, top-20
overlap, and Spearman across everything.

You will find at least one case where the Spearman is **essentially zero**.

- Find it. State it plainly, with the number.
- Then be precise about what it means: same underlying data, same algorithm, one
  decision changed — and the two answers are **not related to each other**. Not
  "somewhat different". Unrelated.
- Which of the two answers is correct?

That last question is the point of the whole part, and it is a trap. Think
carefully before answering.

**4. Do the communities survive?** `ari_raw_vs_projected` in the same file.
Does the grouping change as much as the ranking does? You know from Part 2B how
much Louvain varies with itself — **is this change bigger than that noise?**

**5. The rule.** Close with something usable:

> When you are handed a two-sided graph and asked "which of these things matters
> most", what do you do, and what do you have to tell whoever asked?

---

## Part B — Replicate your colleague's headline claim

### B1. What to do

Pick your colleague's **single most important finding** from Part 2 or Part 3 —
agree between you which one, and pick the one that would matter most if it were
wrong.

Then reproduce it. **From their brief, not from their code and not from their
numbers.** Read what the experiment was supposed to establish, run it yourself,
and see what you get.

Their runner scripts are in the pack and you may use them. What you must not do
is start from their results file, or from a conversation about what they got.

### B2. Write `replication.md`

Five sections, and the checker looks for these exact headings:

```markdown
## The claim I tested
## What I ran
## What I got
## Verdict
## What we shared
```

**Verdict** should be one of: *replicated* / *partly replicated* / *did not
replicate* / *could not attempt*, with the numbers side by side.

**What we shared** is the honest one. You sit together and you have been talking
throughout. Did you know their number before you ran it? Did you use their
script? Did you discuss what to expect?

None of those are wrong. **But a replication by someone who already knew the
answer is a weaker piece of evidence than one by someone who did not**, and a
reader needs to know which they are holding. Say it plainly.

---

## Part C — The joint synthesis

### C1. One document, written together

`synthesis.md`, one copy each in your folders (identical is fine — say so).

Three sections, and the checker looks for these headings:

```markdown
## Every claim
## Replication status
## What we would do differently
```

**Every claim** — a table of every substantive finding either of you made across
all four parts:

| # | Claim | Whose | Graphs | Runs | Confidence |
|---|---|---|---|---|---|

Every row needs its sample size. This is the exercise: go back through your own
memos and find the sentences that stated a result without one. There will be
some. Fix them here.

**Replication status** — for each claim: `replicated` / `not replicated` /
`not attempted`. Most will be *not attempted*, and that is the honest answer.
Resist the urge to mark something replicated because it sounds right.

**What we would do differently** — with hindsight: what would you
measure differently, what did you spend too long on, what turned out not to
matter, and what should the next person do first?

That last section is genuinely useful to us. Be blunt.

---

## What to hand in

```
your-work/<your-name>/part4/
├── part4-memo.md            Part A
├── replication.md           Part B
├── synthesis.md             Part C
├── projection_shape.csv
├── projection_mass.csv
├── projection_rankings.csv
├── projection_effect.csv
├── *.provenance.json
└── charts/
```

## Check your work

```bash
python part-4/check_part4.py --who <your-name>
```

## Definition of done

- [ ] All four CSVs with provenance
- [ ] `part4-memo.md` answers A3.1–A3.5, including "which answer is correct"
- [ ] `replication.md` has all five headings and an explicit verdict
- [ ] `synthesis.md` has all three headings, and **every claim in the table has a
      sample size**
- [ ] Research log covers all four parts
- [ ] `questions.md` handed in — including the questions you answered yourself
- [ ] `check_part4.py` passes
- [ ] **Claims strand finished** — C07, C08, C11 plus `claims-memo.md`
      (`python 06-claims/check_claims.py --who <your-name> --min-done 12`)

## If you finish early

- Run the projection experiment on a graph you build yourself. Take
  `email-Eu-core` and make it two-sided somehow — people ↔ something — then
  project it back and see whether you recover the original.
- `bipartite.weighted_projected_graph` keeps a weight on each derived edge (how
  many shared neighbours). Does using it change any of your A3 answers?
- The most interesting open question in this pack: **the derived edges are not
  all equally meaningful.** Two people at the same 18-person crime are weaker
  evidence than two people at the same 2-person crime. Propose a way to weight
  them, try it, and see whether the ranking gets more sensible. There is no
  correct answer here; a well-argued attempt is worth a lot.
