# Literature Search Methods

## Systematic Literature Review

**When:** Starting a new research project, identifying knowledge gap.

**Process:**

1. **Define search scope**
   - Key terms and synonyms
   - Time range (last 5 years? 10 years? all time?)
   - Domain boundaries

2. **Search multiple sources**
   - Semantic Scholar: broad coverage, good API
   - OpenAlex: open, comprehensive
   - arXiv: preprints, latest work
   - Google Scholar: broadest but no API
   - Domain-specific (PubMed, IEEE, ACM)

3. **Filter systematically**
   - By title relevance (first pass)
   - By abstract relevance (second pass)
   - By full text (final selection)

4. **Extract information**
   - Research question addressed
   - Methods used
   - Key findings
   - Limitations acknowledged
   - Future work suggested

5. **Synthesize**
   - What is known?
   - What is debated?
   - What is unknown?
   - Where does your question fit?

## Literature Object Template

```json
{
  "id": "lit_001",
  "type": "literature",
  "state": "read",
  "attributes": {
    "title": "...",
    "authors": ["...", "..."],
    "year": 2024,
    "doi": "...",
    "research_question": "What question does this address?",
    "methods": ["method1", "method2"],
    "key_findings": ["finding1", "finding2"],
    "limitations": ["limitation1"],
    "relevance": "How does this relate to my research?",
    "cited_by_count": 42
  }
}
```

## Identifying Knowledge Gaps

Ask of the literature:

1. **Missing questions:** What questions haven't been asked?
2. **Contradictions:** Where do papers disagree?
3. **Method gaps:** What methods haven't been applied?
4. **Context gaps:** Has this been studied in X context?
5. **Scale gaps:** Has this been studied at Y scale?

## Literature Convergence Signs

You've read enough when:

- [ ] Can explain the main approaches in the field
- [ ] Know which papers are most influential
- [ ] Understand current debates
- [ ] Can identify clear gaps
- [ ] Know standard methods and their limitations
- [ ] Can position your question relative to existing work

Typically requires: 10-30 papers depending on field maturity.