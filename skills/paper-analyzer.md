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

**Source**: {{source}} | **Date**: {{date}} | **Heat Score**: {{heat_score}}

### Core Technical Points
- [Specific technical point 1, preserving original terminology]
- [Specific technical point 2, preserving original terminology]

### Innovation
[2-3 sentences explaining the essential difference from existing methods]

### Impact on Focus Areas
- **Inference Optimization**: [Specific impact]
- **K8s Infrastructure**: [Specific impact] (if applicable)
- **Hardware Acceleration**: [Specific impact] (if applicable)

### Follow-up Points
- [ ] [Actionable technical point or experiment direction]
- [ ] [Related papers to read further]

---
arXiv: {{arxiv_id}} | [Link]({{url}})
```

## Key Requirements

- **DO NOT over-summarize** - preserve technical details and terminology
- **Focus on what's new** - highlight the innovation, not background
- **Connect to user's domain** - explicitly analyze impact on inference optimization, K8s, and hardware acceleration
- **Be actionable** - suggest concrete follow-up actions

## Output Location

- Instant reports: `reports/daily/{date}-instant.md`
- Weekly reports: `reports/weekly/{year}-W{week}.md`
