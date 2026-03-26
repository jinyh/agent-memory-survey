from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse


@dataclass
class PaperQuality:
    evidence_strength: str
    method_rigor: str
    experiment_coverage: str
    reproducibility: str
    timeliness: str
    project_relevance: str
    risk_notes: str
    recommended_use: str


@dataclass
class BlogQuality:
    credibility: str
    verifiability: str
    engineering_signal: str
    marketing_bias_risk: str
    timeliness: str
    project_relevance: str
    risk_notes: str
    recommended_use: str


@dataclass
class PaperRecord:
    source_type: str
    title: str
    year: int | None
    file_path: str
    identifier: str | None
    paper_type: str
    lifecycle_stages: list[str]
    memory_functions: list[str]
    tags: list[str]
    quality: PaperQuality


@dataclass
class BlogRecord:
    source_type: str
    title: str
    author_or_org: str | None
    published_at: str | None
    file_path: str
    source_url: str | None
    article_type: str
    lifecycle_stages: list[str]
    tags: list[str]
    quality: BlogQuality


@dataclass
class DeepResearchEntry:
    title: str
    source_url: str
    category: str
    status: str
    local_path: str | None
    reason: str


@dataclass
class ReferenceLibrary:
    papers: list[PaperRecord]
    blogs: list[BlogRecord]


def build_reference_library(repo_root: Path) -> ReferenceLibrary:
    deepresearch_map = _build_deepresearch_paper_map(
        repo_root / "ref/DeepResearch/多模态Agent空间推理记忆研究.md"
    )
    papers = _scan_papers(repo_root, deepresearch_map)
    blogs = _scan_blogs(repo_root)
    return ReferenceLibrary(papers=papers, blogs=blogs)


def extract_deepresearch_entries(
    report_path: Path, repo_root: Path
) -> list[DeepResearchEntry]:
    text = report_path.read_text(encoding="utf-8")
    entries: list[DeepResearchEntry] = []
    seen: set[str] = set()

    for title, url in re.findall(r"\d+\.\s+(.+?), accessed .*?\[(https?://[^\]]+)\]", text):
        clean_title = _strip_title(title)
        if clean_title in seen:
            continue
        seen.add(clean_title)
        category = _infer_deepresearch_category(clean_title, url)
        local_path = _find_local_pdf(repo_root, clean_title)
        status = "downloaded" if local_path else "missing"
        reason = "matched_local_pdf" if local_path else "no_open_pdf_downloaded"
        entries.append(
            DeepResearchEntry(
                title=clean_title,
                source_url=url,
                category=category,
                status=status,
                local_path=local_path,
                reason=reason,
            )
        )

    return entries


def resolve_download_url(source_url: str) -> str | None:
    if "arxiv.org/" in source_url:
        match = re.search(r"(\d{4}\.\d{5})(?:v\d+)?", source_url)
        if match:
            return f"https://arxiv.org/pdf/{match.group(1)}.pdf"
    if "openreview.net/forum" in source_url:
        query = parse_qs(urlparse(source_url).query)
        paper_id = query.get("id", [None])[0]
        if paper_id:
            return f"https://openreview.net/pdf?id={paper_id}"
    if source_url.endswith(".pdf"):
        return source_url
    return None


def download_open_deepresearch_papers(
    repo_root: Path, entries: list[DeepResearchEntry]
) -> list[DeepResearchEntry]:
    paper_dir = repo_root / "ref/paper"
    paper_dir.mkdir(parents=True, exist_ok=True)

    updated_entries: list[DeepResearchEntry] = []
    for entry in entries:
        download_url = resolve_download_url(entry.source_url)
        if entry.category != "paper" or not download_url:
            updated_entries.append(entry)
            continue

        file_basename = _download_filename(download_url, entry.title)
        target_path = paper_dir / file_basename
        if not target_path.exists():
            try:
                urllib.request.urlretrieve(download_url, target_path)
            except Exception:
                updated_entries.append(
                    DeepResearchEntry(
                        title=entry.title,
                        source_url=entry.source_url,
                        category=entry.category,
                        status="missing",
                        local_path=None,
                        reason="download_failed",
                    )
                )
                continue

        updated_entries.append(
            DeepResearchEntry(
                title=entry.title,
                source_url=entry.source_url,
                category=entry.category,
                status="downloaded",
                local_path=str(target_path.relative_to(repo_root)),
                reason="downloaded_from_open_source",
            )
        )

    return updated_entries


