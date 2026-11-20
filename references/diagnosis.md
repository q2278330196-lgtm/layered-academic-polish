# Diagnosis: two failure modes and their thresholds

Load this file at Step 2 and Step 5 of the workflow. All thresholds are calibrated
against two real manuscripts of similar length (6152 and 6866 words) and are
reproducible with `scripts/style_scan.py`.

## Why two dimensions, not one

A reviewer evaluates a draft on two independent axes:

- **Contribution visibility** — after reading title, abstract and conclusions, can
  the reviewer state in one sentence what was achieved?
- **Method transparency / trust** — are boundaries, failed results and untested
  assumptions stated plainly enough that the reviewer does not have to dig them out?

Both must be high. Averaging two contrasting voices produces a draft that is
mediocre on both axes. This is the single most common error when an LLM is asked
to "make the tone more balanced".

## Three diagnoses

### Type A — assertive / defensive

Reads like a pre-written response to reviewers. Typical reviewer attribution:
"the author is overselling; I should verify the claims myself", not "this was
written by AI".

Signals: dense boundary idioms (`strictly on inputs rather than outputs`,
`distinct from the bounds`), didactic closers (`must therefore always`,
`is therefore essential for transparent validation`), high sentence-initial
connective density, em dashes as connectors, AI-tone vocabulary, low negation,
and **no standalone limitations section**. The limitations are absent, not hidden
in a caveated sentence.

Reviewer consequence: invites method-level objections that were not previously
on the table, because each pre-emptive denial names the objection it defends
against.

Prescription: **subtract**. Delete boundary idioms, delete didactic closers,
convert reassurance adverbs to plain statements, and create Z5 from the author's
own acknowledged constraints.

### Type B — hedging cascade

Reads like a pre-written disclaimer. Typical reviewer attribution: "the author
was badly burned in a previous review" or "over-cautious first-time author".

Signals: 8%+ of sentences carry a negation, epistemic verbs concentrated in
negative constructions (`does not establish`, `cannot qualify`, `do not identify`),
disclaimers inside figure captions, and **no standalone limitations section**
despite abundant caveats scattered everywhere.

Reviewer consequence: the contribution dissolves, and because every small
objection has already been answered, the only objections left for the reviewer
to raise are fundamental ones (study design, single sample, external validity).
This can push a decision toward rejection even though the draft is trusted.

Prescription: **reposition**. Collect caveats into Z5, restore positive
statements in Z1/Z2/Z7, remove caption disclaimers, and replace epistemic
negations with concrete numbers or "was not tested".

### Type C — mixed

Both patterns coexist. Usually produced by asking a model to "add limitations
and sound more confident" in one pass. Subtract first, then reposition. Tell the
author explicitly how this arose; otherwise the next polishing round recreates it.

## Decision logic (as implemented in the scanner)

Z5 absence is common to both types and has no discriminating power. Report it
separately as a shared defect.

```
A_signals (of 5):
    boundary_idioms_per6k      > 6
    didactic_closers_per6k    >= 2
    initial_connectives_per6k  > 10
    em_dash_connectors_per6k   > 3
    ai_tone_words_per6k        > 4

B_signals (of 3):
    negation_pct               > 5.0
    epistemic_negations_per6k  > 8
    caption_disclaimers       >= 3

A>=4 and B>=2  ->  C
A>=4           ->  A
B>=3           ->  B
A>=2 or B>=2   ->  near target (minor residue)
else           ->  balanced / layered
```

Calibration check (run it after any edit to the scanner):

| Manuscript | Expected | Scanner result |
|---|---|---|
| assertive draft (IJR, compressor models) | A | A, 5/5 A signals, 0/3 B signals |
| hedged draft (JECST, LFP pack) | B | B, 2/5 A signals, 3/3 B signals |

If the scanner stops separating these two, fix the scanner before polishing
anything.

## Full threshold table

