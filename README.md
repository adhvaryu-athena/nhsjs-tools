# NHSJS Conversion Tools

Streamlit web app + Python library for converting and revising NHSJS manuscripts.

## Tools

**LaTeX → Online Format**
Upload an Overleaf `.zip` or `.tex` file. Strips LaTeX markup, embeds figures, auto-numbers figures/tables, resolves cross-references, replaces every citation with the NHSJS `((full citation))` format. Outputs a `.docx`.

**Standard → Online Format**
Upload an NHSJS Word document with real OOXML superscript numbered citations. Finds the References section, parses it, replaces every superscript citation with the corresponding `((full citation))`. Optionally accepts a `.txt` references file when refs aren't in the docx itself.

**Revision → All Outputs**
Paste (or upload) a `revision.md` produced by the **Revise-After-Review v2** agent. Produces all 5 NHSJS submission files in a downloadable zip:
- `{title}-Standard-Tracked.docx` — tracked changes (red bold inserts, red strikethrough deletes)
- `{title}-Standard-Clean.docx` — changes accepted
- `{title}-Online.docx` — `((full citation))` format
- `Response-Letter.docx` — point-by-point reviewer response
- `Student-Handoff.md` — 4-part student sign-off message

Includes a Phase 6 self-audit (10 checks) that surfaces orphan refs, missing superscript runs, identifying language in the anonymous Standard, and more.

## Quick Start (local)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Opens at [http://localhost:8501](http://localhost:8501).

## Library use (Cowork mode)

The same library that powers the web app is installable from PyPI. A Cowork bot mounted in a scholar's review folder can build outputs locally with one call:

```bash
pip install nhsjs-tools
```

```python
from nhsjs_revision_builder import build_all
from nhsjs_audit import audit_revision

result = build_all("revision.md", "revision-log.md", "submit/")
# result = {"standard_tracked": "...", "standard_clean": "...", ...}

audit = audit_revision("revision.md", "submit/", log_path="revision-log.md")
```

CLI equivalents are installed by the same `pip install`:

```bash
nhsjs-build-revision revision.md submit/ --log revision-log.md
nhsjs-audit-revision revision.md submit/ --log revision-log.md
nhsjs-latex-to-online project.zip output.docx
nhsjs-standard-to-online manuscript.docx output.docx
```

The library has no Streamlit dependency — `pip install nhsjs-tools` pulls only `python-docx`, `Pillow`, `lxml`, and `PyYAML`.

## `revision.md` and `revision-log.md` schemas

The library consumes two files produced by the Revise-After-Review v2 agent.

### `revision.md`

YAML frontmatter (`student_name`, `manuscript_title` required) followed by the full revised manuscript body. Body markers:

```text
{{+inserted text+}}                    insertion — red bold in Tracked, kept in Clean
{{-deleted text-}}                     deletion  — red strike in Tracked, dropped in Clean
[[CITE:17,23,24]]                      citation  — real OOXML superscript, no Unicode glyphs
{{RESTRUCTURE: OLD: ... NEW: ... }}    whole-paragraph replacement
```

Numbered references at the end (one per line) are split into individual paragraphs automatically so the Standard→Online converter picks them up.

### `revision-log.md`

```text
## Approved Actions

### Action A1 — Short summary
Comments: R1.1, R1.2
Section: Abstract
Classification: Accept in full
Priority: NON-NEGOTIABLE
Effort: 15 min
Change summary: What was changed.
Location: Abstract, paragraph 1
Status: APPLIED
Reviewer R1.1: "verbatim quote from the reviewer decision PDF"
Reviewer R1.2: "verbatim quote for the second contributing comment"

## Pushed-back comments

### Comment R1.4 — Short summary
Reviewer R1.4: "verbatim quote"
Push-back defense: One paragraph defending the current approach.
Status: DEFENDED
```

`Reviewer R*.* : "..."` lines are optional. When absent, the response letter renders a placeholder for the human reviewer to fill in.

## Build failure mode

Strict. Any of these in `revision.md` causes the build to abort with a line number:
- Missing YAML frontmatter or missing `student_name` / `manuscript_title`
- Unclosed `{{+`, `{{-`, or `{{RESTRUCTURE:` markers
- Unresolved `[[CITE:REF_NEEDED_*]]` placeholders
- Unicode superscript glyphs (`¹²³⁰–⁹`) anywhere in the body
- Malformed `[[CITE:...]]` content (must be comma-separated digits)

The Streamlit tab catches these and renders the error inline. Missing `revision-log.md` is **not** an error — the letter + handoff degrade to placeholder shells.

## Output filename rule

The manuscript title from frontmatter is sanitized to a filename stem:
1. lowercase
2. replace any run of non-alphanumeric chars with a single `-`
3. strip leading/trailing dashes
4. cap at 80 characters

So `"Do Global Forest Datasets Map Mangroves? A Mumbai Study"` becomes `do-global-forest-datasets-map-mangroves-a-mumbai-study`.

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app**.
4. Select your repo, branch `main`, and file `streamlit_app.py`.
5. Click **Deploy**.

Push to update — Streamlit Cloud auto-redeploys on every commit to `main`.

## Publish a new version to PyPI

```bash
# 1. Bump version in pyproject.toml
# 2. Build sdist + wheel
python -m pip install --upgrade build twine
python -m build
# 3. Upload (requires PyPI account + API token)
python -m twine upload dist/*
# 4. Tag the release in git
git tag v1.0.1 && git push --tags
```

## Project Structure

```
nhsjs-tools/
├── streamlit_app.py              # Web app — 3 tabs
├── nhsjs_convert.py              # LaTeX → Online converter library
├── nhsjs_standard_to_online.py   # Standard .docx → Online .docx library
├── nhsjs_revision_builder.py     # RaR v2 revision.md → 5 outputs
├── nhsjs_audit.py                # Phase 6 self-audit (10 checks)
├── tests/
│   ├── smoke.py                  # End-to-end smoke tests
│   └── fixtures/
│       ├── sample_latex.zip
│       ├── sample_standard.docx
│       ├── revision_sample.md
│       └── revision_log_sample.md
├── pyproject.toml                # PyPI metadata + library deps
├── requirements.txt              # Streamlit app deps (superset of pyproject)
├── LICENSE                       # MIT
└── README.md
```

## Future work

- Per-renderer review cards (in-chat preview of `revision.md` markers).
- Reference Hunter integration (currently the RaR v2 agent runs this in a separate chat).
- Multi-file revision support (currently one revision.md → one manuscript).
