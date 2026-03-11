# NHSJS Conversion Tools

A web app that converts LaTeX and Word manuscripts into the NHSJS online-publication citation format.

## Tools

**LaTeX → Online Format**
Upload an Overleaf `.zip` or `.tex` file. The tool strips LaTeX markup, embeds figures, auto-numbers figures/tables, resolves cross-references, and replaces all citations with the NHSJS `((full citation))` format. Outputs a `.docx`.

**Standard → Online Format**
Upload an NHSJS Word document with superscript numbered citations. The tool finds the References section, parses it, and replaces every superscript citation with the corresponding `((full citation))`. Optionally upload a `.txt` file of references if they aren't in the document itself.

## Quick Start (local)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Opens at [http://localhost:8501](http://localhost:8501).

## Deploy to Streamlit Community Cloud (free)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app**.
4. Select your repo, branch `main`, and file `streamlit_app.py`.
5. Click **Deploy**.

Your app is live. To update, just push to GitHub — it redeploys automatically.

## Project Structure

```
nhsjs-tools/
├── streamlit_app.py        # Streamlit web app
├── nhsjs_convert.py        # LaTeX → online .docx converter
├── nhsjs_converter.py      # Standard .docx → online .docx converter
├── requirements.txt
└── README.md
```

## Updating the Converters

Edit `nhsjs_convert.py` or `nhsjs_converter.py`, push to GitHub. Streamlit Community Cloud auto-redeploys on every commit.