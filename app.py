#!/usr/bin/env python3
"""
NHSJS Conversion Tools  —  Web Server
======================================
Two tools served from a single page:
  1. LaTeX project (.zip/.tex/.folder) → NHSJS Online Word (.docx)
  2. Standard NHSJS Word (.docx)       → NHSJS Online Word (.docx)

Run locally:
    uvicorn app:app --host 0.0.0.0 --port 8000

Deploy:
    Railway / Render — push repo, auto-detected via Procfile.
"""

import os
import uuid
import shutil
import tempfile
import threading
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

import nhsjs_convert as latex_conv
import nhsjs_standard_to_online as std_conv

app = FastAPI(title="NHSJS Conversion Tools")

# Lock for latex converter (uses global _MATH_STORE)
_latex_lock = threading.Lock()

TEMP_ROOT = Path(tempfile.gettempdir()) / "nhsjs_web"
TEMP_ROOT.mkdir(exist_ok=True)

MAX_UPLOAD_MB = 100


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_workdir() -> Path:
    d = TEMP_ROOT / uuid.uuid4().hex[:12]
    d.mkdir(parents=True, exist_ok=True)
    return d


def _cleanup(workdir: Path):
    try:
        shutil.rmtree(workdir, ignore_errors=True)
    except Exception:
        pass


def _check_size(file: UploadFile):
    """Reject files over MAX_UPLOAD_MB."""
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(413, f"File too large (max {MAX_UPLOAD_MB} MB)")


# ── Route 1: LaTeX → Online ─────────────────────────────────────────────────

