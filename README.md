# NHSJS Conversion Tools

Library + Streamlit web app for converting and revising NHSJS manuscripts. v2.0.0 adds a v2.2 patch-application engine that's the build half of the **Revise-After-Review v2.2** workflow.

## What's in the box

**LaTeX → Online Format.** Overleaf `.zip` or `.tex` → NHSJS Online `.docx` with `((full citation))` brackets, embedded figures, auto-numbered captions, resolved cross-references.

**Standard → Online Format.** NHSJS Standard `.docx` (real OOXML superscript citations + a References section) → Online `.docx` with citations expanded to `((full citation))`.

**Revision → All Outputs.** A v2.2 `revision.md` (sequence of anchored patches) + the original Standard `.docx` → all 5 NHSJS submission files plus a self-audit report:
- `{title}-Standard-Tracked.docx` — real Word tracked changes (`<w:ins>` / `<w:del>` with author attribution)
- `{title}-Standard-Clean.docx` — derived from Tracked by accepting all changes
- `{title}-Online.docx` — derived from Clean via the Standard→Online converter
- `Response-Letter.docx` — point-by-point reviewer response generated from `revision-log.md`
- `Student-Handoff.md` — 4-part student sign-off message

## Three ways to run it

### 1. Streamlit web app (mentors with a browser)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Opens at [http://localhost:8501](http://localhost:8501). Deployed live on Streamlit Community Cloud — push to `main` and it redeploys.

### 2. Local Python (Cowork bots in a scholar's review folder)

```bash
pip install nhsjs-tools
```

```python
from nhsjs_revision_builder import build_all
from nhsjs_audit import audit_revision

result = build_all("revision.md", "original.docx", "revision-log.md", "submit/")
# result = {"standard_tracked": "...", "standard_clean": "...", ...}

audit = audit_revision("revision.md", "original.docx", "submit/", log_path="revision-log.md")
```

Console scripts available after install:

```bash
nhsjs-start                                                         # print the v2.2 system prompt + auto-detected inputs
nhsjs-build-revision revision.md original.docx submit/ --log revision-log.md
nhsjs-audit-revision revision.md original.docx submit/ --log revision-log.md
nhsjs-latex-to-online project.zip output.docx
nhsjs-standard-to-online manuscript.docx output.docx
```

Library deps: `python-docx`, `Pillow`, `lxml`, `PyYAML`. **No Streamlit** — the package is safe to import from any Python environment.

### 3. One-command bootstrap inside any Claude chat (recommended for new sessions)

The package ships the v2.2 system prompt as bundled data, accessed via a
`nhsjs-start` CLI. Drop your paper + reviewer PDF into a Claude chat with
code execution (Claude.ai analysis tool, Cowork, or Claude Code), then:

```bash
!pip install nhsjs-tools -q
!nhsjs-start
```

`nhsjs-start` prints the v2.2 system prompt to stdout, followed by a
"## Detected inputs" section listing the .docx and .pdf files it found in
the current directory. Claude reads the output, recognizes the "Override
any prior instructions" line at the top, and starts Phase 0 — Triage,
Asset Freeze, patches, build, audit — all in the same chat.

Override the auto-detection if needed:

```bash
nhsjs-start --paper paper.docx --review review.pdf
nhsjs-start --dir /path/to/scholar/folder
nhsjs-start --list           # list bundled prompt versions
nhsjs-start --no-preamble    # prompt only, no inputs section
```

The prompt and the engine ship together, so an `nhsjs-tools` version
upgrade is also a prompt upgrade — they can't drift out of sync.

### 4. Claude.ai analysis tool / sandbox path (direct, no bootstrap)

If you already have a `revision.md` (e.g., produced earlier in another chat) and just want to build the outputs:

1. Upload `original.docx` + `revision.md` (+ optional `revision-log.md`) to the chat.
2. Ask Claude to run:
   ```python
   !pip install nhsjs-tools -q
   from nhsjs_revision_builder import build_all
   result = build_all("revision.md", "original.docx", "revision-log.md", "submit/")
   ```
3. Claude offers each output file in `submit/` as a download.

