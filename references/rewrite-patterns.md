# Rewrite pattern catalogue

Load at Step 4. Every pair below is taken from one of the two calibrated
manuscripts. Apply zone by zone; never run a whole-document rewrite.

## Operating rules

For each edit emit `original → rewrite → reason`. Preserve verbatim: every
number, unit, symbol, equation label, citation key, dataset identifier, figure
and table number, and technical term. Preserve explicitly reported failures and
negative results. Do not add a claim, a limitation or a citation the author did
not supply.

Work from the scanner's `--verbose` hit list so each change is traceable to a
measured signal.

---

## P1 — Boundary idiom to plain statement (Type A)

Pattern: `rather than`, `distinct from`, `separately from`, `instead of`,
`as opposed to`. The sentence pre-answers an objection while stating a fact.

> **Original**: "Engineering tolerances of 1, 2, 3, and 4 K are used to benchmark
> practical acceptability, distinct from the sensor uncertainty bounds analysed
> in Section 4.3."
>
> **Rewrite**: "Four engineering tolerances (1, 2, 3 and 4 K) benchmark
> acceptability. Sensor uncertainty is treated in Section 4.3."

Same information, no defensive framing.

> **Original**: "Both filters rely strictly on operating inputs rather than
> outlet temperature or model residuals, ensuring reproducible,
> output-independent screening."
>
> **Rewrite**: "Both filters use the measured input channels listed in Table S1;
> outlet temperature and model residuals are not inputs."

State the channel set and stop. Do not keep `strictly`, `ensuring` or
`output-independent`.

> **Original**: "The 12 s separation between measured and predicted peaks
> reflects physical inertia rather than a model phase parameter: because the
> algebraic correlation has no dynamic states, its peak tracks the inputs
> instantaneously."
>
> **Rewrite**: "The measured peak lags the predicted peak by 12 s. The algebraic
> correlation has no dynamic states, so its peak follows the inputs immediately,
> whereas the measured discharge peak is delayed by piping/casing capacitance
> and sensor lag."

The `rather than a model phase parameter` clause names an accusation nobody
made. Remove it; keep the mechanism.

Target: ≤3 boundary idioms per 6000 words.

## P2 — Didactic closer removal (Type A)

Pattern: `must therefore`, `is therefore essential`, `should therefore`,
`therefore clear`, `must always`, `must be reported`.

> "Averaged error metrics must therefore always be interpreted alongside their
> supporting valid duration." → delete, or move a single short version to Z7.
>
> "Reporting input stability, retained error, and excluded high-error intervals
> together is therefore essential for transparent model validation." → delete.
>
> "The practical takeaway for HTHP engineers is therefore clear: ..." → "For
> slow-varying monitoring, ..."

Keep at most one normative sentence in the entire paper, in Z7. The facts
already imply the recommendation.

## P3 — Epistemic negation to numbers (Type B)

Pattern: `does not establish / identify / prove / demonstrate / qualify` after a
result. The clause adds no information the numbers do not already carry.

> **Original**: "A near-correct maximum value therefore does not establish
> correct location-specific prediction (Figure 6; Table S6)."
>
> **Rewrite**: "M3's global-peak bias is −0.62/+0.03 K, while its error at the
> observed hottest location is 1.78/0.45 K."

> **Original**: "These are predictive gains from additional effective freedom;
> they do not identify cell-specific physical defects."
>
> **Rewrite**: "The gain arises from the additional effective rate freedom
> (Section S5)."

Replace "what this is not" with "what this is", or simply delete.

