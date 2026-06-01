# Manuscript Structure

## Argument Flow (Not Just Sections)

A paper is an argument, not a form to fill.

```
Introduction: Why should anyone care?
      ↓
Methods: How can we find out?
      ↓
Results: What did we find?
      ↓
Discussion: What does it mean?
```

Each section should make the reader ready for the next.

## Section-by-Section Guide

For a full paper, draft section-by-section rather than as one compressed
summary. Keep section files or an explicit section plan until the final paper
passes validation.

Suggested word allocation for a standard full paper. These are main-text
targets: bibliography, appendices, reproducibility logs, claim audits, and
source inventories are outside the paper body and cannot be used to satisfy a
journal-style word target.

| Section | Typical Target |
|---------|----------------|
| Abstract | 200-300 |
| Introduction | 1000-1500 |
| Literature/background | 1200-1800 |
| Methods/data | 1000-1500 |
| Results/synthesis | 1500-2200 |
| Discussion/limitations | 1200-1800 |
| Conclusion | 400-700 |

Minimum viable section depth for a publication-style paper:

- Introduction should establish the problem, gap, research question, contribution, and stakes across multiple paragraphs.
- Literature/background should synthesize a curated body of evidence rather than list search hits.
- Methods/data should make the analysis reproducible enough that another researcher could rerun it.
- Results should present evidence, uncertainty, negative findings, and figure/table interpretation.
- Discussion should compare results to prior evidence, state mechanisms, limitations, and implications.
- Appendices should contain supplemental evidence or reproducibility artifacts, not material that compensates for an underwritten main text.

### Abstract (~200 words)

Not a teaser. A complete summary.

- 1-2 sentences: Problem + why it matters
- 1-2 sentences: What you did
- 2-3 sentences: What you found
- 1 sentence: Main implication

### Introduction

**Don't start with:** "X is important..."

**Do start with:** The specific problem and gap.

Structure:
1. Context (what's the domain)
2. Gap (what's unknown)
3. Question (what you ask)
4. Contribution (what you do)
5. Significance (why it matters)

### Methods

**Goal:** Someone could reproduce your work.

Include:
- Data sources with access info
- Variables and their definitions
- Methods with rationale (why this method?)
- Parameters and how chosen
- Analysis workflow

### Results

**Show, don't tell.**

- Lead with evidence, not interpretations
- Figures should be embedded, not referenced separately
- Each result answers part of your question
- Report negative findings too

### Discussion

**Interpret, don't repeat.**

- What do results mean?
- How do they compare to literature?
- What are limitations?
- What are implications?
- What's next?

### Conclusions

**Don't just summarize.**

- What's the main takeaway?
- What's the broader impact?
- What questions remain?

## Figure Integration

Figures go where they are discussed, not at the end.

```
...the primary outcome changed substantially after the intervention (Figure 3).

![Figure 3](objects/figure/fig_003.png)
*Figure 3. Outcome trend before and after the intervention...*

This pattern suggests...
```

## Citation Integration

Citations support claims, not just to show you read things.

```
Weak: "Smith et al. (2020) studied X."
Strong: "X has been linked to Y in multiple contexts (Smith 2020, Jones 2021)."
```

## Self-Review Questions

Read your own draft as a reviewer:

- [ ] Is the question clear by paragraph 2?
- [ ] Can I reproduce the methods?
- [ ] Does each figure support a claim?
- [ ] Is every claim backed by evidence?
- [ ] Did I acknowledge limitations?
- [ ] Is the argument logical throughout?
- [ ] Would a non-expert understand the abstract?
