"""
Smoke tests for nhsjs-tools.

Run from the repo root:
    python tests/smoke.py

What this exercises:
  1. LaTeX → Online conversion on tests/fixtures/sample_latex.zip
  2. Standard → Online conversion on tests/fixtures/sample_standard.docx
  3. Revision builder on tests/fixtures/revision_sample.md (added later
     once nhsjs_revision_builder.py exists)

Outputs go to a fresh tempdir per run, printed at the start.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def smoke_latex_to_online(out_dir: Path) -> None:
    """Run LaTeX → Online on the sample zip; assert non-empty docx with content."""
    from nhsjs_convert import convert_latex_to_online

    src = FIXTURES / "sample_latex.zip"
    assert src.exists(), f"missing fixture: {src}"

    out_path = out_dir / "latex_to_online.docx"
    convert_latex_to_online(str(src), str(out_path))

    size = out_path.stat().st_size
    assert size > 5000, f"latex output suspiciously small: {size} bytes"

    from docx import Document
    doc = Document(str(out_path))
    full_text = "\n".join(p.text for p in doc.paragraphs)
    assert "References" in full_text, "latex output missing References heading"
    assert "((" in full_text, "latex output missing any (( online citation"
    print(f"  PASS  latex_to_online    {size:>8} bytes, "
          f"{len(doc.paragraphs)} paras")


def smoke_standard_to_online(out_dir: Path) -> None:
    """Run Standard → Online on the cricket docx; assert citations were converted."""
    from nhsjs_standard_to_online import convert_standard_to_online

    src = FIXTURES / "sample_standard.docx"
    assert src.exists(), f"missing fixture: {src}"

    out_path = out_dir / "standard_to_online.docx"
    convert_standard_to_online(str(src), str(out_path))

    size = out_path.stat().st_size
    assert size > 5000, f"standard output suspiciously small: {size} bytes"

    from docx import Document
    doc = Document(str(out_path))
    full_text = "\n".join(p.text for p in doc.paragraphs)
    assert "((" in full_text, (
        "standard output has no (( citation brackets — Standard→Online "
        "did not convert any superscript runs"
    )
    print(f"  PASS  standard_to_online {size:>8} bytes, "
          f"{len(doc.paragraphs)} paras")


def smoke_revision_builder(out_dir: Path) -> None:
    """Run the revision builder on the sample revision.md if the module exists."""
    try:
        import nhsjs_revision_builder as rb
    except ImportError:
        print("  SKIP  revision_builder   (module not built yet)")
        return

    revision_md = FIXTURES / "revision_sample.md"
    revision_log = FIXTURES / "revision_log_sample.md"
    sub = out_dir / "build_all"
    sub.mkdir(parents=True, exist_ok=True)

    result = rb.build_all(str(revision_md), str(revision_log), str(sub))

    expected_keys = {
        "standard_tracked", "standard_clean", "online",
        "response_letter", "student_handoff",
    }
    assert expected_keys <= set(result.keys()), (
        f"build_all missing outputs: {expected_keys - set(result.keys())}"
    )
    for kind, path in result.items():
        p = Path(path)
        assert p.exists(), f"{kind} output missing: {p}"
        assert p.stat().st_size > 100, f"{kind} suspiciously small: {p}"

    # Verify OOXML superscript actually present in the tracked docx
    from docx import Document
    from docx.oxml.ns import qn

    tracked = Document(result["standard_tracked"])
    found_superscript = False
    for p in tracked.paragraphs:
        for r in p._p.findall(qn("w:r")):
            rPr = r.find(qn("w:rPr"))
            if rPr is not None:
                va = rPr.find(qn("w:vertAlign"))
                if va is not None and va.get(qn("w:val")) == "superscript":
                    found_superscript = True
                    break
        if found_superscript:
            break
    assert found_superscript, (
        "Standard-Tracked has no OOXML superscript runs — citation handling broken"
    )

    print(f"  PASS  revision_builder    5 outputs, real OOXML superscript present")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="nhsjs_smoke_") as tmp:
        out = Path(tmp)
        print(f"Smoke tests — output dir: {out}")
        smoke_latex_to_online(out)
        smoke_standard_to_online(out)
        smoke_revision_builder(out)
    print("All smoke checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
