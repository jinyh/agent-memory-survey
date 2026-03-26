from __future__ import annotations

import json
from pathlib import Path

from src.references import (
    build_reference_library,
    extract_deepresearch_entries,
    resolve_download_url,
    write_reference_indexes,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_build_reference_library_scans_local_sources():
    library = build_reference_library(REPO_ROOT)

    assert len(library.papers) >= 4
    assert len(library.blogs) >= 5
    assert all(record.source_type == "paper" for record in library.papers)
    assert all(record.source_type == "blog" for record in library.blogs)
    assert all(record.file_path.startswith("ref/") for record in library.papers)
    assert all(record.file_path.startswith("ref/blog/") for record in library.blogs)


def test_quality_assessment_is_populated_for_papers_and_blogs():
    library = build_reference_library(REPO_ROOT)

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


def test_build_reference_library_enriches_downloaded_paper_titles():
    library = build_reference_library(REPO_ROOT)

    assert any(
        record.title.startswith("TeleMem:")
        for record in library.papers
    )
    assert any(
        record.title.startswith("MemoryArena:")
        for record in library.papers
    )
    assert any(
        "MemoryAgentBench" in record.title
        for record in library.papers
    )
    assert any(
        record.title.startswith("AMA-Bench:")
        for record in library.papers
    )
    assert any(
        record.title.startswith("Memoria:")
        for record in library.papers
    )
    assert any(
        record.title.startswith("MemSkill:")
        for record in library.papers
    )
    assert any(
        record.title.startswith("BMAM:")
        for record in library.papers
    )


def test_extract_deepresearch_entries_tracks_download_status():
    report_path = REPO_ROOT / "ref/DeepResearch/多模态Agent空间推理记忆研究.md"

    entries = extract_deepresearch_entries(report_path, REPO_ROOT)

    assert len(entries) >= 20
    telemem = next(
        entry for entry in entries if "TeleMem" in entry.title
    )
    assert telemem.category in {"paper", "dataset", "benchmark", "other"}
    assert telemem.status in {"downloaded", "missing"}
    assert telemem.source_url


def test_write_reference_indexes_creates_expected_outputs(tmp_path: Path):
    library = build_reference_library(REPO_ROOT)
    entries = extract_deepresearch_entries(
        REPO_ROOT / "ref/DeepResearch/多模态Agent空间推理记忆研究.md",
        REPO_ROOT,
    )

    write_reference_indexes(tmp_path, library, entries)

    papers_index = tmp_path / "papers-index.json"
    blogs_index = tmp_path / "blogs-index.json"
    deepresearch_index = tmp_path / "deepresearch-ingestion.json"

    assert papers_index.exists()
    assert blogs_index.exists()
    assert deepresearch_index.exists()

    papers_payload = json.loads(papers_index.read_text())
    blogs_payload = json.loads(blogs_index.read_text())
    deepresearch_payload = json.loads(deepresearch_index.read_text())

    assert papers_payload["count"] >= 4
    assert blogs_payload["count"] >= 5
    assert deepresearch_payload["count"] >= 20


def test_resolve_download_url_supports_arxiv_and_openreview():
    arxiv_url = "https://arxiv.org/html/2601.06037v1"
    openreview_url = "https://openreview.net/forum?id=PMz29A7Muq"

    assert resolve_download_url(arxiv_url) == "https://arxiv.org/pdf/2601.06037.pdf"
    assert (
        resolve_download_url(openreview_url)
        == "https://openreview.net/pdf?id=PMz29A7Muq"
    )
