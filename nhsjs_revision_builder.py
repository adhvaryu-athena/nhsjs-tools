"""
nhsjs_revision_builder.py
=========================
Build the 5 NHSJS revision outputs from a single `revision.md` source
file emitted by the Revise-After-Review v2 agent.

Public API
----------
    parse_revision(revision_md_path) -> RevisionDoc
        Read and validate a revision.md file. Raises BuilderError on
        malformed input (unclosed markers, missing frontmatter,
        REF_NEEDED placeholders, Unicode superscript glyphs in body).

    build_standard_tracked(revision, output_path) -> None
        Standard-format .docx with tracked-change markup:
            * red bold for {{+inserted+}} text
            * red strikethrough for {{-deleted-}} text
            * real OOXML <w:vertAlign w:val="superscript"> for [[CITE:N]]
            * docx core property `author` set to revision.student_name

    build_standard_clean(revision, output_path) -> None
        Standard-format .docx with all changes accepted (insertions
        kept, deletions dropped). Same superscript treatment.

    build_response_letter(revision, revision_log_md_path, output_path) -> None
        See nhsjs_revision_builder.build_response_letter docstring.

    build_student_handoff(revision, revision_log_md_path, output_path) -> None
        See nhsjs_revision_builder.build_student_handoff docstring.

    build_all(revision_md_path, revision_log_md_path, output_dir) -> dict
        Orchestrator. Produces all 5 outputs plus `FILES.md` in
        output_dir, chains the clean Standard through the Standard→Online
        converter, returns a dict of {kind: file_path}.

Marker syntax (must match Revise-After-Review v2 Phase 3.5):
    {{+inserted+}}              insertion (kept in clean, marked in tracked)
    {{-deleted-}}               deletion (dropped in clean, marked in tracked)
    [[CITE:17,23,24]]           citation -> real OOXML superscript
    {{RESTRUCTURE: OLD: ... NEW: ... }}  whole-paragraph replacement

Failure mode is **strict** — every validation failure raises BuilderError
with line numbers. The Streamlit tab and CLI both catch and surface the
error to the user; no partial outputs are written.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor


# ─── Constants ─────────────────────────────────────────────────────────────

RED = RGBColor(0xC0, 0x00, 0x00)

# Marker regexes. All are non-greedy, DOTALL-safe.
_CITE_RE = re.compile(r"\[\[CITE:([^\]]+)\]\]")
_INSERT_RE = re.compile(r"\{\{\+(.+?)\+\}\}", re.DOTALL)
_DELETE_RE = re.compile(r"\{\{-(.+?)-\}\}", re.DOTALL)
_RESTRUCTURE_RE = re.compile(
    r"\{\{RESTRUCTURE:\s*OLD:\s*(.*?)\s*NEW:\s*(.*?)\s*\}\}",
    re.DOTALL,
)

# Strict-mode validators
_UNICODE_SUPERSCRIPT = re.compile(
    r"[²³¹⁰-⁹]"  # ², ³, ¹, ⁰–⁹
)
_REF_NEEDED = re.compile(r"\[\[CITE:[^\]]*REF_NEEDED[^\]]*\]\]", re.IGNORECASE)
_VALID_CITE_BODY = re.compile(r"^\s*\d+(\s*,\s*\d+)*\s*$")

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_NUMBERED_LINE_RE = re.compile(r"^\s*\d+[.)]\s+\S")


# ─── Errors ────────────────────────────────────────────────────────────────

class BuilderError(Exception):
    """Raised on malformed revision.md input.

    Attributes:
        line: 1-indexed line number of the first offending location, or
              None when the issue is structural (missing frontmatter).
        kind: short tag — "frontmatter" / "unclosed_marker" / "ref_needed" /
              "unicode_superscript" / "malformed_cite" / "io".
    """

    def __init__(self, message: str, *, kind: str = "io",
                 line: int | None = None):
        super().__init__(message)
        self.kind = kind
        self.line = line


# ─── Data class ────────────────────────────────────────────────────────────

@dataclass
class RevisionDoc:
    """In-memory representation of a parsed revision.md.

    Body is the raw markdown text after frontmatter has been stripped.
    Inline markers (`{{+...+}}`, `[[CITE:N]]`, etc.) are preserved
    verbatim; they are resolved by the build_* functions.
    """
    student_name: str
    manuscript_title: str
    reviewer_decision_date: str
    target_submit_date: str
    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""
    source_path: str | None = None


# ─── parse_revision ────────────────────────────────────────────────────────

def parse_revision(revision_md_path: str) -> RevisionDoc:
    """Read, validate, and return a RevisionDoc.

    Raises BuilderError on:
      * missing or malformed YAML frontmatter
      * any unclosed `{{+`, `{{-`, or `{{RESTRUCTURE:` marker
      * any `[[CITE:REF_NEEDED_N]]` placeholder left in the body
      * any Unicode superscript glyph (¹²³⁰–⁹) — these must be
        re-emitted as `[[CITE:N]]` so they hit real OOXML superscript
      * any `[[CITE:...]]` whose content is not comma-separated digits
    """
    path = Path(revision_md_path)
    if not path.exists():
        raise BuilderError(f"revision.md not found: {revision_md_path}", kind="io")

    raw = path.read_text(encoding="utf-8")

    # 1. Frontmatter
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", raw, re.DOTALL)
    if not m:
        raise BuilderError(
            "revision.md is missing YAML frontmatter. Expected a "
            "leading block delimited by `---` lines containing at least "
            "`student_name` and `manuscript_title`.",
            kind="frontmatter",
        )
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        raise BuilderError(
            f"revision.md frontmatter is not valid YAML: {exc}",
            kind="frontmatter",
        ) from exc
    body = m.group(2)
    # Where in the source file does the body begin? Used to translate
    # body-relative offsets back into file-relative line numbers.
    body_line_offset = raw.count("\n", 0, m.start(2))

    if not fm.get("student_name"):
        raise BuilderError(
            "revision.md frontmatter is missing `student_name` "
            "(required for docx author attribution).",
            kind="frontmatter",
        )
    if not fm.get("manuscript_title"):
        raise BuilderError(
            "revision.md frontmatter is missing `manuscript_title` "
            "(required for output filenames).",
            kind="frontmatter",
        )

    # 2. Strict validation of body markers
    _validate_body(body, line_offset=body_line_offset)

    return RevisionDoc(
        student_name=str(fm["student_name"]),
        manuscript_title=str(fm["manuscript_title"]),
        reviewer_decision_date=str(fm.get("reviewer_decision_date", "")),
        target_submit_date=str(fm.get("target_submit_date", "")),
        frontmatter=fm,
        body=body,
        source_path=str(path),
    )


def _validate_body(body: str, line_offset: int = 0) -> None:
    """Strict validation pass. Raises BuilderError on the first issue found.

    line_offset translates a body-relative offset back into file-relative
    line numbers (the body region typically starts ~5–10 lines into the
    file because of YAML frontmatter).
    """

    def file_line(body_idx: int) -> int:
        return body.count("\n", 0, body_idx) + 1 + line_offset

    # Unicode superscript glyphs — refuse, recommend the right marker.
    m = _UNICODE_SUPERSCRIPT.search(body)
    if m:
        line = file_line(m.start())
        raise BuilderError(
            f"Unicode superscript glyph {m.group(0)!r} found at line "
            f"{line}. Citations must use `[[CITE:N]]` markers — these "
            f"produce real OOXML superscript downstream. Re-run RaR v2 "
            f"with the proper markers, or convert manually.",
            kind="unicode_superscript",
            line=line,
        )

    # REF_NEEDED placeholders — refuse, the Reference Hunter step didn't run.
    m = _REF_NEEDED.search(body)
    if m:
        line = file_line(m.start())
        raise BuilderError(
            f"Unresolved citation placeholder {m.group(0)} at line "
            f"{line}. Run the Reference Hunter flow in RaR v2 Phase 2 to "
            f"fill in real citation numbers before building.",
            kind="ref_needed",
            line=line,
        )

    # Malformed CITE content
    for m in _CITE_RE.finditer(body):
        if not _VALID_CITE_BODY.match(m.group(1)):
            line = file_line(m.start())
            raise BuilderError(
                f"Malformed citation {m.group(0)!r} at line {line}. "
                f"`[[CITE:...]]` must contain only comma-separated digits.",
                kind="malformed_cite",
                line=line,
            )

    # Unclosed insert / delete / restructure markers
    _check_balanced(body, "{{+", "+}}", "insertion ({{+...+}})", line_offset)
    _check_balanced(body, "{{-", "-}}", "deletion ({{-...-}})", line_offset)
    _check_balanced(
        body, "{{RESTRUCTURE:", "}}", "restructure block", line_offset,
        skip_if_resolved=True,
    )


def _check_balanced(body: str, opener: str, closer: str, label: str,
                    line_offset: int,
                    skip_if_resolved: bool = False) -> None:
    """Naive balance check — count opens vs closes."""
    opens = body.count(opener)
    if skip_if_resolved:
        matches = list(_RESTRUCTURE_RE.finditer(body))
        if len(matches) != opens:
            unmatched_idx = body.find(opener, sum(len(m.group(0)) for m in matches))
            line = ((body.count("\n", 0, unmatched_idx) + 1 + line_offset)
                    if unmatched_idx >= 0 else None)
            raise BuilderError(
                f"Unclosed {label} marker. Found {opens} `{opener}` "
                f"opener(s) but only {len(matches)} well-formed block(s).",
                kind="unclosed_marker",
                line=line,
            )
        return

    closes = body.count(closer)
    if opens != closes:
        idx = body.find(opener)
        line = (body.count("\n", 0, idx) + 1 + line_offset) if idx >= 0 else None
        raise BuilderError(
            f"Unbalanced {label} markers — found {opens} `{opener}` "
            f"openers but {closes} `{closer}` closers.",
            kind="unclosed_marker",
            line=line,
        )


# ─── Run helpers (OOXML superscript + styled runs) ─────────────────────────

def _add_superscript_run(paragraph, text: str, *,
                         red: bool = False, bold: bool = False,
                         strike: bool = False):
    """Append a run with real Word native superscript formatting.

    This is the crucial fix vs. legacy converters that used Unicode
    glyphs — only `<w:vertAlign w:val="superscript">` is picked up by
    the downstream Standard→Online converter's is_superscript() check.
    """
    run = paragraph.add_run(text)
    rPr = run._element.get_or_add_rPr()
    va = OxmlElement("w:vertAlign")
    va.set(qn("w:val"), "superscript")
    rPr.append(va)
    if red:
        run.font.color.rgb = RED
    if bold:
        run.bold = True
    if strike:
        run.font.strike = True
    return run


def _add_styled_run(paragraph, text: str, *,
                    red: bool = False, bold: bool = False,
                    strike: bool = False):
    run = paragraph.add_run(text)
    if red:
        run.font.color.rgb = RED
    if bold:
        run.bold = True
    if strike:
        run.font.strike = True
    return run


def _emit_text_with_citations(paragraph, text: str, *,
                              red: bool = False, bold: bool = False,
                              strike: bool = False) -> None:
    """Walk text, emit plain runs and superscript runs for [[CITE:N]] markers.

    The text passed here has already had {{+}} / {{-}} markers stripped
    (or applied) — only [[CITE:...]] tokens remain to be resolved.
    """
    i = 0
    for m in _CITE_RE.finditer(text):
        if m.start() > i:
            _add_styled_run(paragraph, text[i:m.start()],
                            red=red, bold=bold, strike=strike)
        digits = m.group(1).replace(" ", "")
        _add_superscript_run(paragraph, digits,
                             red=red, bold=bold, strike=strike)
        i = m.end()
    if i < len(text):
        _add_styled_run(paragraph, text[i:],
                        red=red, bold=bold, strike=strike)


def _emit_inline_tracked(paragraph, text: str) -> None:
    """Walk text in tracked mode. Insertions render red+bold,
    deletions render red+strikethrough, citations as superscript."""
    i = 0
    while i < len(text):
        ins_m = _INSERT_RE.search(text, i)
        del_m = _DELETE_RE.search(text, i)
        if ins_m and del_m:
            if ins_m.start() < del_m.start():
                marker, kind = ins_m, "ins"
            else:
                marker, kind = del_m, "del"
        elif ins_m:
            marker, kind = ins_m, "ins"
        elif del_m:
            marker, kind = del_m, "del"
        else:
            if i < len(text):
                _emit_text_with_citations(paragraph, text[i:])
            return

        if marker.start() > i:
            _emit_text_with_citations(paragraph, text[i:marker.start()])
        inner = marker.group(1)
        if kind == "ins":
            _emit_text_with_citations(paragraph, inner, red=True, bold=True)
        else:
            _emit_text_with_citations(paragraph, inner, red=True, strike=True)
        i = marker.end()


def _emit_inline_clean(paragraph, text: str) -> None:
    """Walk text in clean mode. Insertions kept as plain text, deletions
    dropped, citations as superscript."""
    text = _INSERT_RE.sub(lambda m: m.group(1), text)
    text = _DELETE_RE.sub("", text)
    _emit_text_with_citations(paragraph, text)


# ─── Body walker (RESTRUCTURE-aware paragraph splitter) ────────────────────

def _split_body_pieces(body: str) -> list[tuple]:
    """Return a list of pieces: ("text", str) or ("restructure", old, new)."""
    pieces: list[tuple] = []
    last = 0
    for m in _RESTRUCTURE_RE.finditer(body):
        if m.start() > last:
            pieces.append(("text", body[last:m.start()]))
        pieces.append(("restructure", m.group(1).strip(), m.group(2).strip()))
        last = m.end()
    if last < len(body):
        pieces.append(("text", body[last:]))
    return pieces


def _apply_doc_chrome(doc: Document, revision: RevisionDoc) -> None:
    """Set core properties + base font."""
    doc.core_properties.author = revision.student_name
    doc.core_properties.last_modified_by = revision.student_name
    if revision.manuscript_title:
        doc.core_properties.title = revision.manuscript_title

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)


def _walk_text_pieces(doc: Document, body: str, *, mode: str) -> None:
    """Render the body into doc, paragraph by paragraph.

    mode == 'tracked'  → insertions red+bold, deletions red+strike.
    mode == 'clean'    → insertions kept plain, deletions dropped.
    """
    emit_inline = _emit_inline_tracked if mode == "tracked" else _emit_inline_clean

    for piece in _split_body_pieces(body):
        if piece[0] == "text":
            text = piece[1].replace("\r\n", "\n").replace("\r", "\n")
            for raw_para in re.split(r"\n\s*\n", text):
                para = raw_para.strip("\n")
                if not para.strip():
                    continue

                # Section heading? (single-line, leading #s)
                lines = para.split("\n")
                if len(lines) == 1:
                    h = _HEADING_RE.match(lines[0])
                    if h:
                        # Strip markers from heading text in clean mode;
                        # in tracked mode keep them visible (rare to have).
                        heading_text = h.group(2)
                        if mode == "clean":
                            heading_text = _INSERT_RE.sub(
                                lambda m: m.group(1), heading_text
                            )
                            heading_text = _DELETE_RE.sub("", heading_text)
                        heading_text = _CITE_RE.sub("", heading_text).strip()
                        doc.add_heading(heading_text,
                                        level=min(len(h.group(1)), 4))
                        continue

                # Numbered-list-style paragraph (e.g. References)?
                # Emit each line as its own paragraph so the downstream
                # Standard→Online parser can find every entry.
                if (len(lines) >= 2
                        and all(_NUMBERED_LINE_RE.match(ln) for ln in lines)):
                    for ln in lines:
                        sub_p = doc.add_paragraph()
                        emit_inline(sub_p, ln.strip())
                    continue

                # Otherwise collapse soft newlines into a single paragraph
                flat = " ".join(line.strip() for line in lines)
                p = doc.add_paragraph()
                emit_inline(p, flat)
        else:
            # RESTRUCTURE block
            _, old_text, new_text = piece
            if mode == "tracked":
                p_old = doc.add_paragraph()
                _emit_text_with_citations(p_old, old_text, red=True, strike=True)
                p_new = doc.add_paragraph()
                _emit_text_with_citations(p_new, new_text, red=True, bold=True)
            else:
                p = doc.add_paragraph()
                _emit_text_with_citations(p, new_text)


# ─── Public builders ───────────────────────────────────────────────────────

def build_standard_tracked(revision: RevisionDoc, output_path: str) -> None:
    """Write the Standard-Tracked .docx (insertions red+bold,
    deletions red+strikethrough)."""
    doc = Document()
    _apply_doc_chrome(doc, revision)
    _walk_text_pieces(doc, revision.body, mode="tracked")
    doc.save(output_path)


def build_standard_clean(revision: RevisionDoc, output_path: str) -> None:
    """Write the Standard-Clean .docx (changes accepted)."""
    doc = Document()
    _apply_doc_chrome(doc, revision)
    _walk_text_pieces(doc, revision.body, mode="clean")
    doc.save(output_path)


# ─── Filename helper ───────────────────────────────────────────────────────

_FILENAME_NONALNUM = re.compile(r"[^a-z0-9]+")
_FILENAME_TRIM = re.compile(r"^-+|-+$")


def sanitize_filename_stem(title: str, *, cap: int = 80) -> str:
    """Stable filename stem from a free-form title.

    Rule (documented in README):
      1. lowercase
      2. replace any run of non-alphanumeric chars with a single `-`
      3. strip leading/trailing dashes
      4. cap at `cap` characters (default 80)
    """
    if not title:
        return "untitled"
    stem = title.lower()
    stem = _FILENAME_NONALNUM.sub("-", stem)
    stem = _FILENAME_TRIM.sub("", stem)
    if len(stem) > cap:
        stem = stem[:cap].rstrip("-")
    return stem or "untitled"


# ─── revision-log.md parser ────────────────────────────────────────────────
#
# revision-log.md schema (pinned by this module, documented in README):
#
#   ## Approved Actions
#
#   ### Action A1 — Short summary
#   Comments: R1.1, R1.2
#   Section: Abstract
#   Classification: Accept in full
#   Priority: NON-NEGOTIABLE
#   Effort: 15 min
#   Change summary: Added a citation supporting the opening claim.
#   Location: Abstract, paragraph 1
#   Status: APPLIED
#   Reviewer R1.1: "verbatim quote from the reviewer decision PDF"
#   Reviewer R1.2: "verbatim quote for the second contributing comment"
#
#   ### Action A2 — ...
#
#   ## Pushed-back comments
#
#   ### Comment R1.4 — Re-run analysis with a different test
#   Reviewer R1.4: "verbatim quote"
#   Push-back defense: One-paragraph defense explaining scope/timeline.
#   Status: DEFENDED
#
# Field rules:
#   * Action / Comment headers MUST start with `### Action ` or `### Comment `.
#   * Lines `Key: value` inside a block are case-insensitive on the key.
#   * `Reviewer R<n>.<m>: "..."` lines provide verbatim quotes used in
#     the response letter. Missing quotes degrade gracefully — the
#     letter emits `[REVIEWER COMMENT QUOTE — INSERT FROM PDF]`.
#   * Comments field is comma-separated comment IDs.
#   * A block ends at the next `### ` header or any `## ` H2.
#
# The parser is intentionally forgiving — extra fields are preserved as
# dict keys so future schema extensions don't break it.

_ACTION_HEADER_RE = re.compile(r"^###\s+Action\s+([A-Za-z0-9]+)\s*(?:—|-)\s*(.+?)\s*$")
_COMMENT_HEADER_RE = re.compile(r"^###\s+Comment\s+(R\d+\.\d+)\s*(?:—|-)\s*(.+?)\s*$")
_KV_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*?)\s*:\s*(.*)$")
_REVIEWER_QUOTE_RE = re.compile(
    r'^Reviewer\s+(R\d+\.\d+)\s*:\s*"?(.*?)"?\s*$', re.IGNORECASE
)


def _parse_revision_log(path: str | Path | None) -> dict:
    """Parse a revision-log.md into a structured dict.

    Returns:
        {"actions": [...], "pushed_back": [...]}

    Returns empty lists for both when path is None or the file doesn't
    exist — callers should emit a placeholder letter/handoff in that case.
    """
    if path is None:
        return {"actions": [], "pushed_back": []}
    p = Path(path)
    if not p.exists():
        return {"actions": [], "pushed_back": []}

    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()

    actions: list[dict] = []
    pushed: list[dict] = []
    current: dict | None = None
    current_kind: str | None = None  # "action" or "comment"

    def _commit():
        nonlocal current, current_kind
        if current is None:
            return
        if current_kind == "action":
            actions.append(current)
        elif current_kind == "comment":
            pushed.append(current)
        current = None
        current_kind = None

    for ln in lines:
        if ln.startswith("## ") and not ln.startswith("### "):
            _commit()
            continue

        m_action = _ACTION_HEADER_RE.match(ln)
        if m_action:
            _commit()
            current = {
                "id": m_action.group(1),
                "summary": m_action.group(2).strip(),
                "comments": [],
                "reviewer_text": {},
            }
            current_kind = "action"
            continue

        m_comment = _COMMENT_HEADER_RE.match(ln)
        if m_comment:
            _commit()
            current = {
                "id": m_comment.group(1),
                "summary": m_comment.group(2).strip(),
                "reviewer_text": {},
            }
            current_kind = "comment"
            continue

        if current is None:
            continue

        m_quote = _REVIEWER_QUOTE_RE.match(ln)
        if m_quote:
            current["reviewer_text"][m_quote.group(1)] = m_quote.group(2).strip()
            continue

        m_kv = _KV_RE.match(ln)
        if m_kv:
            key = m_kv.group(1).strip().lower().replace(" ", "_")
            val = m_kv.group(2).strip()
            if key == "comments":
                current["comments"] = [c.strip() for c in val.split(",") if c.strip()]
            else:
                current[key] = val
            continue

    _commit()
    return {"actions": actions, "pushed_back": pushed}


# ─── build_response_letter ─────────────────────────────────────────────────

_QUOTE_PLACEHOLDER = "[REVIEWER COMMENT QUOTE — INSERT FROM PDF]"


def build_response_letter(revision: RevisionDoc,
                          revision_log_md_path: str | None,
                          output_path: str) -> None:
    """Generate the reviewer response letter as a .docx.

    Format (per RaR v2 Phase 4):
      - Salutation
      - One H2 per reviewer (R1, R2, ...) grouping their comments
      - One H3 per comment, with verbatim quote (blockquote-styled),
        Response paragraph, and Change location line
      - Pushed-back comments interleaved with their reviewer group
      - "Summary of major changes" section at the end
      - Closing "Sincerely, [student_name]"

    When revision_log_md_path is None or missing, the letter emits
    a placeholder shell so the consultant has something to fill in.
    """
    log = _parse_revision_log(revision_log_md_path)
    actions = log["actions"]
    pushed = log["pushed_back"]

    # Group comments by reviewer index. Each comment is a dict:
    #   {"comment_id": "R1.1", "verbatim": "...", "response": "...",
    #    "location": "...", "kind": "action"|"pushback"}
    comments_by_reviewer: dict[int, list[dict]] = {}

    for action in actions:
        comment_ids = action.get("comments", [])
        change_summary = action.get("change_summary", "")
        location = action.get("location", "")
        classification = action.get("classification", "")
        for cid in comment_ids:
            reviewer_idx = _reviewer_index_from_id(cid)
            if reviewer_idx is None:
                continue
            comments_by_reviewer.setdefault(reviewer_idx, []).append({
                "comment_id": cid,
                "verbatim": action["reviewer_text"].get(cid, ""),
                "response": _craft_response_line(classification, change_summary),
                "location": location or "No manuscript change; see response above.",
                "kind": "action",
            })

    for pb in pushed:
        cid = pb.get("id", "")
        reviewer_idx = _reviewer_index_from_id(cid)
        if reviewer_idx is None:
            continue
        comments_by_reviewer.setdefault(reviewer_idx, []).append({
            "comment_id": cid,
            "verbatim": pb["reviewer_text"].get(cid, ""),
            "response": pb.get("push_back_defense", ""),
            "location": "No manuscript change; see response above.",
            "kind": "pushback",
        })

    # Sort comments within each reviewer by their numeric tail (R1.2 < R1.10).
    for idx in comments_by_reviewer:
        comments_by_reviewer[idx].sort(key=_comment_sort_key)

    # ─── Build the docx ────────────────────────────────────────────────
    doc = Document()
    _apply_doc_chrome(doc, revision)

    doc.add_heading("Reviewer Response Letter", level=0)

    para = doc.add_paragraph()
    para.add_run("Dear Editor and Reviewers,")
    doc.add_paragraph(
        "We thank the reviewers for their constructive and detailed feedback. "
        "Below we address each comment point by point. Changes to the "
        "manuscript are marked in red text. Reviewer comments are quoted "
        "verbatim."
    )

    if not comments_by_reviewer:
        warn = doc.add_paragraph()
        warn_run = warn.add_run(
            "[PLACEHOLDER LETTER — no revision-log.md provided. Fill in "
            "comments, responses, and change locations manually.]"
        )
        warn_run.font.color.rgb = RED
        warn_run.italic = True
    else:
        for reviewer_idx in sorted(comments_by_reviewer):
            doc.add_heading(f"Reviewer {reviewer_idx}", level=1)
            for comment in comments_by_reviewer[reviewer_idx]:
                doc.add_heading(f"Comment {comment['comment_id']}", level=2)
                # Verbatim quote in italic, indented look
                q = doc.add_paragraph()
                q_run = q.add_run(
                    f'"{comment["verbatim"]}"' if comment["verbatim"]
                    else _QUOTE_PLACEHOLDER
                )
                q_run.italic = True

                resp_para = doc.add_paragraph()
                bold = resp_para.add_run("Response: ")
                bold.bold = True
                resp_para.add_run(
                    comment["response"] or "[FILL IN RESPONSE — log entry was empty]"
                )

                loc_para = doc.add_paragraph()
                bold = loc_para.add_run("Change location: ")
                bold.bold = True
                loc_para.add_run(comment["location"])

    # Summary section
    doc.add_heading("Summary of major changes", level=1)
    if actions:
        # Plain prose (not bullets) per Athena writing voice
        for action in actions:
            change_summary = action.get("change_summary", "")
            summary = action.get("summary", "")
            if change_summary:
                doc.add_paragraph(f"{summary}. {change_summary}")
            elif summary:
                doc.add_paragraph(summary)
    else:
        doc.add_paragraph("[FILL IN MAJOR CHANGES SUMMARY]")

    doc.add_paragraph()
    doc.add_paragraph("Sincerely,")
    doc.add_paragraph(revision.student_name)

    doc.save(output_path)


def _reviewer_index_from_id(comment_id: str) -> int | None:
    """Extract the reviewer number from `R1.1` → 1."""
    m = re.match(r"^R(\d+)\.\d+$", comment_id)
    if m:
        return int(m.group(1))
    return None


def _comment_sort_key(comment: dict) -> tuple:
    """Sort key so R1.2 < R1.10."""
    m = re.match(r"^R(\d+)\.(\d+)$", comment.get("comment_id", ""))
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (999, 999)


def _craft_response_line(classification: str, change_summary: str) -> str:
    """Compose a one-line response from the action's classification + summary."""
    if not change_summary:
        return "[FILL IN — change summary was missing from the log]"
    cls = (classification or "").lower()
    if "push" in cls:
        return change_summary
    if "out of scope" in cls:
        return f"We respectfully note this. {change_summary}"
    # Default: accepted in full or with scope
    return f"We have made this change. {change_summary}"


