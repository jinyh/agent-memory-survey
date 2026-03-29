from __future__ import annotations

import re
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    docs = [
        repo_root / "README.md",
        repo_root / "docs" / "plans" / "README.md",
        repo_root / "docs" / "references.md",
        repo_root / "docs" / "survey" / "README.md",
        repo_root / "docs" / "survey" / "survey-map.md",
        repo_root / "AGENTS.md",
        repo_root / "CLAUDE.md",
    ]

    broken: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for doc in docs:
        if not doc.exists():
            broken.append(f"missing doc: {doc.relative_to(repo_root)}")
            continue
        base = doc.parent
        text = doc.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            anchor = target.split("#", 1)[0]
            if not anchor:
                continue
            candidate = (base / anchor).resolve()
            if not candidate.exists():
                broken.append(f"{doc.relative_to(repo_root)} -> {target}")

    if broken:
        print("Broken docs links:")
        for item in broken:
            print(f"- {item}")
        return 1

    print("Docs links ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
