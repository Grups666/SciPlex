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
