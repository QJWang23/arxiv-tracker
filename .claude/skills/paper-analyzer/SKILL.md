---
name: paper-analyzer
description: Analyze filtered papers and generate technical summaries
invocable: true
---

# Paper Analyzer Skill

Analyzes papers from the arxiv-tracker and generates detailed technical summaries.

## Usage

```
/paper-analyzer --mode=instant --date=YYYY-MM-DD
/paper-analyzer --mode=weekly --week=YYYY-WNN
```

## Process

1. **Load filtered data** from `data/filtered/{date}.json`
2. **For each paper**, generate:
   - Core technical points (preserving key terminology)
   - Innovation points (2-3 sentences on what's novel)
   - Impact on your focus areas (inference optimization, K8s infra, hardware acceleration)
   - Actionable follow-up points
3. **Output** structured markdown report

## Report Template

```markdown
## {{title}}

**来源**: {{source}} | **日期**: {{date}} | **热度**: {{heat_score}}

### 核心技术要点
- [具体技术要点1，保留原始术语]
- [具体技术要点2，保留原始术语]

### 创新点
[2-3句话说明与现有方法的本质区别]

### 对关注领域的影响
- **推理优化**: [具体影响]
- **K8s 基础设施**: [具体影响]（如适用）
- **硬件加速**: [具体影响]（如适用）

### 后续跟进
- [ ] [可执行的技术要点或实验方向]
- [ ] [相关论文推荐阅读]

---
arXiv: {{arxiv_id}} | [链接]({{url}})
```

## Key Requirements

- **使用中文输出** - 所有报告内容使用中文撰写
- **DO NOT over-summarize** - preserve technical details and terminology
- **Focus on what's new** - highlight the innovation, not background
- **Connect to user's domain** - explicitly analyze impact on inference optimization, K8s, and hardware acceleration
- **Be actionable** - suggest concrete follow-up actions

## Output Location

- Instant reports: `reports/daily/{date}-instant.md`
- Weekly reports: `reports/weekly/{year}-W{week}.md`
