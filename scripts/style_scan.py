#!/usr/bin/env python3
"""Deterministic style-metric scanner for layered academic polishing.

Reads .txt/.md/.docx, measures the two failure modes described in SKILL.md,
assigns a diagnosis (A / B / C / balanced), and can compare a baseline with a
revised draft. Standard library only.

    python style_scan.py draft.txt
    python style_scan.py draft.docx --verbose --zones
    python style_scan.py --baseline before.txt --revised after.txt
    python style_scan.py draft.txt --json
"""

import argparse
import html
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

NORM = 6000  # normalize counts to a 6000-word research paper

NEG = re.compile(
    r"\b(?:does|do|did) not\b|\bcannot\b|\bcan not\b|\bneither\b|\bwithout\b", re.I)
NOT_ANY = re.compile(r"\bnot\b|\bcannot\b|\bneither\b|\bnor\b|\bwithout\b", re.I)
BOUNDARY = re.compile(
    r"\brather than\b|\bdistinct from\b|\bseparately from\b|\binstead of\b|\bas opposed to\b", re.I)
DIDACTIC = re.compile(
    r"\bmust therefore\b|\bis therefore essential\b|\bshould therefore\b|"
    r"\btherefore clear\b|\bmust always\b|\bmust be reported\b|\bis therefore\b|"
    r"\bshould be governed\b|\bis therefore clear\b", re.I)
EPISTEMIC = re.compile(
    r"\b(?:establish|establishes|identify|identifies|prove|proves|demonstrate|demonstrates|qualify|qualifies)\b", re.I)
CONNECTIVES = re.compile(
    r"^(?:However|Moreover|Furthermore|Consequently|Crucially|Conversely|"
    r"Accordingly|Nevertheless|Additionally|Similarly|Notably|Thus|Therefore|"
    r"Overall|In contrast|While|Although)\b", re.I)
AI_TONE = re.compile(
    r"\b(?:innovative|pioneering|revolutionary|transformative|superior|surpass|"
    r"remarkable|unprecedented|breakthrough|notably|yielding|encompass|reveal|"
    r"reveals|underscore|pave the way|stems from|rigid|impede|culminating in)\b", re.I)
REASSURANCE = re.compile(
    r"\b(?:strictly|purely|only afterwards|explicitly|transparent|ensuring|"
    r"unchanged|to ensure)\b", re.I)
PROTOCOL = re.compile(
    r"\b(?:frozen|predefined|prior to|prescribed)\b", re.I)
CAPTION_DISCLAIMER = re.compile(
    r"\bdoes not\b|\bcannot\b|\bnot\b|\bno\b|\bunavailable\b|\bneither\b|\bnor\b|"
    r"\bunsmoothed\b|\brather than\b", re.I)
NOISE_GRAM = re.compile(
    r"http|doi|image|figure|table|january|february|march|april|may|june|july|"
    r"august|september|october|november|december|copyright|zenodo", re.I)
CAPTION_START = re.compile(r"^(?:Figure|Table|Fig\.)\s*\d+[.:]", re.I)
Z5_HEAD = re.compile(r"^\s*(?:\d+(?:\.\d+)?\.?\s+)?(?:scope and limitations?|limitations?|study limitations?)\s*$", re.I | re.M)

HEADINGS = [
    (re.compile(r"^\s*(?:\d+\s+)?abstract\s*$", re.I | re.M), "Z1_abstract"),
    (re.compile(r"^\s*(?:\d+(?:\.\d+)?\.?\s+)?(?:introduction|background)\s*$", re.I | re.M), "Z4_intro"),
    (re.compile(r"^\s*(?:\d+(?:\.\d+)?\.?\s+)?(?:materials? and methods?|methods?|methodology|experimental (?:system|data|setup)[^\n]*)\s*$", re.I | re.M), "Z3_methods"),
    (re.compile(r"^\s*(?:\d+(?:\.\d+)?\.?\s+)?(?:results|results and discussion)\s*$", re.I | re.M), "Z2_results"),
    (re.compile(r"^\s*(?:\d+(?:\.\d+)?\.?\s+)?discussion\s*$", re.I | re.M), "Z4_discussion"),
    (re.compile(r"^\s*(?:\d+(?:\.\d+)?\.?\s+)?conclusions?\s*$", re.I | re.M), "Z7_conclusions"),
    (re.compile(r"^\s*(?:\d+(?:\.\d+)?\.?\s+)?(?:scope and limitations?|limitations?)\s*$", re.I | re.M), "Z5_limitations"),
    (re.compile(r"^\s*(?:\d+\s+)?(?:references|bibliography|nomenclature|declarations)\s*$", re.I | re.M), "BACK"),
]

