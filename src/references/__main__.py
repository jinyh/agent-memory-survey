from __future__ import annotations

from pathlib import Path

from .indexing import (
    build_reference_library,
    download_open_deepresearch_papers,
    extract_deepresearch_entries,
    write_reference_indexes,
)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    output_dir = repo_root / "docs/references"
    report_path = repo_root / "ref/DeepResearch/多模态Agent空间推理记忆研究.md"

    deepresearch_entries = extract_deepresearch_entries(report_path, repo_root)
    deepresearch_entries = download_open_deepresearch_papers(
        repo_root, deepresearch_entries
    )
    library = build_reference_library(repo_root)
    write_reference_indexes(output_dir, library, deepresearch_entries)


if __name__ == "__main__":
    main()
