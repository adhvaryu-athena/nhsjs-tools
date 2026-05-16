"""
nhsjs_audit.py
==============
Self-audit checks for an NHSJS revision build.

Implements the 10 checks from Revise-After-Review v2 Phase 6. Use this
to surface issues before declaring a revision ready to send — and to
catch the kinds of regressions external chat reviewers tend to miss.

Public API
----------
    audit_revision(revision_md_path, submit_dir, *, log_path=None)
        -> list[CheckResult]

    CheckResult(name, status, detail)  — dataclass, status one of
        "PASS", "FAIL", "WARN".

CLI
---
    python -m nhsjs_audit revision.md submit/
    python -m nhsjs_audit revision.md submit/ --log revision-log.md
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.oxml.ns import qn


# ─── Data classes ──────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    status: str  # PASS / FAIL / WARN
    detail: str


# ─── Constants ─────────────────────────────────────────────────────────────

_CITE_RE = re.compile(r"\[\[CITE:([^\]]+)\]\]")
_INSERT_RE = re.compile(r"\{\{\+(.+?)\+\}\}", re.DOTALL)
_DELETE_RE = re.compile(r"\{\{-(.+?)-\}\}", re.DOTALL)
_RESTRUCTURE_RE = re.compile(
    r"\{\{RESTRUCTURE:\s*OLD:\s*(.*?)\s*NEW:\s*(.*?)\s*\}\}",
    re.DOTALL,
)

# Names / phrases that should never appear in an anonymous Standard manuscript.
_IDENTIFYING_PHRASES = [
    r"\bAthena Education\b",
    r"\bmy mentor\b",
    r"\bmy counsell?or\b",
    r"\bmy tutor\b",
    r"\bmy advisor\b",
    r"\bthanks to my\b",
    r"\bhelped me by\b",  # weak but catches "X helped me by..."
]
_IDENTIFYING_REGEX = re.compile("|".join(_IDENTIFYING_PHRASES), re.IGNORECASE)

_AUTHOR_BLOCKLIST = {
    "", "anonymous", "claude", "anthropic", "athena", "athena education",
    "user", "guest",
}


# ─── audit_revision (public entry point) ───────────────────────────────────

def audit_revision(revision_md_path: str | Path,
                   submit_dir: str | Path,
                   *,
                   log_path: str | Path | None = None) -> list[CheckResult]:
    """Run all 10 Phase 6 checks. Returns one CheckResult per check."""
    revision_md_path = Path(revision_md_path)
    submit_dir = Path(submit_dir)
    log_path = Path(log_path) if log_path else None

    if not revision_md_path.exists():
        return [CheckResult("revision.md exists", "FAIL",
                            f"missing file: {revision_md_path}")]

    raw = revision_md_path.read_text(encoding="utf-8")
    body = _strip_frontmatter(raw)
    student_name = _frontmatter_value(raw, "student_name") or ""

    # Locate the submit files
    tracked, clean, online, letter = _locate_outputs(submit_dir)

    results: list[CheckResult] = []
    results.append(_check_citation_count(body))
    results.append(_check_orphan_refs(body))
    results.append(_check_sequential_numbering(body))
    results.append(_check_ooxml_superscript(tracked))
    results.append(_check_standard_online_parity(body, online))
    results.append(_check_duplication_artefacts(body))
    results.append(_check_vanishing_paragraphs(body))
    results.append(_check_author_attribution(tracked, clean, student_name))
    results.append(_check_anonymous_standard(clean))
    results.append(_check_letter_vs_manuscript(letter, clean, log_path))
    return results


# ─── Helpers — frontmatter + body + file location ─────────────────────────

def _strip_frontmatter(raw: str) -> str:
    m = re.match(r"^---\s*\n.*?\n---\s*\n(.*)", raw, re.DOTALL)
    return m.group(1) if m else raw


def _frontmatter_value(raw: str, key: str) -> str | None:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
    if not m:
        return None
    for line in m.group(1).splitlines():
        km = re.match(rf"^{key}\s*:\s*(.+?)\s*$", line)
        if km:
            return km.group(1).strip().strip('"').strip("'")
    return None


def _locate_outputs(submit_dir: Path) -> tuple[Path | None, Path | None, Path | None, Path | None]:
    """Best-effort locate the 4 docx outputs in submit_dir."""
    tracked = clean = online = letter = None
    if not submit_dir.exists():
        return (None, None, None, None)
    for p in submit_dir.glob("*.docx"):
        n = p.name.lower()
        if "standard-tracked" in n:
            tracked = p
        elif "standard-clean" in n:
            clean = p
        elif "online" in n:
            online = p
        elif "response-letter" in n or "response_letter" in n:
            letter = p
    return (tracked, clean, online, letter)


def _all_cite_numbers(body: str) -> list[int]:
    """Every citation number in body order (duplicates allowed)."""
    out: list[int] = []
    for m in _CITE_RE.finditer(body):
        for piece in m.group(1).split(","):
            piece = piece.strip()
            if piece.isdigit():
                out.append(int(piece))
    return out


def _reference_numbers(body: str) -> list[int]:
    """Numbers found in the References section of body."""
    # Find the References heading line
    m = re.search(r"(?im)^#{1,6}\s+References\s*$", body)
    if not m:
        return []
    refs_section = body[m.end():]
    numbers = []
    for line in refs_section.splitlines():
        rm = re.match(r"^\s*(\d+)[.)]\s+\S", line)
        if rm:
            numbers.append(int(rm.group(1)))
    return numbers


# ─── 1. Citation count consistency ─────────────────────────────────────────

def _check_citation_count(body: str) -> CheckResult:
    cited = set(_all_cite_numbers(body))
    refs = set(_reference_numbers(body))
    if cited == refs:
        return CheckResult(
            "Citation count", "PASS",
            f"{len(refs)} unique references, {len(cited)} cited — match.",
        )
    return CheckResult(
        "Citation count", "FAIL",
        f"{len(refs)} reference entries vs {len(cited)} unique cited numbers. "
        f"Only-in-refs: {sorted(refs - cited)} ; only-cited: {sorted(cited - refs)}",
    )


# ─── 2. Orphan refs ────────────────────────────────────────────────────────

def _check_orphan_refs(body: str) -> CheckResult:
    cited = set(_all_cite_numbers(body))
    refs = set(_reference_numbers(body))
    orphan_refs = sorted(refs - cited)
    orphan_cites = sorted(cited - refs)
    issues = []
    if orphan_refs:
        issues.append(f"reference entries never cited: {orphan_refs}")
    if orphan_cites:
        issues.append(f"citations with no reference entry: {orphan_cites}")
    if issues:
        return CheckResult("Orphan refs", "FAIL", "; ".join(issues))
    return CheckResult(
        "Orphan refs", "PASS",
        f"All {len(cited)} cited numbers resolve to a reference entry; no orphans.",
    )


# ─── 3. Sequential numbering ───────────────────────────────────────────────

def _check_sequential_numbering(body: str) -> CheckResult:
    seen: list[int] = []
    for n in _all_cite_numbers(body):
        if n not in seen:
            seen.append(n)
    expected = list(range(1, len(seen) + 1))
    if seen == expected:
        return CheckResult(
            "Sequential numbering", "PASS",
            f"Citations appear in order 1..{len(seen)} with no gaps or skips.",
        )
    # First mismatch
    mismatch = None
    for i, (got, want) in enumerate(zip(seen, expected)):
        if got != want:
            mismatch = (i + 1, got, want)
            break
    detail = (
        f"First-appearance order is {seen}, expected {expected}. "
        f"First mismatch at position {mismatch[0]}: got {mismatch[1]}, "
        f"expected {mismatch[2]}." if mismatch else f"Mismatch: seen {seen} vs expected {expected}."
    )
    return CheckResult("Sequential numbering", "FAIL", detail)


# ─── 4. OOXML superscript sanity ───────────────────────────────────────────

def _check_ooxml_superscript(tracked: Path | None) -> CheckResult:
    if tracked is None or not tracked.exists():
        return CheckResult("OOXML superscript", "WARN",
                           "Standard-Tracked.docx not found in submit dir.")
    doc = Document(str(tracked))
    superscript_runs = 0
    for p in doc.paragraphs:
        for r in p._p.findall(qn("w:r")):
            rPr = r.find(qn("w:rPr"))
            if rPr is None:
                continue
            va = rPr.find(qn("w:vertAlign"))
            if va is not None and va.get(qn("w:val")) == "superscript":
                superscript_runs += 1
    if superscript_runs == 0:
        return CheckResult(
            "OOXML superscript", "FAIL",
            "Standard-Tracked.docx has zero <w:vertAlign w:val=\"superscript\"> "
            "runs. Citations will not survive Standard→Online conversion.",
        )
    return CheckResult(
        "OOXML superscript", "PASS",
        f"Found {superscript_runs} real OOXML superscript run(s) — "
        f"Standard→Online compatibility intact.",
    )


# ─── 5. Standard↔Online citation slot parity ───────────────────────────────

def _check_standard_online_parity(body: str, online: Path | None) -> CheckResult:
    if online is None or not online.exists():
        return CheckResult("Standard↔Online parity", "WARN",
                           "Online docx not found in submit dir.")
    expected = len(_all_cite_numbers(body))
    doc = Document(str(online))
    full_text = "\n".join(p.text for p in doc.paragraphs)
    online_blocks = full_text.count("((")
    if expected == online_blocks:
        return CheckResult(
            "Standard↔Online parity", "PASS",
            f"{expected} citation slots in revision.md, "
            f"{online_blocks} (( blocks in Online docx — match.",
        )
    diff = expected - online_blocks
    return CheckResult(
        "Standard↔Online parity", "FAIL" if diff > 0 else "WARN",
        f"{expected} citation slots in revision.md but {online_blocks} (( "
        f"blocks in Online docx. {'Conversion dropped citations.' if diff > 0 else 'More blocks than expected — may indicate parsing artefact.'}",
    )


# ─── 6. Duplication artefacts ──────────────────────────────────────────────

def _check_duplication_artefacts(body: str) -> CheckResult:
    """Look for substantial passages that appear both as a tracked
    insertion {{+...+}} AND as plain (already-merged) text elsewhere.
    Such passages would duplicate after acceptance.
    """
    insertions = [m.group(1).strip() for m in _INSERT_RE.finditer(body)]
    duplicates = []
    for ins in insertions:
        # Only check substantial inserted spans
        plain = re.sub(r"\[\[CITE:[^\]]+\]\]", "", ins).strip()
        if len(plain) < 40:
            continue
        # Remove the marker itself from the body for the dup search
        body_minus_ins = body.replace(f"{{{{+{ins}+}}}}", "")
        # Strip remaining markers so we compare plain text to plain text
        body_plain = _INSERT_RE.sub(lambda m: m.group(1), body_minus_ins)
        body_plain = _DELETE_RE.sub("", body_plain)
        body_plain = re.sub(r"\[\[CITE:[^\]]+\]\]", "", body_plain)
        if plain in body_plain:
            duplicates.append(plain[:80])
    if duplicates:
        return CheckResult(
            "Duplication artefacts", "FAIL",
            f"{len(duplicates)} insertion(s) duplicate text already present "
            f"in the body. First: '{duplicates[0]}...'",
        )
    return CheckResult(
        "Duplication artefacts", "PASS",
        "No insertions duplicate text already present in the body.",
    )


# ─── 7. Vanishing paragraphs ───────────────────────────────────────────────

def _check_vanishing_paragraphs(body: str) -> CheckResult:
    """Look for content marked both inserted AND deleted, or a RESTRUCTURE
    block with empty NEW text. Both would vanish after acceptance.
    """
    # 7a — RESTRUCTURE with empty new
    empty_restr = sum(
        1 for m in _RESTRUCTURE_RE.finditer(body) if not m.group(2).strip()
    )
    # 7b — A whole paragraph wrapped in both insert+delete markers.
    # Look for {{-X-}}{{+X+}} or {{+X+}}{{-X-}} with identical contents.
    issues = []
    if empty_restr:
        issues.append(f"{empty_restr} RESTRUCTURE block(s) have an empty NEW section")
    # Pair check
    for ins in _INSERT_RE.finditer(body):
        ins_text = ins.group(1).strip()
        if not ins_text:
            continue
        # Look for an adjacent delete with the same text
        if f"{{{{-{ins_text}-}}}}" in body:
            issues.append(f"identical {{+ +}} / {{-}} pair for: '{ins_text[:60]}...'")
            break
    if issues:
        return CheckResult("Vanishing paragraphs", "FAIL", "; ".join(issues))
    return CheckResult(
        "Vanishing paragraphs", "PASS",
        "No empty RESTRUCTURE blocks and no insert/delete pairs of identical text.",
    )


# ─── 8. Author attribution ─────────────────────────────────────────────────

def _check_author_attribution(tracked: Path | None,
                              clean: Path | None,
                              student_name: str) -> CheckResult:
    if not student_name:
        return CheckResult(
            "Author attribution", "FAIL",
            "revision.md frontmatter has no student_name — "
            "docx author cannot be verified.",
        )
    issues = []
    for label, p in (("Tracked", tracked), ("Clean", clean)):
        if p is None or not p.exists():
            issues.append(f"{label} docx missing from submit dir")
            continue
        try:
            doc = Document(str(p))
            author = (doc.core_properties.author or "").strip()
        except Exception as exc:
            issues.append(f"{label} docx unreadable: {exc}")
            continue
        if author.lower() in _AUTHOR_BLOCKLIST:
            issues.append(f"{label} author is {author!r} (blocklisted)")
        elif author != student_name:
            issues.append(
                f"{label} author is {author!r}, expected {student_name!r}"
            )
    if issues:
        return CheckResult("Author attribution", "FAIL", "; ".join(issues))
    return CheckResult(
        "Author attribution", "PASS",
        f"Tracked + Clean docx core_properties.author = {student_name!r}.",
    )


# ─── 9. Anonymous Standard ─────────────────────────────────────────────────

def _check_anonymous_standard(clean: Path | None) -> CheckResult:
    if clean is None or not clean.exists():
        return CheckResult("Anonymous Standard", "WARN",
                           "Clean docx not found in submit dir.")
    doc = Document(str(clean))
    full = "\n".join(p.text for p in doc.paragraphs)
    hits = _IDENTIFYING_REGEX.findall(full)
    if hits:
        return CheckResult(
            "Anonymous Standard", "FAIL",
            f"Identifying language found in Standard-Clean.docx: {list(set(hits))}",
        )
    return CheckResult(
        "Anonymous Standard", "PASS",
        "No identifying language detected in Standard-Clean.docx.",
    )


# ─── 10. Response letter ↔ manuscript reality ──────────────────────────────

def _check_letter_vs_manuscript(letter: Path | None,
                                clean: Path | None,
                                log_path: Path | None) -> CheckResult:
    """Weak check — confirm that the change-location section names in
    the letter all appear in the clean manuscript headings.
    A full claim-by-claim audit needs human review; this catches the
    obvious case of a letter referencing sections that aren't there.
    """
    if letter is None or not letter.exists():
        return CheckResult("Letter ↔ manuscript", "WARN",
                           "Response-Letter.docx not found in submit dir.")
    if clean is None or not clean.exists():
        return CheckResult("Letter ↔ manuscript", "WARN",
                           "Clean docx not found — skipping cross-check.")
    letter_doc = Document(str(letter))
    letter_text = "\n".join(p.text for p in letter_doc.paragraphs)

    # Extract every "Change location: X" line
    locations = re.findall(r"Change location:\s*(.+?)\s*$", letter_text, re.MULTILINE)
    if not locations:
        return CheckResult(
            "Letter ↔ manuscript", "WARN",
            "No 'Change location:' lines found in the letter. "
            "Letter may be a placeholder shell.",
        )

    # Build the set of section/heading-ish strings present in the clean docx.
    clean_doc = Document(str(clean))
    headings = {
        p.text.strip().lower()
        for p in clean_doc.paragraphs
        if p.style.name.lower().startswith("heading")
    }
    if not headings:
        return CheckResult(
            "Letter ↔ manuscript", "WARN",
            "Clean docx has no headings — can't validate change locations.",
        )

    # A location like "Abstract, paragraph 1" should mention a heading.
    misses = []
    for loc in locations:
        loc_lower = loc.lower()
        if loc_lower == "no manuscript change; see response above.":
            continue
        if not any(h.split(",")[0] in loc_lower for h in headings):
            # Try the reverse: section name appears in location text
            section_word = loc_lower.split(",")[0].strip()
            if not any(section_word in h or h in section_word for h in headings):
                misses.append(loc)
    if misses:
        return CheckResult(
            "Letter ↔ manuscript", "WARN",
            f"{len(misses)} 'Change location' line(s) reference sections not "
            f"found as headings in the clean manuscript. Sample: {misses[:2]}",
        )
    return CheckResult(
        "Letter ↔ manuscript", "PASS",
        f"All {len(locations)} 'Change location' lines map to a section "
        f"heading in the clean manuscript. (Claim-by-claim review still recommended.)",
    )


# ─── Reporting helpers ─────────────────────────────────────────────────────

def format_report(results: Iterable[CheckResult]) -> str:
    """Render results as plain text suitable for terminal or Streamlit."""
    lines = []
    width = max(len(r.name) for r in results) + 2
    for r in results:
        lines.append(f"  {r.status:<4}  {r.name:<{width}}  {r.detail}")
    return "\n".join(lines)


def summary_counts(results: Iterable[CheckResult]) -> dict[str, int]:
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    return counts


# ─── CLI ───────────────────────────────────────────────────────────────────

def _cli():
    parser = argparse.ArgumentParser(
        description="Audit an NHSJS revision build against the Phase 6 checklist.",
    )
    parser.add_argument("revision_md", help="Path to revision.md")
    parser.add_argument("submit_dir", help="Directory containing built outputs")
    parser.add_argument("--log", metavar="FILE",
                        help="Optional revision-log.md for cross-checks")
    args = parser.parse_args()

    results = audit_revision(args.revision_md, args.submit_dir, log_path=args.log)
    print(format_report(results))
    print()
    counts = summary_counts(results)
    print(f"Summary: {counts['PASS']} pass, {counts['WARN']} warn, "
          f"{counts['FAIL']} fail")
    raise SystemExit(0 if counts["FAIL"] == 0 else 1)


if __name__ == "__main__":
    _cli()
