# Communication

## Phase Goal

Produce the requested output type with standards appropriate to that target.
Do not default every study to a paper. A scoping study, empirical analysis,
literature synthesis, protocol, technical report, or console audit can require
different structure, length, citation density, and evidence language.

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

Before writing, select and record an `output_target`. Common targets are
`brief`, `report`, `paper`, `protocol`, `registered_report`, and
`console_audit`. The target controls expected structure, length, figure count,
reference depth, and evidence language.

## Output Targets

These are default standards, not hard scientific laws. Project or skill config
may override them, but deviations must be explicit in the output object.

| Target | Typical Use | Default Standard |
|--------|-------------|------------------|
| `brief` | Decision memo or quick synthesis | 800-1500 words, 0-2 figures, 5-12 references, 2+ source roles |
| `report` | General research deliverable | 3000-6000 words, 3-6 figures/tables, 15-35 references, 4+ source roles |
| `paper` | Publication-style manuscript | 7000-10000 main-text words excluding references and appendices, 4-8 main figures/tables, 25-60 references, 5+ source roles, supplement for extras |
| `protocol` | Planned study before execution | Objectives, hypotheses, data, methods, risks, no final findings, 3+ source roles |
| `registered_report` | Hypotheses and analysis plan for review before results | Introduction, hypotheses, data, analysis plan, validation criteria, 4+ source roles |
| `console_audit` | Transparent process artifact | Complete state/event/object summary, not prose-first |

If evidence is only literature synthesis or documented-statistics synthesis,
the output should usually be `report`, `brief`, or `protocol`, unless the paper
clearly states that it is not a completed raw-data empirical study.

For a `paper`, do not mark final if literature coverage is shallow, figures are
mostly illustrative, raw data was promised but not processed, or citation count
falls far below the target without justification.

## Full Paper Protocol

For `output_target=paper`, do not attempt to produce the final manuscript in a
single short pass. Use a staged drafting workflow:

1. Evidence corpus:
   - Create or validate enough cited literature objects for the target.
   - Record source roles and evidence roles.
   - Create a source-coverage summary before writing.

2. Section plan:
   - Create a paper object in `draft` state.
   - Record section-level word targets whose sum meets the paper target.
   - Count the paper target against the manuscript body only. References,
     appendices, reproducibility logs, claim audits, and source inventories do
     not count toward the 7000-10000 word paper target.
   - Typical non-domain-specific allocation:
     - Abstract: 200-300
     - Introduction: 1000-1500
     - Literature/background: 1200-1800
     - Methods/data: 1000-1500
     - Results/synthesis: 1500-2200
     - Discussion/limitations: 1200-1800
     - Conclusion: 400-700

3. Section drafts:
   - Write section files under `objects/paper/sections/`.
   - Each section should cite evidence objects and note which finding it supports.
   - Do not collapse methods, results, and discussion into one short summary.
   - Do not pad to the word target by repeating paragraphs. If a section is too
     short, add new evidence, analysis, limitations, robustness checks, or
     interpretation.
   - Treat a short Introduction, Methods, Results, or Discussion as a blocking
     paper defect even if the full Markdown file exceeds the word target.
   - Use appendices only for real supplemental material: reproducibility tables,
     code/output inventories, extended robustness results, instrument details,
     data dictionaries, or additional figures. Do not use appendices to store
     generic notes that should have been synthesized into the paper body.

4. Figures and tables:
   - Final paper requires real figure/table files referenced by finalized figure objects.
   - A finalized figure must not have `needs_generation=true`.
   - Image figures must be embedded with Markdown image syntax, not only listed
     in metadata or appendix text: `![Figure N](objects/figure/fig_N.png)`.
   - Tables in the manuscript must be valid Markdown tables with separator rows
     or linked as external table files. Do not use plain pipe-delimited text
     without a Markdown header separator.
   - Literature-synthesis figures are allowed when honestly labeled as evidence maps,
     source coverage, effect-size summaries, or evidence-chain diagrams.

5. Assembly:
   - Assemble the final manuscript at `objects/paper/paper_XXX.md`.
   - Update `word_count`, `citation_ids`, `figure_ids`, `finding_ids`, and `file_path`.
   - Keep paper state as `draft` or `reviewed` until validation passes.

6. Finalization:
   - Run `validate-workspace`.
   - If validation fails, keep the paper non-final and write blockers in review.
   - Only mark paper `final` and phase `COMPLETE` after blocking issues are gone.
   - If the manuscript is below the configured word, figure, or citation
     targets, continue drafting or explicitly downgrade the output target before
     finalization. A short manuscript is not a completed paper.
   - Before finalization, compare result prose against generated tables,
     coefficient files, figure captions, and finding objects. If a coefficient
     sign, sample size, date range, unit, or uncertainty interval changed during
     iteration, update the manuscript and review object before marking final.

