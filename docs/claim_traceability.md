# Claim Traceability Matrix

**Repo:** ethical-alpha-audit-paper-2-threshold-justification  
**Updated:** 2026-04-12 (independent QA session noted below)  
**Source manuscript:** `inputs/manuscript.pdf` (JMIR Medical Informatics submission draft)  
**Supplementary:** `inputs/supplementary.pdf`  
**Claims:** 22 | **Verified:** traceability to repo artifacts (notebooks / `src/` / `outputs/`)

RTM targets in `config/trace_map.json` use manuscript internal IDs (D-01, Q-01, F-01, T-01, …). This document adds **P2-Cxx** IDs for portfolio QA.


## P2 Stage 1 — Claim extraction (authoritative source: `inputs/manuscript.docx`)

**ID namespace note:** Stage 1 uses `P2-C01`–`P2-C194` grounded in `inputs/manuscript.docx`. The legacy `## Enumeration` section below retains an older `P2-C01`–`P2-C22` engineer-authored mapping to notebooks and outputs; treat these as **separate registers** until explicitly reconciled.

This section records **claim extraction only** (status `EXTRACTED`). It does **not** assert verification against repo outputs.

### Manuscript fingerprint (extraction run)

| Field | Value |
| --- | --- |
| Repo HEAD (ethical-alpha-audit-paper-2-threshold-justification) | `8d42c5d8d979f8c63eab18afec0e804529648313` |
| Manuscript file | `inputs/manuscript.docx` |
| Manuscript SHA-256 | `1250B1D07EF9D1F626F7522FD2B04AD5D9DE3BD8841E29F9A7565AEBA2E2D64A` |
| Extraction date/time | `2026-04-19T14:25:06+01:00` |

### Claim register (Stage 1)