ABBREV = ["et al.", "e.g.", "i.e.", "Eq.", "Eqs.", "Fig.", "Figs.", "Table", "vs.",
          "cf.", "approx.", "et al", "Dr.", "Prof.", "No.", "Ref.", "Sect."]


def load_text(path, strip_line_numbers=False):
    p = Path(path)
    if p.suffix.lower() == ".docx":
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
        xml = re.sub(r"</w:p>", "\n", xml)
        xml = re.sub(r"<w:tab[^>]*/>", "\t", xml)
        xml = re.sub(r"<w:instrText[^>]*>.*?</w:instrText>", "", xml, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", "", xml))
        text = re.sub(r"\n{3,}", "\n\n", text)
    else:
        text = p.read_text(encoding="utf-8", errors="replace")
        text = html.unescape(text)
    if strip_line_numbers:
        text = "\n".join(re.sub(r"^\s*\d{1,4}\s+", "", ln) for ln in text.split("\n"))
    return text


def sentences(text):
    protected = text
    for i, a in enumerate(ABBREV):
        protected = protected.replace(a, a.replace(".", "\x00"))
    parts = re.split(r"(?<=[.!?])\s+", protected.replace("\n", " "))
    return [s.replace("\x00", ".").strip() for s in parts if s.strip()]


def norm_count(n, words):
    return round(n * NORM / max(words, 1), 2)


def scan(text):
    sents = sentences(text)
    words = len(re.findall(r"\b[\w'-]+\b", text))
    flat = " ".join(sents)

    neg_sents = [s for s in sents if NEG.search(s)]
    did_sents = [s for s in sents if DIDACTIC.search(s)]
    epi_sents = [s for s in sents if EPISTEMIC.search(s)]
    epi_neg_sents = [s for s in sents if EPISTEMIC.search(s) and NOT_ANY.search(s)]
    conn_sents = [s for s in sents if CONNECTIVES.search(s)]

    # em dashes used as sentence connectors (letter/digit on both sides)
    emdash = len(re.findall(r"\w\s*\u2014\s*\w", flat))

    # captions: split at each "Figure/Table N." start; a genuine caption block is
    # short, so long prose blocks that merely cite a figure are excluded.
    cap_hits = []
    blocks = re.split(r"(?=(?:Figure|Table|Fig\.)\s*\d+[.:])", text, flags=re.I)
    for blk in blocks[1:]:
        if not CAPTION_START.match(blk.strip()[:40]):
            continue
        if len(blk.strip()) > 1200:      # long block = running prose, not a caption
            continue
        for s in sentences(blk[:900]):
            if CAPTION_DISCLAIMER.search(s):
                cap_hits.append(s)
    # de-duplicate identical caption sentences
    cap_hits = list(dict.fromkeys(cap_hits))

    # Z5 section
    z5_match = Z5_HEAD.search(text)
    z5_lines = 0
    if z5_match:
        tail = text[z5_match.end():]
        stop = re.search(r"^\s*(?:\d+\s+)?(?:conclusions?|references|acknowledg)", tail, re.I | re.M)
        body = tail[:stop.start()] if stop else tail
        z5_lines = len([ln for ln in body.split("\n") if len(ln.strip()) > 40])

    # repeated abstract noun phrases (>=3 occurrences of a 4-gram)
    stopw = set("the a an of and or in for to with on at by from is are was were be this that these those we our their its as it which such using used between under across both each all can may not than then also into per".split())
    toks = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z-]{2,}", flat)]
    grams = Counter(" ".join(toks[i:i + 4]) for i in range(len(toks) - 3)
                    if all(t not in stopw for t in toks[i:i + 4])
                    and not NOISE_GRAM.search(" ".join(toks[i:i + 4])))
    repeated = [(g, n) for g, n in grams.most_common(25) if 3 <= n <= 15][:5]

    # contribution count consistency
    counts = re.findall(r"\b(one|two|three|four|five|six)\s+(?:main\s+)?(?:contributions?|insights?|findings?|takeaways?)\b", flat, re.I)
    numbered_concl = len(re.findall(r"^\s*\d+\.\s+[A-Z]", text, re.M))

    m = {
        "words": words,
        "sentences": len(sents),
        "negation_sentences": len(neg_sents),
        "negation_pct": round(100 * len(neg_sents) / max(len(sents), 1), 2),
        "boundary_idioms": len(BOUNDARY.findall(flat)),
        "didactic_closers": len(did_sents),
        "epistemic_negations": len(epi_neg_sents),
        "initial_connectives": len(conn_sents),
        "em_dash_connectors": emdash,
        "caption_disclaimers": len(cap_hits),
        "ai_tone_words": len(AI_TONE.findall(flat)),
        "reassurance_adverbs": len(REASSURANCE.findall(flat)),
        "protocol_declarations": len(PROTOCOL.findall(flat)),
        "z5_present": bool(z5_match),
        "z5_lines": z5_lines,
        "repeated_4grams": repeated,
        "contribution_counts": counts,
        "numbered_conclusion_items": numbered_concl,
    }
    for k in ["boundary_idioms", "didactic_closers", "epistemic_negations",
              "initial_connectives", "em_dash_connectors", "caption_disclaimers",
              "ai_tone_words", "reassurance_adverbs", "protocol_declarations"]:
        m[k + "_per6k"] = norm_count(m[k], words)

    # Z5 absence is common to both failure modes and carries no discriminating
    # power, so it is reported separately instead of being used as a signal.
    a = sum([m["boundary_idioms_per6k"] > 6,
             m["didactic_closers_per6k"] >= 2.0,
             m["initial_connectives_per6k"] > 10,
             m["em_dash_connectors_per6k"] > 3,
             m["ai_tone_words_per6k"] > 4])
    b = sum([m["negation_pct"] > 5.0,
             m["epistemic_negations_per6k"] > 8,
             m["caption_disclaimers"] >= 3])
    if a >= 4 and b >= 2:
        diag = "C / mixed (assertive + hedged)"
    elif a >= 4:
        diag = "A / assertive-defensive"
    elif b >= 3:
        diag = "B / hedging cascade"
    elif a >= 2 or b >= 2:
        diag = "near target (minor residue)"
    else:
        diag = "balanced / layered"
    m["diagnosis"] = diag
    m["a_signals"] = a
    m["a_max"] = 5
    m["b_signals"] = b
    m["b_max"] = 3
    m["hits"] = {
        "negation": neg_sents, "didactic": did_sents, "epistemic_negation": epi_neg_sents,
        "connectives": conn_sents, "caption_disclaimers": cap_hits,
    }
    return m


