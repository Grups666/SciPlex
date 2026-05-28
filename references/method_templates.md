# Analysis Method Templates

Common patterns for different research questions.

## Pattern 1: Comparison / Difference Detection

**Question type:** "Is X different from Y?" or "Does X affect Y?"

**Methods:**
- Statistical tests (t-test, Mann-Whitney, chi-square)
- Effect size (Cohen's d, odds ratio)
- Visualization: boxplots, distributions

**Hypothesis mapping:**
- H1: X > Y → test with one-tailed test
- H2: X ≠ Y → test with two-tailed test

## Pattern 2: Correlation / Association

**Question type:** "Is X related to Y?" or "What predicts Y?"

**Methods:**
- Correlation (Pearson, Spearman)
- Regression (linear, logistic, multiple)
- Feature importance

**Hypothesis mapping:**
- H1: Positive correlation → correlation > 0
- H2: Negative correlation → correlation < 0
- H3: No relationship → correlation ≈ 0

## Pattern 3: Classification / Typology

**Question type:** "Are there distinct types/patterns?" or "Can X be categorized?"

**Methods:**
- Clustering (k-means, hierarchical)
- Dimensionality reduction (PCA, t-SNE)
- Classification metrics (if labels exist)

**Hypothesis mapping:**
- H1: k clusters exist → silhouette score, domain interpretability
- H2: Clusters correspond to known categories → validation

## Pattern 4: Time Series / Trend

**Question type:** "How does X change over time?" or "Is there a trend?"

**Methods:**
- Trend analysis (Mann-Kendall, Sen's slope)
- Change point detection
- Time series decomposition

**Hypothesis mapping:**
- H1: Increasing trend → positive slope, significant
- H2: Decreasing trend → negative slope, significant
- H3: No trend → slope ≈ 0

## Pattern 5: Spatial Pattern

**Question type:** "Where does X occur?" or "Is there spatial pattern?"

**Methods:**
- Spatial clustering (hotspot analysis)
- Spatial autocorrelation (Moran's I)
- Visualization: maps, spatial plots

**Hypothesis mapping:**
- H1: Clustered → significant spatial autocorrelation
- H2: Random → no spatial autocorrelation

## Pattern 6: Causal Inference

**Question type:** "Does X cause Y?" (hardest)

**Methods:**
- Quasi-experimental designs
- Instrumental variables
- Difference-in-differences
- Causal graphs + do-calculus

**Warning:** Observational data rarely proves causation. Be careful with claims.

## Method Selection Checklist

- [ ] Method matches hypothesis structure
- [ ] Method appropriate for data type
- [ ] Sample size sufficient for method
- [ ] Assumptions checkable (normality, independence, etc.)
- [ ] Result interpretable for domain
- [ ] Alternative methods considered

## Method Object Template

```json
{
  "id": "meth_001",
  "type": "method",
  "state": "applied",
  "attributes": {
    "name": "Hotspot Analysis",
    "category": "spatial",
    "description": "Identify clusters using Getis-Ord Gi*",
    "parameters": {
      "distance_band": "auto",
      "significance": 0.05
    },
    "assumptions": [
      "Spatial independence tested",
      "Sufficient spatial variation"
    ],
    "limitations": [
      "Sensitive to distance band choice",
      "Requires sufficient spatial coverage"
    ],
    "code_path": "objects/method/meth_001.py"
  }
}
```