| Claim ID | Claim Type | Manuscript Location | Claim Text | Initial Evidence Target | Status |
| --- | --- | --- | --- | --- | --- |
| P2-C01 | QUAL | Title | Scope Conditions for Non-Compensatory Governance Gates: A Theory-Testing Monte Carlo Simulation. | TO_BE_MAPPED | EXTRACTED |
| P2-C02 | QUAL | Title | Article positioned as a simulation study targeting JMIR Medical Informatics. | TO_BE_MAPPED | EXTRACTED |
| P2-C03 | QUAL | Abstract (Background) | Clinical AI governance frameworks recognise the need for explicit deployment decision rules. | TO_BE_MAPPED | EXTRACTED |
| P2-C04 | QUAL | Abstract (Background) | The comparative safety properties of alternative decision architectures remain empirically unevaluated. | TO_BE_MAPPED | EXTRACTED |
| P2-C05 | QUAL | Abstract (Background) | FUTURE-AI defines lifecycle principles for trustworthy AI but does not specify the institutional decision rule converting heterogeneous governance evidence into binary deployment authorisation. | TO_BE_MAPPED | EXTRACTED |
| P2-C06 | METHOD | Abstract (Objective) | The study evaluates, as a theory-testing simulation, deployment safety outcomes of non-compensatory (conjunctive) governance gates compared with weighted composite scoring and a permissive baseline. | notebooks/01_primary_simulation.ipynb; src/run_simulation.py | EXTRACTED |
| P2-C07 | SCOPE | Abstract (Objective) | Analyses are framed under a primary model of evidence heterogeneity. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C08 | METHOD | Abstract (Objective) | Threshold sensitivity and noise robustness analyses are conducted to characterise stability of the gate safety advantage across calibration and measurement conditions. | notebooks/02_sensitivity_and_noise.ipynb; outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv | EXTRACTED |
| P2-C09 | METHOD | Abstract (Methods) | Methods use Monte Carlo simulation of 1,000 clinical AI tools with latent safety states and observed evidence across five governance domains. | notebooks/01_primary_simulation.ipynb; src/run_simulation.py | EXTRACTED |
| P2-C10 | QUANT | Abstract (Methods) | A portfolio of 1,000 tools is selected to provide sufficient statistical power for detecting small differences in unsafe deployment rates (target precision: 95% CI half-width ≤0.5 percentage points at the expected event rate) while remaining within plausible institutional portfolio scales for a national health system. | TO_BE_MAPPED | EXTRACTED |
| P2-C11 | QUAL | Abstract (Methods) | The primary model specifies unsafe tools with heterogeneous evidence profiles (strong in visible, weak in latent domains). | TO_BE_MAPPED | EXTRACTED |
| P2-C12 | METHOD | Abstract (Methods) | Two simulated sensitivity analyses are conducted: threshold sensitivity (gate thresholds varied ±40% of default values) and noise robustness (observation noise SD 0.01–0.20). | notebooks/02_sensitivity_and_noise.ipynb; outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv | EXTRACTED |
| P2-C13 | SCOPE | Abstract (Methods) | Three additional scope conditions—uniform failure, random failure, and partial heterogeneity—are characterised analytically with verification simulations (Multimedia Appendix 2). | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C14 | METHOD | Abstract (Methods) | Rules compared include non-compensatory gates, weighted composite scoring at matched and moderate thresholds, and a majority-rule baseline. | TO_BE_MAPPED | EXTRACTED |
| P2-C15 | SCOPE | Abstract (Methods) | Simulation code and parameters are available in the public repository [15]. | reproduce_all.py; README.md; inputs/manuscript.docx citation [15] | EXTRACTED |
| P2-C16 | QUANT | Abstract (Results) | Under the primary heterogeneous model, non-compensatory gates achieved a 28.5% deployment rate with zero unsafe deployments in the simulated runs under the specified conditions. | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C17 | QUANT | Abstract (Results) | At a moderate composite threshold (calibrated to produce a 62.7% deployment rate), the unsafe deployment rate was 0.9% (95% CI: 0.4%–1.6%), with 1.4% of deployed tools carrying latent unsafe status. | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C18 | QUANT | Abstract (Results) | Gates maintained zero unsafe deployments across the majority of the threshold sensitivity range and across all noise robustness analyses under the specified conditions, with small non-zero rates observed at the lowest threshold multipliers. | notebooks/02_sensitivity_and_noise.ipynb; outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv | EXTRACTED |
| P2-C19 | QUANT | Abstract (Results) | The permissive baseline produced a 2.2% unsafe deployment rate. | outputs/data/metrics_summary.json; outputs/tables/table2_unsafe_rates.csv; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C20 | QUANT | Abstract (Results) | Under verification simulations of additional scope conditions, gates permitted small but non-zero unsafe deployment rates under random failure (0.9%) and partial heterogeneity (0.8%) conditions. | outputs/data/verification_summary.csv; notebooks/03_verification_simulations.ipynb | EXTRACTED |
| P2-C21 | QUAL | Abstract (Results) | Some unsafe tools stochastically passed all five domain thresholds when failures were not systematically concentrated in latent domains. | TO_BE_MAPPED | EXTRACTED |
| P2-C22 | QUAL | Abstract (Results) | Analytical scope-condition characterisation indicates that the gate advantage over composite scoring diminishes when unsafe tools fail uniformly across all domains. | TO_BE_MAPPED | EXTRACTED |
| P2-C23 | QUAL | Abstract (Conclusions) | Non-compensatory governance gates are designed to provide structural protection against unsafe deployment when governance evidence is heterogeneous across domains, as demonstrated within the simulated model. | TO_BE_MAPPED | EXTRACTED |
| P2-C24 | QUAL | Abstract (Conclusions) | The gate advantage diminishes when unsafe tools fail uniformly, reducing to the permissive-baseline comparison only. | TO_BE_MAPPED | EXTRACTED |
| P2-C25 | SCOPE | Abstract (Conclusions) | These scope conditions provide guidance for institutions evaluating whether their evidence environment makes gate adoption appropriate. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C26 | SCOPE | Abstract (Conclusions) | The work sets the research agenda for empirical validation using real-world AI portfolio data. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C27 | QUAL | Introduction | Regulatory instruments for clinical AI clarify what governance evidence must be collected but are largely silent on the decision rule that converts heterogeneous evidence into binary deployment authorisation [1–6]. | TO_BE_MAPPED | EXTRACTED |
| P2-C28 | QUANT | Introduction | FUTURE-AI was developed by 117 experts across 50 countries and published in 2025, defining 30 best practices spanning fairness, universality, traceability, usability, robustness, and explainability across the full AI lifecycle [7]. | TO_BE_MAPPED | EXTRACTED |
| P2-C29 | QUAL | Introduction | FUTURE-AI specifies what must be governed without prescribing how accumulated evidence should crystallise into a binary institutional deployment decision. | TO_BE_MAPPED | EXTRACTED |
| P2-C30 | QUAL | Introduction | In the absence of an explicit deployment decision rule—a gap documented across widely used governance instruments [14]—institutions risk aggregating governance evidence into composite scores or weighted dashboards. | TO_BE_MAPPED | EXTRACTED |
| P2-C31 | QUAL | Introduction | Composite-style aggregation replicates compensatory logic characteristic of multi-criteria decision analysis and composite indicator frameworks [19,20], where strong performance in one domain can offset critical gaps in another. | TO_BE_MAPPED | EXTRACTED |
| P2-C32 | METHOD | Introduction | A non-compensatory gate architecture has been proposed as an alternative [14]: five prerequisite governance domains each define a minimum evidence floor, and failure at any single gate blocks deployment regardless of aggregate performance. | TO_BE_MAPPED | EXTRACTED |
| P2-C33 | COMPARATIVE | Introduction | Gigerenzer and Goldstein [8] demonstrated that non-compensatory heuristics can outperform compensatory models in environments with asymmetric consequences. | TO_BE_MAPPED | EXTRACTED |
| P2-C34 | COMPARATIVE | Introduction | Leveson [9] extended this logic to safety-critical systems engineering where single-point failures can produce irreversible harm. | TO_BE_MAPPED | EXTRACTED |
| P2-C35 | QUAL | Introduction | Conjunctive screening rules are standard practice in contexts where single-point failures produce irreversible harm (e.g., surgical safety checklist, aviation pre-flight checklists, nuclear safety barrier models) [16]. | TO_BE_MAPPED | EXTRACTED |
| P2-C36 | QUAL | Introduction | The simulation properties of the gate architecture—comparative safety performance, behaviour under different evidence distributions, and conditions where its advantage holds or disappears—have not been empirically evaluated. | TO_BE_MAPPED | EXTRACTED |
| P2-C37 | SCOPE | Introduction | The FDA's January 2025 draft guidance on AI-enabled device software functions [17] articulates a Total Product Lifecycle approach. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C38 | QUAL | Introduction | Emerging evidence suggests existing adverse event reporting systems are insufficient for AI/ML devices [18]. | TO_BE_MAPPED | EXTRACTED |
| P2-C39 | METHOD | Introduction | This study is explicitly framed as a theory-testing simulation and does not generate empirical data about real institutional AI portfolios. | TO_BE_MAPPED | EXTRACTED |
| P2-C40 | QUAL | Introduction | The study tests the logical properties of the gate decision rule under a range of modelled evidence conditions. | TO_BE_MAPPED | EXTRACTED |
| P2-C41 | QUAL | Introduction | The study's purpose is threefold: characterise conditions where gate logic retains a safety advantage over composite scoring; identify analytically scope conditions where that advantage diminishes or disappears; and set the research agenda for real-world pilot studies testing whether institutional evidence environments resemble the heterogeneous model. | TO_BE_MAPPED | EXTRACTED |
| P2-C42 | METHOD | Methods (Study design) | Monte Carlo simulation compares three governance decision rules applied to a portfolio of 1,000 clinical AI tools. | notebooks/01_primary_simulation.ipynb; src/run_simulation.py | EXTRACTED |
| P2-C43 | METHOD | Methods (Study design) | Each tool has a latent safety state (safe or unsafe) and observed evidence scores across five governance domains. | notebooks/01_primary_simulation.ipynb; src/run_simulation.py | EXTRACTED |
| P2-C44 | METHOD | Methods (Study design) | Simulation implemented in Python (v3.11). | notebooks/01_primary_simulation.ipynb; src/run_simulation.py | EXTRACTED |
| P2-C45 | SCOPE | Methods (Code availability) | Full simulation code and parameter configurations are available in the public repository [15] (archived via Zenodo; DOI: https://doi.org/10.5281/zenodo.19499791). | reproduce_all.py; README.md; inputs/manuscript.docx citation [15] | EXTRACTED |
| P2-C46 | QUAL | Methods (Code availability) | The repository includes a Quick Start guide (README.md) that allows a reviewer to reproduce the primary heterogeneous model, threshold sensitivity analysis, and noise robustness analysis in under ten minutes using a single command. | reproduce_all.py; README.md | EXTRACTED |
| P2-C47 | QUANT | Methods (Portfolio generation) | The portfolio comprised 30% high-risk tools and 70% standard-risk tools, with latent unsafe probabilities of 0.35 and 0.15 respectively. | outputs/data/metrics_summary.json; src/params_default.json | EXTRACTED |
| P2-C48 | QUAL | Methods (Portfolio generation) | The 30/70 high-risk/standard-risk split reflects the emerging composition of institutional AI portfolios under the EU AI Act (Article 6 and Annex III) versus lower-risk operational tools [3]. | TO_BE_MAPPED | EXTRACTED |
| P2-C49 | QUAL | Methods (Portfolio generation) | The latent unsafe probability of 0.35 for high-risk tools is informed by evidence that a substantial proportion of clinical prediction models fail external validation and related regulatory surveillance notes [6]. | TO_BE_MAPPED (literature / citation claims) | EXTRACTED |
| P2-C50 | QUAL | Methods (Portfolio generation) | The 0.15 rate for standard-risk tools reflects the expectation that lower-complexity systems are less vulnerable to deployment-context failure. | TO_BE_MAPPED | EXTRACTED |
| P2-C51 | SCOPE | Methods (Portfolio generation) | Portfolio size justification is provided in Supplementary Appendix D. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C52 | SCOPE | Methods (Portfolio generation) | Calibration rationale and supplementary sensitivity analyses are reported in Supplementary Appendix E. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C53 | SCOPE | Methods (Portfolio generation) | Simulation parameter mapping to NHS governance artefacts is provided in Supplementary Appendix D. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C54 | QUAL | Methods (Scope-condition motivation) | If unsafe tools failed uniformly or randomly across all five domains, the structural advantage of conjunctive logic over composite scoring would diminish or disappear—a scope condition explicitly tested. | TO_BE_MAPPED | EXTRACTED |
| P2-C55 | METHOD | Methods (Sensitivity scenarios) | Threshold sensitivity varies gate thresholds between 60% and 140% of default values (17 steps), with composite scoring calibrated to match the gate deployment rate at each step. | outputs/data/sensitivity_thresholds.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C56 | METHOD | Methods (Sensitivity scenarios) | Noise robustness varies observation noise SD from 0.01 to 0.20 across 15 steps, with composite calibrated to match gate deployment rate at each noise level. | outputs/data/sensitivity_noise.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C57 | METHOD | Methods (Sensitivity scenarios) | Three scope conditions are characterised analytically and verified through supplementary simulations (Multimedia Appendix 2): uniform failure, random failure, and partial heterogeneity. | TO_BE_MAPPED | EXTRACTED |
| P2-C58 | METHOD | Methods (Sensitivity scenarios) | Uniform failure means unsafe tools fail equally across all five governance domains. | TO_BE_MAPPED | EXTRACTED |
| P2-C59 | METHOD | Methods (Sensitivity scenarios) | Random failure means unsafe tools fail in a randomly assigned combination of two to four domains per tool. | TO_BE_MAPPED | EXTRACTED |
| P2-C60 | METHOD | Methods (Sensitivity scenarios) | Partial heterogeneity means unsafe tools fail in three of five latent-tendency domains (equity, accountability, monitoring) but not in the two visible-tendency domains (safety, documentation). | TO_BE_MAPPED | EXTRACTED |
| P2-C61 | METHOD | Methods (Decision rules) | Non-compensatory gates permit deployment only if all five domains pass risk-tiered thresholds. | TO_BE_MAPPED | EXTRACTED |
| P2-C62 | QUANT | Methods (Decision rules) | A constrained override pathway is modelled for Gates 2–4 with 10% invocation probability. | outputs/data/metrics_summary.json; src/run_simulation.py | EXTRACTED |
| P2-C63 | METHOD | Methods (Decision rules) | Weighted composite scoring is evaluated at (a) a matched threshold calibrated to the gate deployment rate and (b) a moderate threshold calibrated to produce approximately 2.2× the gate deployment rate (resulting in a 62.7% deployment rate). | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C64 | QUAL | Methods (Decision rules) | It is hypothesised that institutional deployment pressures typically produce composite thresholds closer to the moderate level than to the matched level; this is an assumption of the simulation, not an observed parameter. | TO_BE_MAPPED | EXTRACTED |
| P2-C65 | METHOD | Methods (Decision rules) | Permissive baseline deploys if at least three of five gates pass (majority rule). | TO_BE_MAPPED | EXTRACTED |
| P2-C66 | SCOPE | Methods (Decision rules) | Figure 1 provides a schematic comparison of the three decision rules. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C67 | METHOD | Methods (Outcomes) | Primary outcome is unsafe deployment rate (proportion of deployed tools with latent unsafe status). | TO_BE_MAPPED | EXTRACTED |
| P2-C68 | METHOD | Methods (Outcomes) | Secondary outcomes include overall deployment rate and gate failure pattern analysis. | TO_BE_MAPPED | EXTRACTED |
| P2-C69 | METHOD | Methods (Outcomes) | All simulation results are reported as point estimates with bootstrap 95% confidence intervals (1,000 bootstrap resamples). | outputs/data/metrics_summary.json; src/run_simulation.py | EXTRACTED |
| P2-C70 | SCOPE | Methods (Epic case) | A case scenario was constructed based on published external validation data for a widely deployed sepsis prediction model [10]. | outputs/data/epic_case_outputs.csv; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C71 | SCOPE | Methods (Epic case) | The Epic Sepsis case scenario and evidence score assignments are detailed in Supplementary Appendix T. | outputs/data/epic_case_outputs.csv; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C72 | QUAL | Results (Primary outcome note) | The moderate composite threshold produces a 0.9% unsafe deployment rate alongside a 1.4% contamination rate; the difference reflects the larger denominator (all tools vs deployed tools only). | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C73 | QUANT | Results (Primary outcome) | Under the primary heterogeneous evidence model, non-compensatory gates achieved a 28.5% deployment rate with zero unsafe deployments in the simulated runs under the specified conditions. | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C74 | QUAL | Results (Primary outcome) | Composite scoring matched this safety level only at a matched threshold replicating the gates' structural selectivity. | TO_BE_MAPPED | EXTRACTED |
| P2-C75 | QUANT | Results (Primary outcome) | At the moderate composite threshold (62.7% deployment rate), the unsafe deployment rate was 0.9% (95% CI: 0.4%–1.6%), and 1.4% of deployed tools carried latent unsafe status. | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C76 | QUANT | Results (Primary outcome) | The permissive baseline produced a 2.2% unsafe deployment rate. | outputs/data/metrics_summary.json; outputs/tables/table2_unsafe_rates.csv; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C77 | QUAL | Results (Selectivity note) | The 28.5% deployment rate under the gate architecture is a product of the high-risk parameter values used in this simulation to test safety limits. | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C78 | QUAL | Results (Selectivity note) | In institutional portfolios with higher-quality tools, the gate deployment rate would naturally rise; selectivity is conditional on portfolio composition, not fixed by the architecture itself. | TO_BE_MAPPED | EXTRACTED |
| P2-C79 | QUANT | Results (Sensitivity 1: threshold) | Across the threshold-multiplier range tested (60%–140% of default values), non-compensatory gates maintained zero unsafe deployments across the majority of the range, with minimal non-zero unsafe deployment rates observed at the lowest threshold multipliers in the simulated runs under the specified model conditions. | outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C80 | QUANT | Results (Sensitivity 1: threshold) | Composite scoring, calibrated to match the gate deployment rate at each threshold level, produced small non-zero unsafe deployment rates at the lowest threshold multipliers, which fell to zero across the remainder of the tested range. | outputs/data/sensitivity_thresholds.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C81 | QUAL | Results (Sensitivity 1: threshold) | At matched deployment rates the two methods converge on safety; the gate advantage emerges when composite scoring operates at a higher deployment rate (institutional deployment pressure). | outputs/data/sensitivity_thresholds.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C82 | QUANT | Results (Sensitivity 2: noise) | Across observation noise levels from SD = 0.01 to SD = 0.20, non-compensatory gates maintained zero unsafe deployments in the simulated runs under the specified model conditions. | outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C83 | QUANT | Results (Sensitivity 2: noise) | Composite scoring calibrated to match the gate deployment rate at each noise level produced zero unsafe deployments throughout the noise range. | outputs/data/sensitivity_noise.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C84 | QUAL | Results (Sensitivity 2: noise) | Matched-threshold comparison does not reveal a noise-driven divergence at equivalent deployment rates within the primary heterogeneous model. | outputs/data/sensitivity_noise.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C85 | METHOD | Results (Verification scope) | Three scope conditions are characterised through verification simulations (Multimedia Appendix 2), confirming and refining analytical predictions. | outputs/data/verification_summary.csv; notebooks/03_verification_simulations.ipynb | EXTRACTED |
| P2-C86 | QUANT | Results (Uniform failure) | Under uniform failure, gates maintained zero unsafe deployments while composite scoring at the moderate threshold permitted 1.2% unsafe deployments (95% CI: 0.6%–2.0%). | outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv; notebooks/02_sensitivity_and_noise.ipynb | EXTRACTED |
| P2-C87 | QUANT | Results (Uniform failure) | At the matched threshold under uniform failure, the gate advantage over composite scoring was nearly eliminated (both ≈0%). | outputs/data/verification_summary.csv; notebooks/03_verification_simulations.ipynb | EXTRACTED |
| P2-C88 | QUANT | Results (Random failure) | Under random failure, gates permitted 0.9% unsafe deployments (95% CI: 0.4%–1.5%). | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C89 | QUANT | Results (Random failure) | Under random failure, composite scoring at the moderate threshold permitted 6.1% (95% CI: 4.7%–7.7%). | outputs/data/verification_summary.csv; notebooks/03_verification_simulations.ipynb | EXTRACTED |
| P2-C90 | QUANT | Results (Partial heterogeneity) | Under partial heterogeneity, gates permitted 0.8% unsafe deployments (95% CI: 0.3%–1.4%). | outputs/data/verification_summary.csv; notebooks/03_verification_simulations.ipynb | EXTRACTED |
| P2-C91 | QUANT | Results (Partial heterogeneity) | Under partial heterogeneity, composite scoring at the moderate threshold permitted 7.4% (95% CI: 5.9%–9.0%). | outputs/data/verification_summary.csv; notebooks/03_verification_simulations.ipynb | EXTRACTED |
| P2-C92 | QUAL | Results (Mechanism) | Non-zero gate failure rates under random and partial heterogeneity arise because some unsafe tools, by chance, draw sufficiently high evidence scores across all five domains to pass all gates simultaneously. | TO_BE_MAPPED | EXTRACTED |
| P2-C93 | QUAL | Results (Mechanism) | Under the primary heterogeneous model, unsafe tools are systematically disadvantaged in latent domains, making simultaneous passage of all five gates effectively impossible. | TO_BE_MAPPED | EXTRACTED |
| P2-C94 | QUAL | Results (Mechanism) | Under random and partial conditions, systematic concentration of failures is attenuated, allowing a small proportion of unsafe tools to stochastically satisfy all five thresholds. | TO_BE_MAPPED | EXTRACTED |
| P2-C95 | QUAL | Results (Mechanism) | The zero-unsafe-deployment result is specific to the heterogeneous evidence model and should not be interpreted as a universal property of conjunctive decision rules. | TO_BE_MAPPED | EXTRACTED |
| P2-C96 | SCOPE | Results (Tables) | Table 1 summarises scope conditions alongside the primary simulation result. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C97 | SCOPE | Results (Tables) | Table 2 reports unsafe deployment rates across evidence distribution scenarios and decision rules. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C98 | QUAL | Results (Table 1 narrative) | Heterogeneous (primary) evidence distribution is associated with a strong gate safety advantage mechanism: compensation mechanism exploitable; conjunctive rule prevents it structurally. | outputs/tables/table1_scope_conditions.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C99 | QUAL | Results (Table 1 narrative) | Partial heterogeneity yields a moderate confirmed gate advantage (gates 0.8% vs composite moderate 7.4%). | outputs/tables/table1_scope_conditions.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C100 | QUAL | Results (Table 1 narrative) | Random failure yields a small–moderate confirmed gate advantage (gates 0.9% vs composite moderate 6.1%). | outputs/tables/table1_scope_conditions.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C101 | QUAL | Results (Table 1 narrative) | Uniform failure yields no confirmed gate advantage versus composite (no compensation mechanism; architectures equivalent). | outputs/tables/table1_scope_conditions.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C102 | QUAL | Results (Table 1 narrative) | Noise sensitivity is characterised as robust: gate safety maintained across the noise range at matched deployment rates. | outputs/tables/table1_scope_conditions.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C103 | QUAL | Results (Table 1 narrative) | The uniform failure condition specifies the critical boundary for the gate safety advantage. | outputs/tables/table1_scope_conditions.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C104 | QUANT | Results (Table 2: Heterogeneous primary) | For the heterogeneous primary model scenario, non-compensatory gates have 0.0% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C105 | QUANT | Results (Table 2: Heterogeneous primary) | For the heterogeneous primary model scenario, composite (moderate) shows 0.9–1.4% unsafe deployment rate (as presented in the table). | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C106 | QUANT | Results (Table 2: Heterogeneous primary) | For the heterogeneous primary model scenario, composite (matched) has 0.0% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C107 | QUANT | Results (Table 2: Heterogeneous primary) | For the heterogeneous primary model scenario, the permissive baseline has 2.2% unsafe deployment rate. | outputs/data/metrics_summary.json; outputs/tables/table2_unsafe_rates.csv; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C108 | QUANT | Results (Table 2: Uniform failure verified) | For uniform failure (verified), non-compensatory gates have 0.0% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C109 | QUANT | Results (Table 2: Uniform failure verified) | For uniform failure (verified), composite (moderate) has 1.2% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C110 | QUANT | Results (Table 2: Uniform failure verified) | For uniform failure (verified), composite (matched) is approximately 0% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C111 | QUANT | Results (Table 2: Uniform failure verified) | For uniform failure (verified), the permissive baseline has 4.0% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C112 | QUANT | Results (Table 2: Random failure verified) | For random failure (verified), non-compensatory gates have 0.9% unsafe deployment rate. | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C113 | QUANT | Results (Table 2: Random failure verified) | For random failure (verified), composite (moderate) has 6.1% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C114 | QUANT | Results (Table 2: Random failure verified) | For random failure (verified), composite (matched) has 0.9% unsafe deployment rate. | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C115 | QUANT | Results (Table 2: Random failure verified) | For random failure (verified), the permissive baseline has 8.6% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C116 | QUANT | Results (Table 2: Partial heterogeneity verified) | For partial heterogeneity (verified), non-compensatory gates have 0.8% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C117 | QUANT | Results (Table 2: Partial heterogeneity verified) | For partial heterogeneity (verified), composite (moderate) has 7.4% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C118 | QUANT | Results (Table 2: Partial heterogeneity verified) | For partial heterogeneity (verified), composite (matched) has 1.5% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C119 | QUANT | Results (Table 2: Partial heterogeneity verified) | For partial heterogeneity (verified), the permissive baseline has 9.4% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C120 | QUANT | Results (Table 2: Noise robustness low SD) | For noise robustness at low SD (=0.01), non-compensatory gates have 0.0% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C121 | QUANT | Results (Table 2: Noise robustness low SD) | For noise robustness at low SD (=0.01), composite (matched) has 0.0% unsafe deployment rate and permissive baseline 1.9% (as presented). | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C122 | QUANT | Results (Table 2: Noise robustness high SD) | For noise robustness at high SD (=0.20), non-compensatory gates have 0.0% unsafe deployment rate. | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C123 | QUANT | Results (Table 2: Noise robustness high SD) | For noise robustness at high SD (=0.20), composite (matched) has 0.0% unsafe deployment rate and permissive baseline 2.8% (as presented). | outputs/tables/table2_unsafe_rates.csv; notebooks/05_tables_and_summary.ipynb | EXTRACTED |
| P2-C124 | SCOPE | Results (Epic illustration) | An illustrative Epic Sepsis Model case scenario is provided in Supplementary Appendix K. | outputs/data/epic_case_outputs.csv; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C125 | QUAL | Results (Epic illustration) | Under the gate architecture, the case failed all five gates with immediate transparency about which domains drove the refusal. | outputs/data/epic_case_outputs.csv; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C126 | SCOPE | Results (Epic illustration) | The illustration indicates architectural consequences of published evidence scores; it is not a formal empirical audit of the named system. | outputs/data/epic_case_outputs.csv; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C127 | METHOD | Results (Companion historical replay) | The companion historical replay study processed 12 documented AI governance failures through the identical GovernancePolicyEngine used in this simulation. | TO_BE_MAPPED (companion historical replay / P4) | EXTRACTED |
| P2-C128 | QUANT | Results (Companion historical replay) | Under the moderate profile, non-compensatory gates rejected 11 of 12 known failures (91.7% sensitivity in the retrospective Core-12 dataset) in the Core-12 replay. | TO_BE_MAPPED | EXTRACTED |
| P2-C129 | QUANT | Results (Companion historical replay) | The expanded evaluation across 20 core-equivalent failure cases and 12 FDA-cleared control devices yielded sensitivity 1.000 and specificity 1.000, with the caveat that perfect separation reflects structural properties applied to cases with documented multi-gate governance deficiency. | TO_BE_MAPPED | EXTRACTED |
| P2-C130 | QUANT | Results (Companion historical replay) | The safety gate was binding in 83% of cases. | TO_BE_MAPPED | EXTRACTED |
| P2-C131 | QUANT | Results (Companion historical replay) | Every rejected case failed at least 2 gates (mean: 2.6). | TO_BE_MAPPED | EXTRACTED |
| P2-C132 | QUAL | Results (Companion historical replay) | Two cases (Google Flu Trends, Uber AV) demonstrated compensatory masking predicted by this simulation (composite scores exceeding approval threshold due to strong evidence/traceability offsetting critical safety deficiencies). | TO_BE_MAPPED | EXTRACTED |
| P2-C133 | QUANT | Results (Companion historical replay) | Governance outcomes were stable under Monte Carlo perturbation of evidence uncertainty bounds (100% stability across 200 iterations per case). | TO_BE_MAPPED | EXTRACTED |
| P2-C134 | QUAL | Results (Companion historical replay) | These replay results provide structured case-level evidence consistent with the simulation's predictions about safety advantages under heterogeneous evidence conditions. | TO_BE_MAPPED | EXTRACTED |
| P2-C135 | SCOPE | Discussion / extensions | Parameter and evidence sensitivity are treated as formal experimental axes (Supplementary Appendix F). | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C136 | QUAL | Discussion | The most important finding is characterisation of when the gate advantage disappears, not the zero unsafe deployment rate under the primary model (the latter is theoretically predicted by the heterogeneous evidence pattern design). | TO_BE_MAPPED | EXTRACTED |
| P2-C137 | QUAL | Discussion | Under uniform failure, gate logic and composite scoring achieve equivalent safety outcomes. | TO_BE_MAPPED | EXTRACTED |
| P2-C138 | QUAL | Discussion | This scope condition provides an honest account of limits and defines the empirical question for real-world pilots about governance evidence heterogeneity. | TO_BE_MAPPED | EXTRACTED |
| P2-C139 | COMPARATIVE | Discussion | The study sits within theory-testing simulation traditions where conjunctive screening can outperform compensatory models under asymmetric loss functions [8]. | TO_BE_MAPPED | EXTRACTED |
| P2-C140 | QUAL | Discussion | The evaluated gate architecture is compatible with FUTURE-AI-like frameworks and provides a decision-theoretic layer for combining accumulated evidence into deployment authorisation. | TO_BE_MAPPED | EXTRACTED |
| P2-C141 | QUAL | Discussion | Under heterogeneous evidence conditions modelled here, conjunctive logic prevents compensation effects that composite scoring permits. | TO_BE_MAPPED | EXTRACTED |
| P2-C142 | QUAL | Discussion (Committee translation) | If tools under review exhibit heterogeneous evidence profiles, the gate architecture provides structural protection that composite scoring does not. | TO_BE_MAPPED | EXTRACTED |
| P2-C143 | QUANT | Discussion (Encoding robustness) | An encoding perturbation analysis across the companion historical replay dataset reports 239/240 non-baseline perturbation evaluations stable (99.6%) under single-feature perturbation within a ±0.10 stress-test envelope. | TO_BE_MAPPED (companion historical replay / P4) | EXTRACTED |
| P2-C144 | QUAL | Discussion (Encoding robustness) | This computational robustness check does not substitute for independent inter-rater reliability. | TO_BE_MAPPED | EXTRACTED |
| P2-C145 | SCOPE | Discussion | Empirical heterogeneity testing using PhysioNet 2019 clinical data is described in Supplementary Appendix B. | inputs/experiment_pack/; TO_BE_MAPPED | EXTRACTED |
| P2-C146 | QUAL | Discussion | Both models exhibited heterogeneous evidence profiles (feature spread > 0.47), consistent with the simulation's heterogeneous evidence model. | TO_BE_MAPPED | EXTRACTED |
| P2-C147 | SCOPE | Discussion | Enriched triangulation evidence details are provided in Supplementary Appendix A. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C148 | SCOPE | Discussion | The testable prediction regarding empirical heterogeneity is detailed in Supplementary Appendix O. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C149 | QUAL | Discussion (Limits of applicability) | If unsafe tools fail broadly and uniformly across domains, the compensation mechanism gates prevent does not arise and composite scoring achieves equivalent safety. | TO_BE_MAPPED | EXTRACTED |
| P2-C150 | QUAL | Discussion (Limits of applicability) | If gate thresholds are set below the level at which genuine failures would be detected, conjunctive rules provide no structural protection regardless of decision logic. | TO_BE_MAPPED | EXTRACTED |
| P2-C151 | QUAL | Discussion (Limits of applicability) | If evidence scores are inflated (e.g., vendor self-reporting in latent domains), gates may pass tools that would fail under independent assessment; auditor independence and verification are preconditions. | TO_BE_MAPPED | EXTRACTED |
| P2-C152 | SCOPE | Discussion | A counterfactual analysis of composite threshold calibration is provided in Supplementary Appendix Q. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C153 | SCOPE | Discussion | The companion Viewpoint [14] describes the gate architecture and its override pathway. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C154 | METHOD | Discussion | The pilot research design specifies retrospective and prospective assessment of a cohort against all five gates, recording observed domain evidence scores by tool. | TO_BE_MAPPED | EXTRACTED |
| P2-C155 | QUAL | Discussion | If unsafe or borderline tools score systematically higher in audit-visible domains than latent ones, the heterogeneous model is empirically supported and the gate architecture's safety advantage over composite scoring is warranted in that institutional context. | TO_BE_MAPPED | EXTRACTED |
| P2-C156 | SCOPE | Discussion | The pilot is embeddable within existing NHS AI oversight committee structures and requires no change to clinical care pathways. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C157 | COMPARATIVE | Discussion | The companion governance friction optimisation study uses NSGA-II, Sobol sensitivity analysis, and decision curve analysis to address threshold calibration tradeoffs rather than whether gates outperform composite scoring. | TO_BE_MAPPED | EXTRACTED |
| P2-C158 | QUAL | Discussion | Although submitted as a paired contribution, the simulation study is designed to stand independently and does not depend on acceptance of the Viewpoint. | TO_BE_MAPPED | EXTRACTED |
| P2-C159 | SCOPE | Discussion | This work represents a theory-testing simulation and does not constitute prospective real-world validation. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C160 | SCOPE | Discussion | The gate architecture evaluated is fully specified within this paper's Methods; the companion Viewpoint is not required for understanding or evaluating the simulation findings. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C161 | SCOPE | Discussion (Empirical grounding update) | The companion historical replay study has been extended with a control cohort comprising 12 FDA-cleared AI-enabled medical devices encoded under the identical 5-gate non-compensatory schema. | TO_BE_MAPPED (companion historical replay / P4) | EXTRACTED |
| P2-C162 | QUAL | Discussion (Empirical grounding update) | All 20 failure cases have been upgraded to a core-equivalent encoding standard with uniform feature schema, per-feature triangulation, and gate traceability. | TO_BE_MAPPED | EXTRACTED |
| P2-C163 | QUANT | Discussion (Empirical grounding update) | Classification metrics are reported as TP=20, FN=0, TN=12, FP=0 (sensitivity 1.000, specificity 1.000). | TO_BE_MAPPED | EXTRACTED |
| P2-C164 | QUAL | Discussion (Empirical grounding update) | This empirical grounding supports the simulation scope condition that non-compensatory gates discriminate documented governance failures from regulatory-cleared systems, derived from structured retrospective datasets, not prospective validation. | TO_BE_MAPPED | EXTRACTED |
| P2-C165 | SCOPE | Discussion (Empirical grounding update) | Three unresolved gaps (device-specific control encoding differentiation, pending IRR, excluded Band B/C cases) are documented in Encoding Comparison Summary v1. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C166 | SCOPE | Limitations | Findings are bounded by simulation parameters; the heterogeneity pattern is theory-motivated and plausible but not derived from observed institutional data. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C167 | QUAL | Limitations | Portfolio composition parameters are grounded in published evidence but not validated against an observed institutional AI portfolio. | TO_BE_MAPPED | EXTRACTED |
| P2-C168 | QUANT | Limitations | Supplementary calibration sensitivity analyses indicate primary findings are robust across portfolio compositions from 10/90 through 50/50 (five compositions) with gates maintaining zero unsafe deployments across all five tested compositions. | outputs/data/calibration_portfolio.csv; notebooks/04_calibration_sensitivity.ipynb | EXTRACTED |
| P2-C169 | QUANT | Limitations | Across unsafe probability levels, gates maintained zero unsafe deployments for four of five levels tested (as stated). | outputs/data/calibration_unsafe_prob.csv; notebooks/04_calibration_sensitivity.ipynb | EXTRACTED |
| P2-C170 | METHOD | Limitations | Override invocation was modelled with a fixed 10% probability; actual rates are unknown. | TO_BE_MAPPED | EXTRACTED |
| P2-C171 | QUAL | Limitations | Verification simulations confirmed predicted directions but refined that under random failure and partial heterogeneity gates no longer achieve zero unsafe deployments (0.9% and 0.8%). | outputs/data/metrics_summary.json; notebooks/01_primary_simulation.ipynb | EXTRACTED |
| P2-C172 | SCOPE | Limitations | Given commercial interests, independent replication using empirically derived evidence profiles from diverse institutions is explicitly encouraged. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C173 | SCOPE | Limitations | The repository Quick Start guide is provided specifically to lower the barrier to independent replication. | reproduce_all.py; README.md; inputs/manuscript.docx citation [15] | EXTRACTED |
| P2-C174 | METHOD | Validation hierarchy | Evidence supporting the architecture spans Tier 4 (computational simulation) and Tier 3 (structured retrospective replay), while Tier 2 and Tier 1 evaluations remain outstanding. | TO_BE_MAPPED | EXTRACTED |
| P2-C175 | SCOPE | Validation hierarchy | No finding in the present study should be interpreted as evidence from Tier 1 or Tier 2. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C176 | QUAL | Patient-level consequence pathway | Deploying an unsafe system exposes patients to clinical harm; blocking a safe system denies clinical benefit. | TO_BE_MAPPED | EXTRACTED |
| P2-C177 | METHOD | Patient-level consequence pathway | The simulation characterises rates of false positives (blocking safe tools) and false negatives (deploying unsafe tools) as patient-relevant metrics. | TO_BE_MAPPED | EXTRACTED |
| P2-C178 | SCOPE | Scope boundaries | The gate architecture does not address sociotechnical integration failures, procurement governance, clinical trial substitution where required, workflow integration, clinician trust calibration, or real-time human factors. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C179 | QUAL | Conclusions | Analytical scope-condition characterisation (confirmed by verification simulations) indicates the gate advantage over composite scoring diminishes when unsafe tools fail uniformly across all governance domains. | TO_BE_MAPPED | EXTRACTED |
| P2-C180 | QUAL | Conclusions | The gate advantage over permissive governance persists across all evidence conditions (as stated). | TO_BE_MAPPED | EXTRACTED |
| P2-C181 | QUAL | Conclusions | Under random failure and partial heterogeneity, gates no longer achieve zero unsafe deployments but maintain substantially lower rates than composite scoring at moderate thresholds. | TO_BE_MAPPED | EXTRACTED |
| P2-C182 | SCOPE | Conclusions | Prospective pilot studies are needed to determine whether institutional evidence environments resemble the heterogeneous model. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C183 | METHOD | Conclusions | A secondary analysis will evaluate decision stability under controlled joint perturbation of threshold parameters and evidence confidence bounds. | TO_BE_MAPPED | EXTRACTED |
| P2-C184 | SCOPE | Declarations (AI use) | Generative AI tools (Claude [Anthropic]) were used for code assistance in simulation implementation, manuscript formatting, and copy-editing. | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C185 | QUAL | Declarations (AI use) | No AI tool was used to design the simulation architecture, select parameters, interpret results, specify scope conditions, or draft the analytical arguments and conclusions. | TO_BE_MAPPED | EXTRACTED |
| P2-C186 | SCOPE | Declarations (AI use) | A complete prompt/response log can be supplied (Multimedia Appendix 3). | inputs/supplementary.docx; TO_BE_MAPPED (appendix anchors) | EXTRACTED |
| P2-C187 | METHOD | Reproducibility statement | Re-execution from identical inputs produces identical outputs. | reproduce_all.py; scripts/validate_outputs.py; TO_BE_MAPPED (engine versioning artefact) | EXTRACTED |
| P2-C188 | QUAL | Reproducibility statement | An earlier public engine implementation drifted from canonical logic (15-feature compensatory formula issues); results here use corrected canonical logic (5-feature weighted compensatory model with bias inversion, locked threshold profiles). | reproduce_all.py; scripts/validate_outputs.py; TO_BE_MAPPED (engine versioning artefact) | EXTRACTED |
| P2-C189 | QUAL | Reproducibility statement | Alternative implementations may produce different results. | TO_BE_MAPPED | EXTRACTED |
| P2-C190 | METHOD | Multimedia Appendix (PhysioNet) | Governance vectors from two sepsis prediction models evaluated on PhysioNet 2019 clinical data (5,000 patients, 188,453 patient-hours) were used to test the central heterogeneity prediction. | inputs/experiment_pack/; TO_BE_MAPPED | EXTRACTED |
| P2-C191 | QUANT | Multimedia Appendix (PhysioNet) | Both models exhibited heterogeneous evidence profiles (feature spread > 0.30; GradientBoosting spread = 0.474, RandomForest spread = 0.468). | inputs/experiment_pack/; TO_BE_MAPPED | EXTRACTED |
| P2-C192 | QUAL | Multimedia Appendix (PhysioNet) | GradientBoosting scored strongly on bias (0.912 normalised) but weakly on safety (0.438), while RandomForest showed the reverse pattern on calibration (0.886) versus safety (0.418). | inputs/experiment_pack/; TO_BE_MAPPED | EXTRACTED |
| P2-C193 | QUANT | Multimedia Appendix (PhysioNet) | Ranking stability analysis confirmed governance rankings were stable under 90% of scoring weight perturbations (±20%), with rank changes when bias or calibration weights were substantially altered. | TO_BE_MAPPED | EXTRACTED |
| P2-C194 | QUAL | Multimedia Appendix (PhysioNet) | These empirical findings are consistent with, though not a formal validation of, the simulation's prediction about conjunctive protection under heterogeneous real governance evidence. | TO_BE_MAPPED | EXTRACTED |


### P2 Stage 2 — Traceability mapping (ADDED)

Stage 2 adds **trace columns** keyed by `Claim ID`. The Stage 1 table above remains authoritative for **Claim Type**, **Manuscript Location**, **Claim Text**, **Initial Evidence Target**, and **Status = EXTRACTED**; Stage 2 records **Trace Status (Stage 2)** only and does **not** promote claims to VERIFIED.

**Vocabulary:** `TRACED_REPO` (paths under this repository); `TRACED_MANUSCRIPT_ONLY` (manuscript/supplementary narrative without a required quantitative output join in this pass); `TRACED_UPSTREAM` (external repository, Zenodo record, cited third-party sources, or **P4** historical replay); `GAP` (no satisfactory local anchor identified conservatively); `TO_VERIFY_LATER` (plausible anchor; appendix anchor or cross-artifact alignment still required).

#### Stage 2 summary

- **Total claims mapped:** 194 (`P2-C01`–`P2-C194`).
- **Counts by Trace Status (Stage 2):** `TRACED_REPO`: 95; `TRACED_MANUSCRIPT_ONLY`: 48; `TRACED_UPSTREAM`: 31; `TO_VERIFY_LATER`: 17; `GAP`: 3.
- **Claims still GAP:** `P2-C145`, `P2-C183`, `P2-C193`.
- **Claims dependent on P4 (explicit) or other non-repo upstream:** `P2-C127`–`P2-C134`, `P2-C143`, `P2-C161`–`P2-C163` (P4 / companion historical replay). Additional `TRACED_UPSTREAM` claims anchored on manuscript citations / Zenodo / sibling papers: `P2-C15`, `P2-C27`–`P2-C38`, `P2-C45`, `P2-C48`–`P2-C49`, `P2-C139`, `P2-C153`, `P2-C157`.

#### Claim register — Stage 2 trace columns (P2-C01–P2-C194)

| Claim ID | Code Target | Notebook Target | Output / Artefact Target | Dependency Note | Trace Status (Stage 2) |
| --- | --- | --- | --- | --- | --- |
| P2-C01 | — | — | inputs/manuscript.pdf | Title/submission framing in manuscript sources. | TRACED_MANUSCRIPT_ONLY |
| P2-C02 | — | — | inputs/manuscript.pdf | Venue positioning (JMIR Medical Informatics) stated in manuscript metadata. | TRACED_MANUSCRIPT_ONLY |
| P2-C03 | — | — | inputs/manuscript.docx | Cited background framing; not grounded in simulation artefacts. | TRACED_MANUSCRIPT_ONLY |
| P2-C04 | — | — | inputs/manuscript.docx | Cited background framing; not grounded in simulation artefacts. | TRACED_MANUSCRIPT_ONLY |
| P2-C05 | — | — | inputs/manuscript.docx | Cited background framing; not grounded in simulation artefacts. | TRACED_MANUSCRIPT_ONLY |
| P2-C06 | src/run_simulation.py; src/run_verification.py | notebooks/01_primary_simulation.ipynb | — | Compares gates vs composite vs permissive in primary engine path. | TRACED_REPO |
| P2-C07 | src/run_simulation.py (SimConfig.unsafe_gate_profile; primary heterogeneous generator) | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | inputs/supplementary.docx (appendix anchors not machine-verified here). | TRACED_REPO |
| P2-C08 | src/run_simulation.py (threshold/noise sweeps consumed by notebooks) | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv | Sensitivity sweep artefacts per config/trace_map.json. | TRACED_REPO |
| P2-C09 | src/run_simulation.py (simulate_portfolio; GATES) | notebooks/01_primary_simulation.ipynb | outputs/data/simulation_outputs.csv; outputs/data/metrics_summary.json | n_tools and five-domain evidence columns in outputs. | TRACED_REPO |
| P2-C10 | src/run_simulation.py (SimConfig.n_bootstrap; n_tools) | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Precision/half-width narrative maps to supplementary appendix text; CI machinery in engine. | TO_VERIFY_LATER |
| P2-C11 | src/run_simulation.py (unsafe_gate_profile) | notebooks/01_primary_simulation.ipynb | outputs/data/simulation_outputs.csv | Mechanistic heterogeneity for unsafe tools encoded in SimConfig. | TRACED_REPO |
| P2-C12 | src/run_simulation.py | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv | Step counts align Methods; confirm against notebook parameters during verification stage. | TRACED_REPO |
| P2-C13 | src/run_verification.py (simulate_uniform_failure/random/partial) | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | inputs/supplementary.docx (Multimedia Appendix 2 narrative). | TRACED_REPO |
| P2-C14 | src/run_simulation.py; src/run_verification.py (decide_noncomp_gates; decide_weighted_composite; decide_permissive) | notebooks/01_primary_simulation.ipynb (primary); notebooks/03_verification_simulations.ipynb (verification) | outputs/data/metrics_summary.json; outputs/data/verification_summary.csv | Rule implementations in shared engine module. | TRACED_REPO |
| P2-C15 | reproduce_all.py; scripts/run_direct.py | notebooks/01_primary_simulation.ipynb (via harness) | config/expected_outputs.json | Public repo + Zenodo DOI cited in manuscript [15]; Zenodo record outside repo. | TRACED_UPSTREAM |
| P2-C16 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Primary heterogeneous scenario metrics JSON. | TRACED_REPO |
| P2-C17 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Composite (mean) block includes deployment and unsafe rates + bootstrap_ci. | TRACED_REPO |
| P2-C18 | src/run_simulation.py | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_thresholds.csv; outputs/data/sensitivity_noise.csv | Zero unsafe for gates under primary model across sweeps (tabular evidence). | TRACED_REPO |
| P2-C19 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json; outputs/tables/table2_unsafe_rates.csv | Permissive metrics in metrics_summary and assembled Table 2. | TRACED_REPO |
| P2-C20 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | Random/partial non-zero gate unsafe deployments in verification outputs. | TRACED_REPO |
| P2-C21 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv | Mechanistic interpretation of stochastic threshold passage under random/partial generators. | TRACED_REPO |
| P2-C22 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv | Analytical scope claims cross-check verification_summary uniform/near-matched behaviour. | TRACED_REPO |
| P2-C23 | — | — | inputs/manuscript.docx | Discussion/conclusions prose; supplementary cited for scope guidance. | TRACED_MANUSCRIPT_ONLY |
| P2-C24 | — | — | inputs/manuscript.docx | Discussion/conclusions prose; supplementary cited for scope guidance. | TRACED_MANUSCRIPT_ONLY |
| P2-C25 | — | — | inputs/manuscript.docx | Discussion/conclusions prose; supplementary cited for scope guidance. | TRACED_MANUSCRIPT_ONLY |
| P2-C26 | — | — | inputs/manuscript.docx | Discussion/conclusions prose; supplementary cited for scope guidance. | TRACED_MANUSCRIPT_ONLY |
| P2-C27 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C28 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C29 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C30 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C31 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C32 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C33 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C34 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C35 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C36 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C37 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C38 | — | — | inputs/manuscript.docx | Citation-backed narrative; external sources per manuscript reference list. | TRACED_UPSTREAM |
| P2-C39 | — | README.md | inputs/manuscript.docx | Theory-testing / non-empirical framing stated in manuscript. | TRACED_MANUSCRIPT_ONLY |
| P2-C40 | src/run_simulation.py; src/run_verification.py | notebooks/01_primary_simulation.ipynb (primary logic properties) | outputs/data/metrics_summary.json | Logical properties demonstrated via implemented decision rules + outputs. | TRACED_REPO |
| P2-C41 | — | — | inputs/manuscript.docx | Threefold purpose narrative in Introduction. | TRACED_MANUSCRIPT_ONLY |
| P2-C42 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/simulation_outputs.csv; outputs/data/metrics_summary.json | Portfolio size and rule application. | TRACED_REPO |
| P2-C43 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/simulation_outputs.csv | Latent safety + five-domain observed scores columns. | TRACED_REPO |
| P2-C44 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | — | Python 3.11 stated in manuscript; environment pinned in environment.yml (not execution proof). | TO_VERIFY_LATER |
| P2-C45 | reproduce_all.py; scripts/run_direct.py | notebooks/01_primary_simulation.ipynb (via harness) | config/expected_outputs.json | Public repo + Zenodo DOI cited in manuscript [15]; Zenodo record outside repo. | TRACED_UPSTREAM |
| P2-C46 | reproduce_all.py | README.md | — | README Quick Start + reproduce_all orchestration. | TRACED_REPO |
| P2-C47 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json; src/params_default.json | Config echoed in metrics_summary.json config block. | TRACED_REPO |
| P2-C48 | — | — | inputs/manuscript.docx | EU AI Act portfolio composition narrative (citations). | TRACED_UPSTREAM |
| P2-C49 | — | — | inputs/manuscript.docx | Literature-grounded parameter motivation. | TRACED_UPSTREAM |
| P2-C50 | — | — | inputs/manuscript.docx | Qualitative expectation stated in Methods narrative. | TRACED_MANUSCRIPT_ONLY |
| P2-C51 | — | — | inputs/supplementary.docx | Appendix letter references in manuscript bundle only. | TO_VERIFY_LATER |
| P2-C52 | — | — | inputs/supplementary.docx | Appendix letter references in manuscript bundle only. | TO_VERIFY_LATER |
| P2-C53 | — | — | inputs/supplementary.docx | Appendix letter references in manuscript bundle only. | TO_VERIFY_LATER |
| P2-C54 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv | Scope condition tested in verification scenarios. | TRACED_REPO |
| P2-C55 | src/run_simulation.py | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_thresholds.csv | Threshold multiplier sweep data artefact. | TRACED_REPO |
| P2-C56 | src/run_simulation.py | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_noise.csv | Noise SD sweep data artefact. | TRACED_REPO |
| P2-C57 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | inputs/supplementary.docx (appendix crosswalk). | TRACED_REPO |
| P2-C58 | src/run_verification.py | — | — | Docstring + simulate_uniform_failure() implementation. | TRACED_REPO |
| P2-C59 | src/run_verification.py | — | — | Docstring + simulate_random_failure() (rng.integers(2, 5)). | TRACED_REPO |
| P2-C60 | src/run_verification.py | — | — | Docstring + simulate_partial_heterogeneity() failing_gates set. | TRACED_REPO |
| P2-C61 | src/run_simulation.py (decide_noncomp_gates) | notebooks/01_primary_simulation.ipynb | outputs/data/simulation_outputs.csv | Risk-tier thresholds in SimConfig / params JSON. | TRACED_REPO |
| P2-C62 | src/run_simulation.py (override block in decide_noncomp_gates) | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | override_prob=0.1 in config; realised override_rate in metrics. | TRACED_REPO |
| P2-C63 | src/run_simulation.py (set_threshold_to_match_rate; 2.2× cap) | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | composite_thresholds block records matched/moderate thresholds and deployment rates. | TRACED_REPO |
| P2-C64 | — | — | inputs/manuscript.docx | Explicit modelling assumption in manuscript. | TRACED_MANUSCRIPT_ONLY |
| P2-C65 | src/run_simulation.py (decide_permissive; permissive_min_gates_passed) | notebooks/01_primary_simulation.ipynb | outputs/data/simulation_outputs.csv | Majority rule implementation. | TRACED_REPO |
| P2-C66 | — | notebooks/01_primary_simulation.ipynb (figure generation cells) | inputs/supplementary.docx | Figure asset may be supplementary bundle; check notebook outputs paths. | TO_VERIFY_LATER |
| P2-C67 | src/run_simulation.py; src/run_verification.py (compute_metrics) | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | unsafe_deployment_rate definition in engine metrics. | TRACED_REPO |
| P2-C68 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Deployment rates and gate failure patterns in outputs/figures trace_map. | TRACED_REPO |
| P2-C69 | src/run_simulation.py (bootstrap_ci) | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json; outputs/data/verification_results.json | Bootstrap resample count in SimConfig. | TRACED_REPO |
| P2-C70 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/epic_case_outputs.csv | Epic case row generation in primary notebook pipeline. | TRACED_REPO |
| P2-C71 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/epic_case_outputs.csv | inputs/supplementary.docx (Appendix T narrative). | TRACED_REPO |
| P2-C72 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Clarifies denominators in metrics JSON fields. | TRACED_REPO |
| P2-C73 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Duplicate abstract headline numbers in metrics JSON. | TRACED_REPO |
| P2-C74 | — | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_thresholds.csv | Interpretive claim about matched convergence; support via sensitivity tables. | TO_VERIFY_LATER |
| P2-C75 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Moderate composite metrics JSON. | TRACED_REPO |
| P2-C76 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json; outputs/tables/table2_unsafe_rates.csv | Permissive unsafe deployment rate. | TRACED_REPO |
| P2-C77 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Deployment_rate context with configured risk parameters. | TRACED_REPO |
| P2-C78 | — | — | inputs/manuscript.docx | Counterfactual institutional portfolio claim (not a single output field). | TRACED_MANUSCRIPT_ONLY |
| P2-C79 | src/run_simulation.py | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_thresholds.csv | Threshold sweep unsafe deployment columns. | TRACED_REPO |
| P2-C80 | src/run_simulation.py | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_thresholds.csv | Matched composite rows in sensitivity artefact. | TRACED_REPO |
| P2-C81 | — | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_thresholds.csv | Interpretation of matched vs moderate institutional pressure. | TRACED_MANUSCRIPT_ONLY |
| P2-C82 | src/run_simulation.py | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_noise.csv | Noise sweep gate unsafe deployment columns. | TRACED_REPO |
| P2-C83 | src/run_simulation.py | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_noise.csv | Matched composite across noise sweep. | TRACED_REPO |
| P2-C84 | — | notebooks/02_sensitivity_and_noise.ipynb | outputs/data/sensitivity_noise.csv | Interpretation within primary heterogeneous evidence model. | TRACED_MANUSCRIPT_ONLY |
| P2-C85 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | MMA2 label in manuscript for verification scope. | TRACED_REPO |
| P2-C86 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv | Uniform failure scenario row (moderate composite) in verification_summary. | TRACED_REPO |
| P2-C87 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | Uniform failure matched comparison. | TRACED_REPO |
| P2-C88 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | Random failure gates unsafe deployment rate in verification outputs. | TRACED_REPO |
| P2-C89 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | Random failure composite moderate. | TRACED_REPO |
| P2-C90 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | Partial heterogeneity gates. | TRACED_REPO |
| P2-C91 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | Partial heterogeneity composite moderate. | TRACED_REPO |
| P2-C92 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv | Mechanism consistent with stochastic generators. | TRACED_REPO |
| P2-C93 | src/run_simulation.py (unsafe_gate_profile) | notebooks/01_primary_simulation.ipynb | outputs/data/simulation_outputs.csv | Primary heterogeneous unsafe tool design. | TRACED_REPO |
| P2-C94 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv | Random/partial generators attenuate systematic concentration. | TRACED_REPO |
| P2-C95 | — | — | inputs/manuscript.docx | Scope disclaimer in Results/Discussion narrative. | TRACED_MANUSCRIPT_ONLY |
| P2-C96 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table1_scope_conditions.csv | inputs/supplementary.docx (Table 1 placement). | TO_VERIFY_LATER |
| P2-C97 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | inputs/supplementary.docx (Table 2 placement). | TO_VERIFY_LATER |
| P2-C98 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table1_scope_conditions.csv | Assembled scope-condition summary table. | TRACED_REPO |
| P2-C99 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table1_scope_conditions.csv | Assembled scope-condition summary table. | TRACED_REPO |
| P2-C100 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table1_scope_conditions.csv | Assembled scope-condition summary table. | TRACED_REPO |
| P2-C101 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table1_scope_conditions.csv | Assembled scope-condition summary table. | TRACED_REPO |
| P2-C102 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table1_scope_conditions.csv | Assembled scope-condition summary table. | TRACED_REPO |
| P2-C103 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table1_scope_conditions.csv | Assembled scope-condition summary table. | TRACED_REPO |
| P2-C104 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C105 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C106 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C107 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv; outputs/data/metrics_summary.json | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C108 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C109 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C110 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C111 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C112 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv; outputs/data/verification_summary.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C113 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C114 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv; outputs/data/verification_summary.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C115 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C116 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C117 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C118 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C119 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C120 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C121 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C122 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C123 | — | notebooks/05_tables_and_summary.ipynb | outputs/tables/table2_unsafe_rates.csv | Table 2 joins; cross-check verification_summary for scenario-specific rows. | TRACED_REPO |
| P2-C124 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/epic_case_outputs.csv | inputs/supplementary.docx (Appendix K). | TRACED_REPO |
| P2-C125 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/epic_case_outputs.csv | Domain-level refusal fields in epic_case_outputs.csv. | TRACED_REPO |
| P2-C126 | src/run_simulation.py | notebooks/01_primary_simulation.ipynb | outputs/data/epic_case_outputs.csv | Illustration scope disclaimer in manuscript. | TRACED_MANUSCRIPT_ONLY |
| P2-C127 | ethical-alpha-audit-paper-4-historical-replay (P4; not in this repo) | — | — | GovernancePolicyEngine / replay metrics are upstream of P2 outputs. | TRACED_UPSTREAM |
| P2-C128 | ethical-alpha-audit-paper-4-historical-replay (P4; not in this repo) | — | — | GovernancePolicyEngine / replay metrics are upstream of P2 outputs. | TRACED_UPSTREAM |
| P2-C129 | ethical-alpha-audit-paper-4-historical-replay (P4; not in this repo) | — | — | GovernancePolicyEngine / replay metrics are upstream of P2 outputs. | TRACED_UPSTREAM |
| P2-C130 | ethical-alpha-audit-paper-4-historical-replay (P4; not in this repo) | — | — | GovernancePolicyEngine / replay metrics are upstream of P2 outputs. | TRACED_UPSTREAM |
| P2-C131 | ethical-alpha-audit-paper-4-historical-replay (P4; not in this repo) | — | — | GovernancePolicyEngine / replay metrics are upstream of P2 outputs. | TRACED_UPSTREAM |
| P2-C132 | ethical-alpha-audit-paper-4-historical-replay (P4; not in this repo) | — | — | GovernancePolicyEngine / replay metrics are upstream of P2 outputs. | TRACED_UPSTREAM |
| P2-C133 | ethical-alpha-audit-paper-4-historical-replay (P4; not in this repo) | — | — | GovernancePolicyEngine / replay metrics are upstream of P2 outputs. | TRACED_UPSTREAM |
| P2-C134 | ethical-alpha-audit-paper-4-historical-replay (P4; not in this repo) | — | — | GovernancePolicyEngine / replay metrics are upstream of P2 outputs. | TRACED_UPSTREAM |
| P2-C135 | — | — | inputs/supplementary.docx | Supplementary Appendix F pointer. | TO_VERIFY_LATER |
| P2-C136 | — | — | inputs/manuscript.docx | Interpretive emphasis in Discussion. | TRACED_MANUSCRIPT_ONLY |
| P2-C137 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv | Uniform failure equivalence narrative supported by verification outputs. | TRACED_REPO |
| P2-C138 | — | — | inputs/manuscript.docx | Empirical pilot question framing. | TRACED_MANUSCRIPT_ONLY |
| P2-C139 | — | — | inputs/manuscript.docx | Positions within cited theory-testing literature. | TRACED_UPSTREAM |
| P2-C140 | — | — | inputs/manuscript.docx | Compatibility claim with FUTURE-AI-like frameworks. | TRACED_MANUSCRIPT_ONLY |
| P2-C141 | src/run_simulation.py; src/run_verification.py | notebooks/01_primary_simulation.ipynb (mechanism) | outputs/data/metrics_summary.json | Compensation vs conjunctive blocking in implemented scoring. | TRACED_REPO |
| P2-C142 | — | — | inputs/manuscript.docx | Committee translation narrative. | TRACED_MANUSCRIPT_ONLY |
| P2-C143 | ethical-alpha-audit-paper-4-historical-replay (P4) | — | — | Encoding perturbation study not in P2 repo. | TRACED_UPSTREAM |
| P2-C144 | — | — | inputs/manuscript.docx | Methods limitation statement. | TRACED_MANUSCRIPT_ONLY |
| P2-C145 | — | — | inputs/supplementary.docx | PhysioNet appendix described; no PhysioNet pipeline files found under repo root search. | GAP |
| P2-C146 | — | — | inputs/supplementary.docx | Empirical heterogeneity numbers stated in appendix; not reproduced in P2 outputs. | TRACED_MANUSCRIPT_ONLY |
| P2-C147 | — | — | inputs/supplementary.docx | Appendix A pointer. | TO_VERIFY_LATER |
| P2-C148 | — | — | inputs/supplementary.docx | Appendix O pointer. | TO_VERIFY_LATER |
| P2-C149 | — | — | inputs/manuscript.docx | Limits-of-applicability prose. | TRACED_MANUSCRIPT_ONLY |
| P2-C150 | — | — | inputs/manuscript.docx | Limits-of-applicability prose. | TRACED_MANUSCRIPT_ONLY |
| P2-C151 | — | — | inputs/manuscript.docx | Limits-of-applicability prose. | TRACED_MANUSCRIPT_ONLY |
| P2-C152 | — | — | inputs/supplementary.docx | Appendix Q pointer. | TO_VERIFY_LATER |
| P2-C153 | — | — | inputs/manuscript.docx / inputs/supplementary.docx | Companion Viewpoint [14] cross-reference. | TRACED_UPSTREAM |
| P2-C154 | — | — | inputs/manuscript.docx | Pilot design narrative. | TRACED_MANUSCRIPT_ONLY |
| P2-C155 | — | — | inputs/manuscript.docx | Conditional empirical implication statement. | TRACED_MANUSCRIPT_ONLY |
| P2-C156 | — | — | inputs/supplementary.docx | NHS committee embeddability narrative in supplementary/manuscript. | TO_VERIFY_LATER |
| P2-C157 | — | — | inputs/manuscript.docx | Sibling study methods (NSGA-II / Sobol / DCA) described textually. | TRACED_UPSTREAM |
| P2-C158 | — | — | inputs/manuscript.docx | Paired contribution independence statement. | TRACED_MANUSCRIPT_ONLY |
| P2-C159 | — | — | inputs/manuscript.docx | Prospective validation disclaimer. | TRACED_MANUSCRIPT_ONLY |
| P2-C160 | — | — | inputs/manuscript.docx | Companion viewpoint not required statement. | TRACED_MANUSCRIPT_ONLY |
| P2-C161 | P4 historical replay repo | — | — | Control cohort extension outside P2. | TRACED_UPSTREAM |
| P2-C162 | P4 historical replay repo | — | — | Encoding standard upgrade outside P2. | TRACED_UPSTREAM |
| P2-C163 | P4 historical replay repo | — | — | TP/TN/FN/FP table outside P2. | TRACED_UPSTREAM |
| P2-C164 | — | — | inputs/manuscript.docx | Interpretation linking replay to simulation scope (cross-artefact). | TRACED_MANUSCRIPT_ONLY |
| P2-C165 | — | — | inputs/supplementary.docx | Encoding Comparison Summary v1 referenced externally to repo outputs. | TO_VERIFY_LATER |
| P2-C166 | — | — | inputs/manuscript.docx / inputs/supplementary.docx | Simulation bounds narrative. | TRACED_MANUSCRIPT_ONLY |
| P2-C167 | — | — | inputs/manuscript.docx | Parameter grounding disclaimer. | TRACED_MANUSCRIPT_ONLY |
| P2-C168 | src/run_calibration_sensitivity.py | notebooks/04_calibration_sensitivity.ipynb | outputs/data/calibration_portfolio.csv | Portfolio composition sweep output. | TRACED_REPO |
| P2-C169 | src/run_calibration_sensitivity.py | notebooks/04_calibration_sensitivity.ipynb | outputs/data/calibration_unsafe_prob.csv | Unsafe probability sweep output; confirm "four of five" row semantics in Stage 3. | TRACED_REPO |
| P2-C170 | src/run_simulation.py (override_prob) | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | Fixed 10% modelled invocation vs unknown real rates (manuscript limitation). | TRACED_REPO |
| P2-C171 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | Verification outputs quantify 0.9%/0.8% gate unsafe rates under scenarios. | TRACED_REPO |
| P2-C172 | — | — | inputs/manuscript.docx | Replication encouragement statement. | TRACED_MANUSCRIPT_ONLY |
| P2-C173 | reproduce_all.py; README.md | — | — | Quick Start barrier claim tied to harness docs. | TRACED_REPO |
| P2-C174 | — | — | inputs/manuscript.docx | Tiered validation hierarchy narrative spans P2+P4; not single artefact. | TRACED_MANUSCRIPT_ONLY |
| P2-C175 | — | — | inputs/manuscript.docx | Tier disclaimer. | TRACED_MANUSCRIPT_ONLY |
| P2-C176 | — | — | inputs/manuscript.docx | Harm/benefit framing narrative. | TRACED_MANUSCRIPT_ONLY |
| P2-C177 | src/run_simulation.py; src/run_verification.py (compute_metrics) | notebooks/01_primary_simulation.ipynb | outputs/data/metrics_summary.json | False positive/negative proxies via deployment vs latent unsafe flags in outputs. | TRACED_REPO |
| P2-C178 | — | — | inputs/manuscript.docx / inputs/supplementary.docx | Out-of-scope sociotechnical factors list. | TRACED_MANUSCRIPT_ONLY |
| P2-C179 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv | Conclusions tie-back to uniform failure analytical/verification alignment. | TRACED_REPO |
| P2-C180 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/metrics_summary.json | Cross-scenario permissive disadvantage vs gates (tabular). | TRACED_REPO |
| P2-C181 | src/run_verification.py | notebooks/03_verification_simulations.ipynb | outputs/data/verification_summary.csv; outputs/data/verification_results.json | Random/partial gate vs composite moderate comparison. | TRACED_REPO |
| P2-C182 | — | — | inputs/manuscript.docx | Prospective pilots needed statement. | TRACED_MANUSCRIPT_ONLY |
| P2-C183 | — | — | inputs/manuscript.docx | Future secondary analysis proposal (not implemented here). | GAP |
| P2-C184 | — | — | inputs/supplementary.docx | AI use declaration (Claude/Anthropic) in declarations. | TRACED_MANUSCRIPT_ONLY |
| P2-C185 | — | — | inputs/manuscript.docx | Scope of AI assistance disclaimer. | TRACED_MANUSCRIPT_ONLY |
| P2-C186 | — | — | inputs/supplementary.docx | Multimedia Appendix 3 prompt log pointer. | TO_VERIFY_LATER |
| P2-C187 | reproduce_all.py; scripts/validate_outputs.py; scripts/hash_manifest.py | — | config/expected_outputs.json | Deterministic harness + strict/advisory hash policy in expected_outputs.json. | TRACED_REPO |
| P2-C188 | scripts/validate_outputs.py; reproduce_all.py | — | README.md (reproducibility notes) | Engine correction narrative not fully encoded in a single machine-readable proof artefact. | TO_VERIFY_LATER |
| P2-C189 | — | — | inputs/manuscript.docx | General disclaimer on alternative implementations. | TRACED_MANUSCRIPT_ONLY |
| P2-C190 | — | — | inputs/supplementary.docx | Multimedia appendix PhysioNet study not present as executable pipeline in this repo snapshot. | TRACED_MANUSCRIPT_ONLY |
| P2-C191 | — | — | inputs/supplementary.docx | Multimedia appendix PhysioNet study not present as executable pipeline in this repo snapshot. | TRACED_MANUSCRIPT_ONLY |
| P2-C192 | — | — | inputs/supplementary.docx | Multimedia appendix PhysioNet study not present as executable pipeline in this repo snapshot. | TRACED_MANUSCRIPT_ONLY |
| P2-C193 | — | — | inputs/supplementary.docx | Ranking stability / weight perturbation analysis not found as named artefact in repo tree snapshot. | GAP |
| P2-C194 | — | — | inputs/supplementary.docx | Multimedia appendix PhysioNet study not present as executable pipeline in this repo snapshot. | TRACED_MANUSCRIPT_ONLY |

> **Namespace boundary (explicit — legacy register):** The section `## Enumeration` below begins a **separate legacy register** that reuses IDs `P2-C01`–`P2-C22` for engineer-authored notebook/output mappings. Those IDs **do not** align row-for-row with Stage 1 `P2-C01`–`P2-C194`. Keep namespaces isolated unless a future crosswalk is published.

### Extraction summary (Stage 1)

- **Total claims extracted:** 194
- **Count by claim type:** QUANT: 53, QUAL: 70, METHOD: 31, SCOPE: 36, COMPARATIVE: 4
- **Ambiguous claims / later trace resolution:**
  - Claims citing the **companion historical replay**, expanded cohort metrics, encoding perturbation stability, and **P4**-sourced figures require explicit cross-repository trace mapping (placeholder `TO_BE_MAPPED (companion historical replay / P4)`).
  - Claims anchored only to **Supplementary / Multimedia appendices** (e.g., A–T, MMA2–3) need stable in-repo anchors (typically `inputs/supplementary.docx`) beyond first-pass placeholders.
  - **Table 2** reports composite (moderate) as a range (`0.9–1.4%`) for the heterogeneous primary row; split notebook joins for moderate vs contamination-style metrics may be needed during trace mapping.
  - **Limitations** text referencing **four of five** unsafe-probability sweep outcomes requires careful alignment to `outputs/data/calibration_unsafe_prob.csv` row semantics.
  - **Bibliographic / external regulatory** statements (cited instruments and third-party publications) are extracted as claims but are not expected to trace to simulation code outputs.


---

## Enumeration

**CLAIM EXTRACTION COMPLETE: 22 claims identified for P2.**

| Claim ID | Manuscript-grounded statement (paraphrase) | Primary evidence (repo) | Notebook / module | Key outputs |
|----------|--------------------------------------------|-------------------------|-------------------|-------------|
| P2-C01 | Monte Carlo simulation of 1,000 clinical AI tools with latent safety state and five-domain evidence; theory-testing frame | Engine config `n_tools`, design in Methods | `notebooks/01_primary_simulation.ipynb`, `src/run_simulation.py` | `outputs/data/simulation_outputs.csv`, `outputs/data/metrics_summary.json` |
| P2-C02 | Portfolio mix 30% high-risk / 70% standard-risk reflects institutional composition narrative | `p_high_risk`, risk tiers in config | `src/run_simulation.py`, `src/params_default.json` | `metrics_summary.json` → `config` |
| P2-C03 | Latent unsafe probabilities 0.35 (high-risk) and 0.15 (standard-risk) | `p_unsafe_high`, `p_unsafe_standard` | `src/run_simulation.py` | `simulation_outputs.csv`, `metrics_summary.json` |
| P2-C04 | Non-compensatory gates: five domains, risk-tiered thresholds; override on gates 2–4 at modelled invocation rate | Threshold + override parameters | `src/run_simulation.py` | `metrics_summary.json` (override rates) |
| P2-C05 | Weighted composite at matched threshold (to gate deploy rate) and moderate threshold (~2.2× gate rate, capped) | `set_threshold_to_match_rate`, 2.2× rule | `src/run_simulation.py`, `scripts/run_direct.py` | `metrics_summary.json` → `composite_thresholds` |
| P2-C06 | Permissive baseline: majority rule (≥3 of 5 gates) | `decide_permissive` | `src/run_simulation.py` | `simulation_outputs.csv`, metrics |
| P2-C07 | Primary heterogeneous model: gates ~28.5% deployment; **zero** unsafe deployments; moderate composite unsafe deployment ~0.9% with CI; ~1.4% unsafe among deployed | Point estimates + bootstrap | `01_primary_simulation.ipynb` | `metrics_summary.json`, figures |
| P2-C08 | Permissive baseline ~2.2% unsafe deployment rate under primary model | Metrics column `Permissive` | `01_primary_simulation.ipynb` | `metrics_summary.json`, `outputs/tables/table2_unsafe_rates.csv` |
| P2-C09 | Threshold sensitivity: multipliers 60–140% of default (17 steps); gate safety under primary model | Sweep implementation | `02_sensitivity_and_noise.ipynb` | `outputs/data/sensitivity_thresholds.csv`, `fig5_*` |
| P2-C10 | Noise robustness: observation SD 0.01–0.20 (15 steps in engine); matched composite calibration at each level | `noise_robustness` | `02_sensitivity_and_noise.ipynb` | `outputs/data/sensitivity_noise.csv`, `fig6_*` |
| P2-C11 | Extended noise rows (low/high SD) for Table 2 noise section | `noise_extended` generation | `02_sensitivity_and_noise.ipynb`, `scripts/run_direct.py` | `outputs/data/noise_extended.csv` |
| P2-C12 | Verification scenarios: uniform failure, random failure, partial heterogeneity — rates vs composite (moderate/matched) and permissive | Scenario definitions | `03_verification_simulations.ipynb`, `src/run_verification.py` | `verification_summary.csv`, `verification_results.json`, `fig_verification_*` |
| P2-C13 | Uniform failure: gate advantage vs moderate composite collapses toward matched comparison (manuscript Table 1–2 narrative) | Scenario outputs | `03_verification_simulations.ipynb` | `verification_summary.csv`, `table1_scope_conditions.csv` |
| P2-C14 | Random failure: small non-zero unsafe rate under gates; higher under moderate composite | Scenario outputs | `03_verification_simulations.ipynb` | `verification_summary.csv`, tables |
| P2-C15 | Partial heterogeneity: non-zero gate unsafe rate; composite moderate higher | Scenario outputs | `03_verification_simulations.ipynb` | `verification_summary.csv`, tables |
| P2-C16 | Calibration sensitivity: portfolio composition and unsafe-probability sweeps (supplementary / robustness narrative) | Formal axes in appendix reference | `04_calibration_sensitivity.ipynb`, `src/run_calibration_sensitivity.py` | `calibration_portfolio.csv`, `calibration_unsafe_prob.csv`, `fig_portfolio_*`, `fig_unsafe_prob_*` |
| P2-C17 | Table 1: scope-condition summary (mechanism column aligned to manuscript) | Assembled from primary + verification | `05_tables_and_summary.ipynb` | `outputs/tables/table1_scope_conditions.csv` |
| P2-C18 | Table 2: unsafe deployment rates across scenarios and rules | Joins primary metrics + verification + noise | `05_tables_and_summary.ipynb` | `outputs/tables/table2_unsafe_rates.csv` |
| P2-C19 | Epic Sepsis case scenario: under gates, fails all five domains with transparent domain-level refusal | `epic_case_row`, decisions | `01_primary_simulation.ipynb` | `epic_case_outputs.csv`, `fig4_epic_case.*` |
| P2-C20 | Bootstrap 95% CIs (1,000 resamples) for rates | `bootstrap_ci`, `n_bootstrap` | `src/run_simulation.py` | `metrics_summary.json`, `verification_results.json` |
| P2-C21 | Reproducibility: single-command pipeline and manifest validation | Harness | `reproduce_all.py`, `scripts/validate_outputs.py`, `scripts/hash_manifest.py` | `logs/actual_manifest.json`, `config/expected_outputs.json` |
| P2-C22 | Aggregated supplementary numeric report (appendix alignment) | Reporter | `src/report_supplementary.py` | `outputs/logs/supplementary_report.txt` |

### Manuscript-only / sibling-repo claims (no P2 code path)

The manuscript cites the **companion historical replay** (Core-12, expanded cohort, control devices). Those numerical results are produced in **P4** (`ethical-alpha-audit-paper-4-historical-replay`), not in this repository. Treat as **cross-paper traceability**; do not infer P2 outputs validate P4 metrics.

---

## RTM crosswalk (selected)

| P2 claim | trace_map.json RTM targets (examples) |
|----------|--------------------------------------|
| P2-C01, P2-C07 | D-01, D-02, Q-01–Q-10, F-02–F-05 |
| P2-C09 | D-04, Q-27, F-06 |
| P2-C10, P2-C11 | D-05, Q-25, Q-26, F-07 |
| P2-C12–P2-C15 | D-06, D-07, Q-11–Q-24, F-08 |
| P2-C16 | D-08, D-09, Q-30, Q-31, F-09, F-10 |
| P2-C17 | T-01 |
| P2-C18 | T-02 |
| P2-C19 | D-03, Q-28, Q-29, F-05 |
| P2-C22 | supplementary log (no RTM id) |

---

## Status

All listed claims are **grounded** in `inputs/manuscript.pdf` and mapped to **existing** pipeline artifacts. Discrepancies between manuscript prose and regenerated numbers should trigger **escalation**, not silent retuning of simulation logic.

### Independent QA — 2026-04-12 (first post-remediation)

**Harness (this session):** `python -m pytest tests/ -q` → 6 passed. `python reproduce_all.py` → all five notebooks executed via `scripts/notebook_runner.py`; `scripts/hash_manifest.py` and `scripts/validate_outputs.py` → **VALIDATION PASSED** (strict `hash_mode` entries matched after regeneration). `scripts/export_html.py` → 5/5 HTML exports OK.

**Session `VERIFIED` (numeric / structural — artefact evidence only):** the following match the paraphrased quantitative claims when checked against regenerated `outputs/data/metrics_summary.json`, `outputs/tables/table2_unsafe_rates.csv`, `outputs/data/verification_summary.csv`, and `outputs/data/epic_case_outputs.csv` after the run above:

| Claim | Session verification |
|-------|----------------------|
| P2-C01 | **VERIFIED:** `config.n_tools` = 1000 in `metrics_summary.json`. |
| P2-C02 | **VERIFIED:** `p_high_risk` = 0.3 in `metrics_summary.json` `config`. |
| P2-C03 | **VERIFIED:** `p_unsafe_high` = 0.35, `p_unsafe_standard` = 0.15 in `config`. |
| P2-C04 | **VERIFIED:** override block present (`override_rate` 0.012, `n_overrides` 12 under Gates); gate thresholds in `config`. |
| P2-C05 | **VERIFIED:** `composite_thresholds.gate_deploy_rate` 0.285 matches Gates deployment rate; moderate composite thresholds present. |
| P2-C07 | **VERIFIED:** Gates `deployment_rate` 0.285, `unsafe_deployment_rate` 0.0; Composite (mean) `unsafe_deployment_rate` 0.009 with bootstrap CI [0.004, 0.016]; `unsafe_among_deployed` ≈ 0.01435. |
| P2-C08 | **VERIFIED:** Permissive `unsafe_deployment_rate` 0.022; `table2_unsafe_rates.csv` primary row Permissive 2.2%. |
| P2-C12–P2-C15 | **VERIFIED:** scenario rows present in `verification_summary.csv` with ordering consistent with the paraphrases (e.g. Uniform Failure Gates unsafe 0.0 vs moderate 0.012). |
| P2-C19 | **VERIFIED:** `epic_case_outputs.csv` EPIC row: five domains failed, `deploy_gate` = 0. |
| P2-C20 | **VERIFIED:** `bootstrap_ci` block populated in `metrics_summary.json` (1000-resample CIs as implemented). |
| P2-C21 | **VERIFIED:** full `reproduce_all.py` run completed successfully this session. |
| P2-C22 | **VERIFIED:** `outputs/logs/supplementary_report.txt` regenerated; strict hash check passed in `validate_outputs.py`. |

**Not promoted to session `VERIFIED`:** manuscript wording was **not** re-extracted from the PDF in this run (grounding table above remains engineer-authored). **P2-C09–C11, P2-C16–C18:** pipeline and strict output hashes passed; per-step numeric manuscript alignment was not independently re-checked beyond spot-check of `table2_unsafe_rates.csv` / verification tables. **Companion historical replay:** remains **cross-repo** per the manuscript-only section above.

**Non-blocking observation:** nine PDF figure paths in `config/expected_outputs.json` use `hash_mode: "advisory"` and **warned** on hash mismatch after regeneration (PNG hashes were not reported as mismatched in this run); tabular/JSON strict entries matched.


### P2 Stage 4 — Validation ONLY (ADDED)

**Validation date:** `2026-04-19`  
**Scope:** Read-only cross-check of **generated outputs** and **manifest policy** against Stage 1 claim text and Stage 2 trace targets. **No claim promoted to VERIFIED** in this section. **Execution success** (Stage 3: pytest, `reproduce_all.py`, strict hash validation) is **not** treated as proof that every manuscript quantitative sentence matches the regenerated artefacts.

#### Evidence files consulted (this pass)

- `outputs/data/metrics_summary.json`
- `outputs/data/verification_summary.csv`
- `outputs/data/sensitivity_thresholds.csv`
- `outputs/data/sensitivity_noise.csv`
- `outputs/data/noise_extended.csv`
- `outputs/tables/table2_unsafe_rates.csv`
- `outputs/tables/table1_scope_conditions.csv`
- `outputs/data/calibration_portfolio.csv`
- `outputs/data/calibration_unsafe_prob.csv`
- `config/expected_outputs.json` (hash_mode policy for figures)

---

#### 1) Outputs vs claims

**Verdict (threshold-sensitivity family P2-C18 / P2-C79 / P2-C80; active): PASS** — Stage 4 (1) threshold re-validation **δ2** (2026-04-19): plain-text cross-check of `inputs/manuscript.docx` against frozen `outputs/data/sensitivity_thresholds.csv` and `outputs/data/sensitivity_noise.csv` (read-only; no notebook re-execution, no output or manifest changes).

**Verdict (first pass, archival): FAIL** — Superseded for the three IDs above; the table below records **prior** manuscript/register wording vs the same CSV audit trail.

**Supported (spot-check, conservative):** Primary heterogeneous headline quantities in Stage 1 align with `metrics_summary.json` and `outputs/tables/table2_unsafe_rates.csv` (e.g. Gates deployment rate `0.285`, Gates `unsafe_deployment_rate` `0.0`; Composite (mean) deployment `0.627`, `unsafe_deployment_rate` `0.009`, bootstrap unsafe CI `[0.004, 0.016]`; Permissive `unsafe_deployment_rate` `0.022`). Verification scenario rows in `verification_summary.csv` align with Table 2 percentages for uniform / random / partial rows (e.g. Random Failure Gates `0.009`, Composite (moderate) `0.061`; Partial Gates `0.008`, Composite (moderate) `0.074`).

**Contradicted claims (manuscript / register wording vs regenerated `outputs/data/sensitivity_thresholds.csv`):**

| Claim ID | Issue |
| --- | --- |
| **P2-C18** | States gates maintained **zero** unsafe deployments across **full** threshold sensitivity **and** noise robustness under specified conditions. **Noise:** `outputs/data/sensitivity_noise.csv` shows `gate_unsafe_deploy` `0.0` at every listed `obs_noise_sd` (consistent with the noise half of the claim). **Threshold:** at `threshold_multiplier` **`0.6`** the file records `gate_unsafe_deploy` **`0.002`** and at **`0.65`** **`0.001`** (non-zero). So the threshold-sweep half of the claim is **not** supported as written for the full `0.6`–`1.4` range. |
| **P2-C79** | Same threshold-sweep “zero across 60%–140%” narrative; **contradicted** at `0.6` and `0.65` by the same columns in `sensitivity_thresholds.csv`. |
| **P2-C80** | States matched composite also maintained **zero** unsafe deployments **throughout** the threshold range. `sensitivity_thresholds.csv` shows **non-zero** `composite_unsafe_deploy` from **`0.6` through `0.75`** (values `0.004`, `0.003`, `0.002`, `0.001` respectively), then `0.0` at higher multipliers. **Contradicted** as written for the full sweep. |

**Note (distinction):** Several other sensitivity **interpretation** claims (e.g. P2-C81) remain manuscript- or notebook-narrative–dependent. The archival **FAIL** above applied only where **prior** prose asserted **zero throughout** the full threshold sweep for gates or matched composite; **δ2** documents corrected wording for **P2-C18**, **P2-C79**, and **P2-C80** consistent with the CSV.

---

#### Stage 4 (1) threshold re-validation delta (2026-04-19; read-only; post–manuscript correction)

**Method:** Plain-text extraction from `inputs/manuscript.docx` (`word/document.xml`). **No** notebook re-execution, **no** output or manifest regeneration; `outputs/data/sensitivity_thresholds.csv` and `outputs/data/sensitivity_noise.csv` treated as the unchanged numerical ground truth.

**Verdict (threshold-sensitivity quantitative claims vs `sensitivity_thresholds.csv`, superseded by δ2 below):** see **delta 2** for the current **PASS** on the P2-C18 / P2-C79 / P2-C80 family.

| Claim ID | Outcome | Notes |
| --- | --- | --- |
| **P2-C18** | **Resolved** (no longer contradicted) | Abstract now qualifies threshold behaviour: zero across the **majority** of the threshold sweep and **all** noise levels, with **small non-zero** rates at the **lowest** multipliers. Matches `gate_unsafe_deploy` non-zero only at multipliers **0.6** and **0.65**, and `gate_unsafe_deploy` **0.0** at every `obs_noise_sd` in `sensitivity_noise.csv`. |
| **P2-C79** | **Resolved** (no longer contradicted) | Results (Sensitivity 1) uses the same qualified pattern for gates (majority of range; minimal non-zero at lowest multipliers). Consistent with the gate columns in `sensitivity_thresholds.csv`. |
| **P2-C80** | **Resolved** (superseded; see δ2) | Earlier pass still saw “zero **throughout**”; **δ2** re-read confirms manuscript correction (see below). |

**Effect on prior section (1) `FAIL` (historical):** Superseded by **delta 2**: all three IDs are reconciled with `sensitivity_thresholds.csv` after the matched-composite sentence correction.

---

#### Stage 4 (1) threshold re-validation **delta 2** (2026-04-19; read-only; post–P2-C80 manuscript correction)

**Method:** Same as delta 1 — plain-text extraction from `inputs/manuscript.docx` only; artefacts unchanged.

**Verdict (threshold-sensitivity quantitative claims vs `sensitivity_thresholds.csv`): PASS**

| Claim ID | Outcome | Notes |
| --- | --- | --- |
| **P2-C18** | **Resolved** | Unchanged from δ1: abstract wording matches `gate_unsafe_deploy` (non-zero at **0.6**, **0.65** only) and noise columns (**0.0** at all `obs_noise_sd`). |
| **P2-C79** | **Resolved** | Unchanged from δ1: gate-side Results sentence matches the same `gate_unsafe_deploy` pattern. |
| **P2-C80** | **Resolved** | Results (Sensitivity 1) now states matched composite **produced small non-zero unsafe deployment rates at the lowest threshold multipliers**, **which fell to zero across the remainder of the tested range**. This aligns with `composite_unsafe_deploy`: **0.004, 0.003, 0.002, 0.001** at multipliers **0.6–0.75**, then **0.0** from **~0.8** through **1.4** in `sensitivity_thresholds.csv`. |

**Effect on prior section (1) `FAIL`:** For the **threshold-sensitivity / matched-composite sweep** row family only, the original §1 contradictions (**P2-C18**, **P2-C79**, **P2-C80**) are **fully cleared** against the frozen CSV. The archival “contradicted claims” table above remains a record of **prior** wording vs outputs; it is **not** the active assessment after δ2.

---

#### 2) Compensatory vs non-compensatory logic integrity

**Verdict: PASS (artefact-level)**

`metrics_summary.json` and `verification_summary.csv` remain structurally consistent with a conjunctive gate rule versus weighted composite and permissive baselines: under the **primary** heterogeneous configuration, gates show **strict** blocking of unsafe deployments (`n_unsafe_deployed` `0` for Gates), while Composite (mean) admits unsafe deployments at the moderate calibration; under **uniform failure**, verification rows show gate unsafe rate `0.0` with composite (moderate) `0.012`, consistent with the paper’s “advantage collapses / compensation not structured” story at the scenario level. **No output artefact reviewed here contradicts that architectural reading** (separate from the threshold-multiplier sweep issue in §1).

---

#### 3) Statistical consistency (cross-output)

**Verdict: REVIEW**

**PASS (internal joins):** `metrics_summary.json` ↔ `table2_unsafe_rates.csv` (heterogeneous primary row); `verification_summary.csv` ↔ `table2_unsafe_rates.csv` (verified scenario rows); `noise_extended.csv` ↔ Table 2 noise rows (e.g. permissive `0.02` / `0.028` at SD `0.01` / `0.2`); `calibration_portfolio.csv` shows five portfolio compositions with Gates `Gates_unsafe_rate` `0.0` on each row, supporting the limitations sweep narrative in P2-C168 at the artefact level; `calibration_unsafe_prob.csv` shows **one** of five labels with Gates `Gates_unsafe_rate` `0.001` and four with `0.0`, consistent with a “four of five” reading **if** the manuscript refers to **strict zeros** (confirm wording in a manuscript pass outside this file).

**REVIEW driver (updated after Stage 4 threshold δ2):** `sensitivity_thresholds.csv` is **internally consistent**, and the **current** manuscript sentences for **P2-C18**, **P2-C79**, and **P2-C80** (plain-text from `inputs/manuscript.docx`) are **consistent** with the gate and `composite_unsafe_deploy` columns across the tested multiplier grid. **Residual REVIEW** items in this section (e.g. nine PDF `advisory` hashes, GAP pressure) are **unchanged** and are **not** threshold-row contradictions.

---

#### 4) Advisory warnings — nine PDF hash mismatches

**Verdict: REVIEW**

**Observation:** `config/expected_outputs.json` lists **nine** `outputs/figures/*.pdf` paths with `"hash_mode": "advisory"` (`fig1_unsafe_deploy_rate.pdf` through `fig_unsafe_prob_sensitivity.pdf`). Several companion PNG paths are also `advisory`; **tabular and core JSON/CSV outputs** for the simulation path use **`strict`** (including `outputs/data/sensitivity_thresholds.csv`).

**Assessment:** This Stage 4 pass **did not** perform visual or pixel-level diffing of PDFs against prior versions. **Substantive content drift is not evidenced** from hash mismatch alone: PDF export is commonly **non-byte-identical** across toolchains, fonts, and vectorisation. **Byte-level / export-level mismatch is the direct explanation** consistent with strict non-PDF artefacts matching while PDFs warn. **Residual risk:** a future visual regression check remains appropriate before treating figures as submission-identical.

---

#### 5) Gap pressure (GAP / TO_VERIFY_LATER vs blocking)

**Verdict: REVIEW**

**Unchanged GAP (Stage 2):** `P2-C145`, `P2-C183`, `P2-C193` — still no satisfactory in-repo executable anchor for the referenced supplementary / future-work / appendix analyses.

**TO_VERIFY_LATER cluster:** Appendix crosswalks, Python 3.11 execution proof, engine-versioning narrative depth, etc. (Stage 2 list) — unchanged.

**Blocking assessment for Stage 5 (“traceability promotion”):** After **threshold re-validation δ2**, **P2-C18**, **P2-C79**, and **P2-C80** are **not** blocked on threshold-sweep / `sensitivity_thresholds.csv` grounds. **GAP/TO_VERIFY_LATER** items **continue** to block wholesale “all claims VERIFIED” promotion but **do not**, by themselves, invalidate the **core primary + verification CSV** numerical story already under `strict` hashes.

---

#### Contradicted claims (summary list)

- **None** in the §1 threshold-sensitivity family (**P2-C18**, **P2-C79**, **P2-C80**) as of **Stage 4 threshold δ2** (2026-04-19): manuscript wording and `sensitivity_thresholds.csv` agree on non-zero rates at the **lowest** multipliers and zeros elsewhere for gates (and remainder of range for composite). Archival contradiction notes for earlier manuscript wording remain in the §1 table above for audit trail only.

---

#### Still-unresolved claims that could block Stage 5 **promotion to VERIFIED** (non-exhaustive)

- **P2-C145, P2-C183, P2-C193** — remain **GAP**; block verification of supplementary-only quantitative pipelines **in this repo**.
- **P2-C127–P2-C134, P2-C143, P2-C161–P2-C163** — **P4 / upstream**; must not be promoted from P2 outputs alone.
- **TO_VERIFY_LATER** claims tied to appendix-only anchors — block **VERIFIED** until appendix crosswalk is machine-checkable or scoped out.

---

#### Recommendation

**Proceed** with Stage 5 **documentation-only** promotion of **P2-C80** to **VERIFIED** under the usual eligibility rules, now that **δ2** closes the matched-composite threshold sentence against `sensitivity_thresholds.csv`. **GAP/P4** claims remain non-VERIFIED; **TO_VERIFY_LATER** and **advisory** PDF hashes retain **REVIEW** status as before.

**Nine PDF advisories:** Treat as **non-blocking for numeric traceability** given **strict** non-PDF core outputs matched under Stage 3 policy; retain **REVIEW** for submission-identical figure assurance.

## P2 Stage 5 — Traceability Promotion (TARGETED ONLY) (ADDED)

**Recorded:** 2026-04-19 (documentation-only pass). **Delta (same day):** Stage 1 register rows for **P2-C18**–**P2-C80** threshold sentences synced to `inputs/manuscript.docx`; targeted promotion after Stage 4 threshold δ1 — **P2-C18** and **P2-C79** elevated to **VERIFIED**. **Delta 2 (same day):** After **P2-C80** manuscript correction and Stage 4 threshold **δ2 PASS**, **P2-C80** elevated to **VERIFIED**; **NOT VERIFIED — CONTRADICTED** count drops to **0**.

### Promotion policy (Stage 5)

Stage 5 assigns a **single promotion outcome** per Stage 1 claim ID (`P2-C01`–`P2-C194`), keyed to **Stage 2 Trace Status** and **Stage 4** findings. This is **targeted** promotion only: **no blanket** elevation of all claims.

A claim is promoted to **VERIFIED** only when **all** of the following hold:

1. **Stage 2** trace status is **`TRACED_REPO`** (executable / output path closure within this repository).
2. The claim is **not** listed as **CONTRADICTED** in Stage 4 (as of threshold re-validation **δ2**: **no** Stage 4 **CONTRADICTED** rows remain for **P2-C18**, **P2-C79**, or **P2-C80** vs `sensitivity_thresholds.csv`).
3. The claim is **not** **GAP** (**P2-C145**, **P2-C183**, **P2-C193**).
4. The claim is **not** **`TRACED_UPSTREAM`** (includes **P4** companion historical replay: **P2-C127**–**P2-C134**, **P2-C143**, **P2-C161**–**P2-C163**, and other citation / Zenodo / sibling upstream anchors).
5. The claim is **not** **`TO_VERIFY_LATER`** (unresolved appendix crosswalks, Python 3.11 execution proof, engine-versioning depth, etc., per Stage 2).
6. Promotion is **conservative** and **artefact-level**: it reflects **regenerated strict core outputs** validated under Stage 3 policy; it **does not** assert independent manuscript sentence re-extraction from PDF in this pass.

**Explicit non-promotions (preserved from Stage 2 / Stage 4):** **`TRACED_MANUSCRIPT_ONLY`** claims remain **NOT VERIFIED — MANUSCRIPT_ONLY** (they are not given VERIFIED solely because prose is traceable to manuscript sources).

### Stage 5 counts (partition of all Stage 1 claims)

| Outcome | Count |
| --- | --- |
| VERIFIED | 95 |
| NOT VERIFIED — CONTRADICTED | 0 |
| NOT VERIFIED — GAP | 3 |
| NOT VERIFIED — UPSTREAM | 31 |
| NOT VERIFIED — TO_VERIFY_LATER | 17 |
| NOT VERIFIED — MANUSCRIPT_ONLY | 48 |

**Check:** row count = **194**; categories are mutually exclusive.

### Partial closure note (mandatory)

**Stage 5 is partial and conservative, not universal closure.** VERIFIED here means **eligible `TRACED_REPO` claims not excluded by Stage 4 or Stage 2 non-repo / open-question statuses** — it is **not** a warrant that every manuscript sentence, figure byte, or supplementary appendix paragraph has been re-proven against PDF exports.

### Claim-by-claim promotion table (Stage 1 IDs P2-C01–P2-C194)

| Claim ID | Trace Status (Stage 2) | Stage 5 promotion outcome | Basis / exclusion note |
| --- | --- | --- | --- |
| P2-C01 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C02 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C03 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C04 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C05 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C06 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C07 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C08 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C09 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C10 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C11 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C12 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C13 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C14 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C15 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C16 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C17 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C18 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim after Stage 4 threshold re-validation: gate threshold/noise wording reconciled with `sensitivity_thresholds.csv` / `sensitivity_noise.csv`; conservative artefact-level promotion (not independent PDF re-extraction). |
| P2-C19 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C20 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C21 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C22 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C23 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C24 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C25 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C26 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C27 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C28 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C29 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C30 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C31 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C32 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C33 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C34 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C35 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C36 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C37 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C38 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C39 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C40 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C41 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C42 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C43 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C44 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C45 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C46 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C47 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C48 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C49 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C50 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C51 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C52 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C53 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C54 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C55 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C56 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C57 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C58 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C59 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C60 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C61 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C62 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C63 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C64 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C65 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C66 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C67 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C68 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C69 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C70 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C71 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C72 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C73 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C74 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C75 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C76 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C77 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C78 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C79 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim after Stage 4 threshold re-validation: gate-side qualified threshold narrative matches `sensitivity_thresholds.csv`; conservative artefact-level promotion (not independent PDF re-extraction). |
| P2-C80 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim after Stage 4 threshold **δ2**: matched-composite sentence (small non-zero at lowest multipliers, zero across remainder) matches `composite_unsafe_deploy` in `outputs/data/sensitivity_thresholds.csv`; conservative artefact-level promotion (not independent PDF re-extraction). |
| P2-C81 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C82 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C83 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C84 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C85 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C86 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C87 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C88 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C89 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C90 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C91 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C92 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C93 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C94 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C95 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C96 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C97 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C98 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C99 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C100 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C101 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C102 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C103 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C104 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C105 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C106 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C107 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C108 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C109 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C110 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C111 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C112 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C113 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C114 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C115 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C116 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C117 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C118 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C119 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C120 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C121 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C122 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C123 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C124 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C125 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C126 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C127 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C128 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C129 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C130 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C131 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C132 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C133 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C134 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C135 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C136 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C137 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C138 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C139 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C140 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C141 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C142 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C143 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C144 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C145 | GAP | NOT VERIFIED — GAP | Stage 2 GAP unchanged; no satisfactory in-repo executable anchor. |
| P2-C146 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C147 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C148 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C149 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C150 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C151 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C152 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C153 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C154 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C155 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C156 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C157 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: manuscript citations, Zenodo record, or sibling / external sources; not closed under P2 strict regenerated artefacts alone. |
| P2-C158 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C159 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C160 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C161 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C162 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C163 | TRACED_UPSTREAM | NOT VERIFIED — UPSTREAM | Stage 2 TRACED_UPSTREAM: P4 / companion historical replay (explicit); not verifiable from P2 repo outputs alone. |
| P2-C164 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C165 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C166 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C167 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C168 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C169 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C170 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C171 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C172 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C173 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C174 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C175 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C176 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C177 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C178 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C179 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C180 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C181 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C182 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C183 | GAP | NOT VERIFIED — GAP | Stage 2 GAP unchanged; no satisfactory in-repo executable anchor. |
| P2-C184 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C185 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C186 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C187 | TRACED_REPO | VERIFIED | Eligible TRACED_REPO claim: Stage 2 locally traceable; not GAP / not TRACED_UPSTREAM / not TO_VERIFY_LATER; not Stage-4-contradicted; Stage 3 regenerated strict core artefacts (`config/expected_outputs.json` policy) support conservative artefact-level promotion (not sentence-level manuscript re-extraction). |
| P2-C188 | TO_VERIFY_LATER | NOT VERIFIED — TO_VERIFY_LATER | Stage 2 TO_VERIFY_LATER unchanged (appendix crosswalk, execution proof, or narrative depth not machine-closed in this repo pass). |
| P2-C189 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C190 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C191 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C192 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |
| P2-C193 | GAP | NOT VERIFIED — GAP | Stage 2 GAP unchanged; no satisfactory in-repo executable anchor. |
| P2-C194 | TRACED_MANUSCRIPT_ONLY | NOT VERIFIED — MANUSCRIPT_ONLY | Stage 2 TRACED_MANUSCRIPT_ONLY: narrative or manuscript-local anchor without required strict numeric join to regenerated P2 outputs in this promotion pass. |