# ─── build_student_handoff ─────────────────────────────────────────────────

_HANDOFF_DEFAULT_TODO = (
    "Open `Standard-Tracked.docx`, read the red text top to bottom, and "
    "click Accept or Reject as you go. Most should be Accept — the clean "
    "version assumes everything is accepted."
)

_HANDOFF_DEFAULT_CHECKLIST = [
    "Read through `Standard-Clean.docx` and confirm it says what you want",
    "Confirm your name is on the docx as the author (it should be — we set it)",
    "Reply to the NHSJS email with these three files attached: "
    "`{stem}-Standard-Tracked.docx`, `{stem}-Online.docx`, `Response-Letter.docx`",
    "Confirm submission receipt within 24 hours",
]


def build_student_handoff(revision: RevisionDoc,
                          revision_log_md_path: str | None,
                          output_path: str) -> None:
    """Generate the 4-part Student Handoff markdown file."""
    log = _parse_revision_log(revision_log_md_path)
    actions = log["actions"]
    pushed = log["pushed_back"]

    stem = sanitize_filename_stem(revision.manuscript_title)
    lines: list[str] = []

    lines.append(f"# {revision.student_name} — NHSJS Revision Handoff")
    lines.append("")
    lines.append(f"_Manuscript: {revision.manuscript_title}_")
    lines.append("")

    # ─── Section 1: What the reviewer said ──
    lines.append("## 1. What the reviewer said")
    lines.append("")
    if actions:
        # Use action summaries — one bullet each, capped to ~5
        themes = _derive_themes(actions, pushed)
        for theme in themes[:7]:
            lines.append(f"- {theme}")
    else:
        lines.append("- [FILL IN — list 3–5 themes from the reviewer decision]")
    lines.append("")

    # ─── Section 2: What we changed and how ──
    lines.append("## 2. What we changed and how")
    lines.append("")
    if actions:
        for action in actions:
            change_summary = action.get("change_summary", "").strip()
            location = action.get("location", "").strip()
            if change_summary:
                if location:
                    lines.append(f"- {change_summary} (See: {location}.)")
                else:
                    lines.append(f"- {change_summary}")
    else:
        lines.append("- [FILL IN — list each major change with its location]")
    if pushed:
        lines.append("")
        lines.append("Pushed back on:")
        for pb in pushed:
            lines.append(
                f"- {pb.get('summary', pb.get('id', '?'))} "
                f"(see Response-Letter.docx)"
            )
    lines.append("")

    # ─── Section 3: What you need to do ──
    lines.append("## 3. What you need to do")
    lines.append("")
    lines.append(f"- {_HANDOFF_DEFAULT_TODO}")
    lines.append("")

    # ─── Section 4: What's needed to send ──
    lines.append("## 4. What's needed to send")
    lines.append("")
    for item in _HANDOFF_DEFAULT_CHECKLIST:
        lines.append(f"- [ ] {item.format(stem=stem)}")
    lines.append("")
    lines.append("Any questions, ping me.")
    lines.append("")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


