from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

_SPLITS = [
    "Accurate_Retrieval",
    "Test_Time_Learning",
    "Long_Range_Understanding",
    "Conflict_Resolution",
]


def _jsonable(value: Any) -> Any:
    if hasattr(value, "tolist"):
        return _jsonable(value.tolist())
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    return value


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(_jsonable(value), ensure_ascii=False)


def _normalize_row(row: dict[str, Any], split: str, index: int) -> dict[str, Any]:
    context = row.get("context", "")
    if not context:
        context = row.get("metadata", {})

    meta = row.get("metadata", {})
    if not isinstance(meta, dict):
        meta = {"raw_metadata": meta}

    questions = row.get("questions")
    query = ""
    if questions is not None:
        if hasattr(questions, "tolist"):
            questions = questions.tolist()
        if isinstance(questions, list) and questions:
            query = _as_text(questions[0])
        else:
            query = _as_text(questions)
    elif row.get("question"):
        query = _as_text(row.get("question"))

    answer = row.get("answers")
    if hasattr(answer, "tolist"):
        answer = answer.tolist()
    if isinstance(answer, list) and len(answer) == 1:
        answer = answer[0]

    sample_id = row.get("sample_id") or row.get("id") or f"{split}-{index:05d}"

    return {
        "id": str(sample_id),
        "split": split,
        "source": "MemoryAgentBench",
        "query": _as_text(query),
        "answer": _jsonable(answer),
        "context": _as_text(context),
        "meta": _jsonable(meta),
    }


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(_jsonable(row), ensure_ascii=False) + "\n")


def _write_markdown(path: Path, split: str, rows: list[dict[str, Any]]) -> None:
    lines = [
        f"# {split}",
        "",
        f"- count: {len(rows)}",
        "- fields: id, split, source, query, answer, context, meta",
        "",
        "## Samples",
        "",
    ]
    for row in rows[:3]:
        lines.extend([
            f"### {row['id']}",
            f"- query: {row['query']}",
            f"- answer: {_as_text(row['answer'])[:300]}",
            f"- context: {row['context'][:300]}",
            "",
        ])
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def export_memoryagentbench(dataset_root: str, out_root: str) -> dict[str, int]:
    root = Path(dataset_root)
    data_dir = root / "data"
    out_dir = Path(out_root)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary: dict[str, int] = {}
    readme_lines = [
        "# MemoryAgentBench normalized export",
        "",
        "- raw/: 原始 parquet",
        "- normalized/: 转换后的 JSONL + MD",
        "",
    ]

    for split in _SPLITS:
        parquet_path = data_dir / f"{split}-00000-of-00001.parquet"
        df = pd.read_parquet(parquet_path)
        rows = [
            _normalize_row(row, split, idx)
            for idx, row in enumerate(df.to_dict(orient="records"))
        ]
        _write_jsonl(out_dir / f"{split}.jsonl", rows)
        _write_markdown(out_dir / f"{split}.md", split, rows)
        summary[split] = len(rows)
        readme_lines.append(f"- {split}: {len(rows)} rows")

    (out_dir / "README.md").write_text("\n".join(readme_lines).rstrip() + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Export MemoryAgentBench parquet splits to JSONL + MD")
    parser.add_argument("--dataset-root", default="ref/datasets/MemoryAgentBench")
    parser.add_argument("--out-root", default="ref/datasets/MemoryAgentBench/normalized")
    args = parser.parse_args()
    summary = export_memoryagentbench(args.dataset_root, args.out_root)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
