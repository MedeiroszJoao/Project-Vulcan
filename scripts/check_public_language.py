"""Fail on Portuguese phrases in English-facing project sources.

Historical binary files, source patches, external links and frozen JSONs
are excluded deliberately. This is a documentation quality check, not OCR.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {
    "evidence/adversarial_received/changes.patch",
}
EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "node_modules"}
EXTENSIONS = {".md", ".py", ".mmd", ".html", ".yml"}
# Match distinctive Portuguese terms, not surnames, acronyms, or math symbols.
LANGUAGE_CUES = re.compile(
    r"\b(?:não|cenários|consequência|aguardar|realocar|histórico|"
    r"probabilidade|hipótese|correção|observação|evidência|"
    r"revisão|lançamento|publicação|relatório|resultados|"
    r"segurança|congelamento|independente|verificações)\b",
    re.IGNORECASE,
)


def audit() -> int:
    violations = []
    checked = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in EXCLUDE:
            continue
        checked += 1
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if LANGUAGE_CUES.search(line):
                violations.append(f"{rel}:{number}: {line[:125]}")
    if violations:
        raise SystemExit(
            "Portuguese prose found in English-facing files:\n"
            + "\n".join(violations)
        )
    print(f"PASS: no Portuguese prose cues across {checked} source/document files")
    return checked


if __name__ == "__main__":
    audit()
