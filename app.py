#!/usr/bin/env python3
"""
NHSJS Conversion Tools — Web Server
Run with: python app.py
"""

import tempfile
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import converter modules (same directory)
import nhsjs_convert as latex_conv
import nhsjs_converter as std_conv

app = FastAPI(title="NHSJS Conversion Tools")

TEMPLATES_DIR = Path(__file__).parent / "templates"


@app.get("/", response_class=HTMLResponse)
async def index():
    return (TEMPLATES_DIR / "index.html").read_text()


@app.post("/convert/latex-to-online")
async def latex_to_online(file: UploadFile = File(...)):
    """Accept a .zip, .tex, or folder and return converted .docx."""
    work = Path(tempfile.mkdtemp(prefix="nhsjs_web_"))
    try:
        # Save upload
        suffix = Path(file.filename).suffix.lower()
        input_path = work / f"input{suffix}"
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)

        output_path = work / "output.docx"

        # If zip, extract first
        if suffix == ".zip":
            import zipfile
            extract_dir = work / "project"
            extract_dir.mkdir()
            with zipfile.ZipFile(input_path) as zf:
                zf.extractall(extract_dir)
            tex_source, project_root = latex_conv._find_main_tex(extract_dir)
        elif suffix == ".tex":
            tex_source = input_path.read_text(encoding="utf-8")
            project_root = work
        else:
            raise ValueError(f"Unsupported file type: {suffix}. Upload a .zip or .tex file.")

        # Run the full pipeline
        num_bib, key_bib = latex_conv.parse_bibliography(tex_source)
        tex_protected = latex_conv.protect_math(tex_source)
        preamble_title = latex_conv.extract_preamble_title(tex_protected)
        body = latex_conv.get_body(tex_protected)
        blocks = latex_conv.parse_body(body, preamble_title)
        label_map = latex_conv.build_label_map(blocks)
        latex_conv.write_docx(blocks, num_bib, key_bib, label_map,
                              project_root, str(output_path))

        out_name = Path(file.filename).stem + "_nhsjs_online.docx"
        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=out_name,
            background=None,
        )
    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": str(e)}, status_code=400)
    finally:
        # Cleanup is deferred so FileResponse can read the file
        import atexit
        atexit.register(lambda p=work: shutil.rmtree(p, ignore_errors=True))


@app.post("/convert/standard-to-online")
async def standard_to_online(
    file: UploadFile = File(...),
    refs: UploadFile = File(None),
):
    """Accept a standard NHSJS .docx and return online-citation .docx."""
    work = Path(tempfile.mkdtemp(prefix="nhsjs_web_"))
    try:
        input_path = work / file.filename
        with open(input_path, "wb") as f:
            f.write(await file.read())

        refs_path = None
        if refs and refs.filename:
            refs_path = work / refs.filename
            with open(refs_path, "wb") as f:
                f.write(await refs.read())

        output_path = work / "output.docx"
        std_conv.convert(
            str(input_path),
            str(output_path),
            refs_txt=str(refs_path) if refs_path else None,
        )

        out_name = Path(file.filename).stem + "_online.docx"
        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=out_name,
            background=None,
        )
    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": str(e)}, status_code=400)
    finally:
        import atexit
        atexit.register(lambda p=work: shutil.rmtree(p, ignore_errors=True))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)