| Metric | Definition | A | B | Target |
|---|---|---|---|---|
| Negation sentences | sentences containing `does/do/did not`, `cannot`, `neither`, `without` | 4.2% | 8.4% | 2–3% |
| Boundary idioms / 6k | `rather than`, `distinct from`, `separately from`, `instead of`, `as opposed to` | 10.7 | 6.1 | ≤3 |
| Didactic closers / 6k | `must therefore`, `is therefore essential`, `should therefore`, `therefore clear`, `must always`, `must be reported`, `is therefore`, `should be governed` | 3.9 | 2.6 | ≤1, Z7 only |
| Epistemic negations / 6k | sentences containing an epistemic verb **and** a negation | 1.0 | 11.4 | ≤4 |
| Initial connectives / 6k | sentences starting with However/Moreover/Furthermore/Consequently/Crucially/Conversely/Accordingly/Nevertheless/Additionally/Similarly/Notably/Thus/Therefore/Overall/In contrast/While/Although | 19.5 | 0.9 | ≤6 |
| Em-dash connectors / 6k | U+2014 with an alphanumeric character on both sides | 12.7 | 0 | 0 |
| Caption disclaimers | negations or scope caveats in short Figure/Table caption blocks | 0 | 8 | 0 |
| AI-tone words / 6k | project banned-vocabulary list | 7.8 | 0 | ≤2 |
| Reassurance adverbs / 6k | `strictly`, `purely`, `only afterwards`, `explicitly`, `transparent`, `ensuring`, `unchanged`, `to ensure` | 5.9 | 2.6 | ≤3 |
| Protocol declarations / 6k | `frozen`, `predefined`, `prior to`, `prescribed` — report only, shared by both types | 3.9 | 15.7 | no target |
| Z5 | standalone Scope and limitations section, 8–10 lines | missing | missing | present |

Two counting conventions are in play and must not be mixed: the table above
counts **sentences** containing an epistemic verb plus a negation, whereas a
raw keyword count of `establish|identify|prove|demonstrate|qualify` gives roughly
2 (type A) and 17 (type B). Use the scanner column consistently.

## False positives and limits

- **Em dashes from `.docx`**: extracting `word/document.xml` collapses table
  structure, so `| — |` placeholders can appear between two alphanumerics and
  inflate the count. Prefer a clean text export for this metric, or verify by eye.
- **PDF-derived text**: page headers, line numbers and image URLs create spurious
  repeated 4-grams. Use `--strip-line-numbers` and treat repeated-phrase output
  as a hint, not a verdict. Scanner filters obvious URL/date/month noise and
  drops 4-grams repeated more than 15 times (running headers).
- **Caption detection** is heuristic: only short blocks beginning with
  `Figure/Table N.` are treated as captions. Verify the `--verbose` hits.
- **Contribution-count mismatch** is only detectable when abstract, introduction,
  cover letter and conclusions are in the same input. When they are separate
  files, check the counts manually across all of them.
- **`--zones` is a locator, not a measurement.** Heading detection uses keyword
  matching and misassigns short front-matter blocks; use it to find which zone
  needs attention, then re-scan that zone as a standalone clean text file before
  quoting its percentages.
- **`--baseline/--revised` expects two versions of the same manuscript.** Pointing
  it at two different papers produces a numerically valid but meaningless
  comparison.
- **Short zones distort percentages.** A 250-word abstract with two caveat
  sentences reads as 12% negation; judge Z1 by absolute sentence count and by
  the positive-first ordering rule instead.
- Thresholds are calibrated on ~6000-word English engineering manuscripts. For
  short reports (1500 words) or humanities papers, use the percentages but
  relax absolute per-6k counts.
- A fully green table is **not** proof of a good paper. An over-polished draft
  with near-zero negation is a third failure mode; if negation drops below 1%,
  restore caveats rather than accepting the score.
- Metrics say nothing about scientific correctness. Never present a style
  diagnosis as a reviewer verdict or an acceptance prediction.

## Scanner commands

```bash
python scripts/style_scan.py draft.txt                       # metric table + diagnosis
python scripts/style_scan.py draft.docx --verbose            # sentence-level hits
python scripts/style_scan.py draft.txt --zones               # per-zone breakdown
python scripts/style_scan.py draft.txt --json                # structured output
python scripts/style_scan.py --baseline before.txt --revised after.txt
python scripts/style_scan.py draft.txt --strip-line-numbers  # PDF-derived text
```

