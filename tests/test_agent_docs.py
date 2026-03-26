from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_claude_md_declares_agents_as_source_of_truth():
    content = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    assert "AGENTS.md" in content
    assert "共享项目约定以 `AGENTS.md` 为准" in content


def test_claude_md_keeps_minimum_project_context():
    content = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    assert "# AgentResearch" in content
    assert "Claude Code" in content
    assert "Agent Memory" in content
