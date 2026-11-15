# The claim-verification strand

**Runs across all four parts.** Roughly three claims alongside each part. Do not
try to do it all at the end.

**Deliverable:** `your-work/<your-name>/claims.jsonl` plus
`your-work/<your-name>/claims-memo.md` at Part 4.

---

## 1. Why this exists

Everything you have read about graph algorithms — including the context documents
in this pack — rests on a base of published numbers. Those numbers get quoted,
requoted, and summarised until the version everyone knows is some distance from
the version anyone measured.

This is not hypothetical. One of the claims in your list circulates as **four
different numbers** for the same result, and at most some of them can be right.
Another is routinely described as an "accuracy" improvement when the source
measures something else entirely.

Your job is to go back to the primary source for twelve widely-cited claims and
report what is actually there.

**This is a completely different skill from the rest of the pack** — no code, no
graphs, just careful reading — and it is deliberately spread across the four
parts so you switch between the two.

## 2. The four grades

For each claim, after finding the primary source, grade the *evidence*:

| Grade | Means |
|---|---|
| `production` | Serving real users. Described by the operator, with a deployment period or a scale figure |
| `research` | Published and reproducible, but no deployment claimed |
| `product` | Shipped and buyable, but no efficacy evidence published |
| `marketing` | Appears only in vendor prose, or misstates its source |

Grade the **evidence**, not the claim. A carefully-measured research result is
`research` even if you find it convincing, and a real product with no published
numbers is `product` even if it is excellent.

## 3. The method

For each claim in `06-claims/claims.jsonl`:

**1. Find the primary source.** The paper, the engineering blog post, the
documentation page — the place the number was first stated by the people who
measured it. A summary of a summary is not a primary source, and neither is a
vendor page citing a paper.

**2. Find the number in it.** Actually locate the sentence. Copy it out.

**3. Check it says what it is said to say.** This is the real work. Things to
watch for, all of which occur in your list:

- Two different statistics **spliced together** into one sentence
- A *relative* improvement reported as an *absolute* one
- An improvement in one measure described as an improvement in another
- A range reported as its most impressive endpoint
- An internal experiment reported as a deployment
- A result on one dataset described as a general finding

**4. Fill in your row.**

| Field | What goes in it |
|---|---|
| `verdict` | `confirmed` / `misstated` / `unverifiable` / `partly-confirmed` |
| `primary_source` | A URL or full citation |
| `quote` | The actual sentence from the source. **At least 25 characters** |
| `grade` | One of the four above |
| `notes` | What you found, especially any difference between claim and source |

## 4. `unverifiable` is a real verdict

If you cannot reach the source — paywalled, dead link, the trail runs into
secondary sources that all cite each other — then the verdict is `unverifiable`
and you leave `quote` empty.

**That is a genuinely useful result, not a failure.** "This number is repeated
everywhere and I could not find anyone who measured it" is worth knowing, and it
is worth more than a guess. Write in `notes` exactly what you tried, so the next
person does not repeat it.

What is *not* acceptable is marking something `confirmed` because it sounds
right, or because three blog posts agree with each other.

## 5. Pacing

| | Do these |
|---|---|
| End of Part 1 | C01, C09, C10 — the algorithm claims. C01 is the one you will measure yourself in Part 3B |
| End of Part 2 | C02, C06, C12 — the retrieval claims |
| End of Part 3 | C03, C04, C05 — the industrial deployments. These are where grading matters most |
| End of Part 4 | C07, C08, C11, and the memo |

Split them between you however you like, **but do C01 separately and compare** —
it is the one you both have independent measurements for, and it is interesting
to see whether you read the source the same way.

## 6. The memo, at Part 4

`claims-memo.md`. Short. Cover:

- **The tally.** How many confirmed, misstated, unverifiable? By grade?
- **The worst one.** Which claim was furthest from its source, and how?
- **The pattern.** Is there a kind of claim that tends to drift? Deployment
  claims? Percentage improvements? Round numbers?
- **C01 specifically.** You measured this yourself in Part 3B. **Does your
  measurement agree with the source?** If not, is that because the source is
  wrong, or because you measured something different on different graphs? Be
  careful and fair here — this is the most interesting entry in the whole strand
  and the temptation to overclaim runs in both directions.
- **What you would want checked next**, and why.

## 7. Check your work

```bash
python 06-claims/check_claims.py --who <your-name>
```

Validates that every row is well-formed, every verdict is one of the four
allowed, and every row that is not `unverifiable` carries a source and a real
quote.

## 8. Two cautions

**Do not grade a claim by whether you believe it.** The grades are about what
evidence exists, and a claim can be true with weak evidence or false with strong
evidence.

**Do not assume the pack is right.** Several of these claims appear in this
pack's own context documents. If you find that one of them is misstated *here*,
that is the best possible outcome of this exercise and it goes straight into
`questions.md`.