def zone_table(text):
    marks = []
    for rx, name in HEADINGS:
        for hit in rx.finditer(text):
            marks.append((hit.start(), hit.end(), name))
    marks.sort()
    out = []
    for i, (_, start, name) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        if name == "BACK":
            continue
        chunk = text[start:end]
        m = scan(chunk)
        out.append((name, m["words"], m["negation_pct"], m["didactic_closers"],
                    m["epistemic_negations"], m["boundary_idioms"]))
    return out


def table(m):
    rows = [
        ("Words / sentences", f'{m["words"]} / {m["sentences"]}', "-", "-"),
        ("Negation-bearing sentences", f'{m["negation_pct"]}%', "2-3%", "8.2% (B) / 1% (A)"),
        ("Boundary idioms / 6k", m["boundary_idioms_per6k"], "<=3", "11 (A) / 6 (B)"),
        ("Didactic closers / 6k", m["didactic_closers_per6k"], "<=1 (Z7 only)", "4 (A)"),
        ("Epistemic negations / 6k", m["epistemic_negations_per6k"], "<=4", "17 (B)"),
        ("Initial connectives / 6k", m["initial_connectives_per6k"], "<=6", "20 (A) / 0 (B)"),
        ("Em-dash connectors / 6k", m["em_dash_connectors_per6k"], "0", "9 (A) / 0 (B)"),
        ("Caption disclaimers", m["caption_disclaimers"], "0", "0 (A) / 5 (B)"),
        ("AI-tone words / 6k", m["ai_tone_words_per6k"], "<=2", "project rule"),
        ("Reassurance adverbs / 6k", m["reassurance_adverbs_per6k"], "<=3", "A signature"),
        ("Protocol declarations / 6k", m["protocol_declarations_per6k"], "report only", "shared by both types"),
        ("Z5 limitations section", "yes" if m["z5_present"] else "MISSING", "yes, 8-10 lines", "shared defect"),
        ("Z5 content lines", m["z5_lines"], "8-10", "-"),
    ]
    lines = ["| Metric | Measured | Target | Calibration |",
             "|---|---|---|---|"]
    for r in rows:
        lines.append("| " + " | ".join(str(x) for x in r) + " |")
    lines.append("")
    lines.append(f'**Diagnosis:** {m["diagnosis"]}  '
                 f'(A signals {m["a_signals"]}/{m["a_max"]}, B signals {m["b_signals"]}/{m["b_max"]})')
    if not m["z5_present"]:
        lines.append("**Shared defect:** no standalone Scope and limitations section; create Z5.")
    if m["repeated_4grams"]:
        lines.append("**Repeated abstract phrases (>=3x):** " + "; ".join(
            f'"{g}" x{n}' for g, n in m["repeated_4grams"]))
    if len(set(x.lower() for x in m["contribution_counts"])) > 1:
        lines.append(f'**Contribution-count mismatch:** {m["contribution_counts"]}; '
                     f'numbered conclusion items = {m["numbered_conclusion_items"]}')
    return "\n".join(lines)