def write_reference_indexes(
    output_dir: Path,
    library: ReferenceLibrary,
    deepresearch_entries: list[DeepResearchEntry],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "papers-index.json", library.papers)
    _write_json(output_dir / "blogs-index.json", library.blogs)
    _write_json(output_dir / "deepresearch-ingestion.json", deepresearch_entries)

    _write_markdown(output_dir / "papers-index.md", "Papers Index", library.papers)
    _write_markdown(output_dir / "blogs-index.md", "Blogs Index", library.blogs)
    _write_markdown(
        output_dir / "deepresearch-ingestion.md",
        "DeepResearch Ingestion",
        deepresearch_entries,
    )


def _scan_papers(
    repo_root: Path, deepresearch_map: dict[str, str]
) -> list[PaperRecord]:
    candidates = sorted((repo_root / "ref/paper").glob("*.pdf"))
    if not candidates:
        candidates = sorted((repo_root / "ref").glob("*.pdf"))

    records = []
    for path in candidates:
        title = _infer_paper_title(path.stem, deepresearch_map)
        year = _infer_year(path.name)
        identifier = _infer_identifier(path.name)
        paper_type, lifecycle_stages, memory_functions, tags = _classify_paper(
            title
        )
        records.append(
            PaperRecord(
                source_type="paper",
                title=title,
                year=year,
                file_path=str(path.relative_to(repo_root)),
                identifier=identifier,
                paper_type=paper_type,
                lifecycle_stages=lifecycle_stages,
                memory_functions=memory_functions,
                tags=tags,
                quality=_assess_paper_quality(title, path.name),
            )
        )
    return records