## v2.2 patch model — what's in `revision.md`

YAML frontmatter (`student_name`, `manuscript_title` required) followed by a sequence of `## P{N}` patch blocks. Each block has an `OP:` field naming one of 11 operations + 1 audit flag:

```
## P1
OP: FIND_REPLACE
FIND: "original sentence verbatim from the docx"
REPLACE: "revised sentence with [[CITE:23]] citation marker"
```

The 11 ops:

| Op | Use |
|---|---|
| `FIND_REPLACE` | sentence-level swap (default) |
| `APPEND_TO_PARAGRAPH` | trailing caveat sentence |
| `INSERT_AFTER_PARAGRAPH` | new paragraph between two existing |
| `INSERT_AFTER_HEADING` | new subsection at a known location |
| `REPLACE_HEADING` | section rename |
| `DELETE_PARAGRAPH` | remove a single paragraph |
| `DELETE_RANGE` | remove consecutive paragraphs |
| `REF_LIST` | reference list ADD / REPLACE_AT / RENUMBER |
| `TABLE_CELL` | single-cell table content change |
| `INSERT_TABLE` | new whole table after a heading |
| `REPLACE_ALL` | global terminology change (requires `CONFIRM_COUNT`) |

Plus `FIGURE_REGENERATED` — an audit-only flag confirming an offline figure regen happened.

Citation marker `[[CITE:17,23,24]]` resolves to real `<w:vertAlign w:val="superscript">` runs. Unit superscripts (km², m³, CO₂) stay as plain Unicode in patch text and are preserved as-is.

**Full v2.2 spec** lives in the RaR repo as `Revise-After-Review-v2.2.md` (system prompt for the agent that authors `revision.md`).

## `REF_LIST` semantics (v2.0.0 locked)

- **`ADD`** parses the leading "N." from the entry string and inserts the paragraph at position N in the reference list (between current N-1 and N+1).
- **`REPLACE_AT N`** swaps the entry at position N in place. `NEW` carries its own number prefix.
- **`RENUMBER`** takes an explicit `MAP: {old: new}`. The engine applies the map to every `[[CITE:N]]` superscript run in the body (after all text patches are applied).
- Body `[[CITE:N]]` markers in any patch use Phase-2-locked final numbers unless a `RENUMBER` patch is present to remap them.

## Strict failure mode

The build aborts with `BuilderError` and a line number on:
- Missing/malformed YAML frontmatter
- Patch anchor matching zero or >1 locations
- `REPLACE_ALL` `CONFIRM_COUNT` integer ≠ actual count
- Unresolved `[[CITE:REF_NEEDED_*]]` placeholder
- Unicode superscript glyphs `¹²³` used in citation slots (use `[[CITE:N]]`)
- Malformed `[[CITE:...]]` content (must be comma-separated digits)

