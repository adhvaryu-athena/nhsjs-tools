"""
NHSJS Conversion Tools — Streamlit App
Run locally: streamlit run streamlit_app.py
"""

import tempfile
import shutil
import zipfile
from pathlib import Path

import streamlit as st

import nhsjs_convert as latex_conv
import nhsjs_standard_to_online as std_conv

st.set_page_config(page_title="NHSJS Conversion Tools", layout="centered")

st.title("NHSJS Conversion Tools")
st.caption("Convert manuscripts to NHSJS online-publication citation format")

tab1, tab2 = st.tabs(["LaTeX → Online Format", "Standard → Online Format"])

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

                if suffix == ".zip":
                    extract_dir = work / "project"
                    extract_dir.mkdir()
                    with zipfile.ZipFile(input_path) as zf:
                        zf.extractall(extract_dir)
                    tex_source, project_root = latex_conv._find_main_tex(extract_dir)
                else:
                    tex_source = input_path.read_text(encoding="utf-8")
                    project_root = work

                num_bib, key_bib = latex_conv.parse_bibliography(
                    tex_source, project_root
                )
                tex_protected = latex_conv.protect_math(tex_source)
                body = latex_conv.get_body(tex_protected)
                blocks = latex_conv.parse_body(body)
                label_map = latex_conv.build_label_map(blocks)

                output_path = work / "output.docx"
                latex_conv.write_docx(
                    blocks, num_bib, key_bib, label_map,
                    project_root, str(output_path),
                )

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
                std_conv.convert(
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