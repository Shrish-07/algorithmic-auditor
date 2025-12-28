# HMDA Algorithmic Audit — Baseline Specification

## Dataset
- Source: HMDA Loan Application Records (2024 subset)
- Rows (post-cleaning): 41,855
- Protected attribute: Applicant race (grouped)
- Target: Loan approval decision

## Model
- Classifier: Tree-based ensemble
- Inputs: Financial and loan characteristics only
- Race explicitly excluded from training features
- AUC: ~0.79

## Audit Stages
1. Base rate analysis
2. Predictive model training
3. Fairness evaluation:
   - Demographic Parity
   - Equal Opportunity
4. Explainability:
   - Global feature importance
   - Group-wise SHAP
5. Counterfactual fairness:
   - Race-swapping intervention

## Key Findings
- Significant approval rate disparities across race groups
- Disparities persist in model predictions
- Counterfactual race substitution yields zero prediction change

## Interpretation
The model is counterfactually fair with respect to race but reproduces structural disparities present in correlated financial features.

## Baseline Tag
This document corresponds to git tag: `baseline-hmda-2024`