def _scan_blogs(repo_root: Path) -> list[BlogRecord]:
    records = []
    for path in sorted((repo_root / "ref/blog").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = _extract_blog_title(text, path.stem)
        source_url = _extract_first_match(text, r"URL Source:\s*(https?://\S+)")
        published_at = _extract_first_match(text, r"Published Time:\s*(.+)")
        author_or_org = _infer_blog_author(text, source_url)
        article_type, lifecycle_stages, tags = _classify_blog(title, text, source_url)
        records.append(
            BlogRecord(
                source_type="blog",
                title=title,
                author_or_org=author_or_org,
                published_at=published_at,
                file_path=str(path.relative_to(repo_root)),
                source_url=source_url,
                article_type=article_type,
                lifecycle_stages=lifecycle_stages,
                tags=tags,
                quality=_assess_blog_quality(title, text, source_url),
            )
        )
    return records


def _assess_paper_quality(title: str, filename: str) -> PaperQuality:
    text = f"{title} {filename}".lower()
    evidence_strength = "high" if "arxiv" in text or re.search(r"\d{4}\.\d+", filename) else "medium"
    method_rigor = "high" if any(k in text for k in ("attention", "agent", "protocol", "model")) else "medium"
    experiment_coverage = "high" if any(k in text for k in ("msa", "memagent", "recursive")) else "medium"
    reproducibility = "medium"
    timeliness = "high"
    project_relevance = "high"
    risk_notes = "需结合正式出版版本与代码仓库确认最终实验设置。"
    recommended_use = "可作为综述主证据与系统设计参考。"
    return PaperQuality(
        evidence_strength=evidence_strength,
        method_rigor=method_rigor,
        experiment_coverage=experiment_coverage,
        reproducibility=reproducibility,
        timeliness=timeliness,
        project_relevance=project_relevance,
        risk_notes=risk_notes,
        recommended_use=recommended_use,
    )


def _assess_blog_quality(title: str, text: str, source_url: str | None) -> BlogQuality:
    source_text = f"{title}\n{text}\n{source_url or ''}".lower()
    credibility = "high" if any(host in source_text for host in ("oracle", "elastic", "letta")) else "medium"
    verifiability = "high" if "url source:" in text.lower() else "medium"
    engineering_signal = "high" if any(
        token in source_text for token in ("benchmark", "latency", "architecture", "implementation", "hybrid")
    ) else "medium"
    marketing_bias_risk = "high" if any(
        token in source_text for token in ("exclusive", "sota", "leader", "pricing", "product")
    ) else "medium"
    timeliness = "high"
    project_relevance = "high"
    risk_notes = "偏工程视角，涉及产品比较时需回到论文或官方文档复核。"
    recommended_use = "适合补充工程实践、系统选型与 benchmark 争议背景。"
    return BlogQuality(
        credibility=credibility,
        verifiability=verifiability,
        engineering_signal=engineering_signal,
        marketing_bias_risk=marketing_bias_risk,
        timeliness=timeliness,
        project_relevance=project_relevance,
        risk_notes=risk_notes,
        recommended_use=recommended_use,
    )


def _classify_paper(title: str) -> tuple[str, list[str], list[str], list[str]]:
    lower = title.lower()
    lifecycle = ["retrieval"]
    functions = ["semantic"]
    paper_type = "system"
    tags = ["agent-memory"]

    if any(k in lower for k in ("memoryagentbench", "memoryarena", "ama-bench", "locomo", "longmemeval", "very long-term conversational", "long-term interactive memory")):
        lifecycle = ["evaluation"]
        functions = ["episodic", "working"]
        paper_type = "benchmark"
        tags.extend(["benchmark", "agent-eval"])
    elif "recursive" in lower:
        lifecycle = ["formation", "retrieval"]
        functions = ["working"]
        paper_type = "mechanism"
        tags.extend(["recursive", "long-context"])
    elif "sparse attention" in lower or "msa" in lower:
        lifecycle = ["retrieval", "evolution"]
        functions = ["working", "semantic"]
        paper_type = "mechanism"
        tags.extend(["latent-memory", "attention"])
    elif "agentorchestra" in lower or "tea" in lower:
        lifecycle = ["evolution", "retrieval"]
        functions = ["procedural", "episodic"]
        paper_type = "framework"
        tags.extend(["multi-agent", "protocol"])
    elif "memskill" in lower:
        lifecycle = ["formation", "evolution"]
        functions = ["episodic", "procedural"]
        paper_type = "method"
        tags.extend(["memory-policy", "skill"])
    elif "memoria" in lower:
        lifecycle = ["formation", "evolution", "retrieval"]
        functions = ["episodic", "semantic"]
        paper_type = "framework"
        tags.extend(["personalization", "memory-service"])
    elif "bmam" in lower:
        lifecycle = ["evolution", "retrieval"]
        functions = ["episodic", "semantic", "procedural"]
        paper_type = "framework"
        tags.extend(["brain-inspired", "multi-agent"])
    elif "memagent" in lower:
        lifecycle = ["formation", "evolution", "retrieval"]
        functions = ["working", "episodic"]
        paper_type = "system"
        tags.extend(["rl", "long-context"])

    return paper_type, lifecycle, functions, tags


def _classify_blog(
    title: str, text: str, source_url: str | None
) -> tuple[str, list[str], list[str]]:
    lower = f"{title}\n{text}\n{source_url or ''}".lower()
    article_type = "engineering-practice"
    lifecycle = ["retrieval", "evaluation"]
    tags = ["agent-memory"]

    if "benchmark" in lower:
        article_type = "benchmark-analysis"
        lifecycle = ["evaluation"]
        tags.append("benchmark")
    elif "builder" in lower or "guide" in lower or "how to fix" in lower:
        article_type = "engineering-guide"
        lifecycle = ["formation", "retrieval"]
        tags.append("guide")
    elif "elasticsearch" in lower or "oracle" in lower:
        article_type = "architecture-practice"
        lifecycle = ["formation", "retrieval", "evolution"]
        tags.extend(["database", "memory-service"])
    elif "amnesia" in lower:
        article_type = "opinionated-essay"
        lifecycle = ["formation", "evolution"]
        tags.append("state-management")

    return article_type, lifecycle, tags


def _infer_deepresearch_category(title: str, url: str) -> str:
    lower = f"{title} {url}".lower()
    if any(token in lower for token in ("benchmark", "dataset", "teleego", "findingdory")):
        return "benchmark"
    if any(token in lower for token in ("github", "catalyzex", "youtube", "scribd", "researchgate")):
        return "other"
    return "paper"


def _find_local_pdf(repo_root: Path, title: str) -> str | None:
    normalized_title = _normalize_name(title)
    for path in sorted((repo_root / "ref/paper").glob("*.pdf")):
        if _normalize_name(path.stem) in normalized_title or normalized_title in _normalize_name(path.stem):
            return str(path.relative_to(repo_root))
    return None


def _infer_paper_title(stem: str, deepresearch_map: dict[str, str]) -> str:
    arxiv_id_match = re.search(r"(\d{4}\.\d{5})", stem)
    if arxiv_id_match and arxiv_id_match.group(1) in deepresearch_map:
        return deepresearch_map[arxiv_id_match.group(1)]
    if stem.startswith("2506.12508"):
        return "AgentOrchestra: Orchestrating Multi-Agent Intelligence with the TEA Protocol"
    if stem.startswith("2507.05257"):
        return "MemoryAgentBench: Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions"
    if stem.startswith("2507.02259"):
        return "MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"
    if stem.startswith("2512.12686"):
        return "Memoria: A Scalable Agentic Memory Framework for Personalized Conversational AI"
    if stem.startswith("2512.13564"):
        return "Memory in the Age of AI Agents: A Survey"
    if stem.startswith("2512.24601"):
        return "Recursive Language Models"
    if stem.startswith("2601.01885"):
        return "Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents"
    if stem.startswith("2601.20465"):
        return "BMAM: Brain-inspired Multi-Agent Memory Framework"
    if "MSA__" in stem:
        return "MSA: Memory Sparse Attention for Efficient End-to-End Memory Model Scaling to 100M Tokens"
    if stem.startswith("2602.02474"):
        return "MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents"
    if stem.startswith("2402.17753"):
        return "Evaluating Very Long-Term Conversational Memory of LLM Agents"
    if stem.startswith("2410.10813"):
        return "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory"
    if stem.startswith("2602.16313"):
        return "MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks"
    if stem.startswith("2602.22769"):
        return "AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications"
    if stem.startswith("2603.04740"):
        return "Memory as Ontology: A Constitutional Memory Architecture for Persistent Digital Citizens"
    return stem.replace("_", " ")


def _infer_year(filename: str) -> int | None:
    match = re.search(r"(20\d{2}|2[5-6]\d{2})", filename)
    if not match:
        return None
    raw = match.group(1)
    if raw.startswith(("25", "26")):
        return 2000 + int(raw[:2])
    return int(raw)


def _infer_identifier(filename: str) -> str | None:
    match = re.search(r"(\d{4}\.\d{5})", filename)
    return f"arXiv:{match.group(1)}" if match else None


def _extract_blog_title(text: str, fallback: str) -> str:
    title = _extract_first_match(text, r"Title:\s*(.+)")
    if title:
        return title
    first_heading = _extract_first_match(text, r"^#\s+(.+)", flags=re.MULTILINE)
    return first_heading or fallback.replace("-", " ")


def _infer_blog_author(text: str, source_url: str | None) -> str | None:
    lower = text.lower()
    if "oracle" in lower or (source_url and "oracle.com" in source_url):
        return "Oracle"
    if "elastic" in lower or (source_url and "elastic.co" in source_url):
        return "Elastic"
    if "letta" in lower or (source_url and "letta.com" in source_url):
        return "Letta"
    if source_url and "medium.com" in source_url:
        return "Medium"
    if source_url and "sellscale.com" in source_url:
        return "SellScale"
    return None


def _extract_first_match(
    text: str, pattern: str, *, flags: int = 0
) -> str | None:
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None


def _normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _strip_title(value: str) -> str:
    value = re.sub(r"^\[.*?\]\s*", "", value)
    value = value.replace("\\", "")
    value = re.sub(
        r"\s*-\s*(arXiv(?:\.org)?|OpenReview|ResearchGate|YouTube|Scribd|GitHub|CatalyzeX)$",
        "",
        value,
        flags=re.IGNORECASE,
    )
    return value.strip()


def _write_json(path: Path, records: list[object]) -> None:
    payload = {
        "count": len(records),
        "records": [asdict(record) for record in records],
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_markdown(path: Path, title: str, records: list[object]) -> None:
    lines = [f"# {title}", "", f"- count: {len(records)}", ""]
    for record in records:
        data = asdict(record)
        record_title = data.get("title", "unknown")
        lines.append(f"## {record_title}")
        for key, value in data.items():
            if key == "title":
                continue
            lines.append(f"- {key}: {value}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _download_filename(download_url: str, title: str) -> str:
    arxiv_match = re.search(r"(\d{4}\.\d{5})", download_url)
    if arxiv_match:
        return f"{arxiv_match.group(1)}.pdf"
    openreview_id = parse_qs(urlparse(download_url).query).get("id", [None])[0]
    if openreview_id:
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        return f"{slug}-{openreview_id}.pdf"
    return f"{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')}.pdf"


def download_hf_dataset(hf_repo_id: str, dest_dir: Path) -> Path:
    """从 HuggingFace 下载数据集快照到 dest_dir/{repo_name}/。"""
    from huggingface_hub import snapshot_download

    local_dir = dest_dir / hf_repo_id.split("/")[-1]
    local_dir.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id=hf_repo_id, repo_type="dataset", local_dir=str(local_dir))
    return local_dir


def download_github_files(file_urls: list[str], dest_dir: Path) -> list[Path]:
    """下载 GitHub raw 文件列表到 dest_dir/，返回成功写入的路径列表。"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for url in file_urls:
        filename = url.split("/")[-1]
        target = dest_dir / filename
        if not target.exists():
            urllib.request.urlretrieve(url, target)
        downloaded.append(target)
    return downloaded


def _build_deepresearch_paper_map(report_path: Path) -> dict[str, str]:
    if not report_path.exists():
        return {}

    text = report_path.read_text(encoding="utf-8")
    mapping: dict[str, str] = {}
    for raw_title, url in re.findall(
        r"\d+\.\s+(.+?), accessed .*?\[(https?://[^\]]+)\]", text
    ):
        clean_title = _strip_title(raw_title)
        match = re.search(r"(\d{4}\.\d{5})", url)
        if match and clean_title:
            mapping.setdefault(match.group(1), clean_title)
    return mapping