def compare(before, after):
    keys = ["negation_pct", "boundary_idioms_per6k", "didactic_closers_per6k",
            "epistemic_negations_per6k", "initial_connectives_per6k",
            "em_dash_connectors_per6k", "caption_disclaimers", "ai_tone_words_per6k",
            "reassurance_adverbs_per6k"]
    labels = {"negation_pct": "2-3%", "boundary_idioms_per6k": "<=3",
              "didactic_closers_per6k": "<=1", "epistemic_negations_per6k": "<=4",
              "initial_connectives_per6k": "<=6", "em_dash_connectors_per6k": "0",
              "caption_disclaimers": "0", "ai_tone_words_per6k": "<=2",
              "reassurance_adverbs_per6k": "<=3"}
    lines = ["| Metric | Before | After | Target |", "|---|---|---|---|"]
    for k in keys:
        lines.append(f"| {k} | {before[k]} | {after[k]} | {labels[k]} |")
    lines.append(f'| Z5 present | {before["z5_present"]} | {after["z5_present"]} | yes |')
    lines.append(f'| Z5 lines | {before["z5_lines"]} | {after["z5_lines"]} | 8-10 |')
    lines.append("")
    lines.append(f'**Diagnosis:** {before["diagnosis"]}  →  {after["diagnosis"]}')
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="manuscript .txt/.md/.docx")
    ap.add_argument("--baseline", help="baseline text for comparison mode")
    ap.add_argument("--revised", help="revised text for comparison mode")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--verbose", action="store_true", help="list matched sentences")
    ap.add_argument("--zones", action="store_true", help="per-zone breakdown")
    ap.add_argument("--strip-line-numbers", action="store_true",
                    help="strip leading numeric line numbers (PDF-derived text)")
    args = ap.parse_args()

    if args.baseline or args.revised:
        if not (args.baseline and args.revised):
            ap.error("--baseline and --revised must be given together")
        b = scan(load_text(args.baseline, args.strip_line_numbers))
        a = scan(load_text(args.revised, args.strip_line_numbers))
        print(compare(b, a))
        return

    if not args.input:
        ap.error("provide an input file, or --baseline and --revised")

    text = load_text(args.input, args.strip_line_numbers)
    m = scan(text)

    if args.json:
        out = {k: v for k, v in m.items() if k != "hits"}
        if args.verbose:
            out["hits"] = m["hits"]
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print(f"# Style scan: {Path(args.input).name}\n")
    print(table(m))

    if args.zones:
        print("\n## Per-zone breakdown\n")
        print("| Zone | Words | Neg % | Didactic | Epistemic neg | Boundary |")
        print("|---|---|---|---|---|---|")
        for row in zone_table(text):
            print("| " + " | ".join(str(x) for x in row) + " |")

    if args.verbose:
        print("\n## Sentence-level hits\n")
        for name, hits in m["hits"].items():
            if not hits:
                continue
            print(f"### {name} ({len(hits)})\n")
            for s in hits[:40]:
                print(f"- {s[:230]}")
            if len(hits) > 40:
                print(f"- ... {len(hits) - 40} more")
            print()


if __name__ == "__main__":
    main()

