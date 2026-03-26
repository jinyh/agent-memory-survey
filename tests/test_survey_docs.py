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
    framework = (SURVEY_DIR / "01-framework.md").read_text(encoding="utf-8")
    evaluation = (SURVEY_DIR / "05-evaluation.md").read_text(encoding="utf-8")

    assert "分析型综述" in overview
    assert "为什么生命周期比静态分类更有效" in framework
    assert "评测什么" in evaluation
