# Communication

## Phase Goal

Produce publication-quality manuscript.

## Process

```
Input: {findings, figures, literature}
Steps:
  1. Structure argument
     - Not just sections—narrative flow
     - Question → Evidence → Conclusion
  
  2. Write sections
     - Abstract: Complete summary
     - Introduction: Problem → Gap → Question
     - Methods: Reproducible
     - Results: Evidence-first
     - Discussion: Interpret, don't repeat
     - Conclusions: Takeaway, not summary
  
  3. Embed figures
     - Figures where discussed
     - Complete captions
     - Reference in text
  
  4. Integrate citations
     - Support claims, not decoration
     - Accurate attribution
  
  5. Self-review
     - Read as reviewer
     - Check quality checklist
Output: manuscript.md
```

## Argument Structure

Use `references/manuscript_template.md` for detailed guidance.

A paper is an argument, not a form:

```
Introduction: Why should anyone care?
      ↓
Methods: How can we find out?
      ↓
Results: What did we find?
      ↓
Discussion: What does it mean?
```

Each section should make reader ready for next.

## Abstract (~200 words)

Complete summary, not teaser:

- 1-2 sentences: Problem + why it matters
- 1-2 sentences: What you did
- 2-3 sentences: What you found
- 1 sentence: Main implication

## Introduction

**Don't start with:** "X is important..."

**Do start with:** The specific problem and gap.

Structure:
1. Context (what's the domain)
2. Gap (what's unknown)
3. Question (what you ask)
4. Contribution (what you do)
5. Significance (why it matters)

## Methods

**Goal:** Someone could reproduce your work.

Include:
- Data sources with access info
- Variables and definitions
- Methods with rationale
- Parameters and how chosen
- Analysis workflow

## Results

**Show, don't tell.**

- Lead with evidence, not interpretations
- Figures embedded, not referenced separately
- Each result answers part of question
- Report negative findings too

## Discussion

**Interpret, don't repeat.**

- What do results mean?
- How compare to literature?
- What are limitations?
- What are implications?
- What's next?

## Conclusions

**Don't just summarize.**

- What's the main takeaway?
- What's the broader impact?
- What questions remain?

## Figure Integration

Figures go where discussed:

```markdown
...groundwater declined significantly (Figure 3).

![Figure 3](objects/figure/fig_003.png)
*Figure 3. Groundwater storage change 2000-2019...*

This pattern suggests...
```

## Citation Integration

Citations support claims:

```markdown
Weak: "Smith et al. (2020) studied X."
Strong: "X has been linked to Y in multiple contexts (Smith 2020, Jones 2021)."
```

## Self-Review

Read your draft as reviewer:

- [ ] Is question clear by paragraph 2?
- [ ] Can I reproduce the methods?
- [ ] Does each figure support a claim?
- [ ] Is every claim backed by evidence?
- [ ] Did I acknowledge limitations?
- [ ] Is argument logical throughout?
- [ ] Would non-expert understand abstract?

## Manuscript Object

```json
{
  "id": "paper_001",
  "type": "paper",
  "state": "draft",
  "attributes": {
    "title": "Paper title",
    "abstract": "...",
    "word_count": 4500,
    "figures": ["fig_001", "fig_002", "fig_003"],
    "citations": ["lit_001", "lit_002"],
    "file_path": "objects/paper/paper_001.md"
  }
}
```

## Quality Gate

Before complete:

- [ ] Full manuscript structure
- [ ] All figures embedded with captions
- [ ] All citations accurate
- [ ] Word count > 3000
- [ ] Self-review passed
- [ ] Evidence chains traceable