> **Original**: "This quantifies the persistent component of the range error
> without assigning its physical cause."
>
> **Rewrite**: delete. The preceding sentence ("squared mean bias accounts for
> 51.3–84.0% of range MSE") already says it.

## P4 — Epistemic negation to "was not tested" (Type B)

When the caveat protects a real inference, keep it but make it operational.

> **Original**: "Absence of rejection does not demonstrate that a homogeneous
> model reproduces the trimmed trajectory."
>
> **Rewrite**: "Trimming removes the 004 rejection; whether a homogeneous model
> then reproduces the trimmed trajectory was not tested."

> **Original**: "The fixed physical sites do not provide an exchangeability
> model for a permutation significance test."
>
> **Rewrite**: "The 100 assignments are reported as a descriptive reference set;
> no significance test is claimed."

Shorter, more honest, and it removes the epistemic verb.

## P5 — Abstract-phrase loop breaking (Type A/B)

The scanner reports repeated 4-grams. A three-item abstract noun group repeated
in abstract, introduction, discussion and conclusions is a theme-sentence loop.

Example of the loop: `target time scale / operating envelope / required coverage`
appearing four times, `valid coverage duration` five times.

Action: keep the triad once, in Z7. In Z1 and Z2 replace it with the concrete
numbers it stands for (`1.01 K RMSE over 6847 s`, `26.4 K peak`, `2550 s of
300 s coverage`). In Z4 delete the restatement.

## P6 — Caption disclaimer migration (Type B)

Delete from Z6, or move the substantive content once to Z3.

| Caption sentence | Action |
|---|---|
| "The schematic does not specify undocumented sensor attachment coordinates." | Move to Z5 as one flat line |
| "Across-assignment variation describes alternative spatial assignments rather than an experimental confidence interval." | Move to Z3, once |
| "No uncertainty bars are assigned." | Delete |
| "Every score and peak calculation uses unsmoothed data." | Move the fact to Z3, once |
| "Fold trajectories are not combined into a predicted field." | Move to Z3, once |

After migration the caption contains only panels, axes, units, sample counts
and one finding sentence.

## P7 — Positive-first ordering (Type B)

> **Original (abstract conclusion)**: "Limited spatial freedom improved
> integrated prediction at calibrated positions, but omitted-position and
> extreme-temperature capability remained output dependent."
>
> **Rewrite**: "Column-and-row rates reduce frozen driving RMSE by about 16% at
> calibrated positions and outperform most matched-freedom assignments. These
> gains do not extend to excluded positions or synchronous range, so
> qualification requires output-specific checks."

Same honesty, different order. Apply the same rule to Z7's closing line: end on
a condition, not a denial.

## P8 — Collecting Z5 (both types)

Assemble from scattered caveats, not from new content. From the hedged draft,
the raw caveats were: one-pack sampling, retrospective development,
measured-boundary conditioning, inferred clock conversion, unavailable
experiment-specific sensor accuracy, no contact-temperature measurements, no
independent repeated packs. Written as 8–10 flat lines they form Z5; left in
place they produce the 8.4% negation rate.

From the assertive draft, Z5 must be built from constraints the author already
stated elsewhere: single 599-sample calibration window, no dynamic model fitted,
arbitrary 4 K tolerance, sensor time constant not measured, guideline derived
and evaluated on the same days.

## P9 — Connective and em-dash cleanup (Type A)

- Replace sentence-initial `Consequently / Furthermore / Crucially / Conversely /
  Accordingly` with a noun phrase that names the link, or delete it.
- Replace em dashes used as sentence connectors with a comma, semicolon or full
  stop. Do not touch the em dash in a cited article title, or `| — |` table
  placeholders.
- Target: ≤6 initial connectives and zero em-dash connectors per 6000 words.

## P10 — Contribution-count consistency (both types)

Count the contribution items in the abstract / cover letter, the introduction
("three main contributions") and the conclusions (numbered items). Make them
identical. Replace `This study delivers four concrete insights for X researchers
and practitioners` with two or three plain sentences in the cover letter.

The scanner only detects mismatches when all sections are in one input; check
separate files manually.

---

## Anti-patterns (do not do these)

- **Batch-deleting all negations with an LLM.** Produces a uniformly positive
  draft — a third failure mode. Target the 2–3% band, not zero.
- **Replacing every negation with `may / appears to / could`.** Converts a
  disclaimer cascade into a hedge cascade; the metric improves while the prose
  gets worse.
- **Asking for a "more balanced tone" in one prompt.** This is how Type C is
  manufactured.
- **Turning a technical uncertainty into a marketing adjective.** Never replace
  `unavailable sensor accuracy` with `well-characterized measurements`.
- **Rewriting the whole document in one pass.** Zone by zone, with a re-scan
  after each zone for long papers.
- **Deleting negative results.** "Both M3 peak identities remain incorrect" and
  "reproduces only 52.9%/43.2% of mean absolute range" are the least AI-like
  sentences in a manuscript. Keep them verbatim.

## Verification checklist before delivery

- Re-scan: all metrics inside target bands, no metric below the floor.
- Z5 exists, 8–10 lines, contains every removed caveat.
- Z6 contains zero disclaimers.
- Every removed limitation is either in Z5 or still in the body.
- Numbers, units, citations, figure/table numbers unchanged.
- Contribution counts consistent across all files.
- AI disclosure retained.
- Output includes the unchanged declaration and an explicit note that
  scientific risks are out of scope.

