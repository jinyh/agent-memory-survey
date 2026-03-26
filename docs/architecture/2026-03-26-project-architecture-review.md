# AgentResearch 项目架构评审

> 2026-03-26 | 状态：Proposed

## 背景

对 AgentResearch 项目的整体架构进行全面评审，覆盖代码原型（`src/memory/`、`src/references/`）、研究综述（`docs/survey/`）和工具链三个领域。评审基于 memory-core-v1 实施完成、survey v3.0 重构完成后的当前状态。

## 影响面

- 代码原型：`src/memory/` 7 个模块、`src/references/` 3 个模块、`tests/` 4 个测试文件
- 研究综述：`docs/survey/` 10 个文件、`docs/references/` 索引文件
- 工具链：`src/references/indexing.py`、`pyproject.toml`
- 配置：`AGENTS.md`、`CLAUDE.md`

## 决策

### 关键决策

1. **`MemoryStore` ABC 缺少序列化抽象方法**
   - 现状：`to_snapshot_dict()` / `from_snapshot_dict()` 只在子类中实现，未在 `MemoryStore` ABC 中声明
   - 决策：应在 `MemoryStore` 中添加 `@abstractmethod` 声明，确保新增 store 类型必须实现序列化
   - 替代方案：用 Protocol 做结构化类型约束（过度设计，不推荐）

2. **`from_snapshot_dict` 签名不一致导致 `load_snapshot` 潜在 bug**
   - 现状：三个 store 的 `from_snapshot_dict` 接受不同参数，但 `MemoryManager.load_snapshot` 传入 `(store_data, existing_store)`，与实际签名不匹配
   - 证据：`evaluation.py` 的 `check_roundtrip` 绕过了 `load_snapshot`，手动调用各 store 的 `from_snapshot_dict`
   - 决策：统一签名，让 `load_snapshot` 从 existing_store 提取构造参数后正确传递
   - 替代方案：让 `from_snapshot_dict` 接受 existing_store 实例并从中提取参数（耦合度更高）

3. **`__init__.py` 导出不完整**
   - 决策：补充导出 `GraphMemoryStore`、`VectorMemoryStore`、`FusionConfig`

### 重要决策

4. **检索评分权重硬编码**
   - 现状：各 store 的 `query()` 中评分权重为魔法数字（如 0.5/0.3/0.2、0.4/0.2/0.1/0.3、0.7/0.3）
   - 决策：将权重提取为 store 构造函数参数，支持外部配置
   - 替代方案：保持硬编码但在文档中标注（如果定位为纯概念原型可接受）

5. **`recall` 与 `recall_with_trace` 代码重复**
   - 决策：提取共享的 `_fuse_results` 内部方法，`recall` 调用后丢弃 trace

6. **`chromadb` 声明为依赖但未使用**
   - 决策：从 `pyproject.toml` 移除

7. **中文分词 `split()` 的局限性**
   - 决策：在代码注释和项目文档中明确标注此限制，暂不引入 jieba

8. **survey 与原型代码的映射关系未显式化**
   - 决策：在 `survey-map.md` 中增加"原型代码 ↔ survey 章节"对照表

9. **`__main__.py` 硬编码 DeepResearch 报告路径**
   - 决策：改为扫描 `ref/DeepResearch/*.md` 全部文件

### 可延迟决策

10. **并发安全**：v1 明确不处理，合理
11. **VectorMemoryStore embedding 模型可插拔性**：后续按需扩展
12. **评测场景扩展**：当前 7 个 query 足够验证基本功能
13. **`indexing.py` 拆分**：当前可工作，后续修改质量评估规则时再拆
14. **survey 跨章节引用编号体系**：生成完整论文时再统一

## 风险与依赖

### 跨领域影响

- `from_snapshot_dict` 签名修复 → 需同步更新 `evaluation.py` 的 `check_roundtrip`（可改为直接使用 `load_snapshot`）
- survey 巩固路径描述 ↔ 原型 `consolidate_episodic_to_semantic` 实现 → 需标注原型的简化程度

### 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| `load_snapshot` 签名不匹配导致运行时崩溃 | 高 | 高 | 统一 `from_snapshot_dict` 接口签名 |
| 中文分词 `split()` 在真实场景下检索质量差 | 中 | 中 | 明确标注为概念原型限制 |
| `chromadb` 未使用但占用依赖 | 低 | 低 | 从 `pyproject.toml` 移除 |
| `indexing.py` 单文件过大 | 中 | 中 | 后续拆分时补充测试覆盖 |

## 替代方案

- **全面重构 store 接口为 Protocol 模式**：过度设计，当前 ABC 模式足够，不推荐
- **引入 Pydantic 做序列化**：增加依赖复杂度，dataclass + 手动序列化对概念原型足够
- **用 ChromaDB 替换自实现的 VectorMemoryStore**：增加外部依赖和运维复杂度，概念原型阶段不值得
