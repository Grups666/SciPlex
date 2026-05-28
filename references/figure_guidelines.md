# Figure Guidelines

## Purpose of Figures

Figures are not decoration. They **communicate evidence**.

Every figure should:
- Answer a specific question
- Show a pattern that words cannot convey
- Support a claim in your argument

## Figure Types by Purpose

| Question | Figure Type |
|----------|-------------|
| How is X distributed? | Histogram, boxplot, violin |
| Is X different from Y? | Comparison plot, effect size |
| Is X related to Y? | Scatter plot, regression line |
| What are the patterns? | Heatmap, cluster dendrogram |
| Where are the patterns? | Map, spatial plot |
| How does X change over time? | Time series, trend line |
| What are the categories? | Confusion matrix, type breakdown |

## Design Standards

**Essential elements:**
- Title or caption explaining what it shows
- Axis labels with units
- Legend if multiple elements
- Colorblind-friendly palette (viridis, colorbrewer)

**Avoid:**
- 3D plots (harder to read)
- Rainbow colormap (misleading)
- Too much in one figure (split instead)
- Tiny text, illegible labels

**Resolution:**
- Publication: 300 DPI minimum
- Web: PNG or SVG

## Caption Template

```
Figure X. [What this shows]. [Key pattern observed]. 
[Method used to generate]. [Data source].
```

Example:
```
Figure 1. Spatial distribution of water-use hotspots (red) across 
global land areas. Hotspots concentrated in major agricultural regions 
(South Asia, North China Plain). Defined as cells where total water 
use exceeds 75th percentile (WaterGAP v2.2e, 2000-2019 mean).
```

## Figure Object Template

```json
{
  "id": "fig_001",
  "type": "figure",
  "state": "finalized",
  "attributes": {
    "name": "Hotspot Distribution",
    "purpose": "Show where water-use hotspots are located",
    "type": "map",
    "caption": "Figure 1. Spatial distribution...",
    "data_source": "exp_001",
    "key_pattern": "Hotspots concentrated in agricultural regions",
    "format": "png",
    "dimensions": [1600, 900],
    "file_path": "objects/figure/fig_001.png"
  }
}
```

## Review Your Figures

After generating a figure:

1. **Open it and look at it** — Don't just assume it worked
2. **Describe what you see** — Write down the pattern
3. **Check against hypothesis** — Does this support/refute?
4. **Decide: good enough?** — Or need refinement?

Bad figure = misleading conclusion. Always inspect.