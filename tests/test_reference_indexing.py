from __future__ import annotations

import json
from pathlib import Path

from src.references import (
    build_reference_library,
    download_open_deepresearch_papers,
    extract_deepresearch_entries,
    resolve_download_url,
    write_reference_indexes,
)


SAMPLE_PAPER_FILES = [
    "2402.17753.pdf",
    "2507.05257.pdf",
    "2512.12686.pdf",
    "2602.02474.pdf",
    "2601.20465.pdf",
]

REPO_ROOT = Path(__file__).resolve().parents[1]


def _seed_sample_papers(repo_root: Path) -> None:
    paper_dir = repo_root / "ref/paper"
    paper_dir.mkdir(parents=True, exist_ok=True)
    for filename in SAMPLE_PAPER_FILES:
        (paper_dir / filename).write_bytes(b"%PDF-1.4\n% test fixture\n")


def test_build_reference_library_scans_local_sources(tmp_path: Path):
    _seed_sample_papers(tmp_path)
    library = build_reference_library(tmp_path)

    assert len(library.papers) >= 4
    assert len(library.blogs) == 0
    assert all(record.source_type == "paper" for record in library.papers)
    assert all(record.file_path.startswith("ref/") for record in library.papers)


def test_quality_assessment_is_populated_for_papers_and_blogs(tmp_path: Path):
    _seed_sample_papers(tmp_path)
    blog_dir = tmp_path / "ref/blog"
    blog_dir.mkdir(parents=True, exist_ok=True)
    (blog_dir / "sample-blog.md").write_text(
        "Title: Sample Blog\nURL Source: https://example.com/post\nPublished Time: 2026-04-04\n\nClaude Code and Agent Memory benchmark architecture implementation.\n",
        encoding="utf-8",
    )

    library = build_reference_library(tmp_path)

    paper = library.papers[0]
    blog = library.blogs[0]

    assert paper.quality.evidence_strength
    assert paper.quality.method_rigor
    assert paper.quality.project_relevance
    assert paper.quality.recommended_use

    assert blog.quality.credibility
    assert blog.quality.verifiability
    assert blog.quality.marketing_bias_risk
    assert blog.quality.project_relevance
    assert blog.quality.recommended_use


def test_build_reference_library_enriches_downloaded_paper_titles(tmp_path: Path):
    _seed_sample_papers(tmp_path)
    library = build_reference_library(tmp_path)

    assert any(record.title.startswith("Evaluating Very Long-Term Conversational Memory") for record in library.papers)
    assert any("MemoryAgentBench" in record.title for record in library.papers)
    assert any(record.title.startswith("Memoria:") for record in library.papers)
    assert any(record.title.startswith("MemSkill:") for record in library.papers)
    assert any(record.title.startswith("BMAM:") for record in library.papers)


def test_extract_deepresearch_entries_tracks_download_status():
    report_path = next(
        (
            path
            for path in sorted((REPO_ROOT / "ref/DeepResearch").glob("*.md"))
            if "记忆研究" in path.name
        ),
        REPO_ROOT / "ref/DeepResearch/多模态Agent空间推理记忆研究.md",
    )

    entries = extract_deepresearch_entries(report_path, REPO_ROOT)

    assert len(entries) >= 20
    telemem = next(entry for entry in entries if "TeleMem" in entry.title)
    assert telemem.category in {"paper", "dataset", "benchmark", "other"}
    assert telemem.status in {"downloaded", "missing"}
    assert telemem.source_url


def test_write_reference_indexes_creates_expected_outputs(tmp_path: Path):
    fixture_root = tmp_path / "repo"
    _seed_sample_papers(fixture_root)
    blog_dir = fixture_root / "ref/blog"
    blog_dir.mkdir(parents=True, exist_ok=True)
    (blog_dir / "sample-blog.md").write_text(
        "Title: Sample Blog\nURL Source: https://example.com/post\nPublished Time: 2026-04-04\n\nbenchmark architecture implementation\n",
        encoding="utf-8",
    )

    library = build_reference_library(fixture_root)
    entries = extract_deepresearch_entries(
        next(
            (
                path
                for path in sorted((REPO_ROOT / "ref/DeepResearch").glob("*.md"))
                if "记忆研究" in path.name
            ),
            REPO_ROOT / "ref/DeepResearch/多模态Agent空间推理记忆研究.md",
        ),
        REPO_ROOT,
    )

    output_dir = tmp_path / "out"
    write_reference_indexes(output_dir, library, entries)

    papers_index = output_dir / "papers-index.json"
    blogs_index = output_dir / "blogs-index.json"
    deepresearch_index = output_dir / "deepresearch-ingestion.json"

    assert papers_index.exists()
    assert blogs_index.exists()
    assert deepresearch_index.exists()

    papers_payload = json.loads(papers_index.read_text())
    blogs_payload = json.loads(blogs_index.read_text())
    deepresearch_payload = json.loads(deepresearch_index.read_text())

    assert papers_payload["count"] >= 4
    assert blogs_payload["count"] >= 1
    assert deepresearch_payload["count"] >= 20


def test_references_package_exports_ingest_helpers():
    assert callable(extract_deepresearch_entries)
    assert callable(download_open_deepresearch_papers)


def test_resolve_download_url_supports_arxiv_and_openreview():
    arxiv_url = "https://arxiv.org/html/2601.06037v1"
    openreview_url = "https://openreview.net/forum?id=PMz29A7Muq"

    assert resolve_download_url(arxiv_url) == "https://arxiv.org/pdf/2601.06037.pdf"
    assert (
        resolve_download_url(openreview_url)
        == "https://openreview.net/pdf?id=PMz29A7Muq"
    )
