---
name: layered-academic-polish
description: "Polishes academic manuscripts by assigning tone per functional zone instead of averaging one balanced voice, then verifies the result with a deterministic style-metric scanner. Diagnoses and fixes two opposite failure modes: assertive/defensive writing (hedge-free claims, strictly/purely boundary drawing, didactic must-therefore closers, hidden limitations) and hedging cascades (every result followed by does-not-establish, disclaimers in figure captions, contributions dissolved by self-negation). Use when the user asks to polish, de-hype or de-AI a paper, reduce defensive tone, reorganize limitations, or make AI-assisted writing sound natural; also when a draft reads too salesy or too apologetic. Chinese triggers: 论文润色、去 AI 味、降防御性、改写局限性、语气太满、太保守、审稿人视角润色. Not a substitute for scientific review; does not add data or change claims."
agent_created: true
license: CC-BY-4.0
---

# Layered Academic Polish

## Overview

AI-assisted polishing fails in a predictable way: it produces one uniform voice
across the entire manuscript. Two opposite uniform voices are equally damaging.
An assertive draft hides its limitations behind `strictly`, `must therefore` and
pre-emptive boundary drawing, which makes reviewers start hunting for problems.
An over-hedged draft appends `does not establish` to every result, which dissolves
the contribution and pushes reviewers toward fundamental objections.

This skill replaces "find a middle tone" with **tone layering by zone**: keep the
confidence of the abstract and conclusions, keep the honesty of the methods and
limitations, and never mix the two inside one sentence. Every claim is measurable,
so a bundled scanner verifies the result instead of relying on impression.

## Core principle

Two independent dimensions, not one scale:

- **Contribution visibility** — can a reader state what was achieved after reading
  the title, abstract and conclusions?
- **Method transparency / trust** — are the boundaries, failures and untested
  assumptions stated plainly enough that a reviewer does not have to dig them out?

The target is **high on both**. Averaging the two voices lands in the middle of
the plot, which is low on both. Fix each manuscript by adding the dimension it
lacks, never by moderating its existing strength.

| Zone | Tone | Allowed | Forbidden |
|---|---|---|---|
| Z1 Title / Abstract / Cover letter | Confident, concrete | 3 positive sentences + 1 boundary sentence | Ending on a negation; `delivers N insights` |
| Z2 Results | Plain statement | Numbers, facts, unchanged negative findings | Trailing `but this does not prove X` |
| Z3 Methods | Exact, procedural | What was done, parameters, exclusions | `strictly` / `purely` / `only` as reassurance; "we did not do Y" |
| Z4 Discussion | Explanatory | Interpretation, comparison with literature | Didactic `is therefore essential` |
| Z5 Scope and limitations | Plain, exhaustive, compact | 8–10 lines, flat enumeration | `however` / `nevertheless` / `it should be noted` |
| Z6 Figure / table captions | Descriptive only | What is shown, what it shows | Any disclaimer, uncertainty note or scope caveat |
| Z7 Conclusions | Positive first | 2–3 takeaways, then 1 condition sentence | Pure negation as the closing line |

Zone rules, including sentence templates, live in `references/zone-rules.md`.

## When to use

- Polishing, de-hyping or "de-AI-ing" an English academic manuscript or cover letter.
- A draft that reads too assertive, too apologetic, or mechanically uniform.
- Reorganizing scattered limitations into one section.
- Auditing whether AI-assisted editing left detectable stylistic residue.
- Preparing a resubmission after reviewers commented on tone, overclaiming or
  missing limitations.

## When NOT to use

- Finding scientific errors, missing baselines, statistical flaws → `pre-submission-reviewer`,
  `manuscript-structure-auditor`, `citation-integrity-auditor`.
- Choosing a journal or writing a cover letter from scratch → `journal-submission-advisor`.
- Grammar-only or generic language cleanup → `paper-polish`, `humanizer`.
- Generating new content, data, citations or figures. This skill rewrites wording
  and placement only; it never changes numbers, claims, references or conclusions.

## Workflow

### Step 1 — Ingest and zone

Read the manuscript into plain text. `.docx` is handled directly by
`scripts/style_scan.py`; PDFs must first be converted to text with the PDF reading
skill. Identify Z1–Z7 by heading keywords. When the paper has no Limitations
section, mark Z5 as **missing** rather than treating scattered caveats as Z5.

### Step 2 — Baseline scan

Run the scanner before changing anything:

```bash
python scripts/style_scan.py <manuscript.txt> --verbose
```

