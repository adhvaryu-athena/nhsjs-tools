---
student_name: "Test Scholar"
manuscript_title: "Sample Revised Manuscript for Builder Tests"
reviewer_decision_date: "2026-05-10"
target_submit_date: "2026-05-17"
voice_overrides: []
---

# Sample Revised Manuscript for Builder Tests

## Abstract

This study examines a fabricated phenomenon for the sole purpose of exercising the revision builder. The findings are not real. {{+We added this sentence to demonstrate an inserted insertion that also carries a citation[[CITE:1]].+}} {{-This sentence will be removed at acceptance.-}} The remainder of this paragraph is unchanged.

## Introduction

Prior work shows the effect exists in three settings[[CITE:1,2,3]]. {{-We previously claimed the effect was universal-}}{{+We now claim the effect is consistent with our observations+}} across those settings. Further support comes from recent reviews[[CITE:4]].

{{RESTRUCTURE:
OLD:
This paragraph had a structural issue. It mixed methodology and motivation in a way that the reviewer found confusing. The point was eventually made but only after two readings.
NEW:
This paragraph has been restructured. The motivation is stated first, followed by the methodology. The point is now made in a single reading.
}}

## Methods

We collected synthetic data with no real instrument. Analyses were run in Python 3.10 using NumPy 1.26 and pandas 2.2[[CITE:5]]. {{+All scripts are available at the project repository (URL to be added on acceptance).+}}

## Results

The effect was observed in 4 of 5 settings (80%, 95% CI 28%–99%, p = 0.19)[[CITE:6]]. {{+This is consistent with prior reports[[CITE:1,2]] but the small sample limits inference.+}}

## Discussion

{{-Our findings prove the effect is real.-}}{{+Our findings are consistent with the effect being real but cannot establish causation given the observational design.+}} Future work with a pre-registered design would strengthen the claim[[CITE:7]].

## References

1. Sample A. First Reference Title. Journal of Examples. Vol. 1, pg. 1-10, 2024.
2. Sample B. Second Reference Title. Journal of Examples. Vol. 2, pg. 11-20, 2024.
3. Sample C. Third Reference Title. Journal of Examples. Vol. 3, pg. 21-30, 2024.
4. Sample D. A Review of Sample Effects. Annual Review of Examples. Vol. 1, pg. 1-25, 2025.
5. Harris CR et al. Array programming with NumPy. Nature. Vol. 585, pg. 357-362, 2020. DOI: 10.1038/s41586-020-2649-2.
6. Sample E. The Fifth Reference. Journal of Examples. Vol. 5, pg. 41-50, 2025.
7. Sample F. Pre-registration in Sample Studies. Journal of Examples. Vol. 6, pg. 51-60, 2025.
