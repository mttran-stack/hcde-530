# C6 — Data Visualization Competency Claim

My analysis uses **two complementary visual structures**:

1. **Horizontal bar chart** to compare the **mean rating** for each hospital-related factor.
2. **Scatter plot** to show how **each patient’s** personable **and** operational composites relate to **overall satisfaction in RM** on one plot (two colors)—so association is visible in the clouds of points, not only as a single number.
---

## Chart-type justification

- **Horizontal bars:** Visually putting categories on the **y-axis** made the chart easier to read, especially because the dataset has **many aspect names** (long labels). While `df.describe()` can show which category has the highest mean through numeric values on a table, the horizontal bar chart lets a reader **compare ranks at a glance** and see how far apart the highest and lowest aspects are on the same scale.

- **Scatter plot:** `patient_satisfaction.png` puts **two patient-level series on one figure**: each person contributes a **Personable** composite and an **Operational** composite, both plotted against **satisfaction in RM** on the y-axis, with **color** distinguishing the two composites and **opacity** so dense overlap reads as darker regions. The y-axis shows **discrete satisfaction bands** (for example stacked near whole-number ratings), while the x-axis is the **mean composite rating (1–5)** for that patient—so you can compare how the two clouds sit relative to each other without collapsing everything into a single bar of means. That matches the chart’s title and legend (“Composite”: Personable vs Operational) and keeps the **unit of analysis** at the patient for an association-style read.

| Artifact | What it shows |
|----------|----------------|
| `hospital_factors.png` | Mean rating by hospital aspect (horizontal bars, sorted for comparison). |
| `patient_satisfaction.png` | Each patient: personable **and** operational composites vs satisfaction in RM (one scatter, two colors). |

- **Notebook (code + outputs + markdown):** `week 6/mp1a/week6_mp1_starter copy.ipynb` — patient satisfaction load, composites, correlations, and Plotly figures used for exports (in progress).

---

## Interpretation (what the charts support)

**Hospital aspects (horizontal bars):** The bar chart supports a prioritization story—which aspects of care sit higher or lower on average in this sample—so a practitioner or designer can see **where attention might matter most** relative to peers on the same scale.

**Personable and operational vs satisfaction (scatter):** The scatterplot overlays both composite types so you can compare **two clouds** on the same axes—whether one kind of composite tracks satisfaction differently from the other, and how much **spread** and **overlap** there is at each satisfaction level. I still report correlations in the notebook where appropriate, but the figure carries the **shape** of that comparison.

Overall, these visualizations help paint the picture of what is ranked higher in satisfaction and how these hospital-related factors are correlated to the mean of patient satisfaction.