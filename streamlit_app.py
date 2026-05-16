"""
NHSJS Conversion Tools — Streamlit App
Run locally: streamlit run streamlit_app.py
"""

import io
import tempfile
import shutil
import zipfile
from pathlib import Path

import streamlit as st

from nhsjs_convert import convert_latex_to_online
from nhsjs_standard_to_online import convert_standard_to_online
from nhsjs_revision_builder import build_all, BuilderError
from nhsjs_audit import audit_revision, summary_counts

st.set_page_config(page_title="NHSJS Conversion Tools", layout="wide")

st.title("NHSJS Conversion Tools")
st.caption("Convert manuscripts to NHSJS online-publication citation format")

tab1, tab2, tab3 = st.tabs([
    "LaTeX → Online Format",
    "Standard → Online Format",
    "Revision → All Outputs",
])

# ── Tab 1: LaTeX → Online ──────────────────────────────────────────────────

with tab1:
    st.markdown(
        "Upload your Overleaf **.zip** or **.tex** file. "
        "Returns a .docx with inline ((citations)), embedded figures, "
        "and numbered captions."
    )
    uploaded = st.file_uploader(
        "Choose a .zip or .tex file",
        type=["zip", "tex"],
        key="latex_upload",
    )

    if uploaded and st.button("Convert", key="latex_btn"):
        work = Path(tempfile.mkdtemp(prefix="nhsjs_st_"))
        try:
            with st.spinner("Converting…"):
                suffix = Path(uploaded.name).suffix.lower()
                input_path = work / f"input{suffix}"
                input_path.write_bytes(uploaded.getvalue())

                output_path = work / "output.docx"
                convert_latex_to_online(input_path, output_path)

                result_bytes = output_path.read_bytes()
                out_name = Path(uploaded.name).stem + "_nhsjs_online.docx"

            st.success("Done!")
            st.download_button(
                label="Download .docx",
                data=result_bytes,
                file_name=out_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        except Exception as e:
            st.error(f"Conversion failed: {e}")
        finally:
            shutil.rmtree(work, ignore_errors=True)


# ── Tab 2: Standard → Online ──────────────────────────────────────────────

with tab2:
    st.markdown(
        "Upload an NHSJS **.docx** with superscript numbered citations. "
        "Returns a .docx with inline ((citations))."
    )
    uploaded_doc = st.file_uploader(
        "Choose a .docx file",
        type=["docx"],
        key="std_upload",
    )
    uploaded_refs = st.file_uploader(
        "Optional: references .txt file",
        type=["txt"],
        key="refs_upload",
    )

    if uploaded_doc and st.button("Convert", key="std_btn"):
        work = Path(tempfile.mkdtemp(prefix="nhsjs_st_"))
        try:
            with st.spinner("Converting…"):
                input_path = work / uploaded_doc.name
                input_path.write_bytes(uploaded_doc.getvalue())

                refs_path = None
                if uploaded_refs:
                    refs_path = work / uploaded_refs.name
                    refs_path.write_bytes(uploaded_refs.getvalue())

                output_path = work / "output.docx"
                convert_standard_to_online(
                    str(input_path),
                    str(output_path),
                    refs_txt=str(refs_path) if refs_path else None,
                )

                result_bytes = output_path.read_bytes()
                out_name = Path(uploaded_doc.name).stem + "_online.docx"

            st.success("Done!")
            st.download_button(
                label="Download .docx",
                data=result_bytes,
                file_name=out_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        except Exception as e:
            st.error(f"Conversion failed: {e}")
        finally:
            shutil.rmtree(work, ignore_errors=True)


# ── Tab 3: Revision → All Outputs ─────────────────────────────────────────
#
# Consumes a `revision.md` (the source-of-truth artefact emitted by the
# Revise-After-Review v2 agent) and produces all 5 NHSJS submission
# files in a single downloadable zip.
#
# This is the bridge that makes Sonnet-online mode work for users without
# file tools: paste the bot's emitted revision.md block, optionally paste
# the matching revision-log.md, click Build All, download the zip.

with tab3:
    st.markdown(
        "Paste the `revision.md` produced by the **Revise-After-Review v2** "
        "agent. The builder produces all 5 submission files — "
        "Standard-Tracked, Standard-Clean, Online, Response-Letter, "
        "Student-Handoff — plus a `FILES.md` manifest, packaged as a zip."
    )
    st.markdown(
        "The `revision-log.md` is optional. When provided it drives the "
        "point-by-point reviewer response letter and the student handoff "
        "themes; when omitted, both files emit placeholder shells you can "
        "fill in by hand."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("revision.md (required)")
        rev_file = st.file_uploader(
            "Upload revision.md",
            type=["md", "txt"],
            key="rev_upload",
            label_visibility="visible",
        )
        rev_paste = st.text_area(
            "…or paste the contents below",
            key="rev_paste",
            height=240,
            placeholder=(
                "---\n"
                "student_name: \"Aaryamann Goenka\"\n"
                "manuscript_title: \"Your Manuscript Title\"\n"
                "reviewer_decision_date: \"2026-04-15\"\n"
                "target_submit_date: \"2026-04-22\"\n"
                "---\n\n"
                "# Title\n\n"
                "## Abstract\n\n"
                "Your abstract with {{+inserted+}} text and [[CITE:1]] citations.\n"
            ),
        )

    with col2:
        st.subheader("revision-log.md (optional)")
        log_file = st.file_uploader(
            "Upload revision-log.md",
            type=["md", "txt"],
            key="log_upload",
        )
        log_paste = st.text_area(
            "…or paste the contents below",
            key="log_paste",
            height=240,
            placeholder=(
                "## Approved Actions\n\n"
                "### Action A1 — Short summary\n"
                "Comments: R1.1\n"
                "Section: Abstract\n"
                "Classification: Accept in full\n"
                "Priority: NON-NEGOTIABLE\n"
                "Effort: 15 min\n"
                "Change summary: What was changed.\n"
                "Location: Abstract, paragraph 1\n"
                "Status: APPLIED\n"
                "Reviewer R1.1: \"verbatim quote from PDF\"\n"
            ),
        )

    st.divider()
    if st.button("Build All", key="rev_btn", type="primary"):
        rev_md = (
            rev_file.getvalue().decode("utf-8")
            if rev_file else rev_paste
        )
        log_md = (
            log_file.getvalue().decode("utf-8")
            if log_file else log_paste
        )

        if not rev_md.strip():
            st.error("revision.md is required — upload a file or paste the contents.")
            st.stop()

        work = Path(tempfile.mkdtemp(prefix="nhsjs_rev_"))
        try:
            with st.spinner("Building outputs…"):
                rev_path = work / "revision.md"
                rev_path.write_text(rev_md, encoding="utf-8")
                log_path = None
                if log_md.strip():
                    log_path = work / "revision-log.md"
                    log_path.write_text(log_md, encoding="utf-8")

                out_dir = work / "submit"
                result = build_all(
                    str(rev_path),
                    str(log_path) if log_path else None,
                    str(out_dir),
                )

                # Audit
                audit_results = audit_revision(
                    str(rev_path), str(out_dir),
                    log_path=str(log_path) if log_path else None,
                )
                counts = summary_counts(audit_results)

                # Zip everything
                zip_bytes = io.BytesIO()
                with zipfile.ZipFile(zip_bytes, "w", zipfile.ZIP_DEFLATED) as zf:
                    for p in out_dir.glob("*"):
                        if p.is_file():
                            zf.write(p, arcname=p.name)
                zip_bytes.seek(0)

            st.success(
                f"Build complete — 5 outputs + FILES.md. "
                f"Audit: {counts['PASS']} pass, "
                f"{counts['WARN']} warn, {counts['FAIL']} fail."
            )

            st.download_button(
                label="Download submit.zip",
                data=zip_bytes.getvalue(),
                file_name="submit.zip",
                mime="application/zip",
                type="primary",
            )

            # Output summary table
            st.subheader("Files produced")
            rows = []
            for kind, path in result.items():
                p = Path(path)
                rows.append({
                    "Kind": kind.replace("_", " "),
                    "Filename": p.name,
                    "Size (KB)": f"{p.stat().st_size / 1024:.1f}",
                })
            st.dataframe(rows, hide_index=True, use_container_width=True)

            # Audit diagnostics
            st.subheader("Self-audit (Phase 6 checks)")
            status_emoji = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
            audit_rows = [
                {
                    "": status_emoji.get(r.status, "?"),
                    "Check": r.name,
                    "Status": r.status,
                    "Detail": r.detail,
                }
                for r in audit_results
            ]
            st.dataframe(audit_rows, hide_index=True, use_container_width=True)

            if counts["FAIL"] > 0:
                st.warning(
                    f"{counts['FAIL']} audit check(s) failed. Review the table "
                    f"above before submitting — these are usually fixable in "
                    f"`revision.md` and re-running Build All."
                )

        except BuilderError as exc:
            line_str = f" (line {exc.line})" if exc.line else ""
            st.error(f"**{exc.kind}**{line_str}: {exc}")
            st.info(
                "Build aborted in strict mode. Fix the issue above in "
                "`revision.md` and click Build All again."
            )
        except Exception as exc:
            st.error(f"Unexpected build failure: {exc}")
            raise
        finally:
            shutil.rmtree(work, ignore_errors=True)