# NHSJS Conversion Tools

A web app that converts LaTeX and Word manuscripts into the NHSJS online-publication citation format.

## Tools

**LaTeX → Online Format**
Upload an Overleaf `.zip`, a folder, or a `.tex` file. The tool strips LaTeX markup, embeds figures, auto-numbers figures/tables, resolves cross-references, and replaces all citations with the NHSJS `((full citation))` format. Outputs a `.docx`.

**Standard → Online Format**
Upload an NHSJS Word document with superscript numbered citations. The tool finds the References section, parses it, and replaces every superscript citation with the corresponding `((full citation))`. Optionally upload a `.txt` file of references if they aren't in the document itself.

## Quick Start

```bash
git clone https://github.com/YOUR_USER/nhsjs-tools.git
cd nhsjs-tools
pip install -r requirements.txt
python app.py
```

Open [http://localhost:8000](http://localhost:8000).

## Project Structure

```
nhsjs-tools/
├── app.py                  # FastAPI server
├── nhsjs_convert.py        # LaTeX → online .docx converter
├── nhsjs_converter.py      # Standard .docx → online .docx converter
├── templates/
│   └── index.html          # Frontend
├── requirements.txt
├── Dockerfile
└── README.md
```

## Deployment Options

### Option A: Railway / Render (easiest)

1. Push this repo to GitHub.
2. Connect it to [Railway](https://railway.app) or [Render](https://render.com).
3. Set the start command to `uvicorn app:app --host 0.0.0.0 --port $PORT`.
4. Deploy. Done.

### Option B: Docker

```bash
docker build -t nhsjs-tools .
docker run -p 8000:8000 nhsjs-tools
```

### Option C: Any server with Python

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Updating the Converters

Edit `nhsjs_convert.py` or `nhsjs_converter.py` directly, then restart the server (or push to trigger a redeploy). The web app calls these scripts at runtime, so changes take effect immediately on restart.

## Requirements

- Python 3.10+
- See `requirements.txt`