For `report` and `paper` outputs, cited literature objects should be in `read`,
`cited`, or `validated` state. A source that is only `identified` can motivate
follow-up, but it should not support final claims.

For `paper` outputs, cited literature must also be curated for relevance. Each
cited literature object should record a generic `source_role`/`evidence_role`
and a short `relevance_assessment`, `inclusion_reason`, or equivalent note.
Do not bulk-import search hits into the reference list. If a source is only
background context or weakly related, say so and do not let it count as core
evidence.

Final outputs should include a compact source-coverage statement. Source roles
are generic evidence roles, not domain categories. Examples include theory,
review, dataset documentation, observational study, experiment, benchmark,
negative evidence, methodological critique, or policy context. The point is to
avoid one-sided evidence, not to impose a field-specific bibliography.

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
...the primary outcome changed substantially after the intervention (Figure 3).

![Figure 3](objects/figure/fig_003.png)
*Figure 3. Outcome trend before and after the intervention...*

This pattern suggests...
```

## Citation Integration

Citations support claims:

```markdown
Weak: "Smith et al. (2020) studied X."
Strong: "X has been linked to Y in multiple contexts (Smith 2020, Jones 2021)."
```

For publication-style outputs, cited literature and data sources should be
clickable where they appear in source-facing sections:

- Bibliography entries should include a DOI, provider page, repository page, or
  source URL as a Markdown link.
- In-text author-year references should usually link the author/year phrase or
  source title to the DOI/provider URL at first substantive mention, for example
  `[Smith (2020)](https://doi.org/...)`.
- Data descriptions should link to the dataset landing page or acquired source
  URL when public.
- Do not put all URLs only in object metadata; the final manuscript must expose
  the links a reader needs.
- Keep internal SciPlex artifact paths such as `objects/data/...` out of the
  main prose. Use human-facing source names and public URLs in the manuscript
  body; put internal file paths in a reproducibility appendix or audit table.
- Do not write mechanical citation inventory sentences such as
  "`Author (Year) is used as contextual literature on ...`". Synthesize sources
  into the argument instead.

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
    "output_target": "paper",
    "evidence_mode": "raw_data_analysis",
    "standards": {
      "word_count_target": "7000-10000",
      "main_figures_target": "4-8",
      "reference_target": "25-60"
    },
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

- [ ] Output target selected and standards recorded
- [ ] Output object includes `file_path` relative to the `sciplex/` root and the file exists
- [ ] Output object links the hypotheses, data/sources, methods, findings, figures, and citations it depends on
- [ ] Output object includes a structured key-claim audit: claim text, evidence links, strength, and limitations
- [ ] For paper targets, the body alone meets the configured word target; references and appendices are excluded
- [ ] Core paper sections are substantive, not one-paragraph placeholders
- [ ] Appendices contain supplemental evidence or reproducibility material, not padding
- [ ] For `paper`, section drafts or an equivalent section plan demonstrate the target length was intentionally built
- [ ] Full manuscript structure
- [ ] All figures embedded with captions
- [ ] Image figures use Markdown image syntax, not only raw path text
- [ ] Tables render as valid Markdown tables or are linked as separate files
- [ ] Every main figure/table object is linked by file path in the final manuscript
- [ ] Finalized image files are real renderable images, not text placeholders saved with image extensions
- [ ] Finalized figures/tables record evidence sources and the data points, statistics, rows, or visual encoding they display
- [ ] All citations accurate
- [ ] Word count appropriate to output target
- [ ] Word count is inside the target range, not merely above the minimum
- [ ] Reference coverage appropriate to output target
- [ ] Source coverage broad enough for output target
- [ ] Cited literature objects are `cited` or `validated`, not merely identified/read
- [ ] Cited literature has stable identifiers or is explicitly marked `needs_verification`
- [ ] Reference section is generated from or checked against literature object metadata
- [ ] Literature and data source entries expose clickable external URLs where available
- [ ] First substantive in-text mentions of cited sources expose clickable URLs where available
- [ ] Main prose uses public source names/URLs, while internal object paths are limited to reproducibility appendices
- [ ] No repeated filler paragraphs or mechanical citation inventory prose
- [ ] Bibliography entries are used in the manuscript argument, not only listed
- [ ] Provider metadata audit has been run when stable provider IDs are available
- [ ] Main vs supplementary figures handled when figure count is large
- [ ] Evidence mode stated and consistent with methods
- [ ] Referenced findings include explicit evidence chains
- [ ] Result prose agrees with generated tables, figures, coefficients, sample sizes, dates, and units
- [ ] Final review covers method fidelity, evidence chains, claim validity, source coverage, result consistency, output standards, limitations, and overclaim risk
- [ ] Evidence chains traceable
