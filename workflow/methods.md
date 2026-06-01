# Method Design

## Phase Goal

Design methods that distinguish between hypotheses.

## Process

```
Input: {question, hypotheses, evidence_patterns}
Steps:
  1. Map hypotheses → required evidence
     - What data would distinguish H1 from H2?
     - What analyses would reveal patterns?
  
  2. Identify data sources
     - What data exists?
     - What are limitations?
     - What preprocessing needed?
     - Can it be acquired now, or only documented?
  
  3. Select analytical methods
     - Match method to hypothesis structure
     - Consider alternatives
     - Document rationale
  
  4. Design workflow
     - Sequence of analyses
     - Decision points (if X, then Y)
     - Validation steps
  
  5. Identify confounders
     - What else could cause observed patterns?
     - How to control or measure?
Output: {methods[], workflow, data_sources[], confounders[]}
```

## Method Selection

Use `references/method_templates.md` for common patterns.

Match method to question type:

| Question Type | Methods |
|---------------|---------|
| Is X different from Y? | Comparison tests, effect sizes |
| Is X related to Y? | Correlation, regression |
| Are there types/patterns? | Clustering, dimensionality reduction |
| How does X change over time? | Time series, trend analysis |
| Where does X occur? | Spatial analysis, mapping |
| Does X cause Y? | Quasi-experimental, causal inference |

## Method Documentation

For each method, create object:
```json
{
  "id": "meth_001",
  "type": "method",
  "state": "designed",
  "attributes": {
    "name": "Method name",
    "purpose": "What question this addresses",
    "hypothesis_tested": ["hyp_001"],
    "description": "How it works",
    "parameters": {...},
    "assumptions": ["Assumption 1", "Assumption 2"],
    "limitations": ["Limitation 1"],
    "alternatives_considered": ["Alternative method"],
    "rationale": "Why this method over alternatives"
  }
}
```

## Data Documentation

For each data source, create object:
```json
{
  "id": "data_001",
  "type": "data",
  "state": "identified",
  "attributes": {
    "name": "Dataset name",
    "source": "Where from",
    "access": "How to access",
    "format": "File format",
    "variables": ["var1", "var2"],
    "time_range": "2000-2020",
    "spatial_coverage": "Global",
    "limitations": ["Limitation 1"],
    "preprocessing_needed": ["Step 1"]
  }
}
```

## Data Acquisition

Public data should be acquired as an artifact when the study claims raw-data
analysis. Do not treat a dataset landing page, API description, or paper
summary as acquired raw data.

Use the generic acquisition helper for stable public URLs:

```bash
python scripts/data_acquire.py --workspace <working-directory> \
  --url "<public-data-url>" \
  --name "<dataset name>" \
  --source "<provider>"
```

The helper writes:

- `objects/data/<data_id>/raw/<filename>`: downloaded artifact
- `objects/data/<data_id>/manifest.json`: URL, bytes, checksum, headers
- `objects/data/<data_id>.json`: data object with `access_status: acquired`

If the source requires registration, manual browser interaction, paid access,
or credentials, record the blocker in the data object and do not label the study
as `raw_data_analysis` until files are actually acquired and processed.

When acquisition fails for a public URL, do not infer that the dataset is
unavailable from a single failed request. Use a generic fallback sequence:

1. Retry with source-page `--referer` and normal browser-like request headers.
2. Check the provider landing page for alternate direct files, API endpoints,
   mirrors, documentation files, or smaller extracts.
3. Record each failed attempt as a `failed` object and keep the data object at
   `identified` or `blocked`, not `acquired`.
4. If at least one relevant dataset is acquired, proceed with a narrower raw-data
   analysis and clearly state which hypotheses it can and cannot test.
5. If no data is acquired, switch to `documented_statistics_synthesis`,
   `protocol`, or `report`; do not present it as completed raw-data analysis.

## Workflow Design

Design analysis sequence with decision points:

```
1. Load and validate data
   - Check structure, missing values, outliers
   
2. Exploratory analysis
   - Visualize distributions
   - Check assumptions
   
3. Primary analysis
   - Test H1
   - Generate figures
   
4. Secondary analysis
   - Test H2
   - Compare with H1 results
   
5. Robustness checks
   - Sensitivity analysis
   - Subset validation
   
6. Decision point:
   - If results clear → proceed to synthesis
   - If ambiguous → iterate or acknowledge limitation
```

## Confounder Analysis

For causal claims, explicitly identify:

```
Potential confounders:
- Confounder 1: How to address?
- Confounder 2: How to measure/control?
- Confounder 3: Acknowledge as limitation?

Strategy:
- Measure and control statistically
- Design analysis to minimize
- Acknowledge unaddressed confounders
```

## Quality Gate

Before proceeding to Execution:

- [ ] Each hypothesis has corresponding method
- [ ] Methods can distinguish between hypotheses
- [ ] Data sources documented with limitations
- [ ] Workflow has decision points
- [ ] Confounders identified
- [ ] Method rationale documented