def _derive_themes(actions: list[dict], pushed: list[dict]) -> list[str]:
    """Collapse Action summaries into a small set of themes, by Section field.

    Falls back to using raw summaries when sections are missing.
    """
    by_section: dict[str, list[str]] = {}
    for action in actions:
        section = action.get("section", "").strip() or "General"
        by_section.setdefault(section, []).append(action.get("summary", ""))

    themes: list[str] = []
    for section, summaries in by_section.items():
        if len(summaries) == 1:
            themes.append(f"{section}: {summaries[0]}")
        else:
            themes.append(
                f"{section}: {len(summaries)} comments addressed "
                f"({'; '.join(summaries[:2])}"
                + (", ..." if len(summaries) > 2 else "")
                + ")"
            )

    if pushed:
        themes.append(
            f"{len(pushed)} comment(s) respectfully declined as out of scope "
            f"or beyond the revision-week budget"
        )
    return themes


# ─── build_all orchestrator ────────────────────────────────────────────────

_FILES_MD_TEMPLATE = """\
# Submission Files — {title}

Generated by nhsjs-tools v{version} on {date}.

| File | What it is |
|------|-----------|
| `{tracked_name}` | Standard-format manuscript with tracked changes. Insertions in red bold, deletions in red strikethrough. Send to NHSJS so reviewers can see exactly what changed. |
| `{clean_name}` | Standard-format manuscript with all changes accepted (no markup). This is the version of record for the resubmission. |
| `{online_name}` | Online-publication format derived from the clean Standard. Citations are full-text in `((double parens))` instead of numeric superscript. Send to NHSJS in addition to the Standard version. |
| `Response-Letter.docx` | Point-by-point reviewer response letter. Send to NHSJS as a separate attachment. |
| `Student-Handoff.md` | Internal handoff message for the student. Not for submission — sign-off + checklist. |

## Author attribution

The docx files are attributed to **{student_name}** (docx core property `author`).

## Reproducing this build

```bash
python -m nhsjs_revision_builder revision.md submit/ --log revision-log.md
```

## Audit

Run `python -m nhsjs_audit submit/` to re-run the Phase 6 self-audit
against the built files.
"""


