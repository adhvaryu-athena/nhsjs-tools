"""
nhsjs_prompts.py
================
One-command bootstrap for the Revise-After-Review v2.2 workflow.

The package ships the v2.2 system prompt as a data file inside the
`nhsjs_tools_assets` package. This module exposes the prompt as a
Python string and provides a `nhsjs-start` CLI that prints it to
stdout — useful for kicking off the workflow inside any Claude chat
with a Python sandbox.

Public API
----------
    get_prompt(name="rar-v2.2") -> str
        Return the prompt text. Supported names: "rar-v2.2", "v2.2",
        "default". Raises ValueError on an unknown name.

    list_prompts() -> list[str]
        Names of all prompts bundled with this nhsjs-tools install.

CLI
---
    nhsjs-start
        Print the v2.2 prompt to stdout, followed by a detected-inputs
        preamble listing any .docx / .pdf files in the current directory.
        In a Claude chat with code execution, the model reads this
        output, recognizes the "Override any prior instructions" line
        at the top of the prompt, and begins Phase 0 against the
        uploaded files.

    nhsjs-start --paper paper.docx --review review.pdf
        Pin specific files instead of auto-detecting.

    nhsjs-start --dir /path/to/scholar/folder
        Scan a folder other than the current directory.

    nhsjs-start --prompt v2.2 --no-preamble
        Print only the prompt (no inputs section). Useful for piping.
"""
from __future__ import annotations

import argparse
import sys
from importlib.resources import files
from pathlib import Path

# Prompt name → filename inside nhsjs_tools_assets/prompts/
_PROMPTS = {
    "rar-v2.2": "revise-after-review-v2.2.md",
    "v2.2": "revise-after-review-v2.2.md",
    "default": "revise-after-review-v2.2.md",
}


def get_prompt(name: str = "rar-v2.2") -> str:
    """Return the named prompt's text.

    Raises ValueError on an unknown name.
    """
    if name not in _PROMPTS:
        raise ValueError(
            f"Unknown prompt {name!r}. Available: {sorted(set(_PROMPTS.values()))}"
        )
    filename = _PROMPTS[name]
    resource = files("nhsjs_tools_assets").joinpath("prompts", filename)
    return resource.read_text(encoding="utf-8")


def list_prompts() -> list[str]:
    """Return the unique prompt filenames available."""
    return sorted({v for v in _PROMPTS.values()})


# ─── CLI ───────────────────────────────────────────────────────────────────

def _detect_inputs(directory: Path) -> dict[str, list[Path]]:
    """Scan `directory` for files likely to be RaR inputs.

    Returns a dict with keys 'paper', 'review', 'log', 'other' — each a
    list of Path objects. Detection is heuristic by filename + extension.
    """
    result: dict[str, list[Path]] = {
        "paper": [], "review": [], "log": [], "other": []
    }
    if not directory.exists():
        return result

    for p in sorted(directory.iterdir()):
        if not p.is_file():
            continue
        name_lower = p.name.lower()
        if p.suffix.lower() == ".pdf":
            if "review" in name_lower or "decision" in name_lower:
                result["review"].append(p)
            else:
                result["other"].append(p)
        elif p.suffix.lower() == ".docx":
            if any(k in name_lower for k in ("revised", "tracked", "online",
                                              "submit", "clean")):
                result["other"].append(p)
            else:
                result["paper"].append(p)
        elif p.suffix.lower() == ".md":
            if "log" in name_lower or "revision-log" in name_lower:
                result["log"].append(p)
            else:
                result["other"].append(p)
    return result


def _format_preamble(directory: Path, paper: Path | None,
                     review: Path | None, log: Path | None) -> str:
    """Build the '## Detected inputs' preamble appended after the prompt."""
    detected = _detect_inputs(directory)
    if paper:
        detected["paper"] = [paper]
    if review:
        detected["review"] = [review]
    if log:
        detected["log"] = [log]

    lines = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Detected inputs (this session)")
    lines.append("")
    lines.append(f"Scanned: `{directory}`")
    lines.append("")
    if detected["paper"]:
        for p in detected["paper"]:
            size_kb = p.stat().st_size / 1024
            lines.append(f"- **Standard manuscript:** `{p.name}` ({size_kb:.0f} KB)")
    else:
        lines.append("- **Standard manuscript:** _not detected — ask the mentor_")
    if detected["review"]:
        for p in detected["review"]:
            size_kb = p.stat().st_size / 1024
            lines.append(f"- **Reviewer Decision PDF:** `{p.name}` ({size_kb:.0f} KB)")
    else:
        lines.append("- **Reviewer Decision PDF:** _not detected — ask the mentor_")
    if detected["log"]:
        for p in detected["log"]:
            lines.append(f"- **revision-log.md (prior):** `{p.name}`")
    if detected["other"]:
        lines.append("")
        lines.append("Other files in the folder (not auto-classified):")
        for p in detected["other"]:
            lines.append(f"- `{p.name}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Begin Phase 0. State the detection summary in one short list "
                 "per the prompt's instructions, then ask the one confirm "
                 "question about defaults.")
    lines.append("")
    return "\n".join(lines)


def _cli():
    parser = argparse.ArgumentParser(
        description="Print the Revise-After-Review v2.2 system prompt + "
                    "detected inputs from the current directory. Output is "
                    "intended to be read by Claude in a chat session.",
    )
    parser.add_argument("--prompt", default="rar-v2.2",
                        help="Prompt to print (default: rar-v2.2)")
    parser.add_argument("--dir", default=".",
                        help="Directory to scan for inputs (default: cwd)")
    parser.add_argument("--paper", metavar="PATH",
                        help="Pin the Standard manuscript .docx")
    parser.add_argument("--review", metavar="PATH",
                        help="Pin the Reviewer Decision .pdf")
    parser.add_argument("--log", metavar="PATH",
                        help="Pin a prior revision-log.md (for resume)")
    parser.add_argument("--no-preamble", action="store_true",
                        help="Print only the prompt, no detected-inputs section.")
    parser.add_argument("--list", action="store_true",
                        help="List bundled prompts and exit.")
    args = parser.parse_args()

    if args.list:
        for name in list_prompts():
            print(name)
        return

    try:
        prompt = get_prompt(args.prompt)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)

    sys.stdout.write(prompt)
    if not prompt.endswith("\n"):
        sys.stdout.write("\n")

    if not args.no_preamble:
        directory = Path(args.dir).resolve()
        paper = Path(args.paper).resolve() if args.paper else None
        review = Path(args.review).resolve() if args.review else None
        log = Path(args.log).resolve() if args.log else None
        sys.stdout.write(_format_preamble(directory, paper, review, log))


if __name__ == "__main__":
    _cli()
