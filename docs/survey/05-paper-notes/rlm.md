# Recursive Language Models (RLM)

> arXiv:2512.24601v2 | MIT CSAIL | 2026

## 核心贡献

1. **RLM 范式**: 将长 prompt 作为外部环境变量，LLM 通过 REPL 递归分解和处理
2. **符号递归**: LLM 生成代码来操作自身的输入，实现无界输入/输出
3. **RLM-Qwen3-8B**: 首个原生递归语言模型，微调后性能提升 28.3%

## 与记忆的关系

### 工作记忆扩展
- 传统方法：上下文压缩（context compaction）—— 有损且假设部分信息可安全丢弃
- RLM 方法：prompt 存储为 REPL 变量，LLM 通过代码片段按需访问
- 中间结果存储在程序变量中，不占用 LLM 上下文

### 关键设计差异（vs 传统 Agent scaffold）
1. **符号句柄**: RLM 给 LLM 一个 prompt 的符号引用，模型可以编程操作它
2. **递归调用**: 代码在环境 E 内运行，可以调用 sub-RLM，实现递归处理
3. **无界语义**: 可以做 Ω(|P|) 甚至 Ω(|P|²) 的语义工作

### 算法核心 (Algorithm 1)
```
state ← InitREPL(prompt=P)
state ← AddFunction(state, sub_RLM)
while True:
    code ← LLM(hist)              # LLM 生成代码
    (state, stdout) ← REPL(state, code)  # 在环境中执行
    hist ← hist || code || Metadata(stdout)
    if state[Final] is set:
        return state[Final]
```

## 实验结果

在 4 个长上下文任务上评估 (GPT-5 和 Qwen3-Coder-480B):
- S-NIAH: 针对 needle-in-a-haystack
- BrowseComp+ (1K documents): 多跳推理
- OOLONG: 线性复杂度长推理
- OOLONG-Pairs: 二次复杂度长推理

RLM 在 10M+ token 规模仍保持强劲表现，显著优于基线方法。

## 对 Agent Memory 的启发

1. **程序化记忆管理**: 与其让记忆系统管理上下文，不如让 Agent 写代码来管理
2. **惰性加载**: 只在需要时加载 prompt 的相关部分到上下文
3. **中间变量作为记忆**: REPL 状态本质上是一种结构化工作记忆
4. **递归分治**: 复杂记忆检索可以递归分解为子问题