Capture the metric table and the diagnosis (type A, B, C or balanced). Read
`references/diagnosis.md` for thresholds and decision logic. Do not skip this
step: the diagnosis determines whether the prescription is subtraction or
repositioning, and the two are opposites.

### Step 3 — Diagnose

- **Type A (assertive / defensive)**: high boundary-drawing and didactic closers,
  low negation, Z5 missing. Prescription: **subtract** — delete boundary idioms,
  delete didactic closers, add Z5.
- **Type B (hedging cascade)**: high negation density, epistemic negations,
  disclaimers in Z6, no Z5 despite abundant caveats. Prescription: **reposition** —
  collect caveats into Z5, restore positive statements in Z1/Z2/Z7, delete
  caption disclaimers.
- **Type C (mixed)**: both patterns. Prescription: subtract first, then reposition.
  Warn the author that this is the most common outcome of asking an LLM to
  "make the tone more balanced".

Never apply a single averaged rewrite to the whole document. Work zone by zone.

### Step 4 — Rewrite zone by zone

Load `references/rewrite-patterns.md` and apply its operations. For each edit,
produce `original → rewrite → one-line reason`. Preserve every number, symbol,
unit, citation key and technical term verbatim. Preserve explicitly reported
failures and negative results: they are the least AI-like content in the paper.

Do not batch-delete negations with a language model. A blanket "remove hedges"
instruction produces a uniformly positive draft, which is a third failure mode.
Target a reduction from the measured baseline to the 2–3% negation band (roughly
10–15 caveat sentences in a 6000-word draft, depending on sentence length), so
reviewers still have medium-granularity points to raise.

### Step 5 — Re-scan and verify

Run the scanner again on the revised text. Confirm every metric moved into its
target band and that Z5 exists with 8–10 lines. Re-check Z6 contains zero
disclaimers. If a metric overshot (for example negation density fell below 1%),
restore a caveat rather than accepting a falsely clean score.

### Step 6 — Deliver

Output, in order:

1. Diagnosis (type, one paragraph, with baseline numbers).
2. Before/after metric table.
3. Zone-by-zone change list, each with original → rewrite → reason.
4. **Unchanged declaration**: numbers, claims, references, data and negative
   results were not modified.
5. Residual risks that are scientific rather than stylistic, explicitly labelled
   as out of scope for this skill.

Offer a tracked-changes DOCX only when the author asks; default to a reviewable
change list so the author accepts edits individually.

## Metric quick reference

Full thresholds and their derivation are in `references/diagnosis.md`. Normalize
all counts per 6000 words.

All counts normalized per 6000 words. Calibration values are scanner output on
two real ~6000-word manuscripts, not estimates.

| Metric | Type A (assertive) | Type B (hedged) | Target |
|---|---|---|---|
| Negation-bearing sentences | 4.2% | 8.4% | 2–3% |
| Boundary idioms / 6k | 10.7 | 6.1 | ≤3 |
| Didactic closers / 6k | 3.9 | 2.6 | ≤1, in Z7 only |
| Epistemic negations / 6k | 1.0 | 11.4 | ≤4 |
| Sentence-initial connectives / 6k | 19.5 | 0.9 | ≤6 |
| Em-dash connectors / 6k | 12.7 | 0 | 0 |
| Caption disclaimers | 0 | 8 | 0 |
| AI-tone words / 6k | 7.8 | 0 | ≤2 |
| Reassurance adverbs / 6k | 5.9 | 2.6 | ≤3 |
| Z5 present, 8–10 lines | no | no | yes |

## Hard constraints

- Never invent or alter data, results, equations, units, citations or claims.
- Never remove a stated limitation without relocating it into Z5.
- Never add a limitation the author did not supply.
- Never delete the generative-AI disclosure; advise keeping it.
- Never promise acceptance, minor revision or a reviewer's verdict.
- Never modify the reference list or the numbering of figures and tables.
- Report unverified journal requirements as unverified; check the live guide for
  abstract word limits, mandatory Highlights and Limitations policies.
- State honestly that tone alone cannot be used to attribute AI authorship.

## Resources

- `scripts/style_scan.py` — deterministic metric scanner. Accepts `.txt`, `.md`,
  `.docx`; `--json` for structured output, `--verbose` for sentence-level hits,
  `--zones` for per-zone breakdown, `--baseline/--revised` for a comparison table.
- `references/diagnosis.md` — type A/B/C decision logic, full threshold table,
  calibration baselines and false-positive notes.
- `references/zone-rules.md` — per-zone permitted and forbidden constructions,
  sentence templates, and the abstract/conclusion ordering rule.
- `references/rewrite-patterns.md` — operation catalogue with real before/after
  pairs taken from two contrasting manuscripts.