@app.post("/convert/latex-to-online")
async def convert_latex(file: UploadFile = File(...)):
    _check_size(file)

    name = file.filename or "upload"
    suffix = Path(name).suffix.lower()
    if suffix not in ('.zip', '.tex'):
        raise HTTPException(400, "Please upload a .zip or .tex file.")

    workdir = _make_workdir()
    try:
        # Save upload
        input_path = workdir / name
        content = await file.read()
        input_path.write_bytes(content)

        out_stem = Path(name).stem
        output_path = workdir / f"{out_stem}_nhsjs_online.docx"

        # Run converter (thread-safe due to global _MATH_STORE)
        log = StringIO()
        with _latex_lock, redirect_stdout(log), redirect_stderr(log):
            tex, project_root = latex_conv.load_project(str(input_path))
            num_bib, key_bib = latex_conv.parse_bibliography(tex)
            tex = latex_conv.protect_math(tex)
            body = latex_conv.get_body(tex)
            blocks = latex_conv.parse_body(body)
            label_map = latex_conv.build_label_map(blocks)
            latex_conv.write_docx(
                blocks, num_bib, key_bib, label_map,
                project_root, str(output_path)
            )

        if not output_path.exists():
            raise HTTPException(500, f"Conversion failed.\n{log.getvalue()}")

        return FileResponse(
            path=str(output_path),
            filename=output_path.name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            background=None,  # keep file until response sent
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Conversion error: {e}")
    finally:
        # Schedule cleanup after a delay so FileResponse can finish
        import threading
        threading.Timer(30, _cleanup, args=[workdir]).start()


# ── Route 2: Standard → Online ──────────────────────────────────────────────

@app.post("/convert/standard-to-online")
async def convert_standard(
    file: UploadFile = File(...),
    refs: UploadFile = File(None),
):
    _check_size(file)

    name = file.filename or "upload.docx"
    if not name.lower().endswith('.docx'):
        raise HTTPException(400, "Please upload a .docx file.")

    workdir = _make_workdir()
    try:
        input_path = workdir / name
        content = await file.read()
        input_path.write_bytes(content)

        refs_path = None
        if refs and refs.filename:
            refs_path = workdir / refs.filename
            refs_content = await refs.read()
            refs_path.write_bytes(refs_content)

        out_stem = Path(name).stem
        output_path = workdir / f"{out_stem}_online.docx"

        log = StringIO()
        with redirect_stdout(log), redirect_stderr(log):
            std_conv.convert(
                str(input_path),
                str(output_path),
                refs_txt=str(refs_path) if refs_path else None,
            )

        if not output_path.exists():
            raise HTTPException(500, f"Conversion failed.\n{log.getvalue()}")

        return FileResponse(
            path=str(output_path),
            filename=output_path.name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            background=None,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Conversion error: {e}")
    finally:
        import threading
        threading.Timer(30, _cleanup, args=[workdir]).start()


# ── Frontend ─────────────────────────────────────────────────────────────────

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NHSJS Conversion Tools</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f5f5f5;
    color: #222;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .subtitle {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 2rem;
  }

  .tabs {
    display: flex;
    gap: 0;
    margin-bottom: 0;
    position: relative;
    z-index: 1;
  }

  .tab {
    padding: 0.65rem 1.5rem;
    background: #e8e8e8;
    border: 1px solid #ccc;
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
    color: #555;
    transition: background 0.15s, color 0.15s;
  }

  .tab:hover { background: #f0f0f0; }

  .tab.active {
    background: #fff;
    color: #222;
    border-bottom: 1px solid #fff;
    margin-bottom: -1px;
  }

  .card {
    background: #fff;
    border: 1px solid #ccc;
    border-radius: 0 8px 8px 8px;
    padding: 1.75rem;
    width: 100%;
    max-width: 520px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }

  .panel { display: none; }
  .panel.active { display: block; }

  .drop-zone {
    border: 2px dashed #ccc;
    border-radius: 8px;
    padding: 2rem 1rem;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    margin-bottom: 1rem;
    position: relative;
  }

  .drop-zone:hover,
  .drop-zone.dragover {
    border-color: #4a90d9;
    background: #f0f6ff;
  }

  .drop-zone input[type="file"] {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
  }

  .drop-zone .icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
  .drop-zone .label { font-size: 0.85rem; color: #666; }
  .drop-zone .filename {
    margin-top: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    color: #222;
    word-break: break-all;
  }

  .refs-row {
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: #555;
  }

  .refs-row label {
    display: block;
    margin-bottom: 0.3rem;
    font-weight: 500;
  }

  .refs-row input[type="file"] { font-size: 0.85rem; }

  .refs-filename {
    font-weight: 600;
    color: #222;
    margin-top: 0.25rem;
    font-size: 0.85rem;
  }

  button.convert {
    width: 100%;
    padding: 0.7rem;
    background: #222;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
  }

  button.convert:hover { background: #444; }
  button.convert:disabled { background: #999; cursor: not-allowed; }

  .status {
    margin-top: 0.75rem;
    font-size: 0.85rem;
    text-align: center;
    min-height: 1.2em;
  }

  .status.error { color: #c0392b; }
  .status.success { color: #27ae60; }

  .spinner {
    display: inline-block;
    width: 14px; height: 14px;
    border: 2px solid #ccc;
    border-top-color: #222;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
    vertical-align: middle;
    margin-right: 0.4rem;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  footer {
    margin-top: 2rem;
    font-size: 0.75rem;
    color: #999;
  }
</style>
</head>
<body>

<h1>NHSJS Conversion Tools</h1>
<p class="subtitle">Convert manuscripts to NHSJS online citation format</p>

<div class="tabs">
  <div class="tab active" onclick="switchTab(0)">LaTeX → Online</div>
  <div class="tab" onclick="switchTab(1)">Standard → Online</div>
</div>

<div class="card">

  <!-- Panel 1: LaTeX to Online -->
  <div class="panel active" id="panel0">
    <div class="drop-zone" id="dz0">
      <input type="file" accept=".zip,.tex" id="file0"
             onchange="fileSelected(0, this)">
      <div class="icon">📁</div>
      <div class="label">Drop a <strong>.zip</strong> or <strong>.tex</strong> file here, or click to browse</div>
      <div class="filename" id="fname0"></div>
    </div>
    <button class="convert" id="btn0" disabled onclick="doConvert(0)">Convert to Online Format</button>
    <div class="status" id="status0"></div>
  </div>

  <!-- Panel 2: Standard to Online -->
  <div class="panel" id="panel1">
    <div class="drop-zone" id="dz1">
      <input type="file" accept=".docx" id="file1"
             onchange="fileSelected(1, this)">
      <div class="icon">📄</div>
      <div class="label">Drop a <strong>.docx</strong> file here, or click to browse</div>
      <div class="filename" id="fname1"></div>
    </div>
    <div class="refs-row">
      <label>Optional: references .txt file</label>
      <input type="file" accept=".txt" id="refsFile"
             onchange="refsSelected(this)">
      <div class="refs-filename" id="refsName"></div>
    </div>
    <button class="convert" id="btn1" disabled onclick="doConvert(1)">Convert to Online Format</button>
    <div class="status" id="status1"></div>
  </div>

</div>

<footer>Conversion runs server-side · files are deleted after processing</footer>

<script>
  const endpoints = ['/convert/latex-to-online', '/convert/standard-to-online'];
  const files = [null, null];
  let refsFile = null;

  function switchTab(idx) {
    document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', i === idx));
    document.querySelectorAll('.panel').forEach((p, i) => p.classList.toggle('active', i === idx));
  }

  function fileSelected(idx, input) {
    files[idx] = input.files[0] || null;
    document.getElementById('fname' + idx).textContent = files[idx] ? files[idx].name : '';
    document.getElementById('btn' + idx).disabled = !files[idx];
    document.getElementById('status' + idx).textContent = '';
    document.getElementById('status' + idx).className = 'status';
  }

  function refsSelected(input) {
    refsFile = input.files[0] || null;
    document.getElementById('refsName').textContent = refsFile ? refsFile.name : '';
  }

  // Drag-and-drop
  document.querySelectorAll('.drop-zone').forEach((dz, i) => {
    dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('dragover'); });
    dz.addEventListener('dragleave', () => dz.classList.remove('dragover'));
    dz.addEventListener('drop', e => {
      e.preventDefault();
      dz.classList.remove('dragover');
      const input = dz.querySelector('input[type="file"]');
      input.files = e.dataTransfer.files;
      input.dispatchEvent(new Event('change'));
    });
  });

  async function doConvert(idx) {
    const f = files[idx];
    if (!f) return;
    const btn = document.getElementById('btn' + idx);
    const status = document.getElementById('status' + idx);

    btn.disabled = true;
    status.className = 'status';
    status.innerHTML = '<span class="spinner"></span> Converting…';

    const form = new FormData();
    form.append('file', f);
    if (idx === 1 && refsFile) form.append('refs', refsFile);

    try {
      const resp = await fetch(endpoints[idx], { method: 'POST', body: form });
      if (!resp.ok) {
        let msg = 'Conversion failed';
        try { const j = await resp.json(); msg = j.detail || msg; } catch {}
        throw new Error(msg);
      }
      const blob = await resp.blob();
      const cd = resp.headers.get('content-disposition') || '';
      const fnMatch = cd.match(/filename="?([^";\n]+)"?/);
      const filename = fnMatch ? fnMatch[1] : 'converted.docx';

      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      a.click();
      URL.revokeObjectURL(a.href);

      status.className = 'status success';
      status.textContent = '✓ Done — file downloaded.';
    } catch (e) {
      status.className = 'status error';
      status.textContent = '✗ ' + e.message;
    } finally {
      btn.disabled = false;
    }
  }
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE