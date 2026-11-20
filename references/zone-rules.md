# Zone rules

One zone, one tone. Never mix a confident claim and its own disclaimer inside a
single sentence; put them in different zones instead. Apply these rules in Step 4.

## Z1 — Title, abstract, cover letter

Purpose: make the contribution visible in under 30 seconds. This is the only zone
where an editor decides whether to send the paper out for review.

Permitted:
- Three positive sentences: what was done, what improved, the quantified result.
- One boundary sentence stating the applicable scope.
- Concrete numbers instead of evaluative adjectives.

Forbidden:
- Ending on a negation or a limitation (`... remained output dependent.`).
- `This study delivers N concrete insights`, `culminating in`, `pioneering`,
  `underscores the potential of`.
- Listing more contribution items than the introduction and conclusions list.

Template:

```
[What was measured / built and on what data].
[Primary quantitative result, with numbers and conditions].
[Second result or the discriminating test].
[Single boundary sentence: where the result does / does not apply].
```

Cover letter: 250–350 words, plain prose, no numbered insight list. Name the
handling editor when the journal requires routing, include the date, and attach
reviewer suggestions when the submission checklist requires them. Do not remove
the generative-AI disclosure.

## Z2 — Results

Purpose: report what happened. Numbers are the argument.

Permitted:
- Plain declarative statements with units and conditions.
- Negative and unsuccessful results, stated without apology.
- References to tables, figures and supplementary sections.

Forbidden:
- A trailing `but this does not prove / establish / identify X` on every
  paragraph.
- Interpretive or methodological justification inside a results paragraph.
- `notably`, `remarkably`, `crucially`.

Rule: **one paragraph, at most one caveat sentence**, and only when the caveat
changes how the number should be read (for example a missing window or a
conditional metric). Everything else moves to Z5.

## Z3 — Methods

Purpose: reproducibility.

Permitted:
- What was done, parameters, bounds, exclusion rules, seeds, versions.
- Data-availability and code-availability statements.
- Dataset corrections and version identifiers, stated once.

Forbidden:
- Reassurance adverbs used to pre-empt an accusation: `strictly on inputs
  rather than outputs`, `purely from target speed`, `ensuring reproducible,
  output-independent screening`. State the input channels and stop.
- `we did not use Y` when Y was never a plausible option.
- Repeating `frozen`, `unchanged`, `predefined`, `prior to` as a credibility
  ritual. One statement of the protocol is enough.

Convert "what was not done" into "what was done": list the actual channels,
thresholds and order of operations. A reviewer who wants to know whether outputs
were used can read the channel list.

## Z4 — Discussion

Purpose: interpretation and positioning.

Permitted:
- Mechanistic interpretation clearly marked as interpretation.
- Comparison with prior work, including where the present result differs.
- Explanation of why an output-specific result changed.

Forbidden:
- Didactic closers: `Reporting X together is therefore essential for transparent
  validation`, `Metrics must therefore always be interpreted alongside Y`.
- Claiming a physical cause when only an association was measured; say what the
  data constrain instead.

Move all "should / must therefore" sentences to Z7, and keep at most one there.

## Z5 — Scope and limitations

Purpose: concentrate honesty so it does not dilute the rest of the paper.

Required structure:
- A standalone headed section (`4.x Scope and limitations` or `Limitations`),
  8–10 lines, placed after Discussion and before Conclusions.
- Flat enumeration, one limitation per sentence, no rhetorical cushioning.
- Only limitations the author actually supplied. Never invent a limitation.

Permitted content:
- Single unit / single dataset / single calibration window.
- Retrospective development or data available during model development.
- Unmeasured quantities, unavailable sensor characterization, inferred units
  or clock conversions lacking acquisition-level confirmation.
- Thresholds chosen without external validation.
- Untested alternatives (a dynamic model that was recommended but not fitted).

Forbidden:
- `however`, `nevertheless`, `it should be noted`, `while we acknowledge`.
- Restating the contribution inside this section.
- Apologetic framing; a flat list reads as more competent than a humble one.

Template:

```
### Scope and limitations
This evaluation uses [unit / dataset / calibration window]. [Development was
retrospective: ...]. [Quantity X was prescribed rather than measured]. [The
time base was inferred from ... without acquisition-level confirmation].
[Thresholds of ... were chosen as engineering references and were not derived
from process requirements]. [No dynamic / coupled model was fitted, so ...].
[Replication on additional units with characterized sensors would test ...].
```

Every caveat removed from Z2, Z3, Z4 or Z6 must land here. Never silently delete
a stated limitation.

## Z6 — Figure and table captions

Purpose: say what is in the figure and what it shows.

Permitted:
- Panel descriptions, axes, units, symbols, scales, sample counts.
- One sentence stating the finding the figure supports.

Forbidden — all of these are disclaimers, not captions:
- `The schematic does not specify undocumented sensor attachment coordinates.`
- `No uncertainty bars are assigned.`
- `Every score and peak calculation uses unsmoothed data.`
- `Across-assignment variation describes alternative spatial assignments rather
  than an experimental confidence interval.`
- `Fold trajectories are not combined into a predicted field.`

Move the substantive ones to Z3 (once) or Z5; delete the rest. A caption that
needs a disclaimer usually means the method section is incomplete.

## Z7 — Conclusions

Purpose: leave the reader with takeaways.

Permitted:
- Two to three positive, quantified conclusions.
- One final condition sentence defining the applicable envelope.

Forbidden:
- A pure negation as the closing line (`These gains do not qualify every
  spatial output.`).
- A numbered list whose item count disagrees with the contribution count in Z1
  and the introduction.
- Introducing new limitations here; they belong in Z5.

Order rule (also applies to the abstract): **positive first, condition last**.
The same facts in the opposite order read as an apology.

## Cross-zone migration map

| Found in | Move to | Action |
|---|---|---|
| Z1 trailing negation | Z1 end as one boundary sentence | Rewrite as a condition, not a denial |
| Z2 trailing `does not establish` | Z5 | Keep the number, drop the epistemology |
| Z3 `strictly / purely / rather than` | delete | Replace with the actual channel list |
| Z4 `must therefore / is essential` | Z7, one instance | Or delete |
| Z6 any disclaimer | Z3 / Z5 / delete | Captions stay descriptive |
| Z7 closing negation | Z5 | Replace closing line with a condition |

## Journal compliance (verify, do not assume)

Before rewriting Z1, check the live Guide for Authors for: abstract word cap,
mandatory Highlights and their bullet/character limits, required keywords,
maximum word count, reference style, reviewer-suggestion requirements, and
whether a Limitations section is permitted or required. Report anything that
could not be verified as unverified. Elsevier's "Your Paper Your Way" relaxes
layout at first submission but does not waive separately uploaded items such as
Highlights.

Do not promise that fixing tone changes a decision. Do not attribute AI
authorship from tone alone.

