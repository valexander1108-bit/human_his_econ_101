# Interactive Model Objective Fit Audit

Source checked: `modules_data.py`, `streamlit_app.py`, and app implementations in `apps/`.

## Summary

The interactive model set now supports the final V6 syllabus structure at the Tier 2 standard algebra level. The strongest coverage is in Modules 1, 3, 4, 5, 9, 10, 11, and 12, where the models directly teach the stated graphs, tables, formulas, and policy comparisons. Modules 2, 6, 7, and 8 are also supported, with explicit async/bridge needs addressed through targeted module framing.

Coding, calculus, linear algebra, proofs, and simulations remain Tier 3 extensions. The app uses sliders and computed diagrams to make those ideas visible, but the core student-facing tasks remain algebraic and graphical.

## Module-Level Verification

| Module | Interactive models | Fit to objectives | Verification notes |
| --- | --- | --- | --- |
| 1 — Economic Thought & Modeling | Budget Constraint; PPC; Comparative Advantage | Strong | Models cover slopes, intercepts, opportunity cost, PPM/PPF tradeoffs, specialization, and comparative advantage. Full-analysis toggles support model-limits discussion. |
| 2 — ASYNC — Choice | Labor-Leisure Choice; Intertemporal Choice; Behavioral Policy | Strong | Models support feasible frontiers, wage and interest-rate tradeoffs, borrower/lender contrast, and behavioral limits. Good fit for recorded async work because students can manipulate one choice setting at a time. |
| 3 — Supply and Demand | Utility; Income/Substitution Effects; Optimal Choice; Demand; Supply; Market Model; Single Shifts; Double Shifts | Strong | Models cover utility/MRS, budget tangency, income/substitution effects, linear demand/supply, algebraic equilibrium, and shifts. This is the most complete module-model pairing. |
| 4 — Market Analysis: Elasticity & Efficiency | PED; Total Revenue; PES; Surplus; Price Floor; Price Ceiling; Deadweight Loss; Tax Incidence | Strong | Models cover elasticity classification, total revenue, supply elasticity, CS/PS/TS, intervention, DWL, and incidence. Tax incidence directly ties elasticity to burden sharing. |
| 5 — Factor Markets | Land + Rent; Labor + Wage; Labor Market Policy; Capital + Interest | Strong | Models cover VMP/MRP logic, land/labor/capital markets, wages, rents, interest rates, and basic policy wedges. Monopsony remains mostly conceptual but is supported by labor policy and later inequality models. |
| 6 — BRIDGE — Markets, History & Global Economy | Malthus and Growth; GDP and Wellbeing Limits; Capitalism and Climate Change; Capitalism and Global Inequality | Strong | Models support the bridge function: Malthusian pressure, hockey-stick growth, GDP limits, climate as externality, and inequality/distribution. They help synthesize blind spots from Modules 1-5. |
| 7 — ASYNC — Structural Inequality: Core + Game Theory Preview | Structural Inequality Model; Credit Exclusion and Labor Power; Game Theory Preview; Competition and Fairness | Strong after fix | Added targeted support for credit exclusion/labor power and game theory preview. Preview model avoids requiring formal Nash equilibrium, matching the async objective. |
| 8 — Structural Inequality: Extensions | Technology, AI Bias, and Climate Inequality; Climate as Distributional Injustice; AI Bias and Algorithmic Fairness | Strong after fix | Added targeted technology/AI/climate model and climate-distribution model. These now teach S-curve diffusion, proxy bias, MRP gaps, exposure, adaptation capacity, and distributional climate burden. |
| 9 — Firms & Cost of Production | Cost of Production; Economies of Scale | Strong | Cost model covers TR, FC, VC, TC, AFC, AVC, ATC, MR, and MC as supply. Economies model covers LRATC and minimum efficient scale. Principal-agent remains conceptual in the module text rather than a standalone model. |
| 10 — Profit Maximization | Perfect Competition Profit Maximization; Shutdown Point; Long-Run Equilibrium and Firm Exit; Monopoly and Monopolistic Competition; Price Discrimination | Strong | Models cover MR=MC, price-taking firms, shutdown, entry/exit, monopoly pricing, and discrimination. Output/welfare comparison is visible through graphs and metrics. |
| 11 — Imperfect Competition & Game Theory | Monopolistic Competition and Oligopoly; Game Theory; Antitrust HHI; Competition, Information, and Fairness | Strong | Models cover strategic interdependence, payoff matrices, Nash equilibrium, cartel instability, HHI/merger analysis, concentration, entry barriers, information gaps, and bargaining gaps. |
| 12 — Policy, Paradox & Human Perspectives | Types of Goods; Public Goods/Common Resources; Externalities; Pigouvian Tax/Subsidy; Dynamic Policy Tax Incidence; Behavioral Policy; Climate Policy | Strong | Models cover goods classification, public-goods/common-resource failures, positive/negative externalities, tax/subsidy corrections, incidence, climate policy, and behavioral policy design. |

## Targeted Fixes Completed

- Added `game_theory_preview_app()` so Module 7 teaches players, strategies, payoffs, and prisoner's-dilemma structure without requiring formal Nash equilibrium.
- Added `credit_exclusion_labor_power_app()` so Module 7's credit-exclusion and Marcus/Ray labor-power objective has a direct model instead of opening a generic labor-policy page.
- Added `technology_ai_climate_inequality_app()` so Module 8 directly teaches S-curve technology diffusion, skill complementarity, proxy bias, climate exposure, and MRP gaps.
- Added `climate_distributional_injustice_app()` so Module 8 distinguishes climate as distributional injustice from Module 6/12 climate externality-policy models.

## Remaining Improvement Opportunities

- Module 5 could eventually add a dedicated monopsony diagram if the course wants monopsony to be more than a preview before Module 7.
- Module 9 could eventually add a principal-agent-within-firms model, but current syllabus language can be taught conceptually with the cost model and later game theory tools.
- Module 12 could eventually add a dynamic policy timeline model for path dependence; the existing tax incidence and climate policy models cover the Tier 2 version.

## Verification Commands

- `python -m py_compile streamlit_app.py modules_data.py pages/course_syllabus.py pages/explore_map_timeline.py apps/*.py`
- Catalog check: 58 model pages, 58 unique labels, no duplicates.
- New targeted model callables imported successfully from `apps.remaining_models`.