`CONFIRM_COUNT: unknown` (Sonnet-online mode where the bot can't read the docx) auto-applies with the actual count surfaced in the audit report as a `WARN`. The mentor reviews the count and can edit the patch to a strict integer if needed.

## Self-audit — 13 checks (RaR v2.2 Phase 6)

`nhsjs_audit.audit_revision()` runs:

1. Patch anchor integrity — every FIND / anchor matched ≤1 paragraph
2. `REPLACE_ALL` count verification — every `CONFIRM_COUNT` matches actual
3. Citation count consistency — patches' citation usage vs `REF_LIST` adds
4. Orphan refs — `REF_LIST`-added refs are cited somewhere
5. Sequential numbering — citations appear in 1..N order
6. OOXML superscript sanity — Standard-Tracked has real superscript runs
7. Standard↔Online citation parity — Online has `((..))` blocks
8. No duplication artefacts — no `<w:ins>` content duplicating existing body text
9. No vanishing content — no paragraphs that survive Accept-All as empty
10. Author attribution — docx core property = `student_name`, not "Claude"/"Athena"/etc.
11. Anonymous Standard — no "my mentor" / "Athena Education" leaks
12. Figure regeneration flags — every `FIGURE_REGENERATED` patch's `NEW_FILE` exists
13. Response letter ↔ manuscript reality — every "Change location" line maps to a section

Result statuses: `PASS` / `WARN` / `FAIL`. The Streamlit tab renders them as a table; CLI prints with a summary line.

## Output filename rule

`{manuscript_title}` is sanitized to a filename stem:
1. lowercase
2. replace any run of non-alphanumeric chars with a single `-`
3. strip leading/trailing dashes
4. cap at 80 characters

`"Do Global Forest Datasets Map Mangroves? A Mumbai Study"` → `do-global-forest-datasets-map-mangroves-a-mumbai-study`.

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. [share.streamlit.io](https://share.streamlit.io) → **New app** → repo, branch `main`, file `streamlit_app.py` → **Deploy**.
3. Push to update — Cloud auto-redeploys.

## Publish a new version to PyPI

```bash
# 1. Bump version in pyproject.toml
# 2. Build sdist + wheel
python -m pip install --upgrade build twine
python -m build
# 3. Upload (requires PyPI API token at https://pypi.org/manage/account/token/)
python -m twine upload dist/*
#    username: __token__
#    password: <paste token starting with pypi->
# 4. Tag the release
git tag v2.0.1 && git push --tags
```

## Project structure

```
nhsjs-tools/
├── streamlit_app.py              # Web app — 3 tabs
├── nhsjs_convert.py              # LaTeX → Online (unchanged from v1)
├── nhsjs_standard_to_online.py   # Standard .docx → Online (unchanged from v1)
├── nhsjs_revision_builder.py     # v2.2 patch-application engine (v2.0.0 rewrite)
├── nhsjs_audit.py                # 13 Phase 6 checks (v2.0.0 rewrite)
├── tests/
│   ├── smoke.py                  # End-to-end smoke tests + Aaryamann regression
│   └── fixtures/
│       ├── sample_latex.zip      # Real Overleaf project for LaTeX→Online
│       ├── sample_standard.docx  # Real NHSJS Standard for Standard→Online
│       └── aaryamann/            # Real v2.0.0 regression gate
│           ├── original.docx     #   the submitted Standard
│           ├── final-tracked.docx #  human-produced revised tracked
│           └── revision.md       #   v2.2 patch list (reverse-engineered)
├── pyproject.toml
├── requirements.txt              # Streamlit app deps (library deps are in pyproject)
├── LICENSE                       # MIT
└── README.md
```

## v2.0.0 vs v1.0.0

v1.0.0 used a marker-in-full-manuscript model: `revision.md` contained the entire revised manuscript with `{{+inserted+}}` / `{{-deleted-}}` markers inline, and the builder wrote a fresh docx from scratch. That approach made long-form transcription hallucinations a constant risk.

v2.0.0 switched to a patch model: `revision.md` is a sequence of anchored patch blocks against the original docx. The builder applies patches to the live docx XML with FIND-must-match-verbatim verification, so the bot never re-emits unchanged text. This is the load-bearing anti-hallucination move in v2.2 / v2.0.0.

The Aaryamann reconstruction test (real mangroves paper, 73 patches, 21k chars revised) reconciles at 1.000 ratio against the human-produced final tracked docx. That's the regression gate for any future v2.x release.

v1.0.0 is yanked from PyPI as of v2.0.0 publish. Existing installs continue to work but new `pip install nhsjs-tools` resolves to v2.0.0.

## Future work

- Surgical FIND_REPLACE — currently the engine does paragraph-level swaps (entire paragraph wrapped in `<w:del>` + new content in `<w:ins>`). A future v2.x can split runs around the FIND boundaries so the tracked changes in Word appear at sentence granularity rather than paragraph granularity.
- Word auto-numbered reference lists — `nhsjs_standard_to_online` currently requires explicit "N." prefixes in the references section. Papers that use Word's list-numbering feature (digit only via formatting, not in text) skip the converter's parser. Fix: synthesize numbering from paragraph position when no prefixes are found.
- Streamlit `REPLACE_ALL: unknown` two-step UI — instead of auto-applying with an audit warning, show occurrence counts before applying and let the mentor confirm.
- Patch coverage stats — surface "patches covered N% of the original docx" in the audit so mentors can spot under-revision.
