from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SURVEY_DIR = REPO_ROOT / "docs" / "survey"
ARCHIVE_DIR = REPO_ROOT / "docs" / "archive" / "survey-2026-03-25-v2"


def test_survey_archive_exists_with_previous_structure():
    assert ARCHIVE_DIR.exists()
    assert (ARCHIVE_DIR / "01-framework.md").exists()
    assert (ARCHIVE_DIR / "07-frontiers.md").exists()
    assert (ARCHIVE_DIR / "05-paper-notes" / "rlm.md").exists()


def test_new_survey_has_overview_and_all_chapters():
    assert (SURVEY_DIR / "README.md").exists()
    assert (SURVEY_DIR / "survey-map.md").exists()

    for name in [
        "01-framework.md",
        "02-formation.md",
        "03-evolution.md",
        "04-retrieval.md",
        "05-evaluation.md",
        "06-systems-and-engineering.md",
        "07-frontiers.md",
    ]:
        assert (SURVEY_DIR / name).exists()


def test_new_survey_chapters_are_analysis_oriented():
    overview = (SURVEY_DIR / "README.md").read_text(encoding="utf-8")
    survey_map = (SURVEY_DIR / "survey-map.md").read_text(encoding="utf-8")
    framework = (SURVEY_DIR / "01-framework.md").read_text(encoding="utf-8")
    evaluation = (SURVEY_DIR / "05-evaluation.md").read_text(encoding="utf-8")

    assert "分析型综述" in overview
    assert "按问题读" in overview
    assert "按系统读" in overview
    assert "证据地图" in survey_map
    assert "Mem0" in survey_map
    assert "Hindsight" in survey_map
    assert "为什么生命周期比静态分类更有效" in framework
    assert "评测什么" in evaluation


def test_new_survey_chapters_include_evidence_anchors():
    chapter_names = [
        "01-framework.md",
        "02-formation.md",
        "03-evolution.md",
        "04-retrieval.md",
        "05-evaluation.md",
        "06-systems-and-engineering.md",
        "07-frontiers.md",
    ]

    for name in chapter_names:
        content = (SURVEY_DIR / name).read_text(encoding="utf-8")
        assert "## 研究矩阵" in content
        assert "| 优势 | 局限 | 当前证据强度 |" in content
        assert "## 关键概念与代表引用" in content
        assert "## 代表工作定位" in content
        assert "## 本章主要证据来源" in content


def test_survey_enforces_key_concept_evidence_rules():
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    claude = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    assert "关键概念、方法范式、系统路线、评测对象、组织性判断，必须绑定明确代表引用" in agents
    assert "代表引用优先 `paper`；`blog` 只能做工程补充；`DeepResearch` 只能做线索" in agents
    assert "编辑 survey 时必须遵守 `AGENTS.md` 的关键概念引用规则" in claude


def test_survey_promotes_required_2026_evidence():
    framework = (SURVEY_DIR / "01-framework.md").read_text(encoding="utf-8")
    formation = (SURVEY_DIR / "02-formation.md").read_text(encoding="utf-8")
    evolution = (SURVEY_DIR / "03-evolution.md").read_text(encoding="utf-8")
    retrieval = (SURVEY_DIR / "04-retrieval.md").read_text(encoding="utf-8")
    evaluation = (SURVEY_DIR / "05-evaluation.md").read_text(encoding="utf-8")
    systems = (SURVEY_DIR / "06-systems-and-engineering.md").read_text(encoding="utf-8")
    frontiers = (SURVEY_DIR / "07-frontiers.md").read_text(encoding="utf-8")
    overview = (SURVEY_DIR / "README.md").read_text(encoding="utf-8")

    for content in (framework, retrieval, systems):
        assert "Recursive Language Models" in content

    for token in ("MemoryAgentBench", "MemoryArena", "AMA-Bench"):
        assert token in evaluation

    assert any("Memora" in content for content in (formation, evolution, retrieval))
    assert "AgentOrchestra" in evolution
    assert "主证据" in evolution
    assert "补充" in evolution
    assert "TeleMem" in frontiers
    assert "Think3D" in frontiers
    assert "RenderMem" in frontiers
    assert "先看研究矩阵，再看关键概念与代表引用，再读正文论证" in overview