def build_all(revision_md_path: str,
              revision_log_md_path: str | None,
              output_dir: str) -> dict[str, str]:
    """Orchestrate the full build: 5 outputs + FILES.md in output_dir.

    Returns a dict mapping each output kind to its absolute path:
        {
          "standard_tracked": "...",
          "standard_clean":   "...",
          "online":           "...",
          "response_letter":  "...",
          "student_handoff":  "...",
          "files_md":         "...",
        }

    Raises BuilderError if revision.md is malformed (strict mode).
    Missing revision-log.md is tolerated — letter + handoff degrade
    to placeholder shells.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    revision = parse_revision(revision_md_path)
    stem = sanitize_filename_stem(revision.manuscript_title)

    tracked_path = out / f"{stem}-Standard-Tracked.docx"
    clean_path = out / f"{stem}-Standard-Clean.docx"
    online_path = out / f"{stem}-Online.docx"
    letter_path = out / "Response-Letter.docx"
    handoff_path = out / "Student-Handoff.md"
    files_md_path = out / "FILES.md"

    # 1, 2 — Standard docx (tracked + clean)
    build_standard_tracked(revision, str(tracked_path))
    build_standard_clean(revision, str(clean_path))

    # 3 — Online format, by piping the clean Standard through the
    # existing Standard→Online converter. Imported lazily so the
    # revision builder is usable without pulling everything.
    from nhsjs_standard_to_online import convert_standard_to_online
    convert_standard_to_online(str(clean_path), str(online_path))

    # 4 — Response letter
    build_response_letter(revision, revision_log_md_path, str(letter_path))

    # 5 — Student handoff
    build_student_handoff(revision, revision_log_md_path, str(handoff_path))

    # FILES.md manifest
    import datetime
    files_md_path.write_text(
        _FILES_MD_TEMPLATE.format(
            title=revision.manuscript_title,
            version=_VERSION,
            date=datetime.date.today().isoformat(),
            student_name=revision.student_name,
            tracked_name=tracked_path.name,
            clean_name=clean_path.name,
            online_name=online_path.name,
        ),
        encoding="utf-8",
    )

    return {
        "standard_tracked": str(tracked_path.resolve()),
        "standard_clean":   str(clean_path.resolve()),
        "online":           str(online_path.resolve()),
        "response_letter":  str(letter_path.resolve()),
        "student_handoff":  str(handoff_path.resolve()),
        "files_md":         str(files_md_path.resolve()),
    }


_VERSION = "1.0.0"


# ─── CLI ───────────────────────────────────────────────────────────────────

def _cli():
    parser = argparse.ArgumentParser(
        description="Build NHSJS revision outputs from a revision.md file.",
    )
    parser.add_argument("revision_md", help="Path to revision.md")
    parser.add_argument("output_dir", nargs="?", default="submit",
                        help="Output directory (default: submit/)")
    parser.add_argument("--log", metavar="FILE",
                        help="Optional revision-log.md for letter + handoff")
    args = parser.parse_args()

    try:
        result = build_all(args.revision_md, args.log, args.output_dir)
    except BuilderError as exc:
        print(f"error: {exc}", file=sys.stderr)
        if exc.line:
            print(f"  at line {exc.line}", file=sys.stderr)
        raise SystemExit(2)

    for kind, path in result.items():
        print(f"  {kind:<20}  {path}")


if __name__ == "__main__":
    _cli()
