# Original repository review — 2026-11-15

Review inputs: `README.md`, `.gitignore`, `requirements.txt`, `eda_2025_baseline.py`, `evaluate_2026_kpi.py`, `preprocess_logs.py`, and nine presentation slides provided in this chat.

## Findings addressed

| Area | Original behavior | Updated behavior |
|---|---|---|
| Data definition | In-code monthly values mixed with chart drawing | Published aggregate values in `data/aggregates.json` with metadata |
| KPI comparison | Same-period growth calculations correct but comments/hard-coded rates mixed | Year-over-year calculations isolated and exported to JSON; rates labeled with their distinct periods |
| PII handling | `sha256(name)[:12]` pseudonym (re-identifiable by guessing), `birth_year` retained | Allowlist fields, drop names, birth dates, identifiers, contact and unstructured notes |
| Missing checkout | Substitutes 19:00/21:00, which invents stay time | Missing values kept null and flagged as `missing_checkout` |
| Time order | Negative stays clipped to zero | Out-of-order timestamps flagged separately |
| Short/utility visits | Labeled `utility_noise` | Labeled but retained, not incorrectly discarded |
| Dependencies | Missing `.xlsx` engine `openpyxl` | Added `openpyxl` to requirements |
| Charts | Values and axes hardcoded in individual scripts | Public aggregate based charts plus KPI JSON, checked against user-supplied sums |
| Tests | No automated regression checks supplied | 12 tests, public-data report generation, private-data smoke workflow |
| External coverage | Linked article mislabeled as D→B ranking coverage | Removed unrelated classification; external article is about national youth funding approval |

## Context incorporated in final version

- Center operations switched from private management to direct municipal operation in 2025, following low prior evaluations (project author's account). A location closure and broader site reorganization were part of that period.
- May 2026 evaluation preparation, rather than generic attendance growth, was the work objective. Prior-year monthly data served as the baseline.
- Internally reported D→B evaluation improvement and the separate publicly reported youth-project award/funding are not treated as interchangeable evidence or as causal proof.
- The README omits a final employment month because the source history contains different end dates; confirm against employment records before publishing.

## Not independently verified

- Underlying individual-level administrative records were not supplied. Public aggregation is based on user-uploaded scripts/slides.
- A government notice or official evaluation record for D→B rating was not supplied.
- The denominator definitions for completion rates and participant counts need confirmation.
- Actual registration, attendance, and unique-person counting semantics may differ.
- Personal contributions and operational authority require separate verification against employment/project documents.
- The original sample-data screenshots were not all provided in a verifiable form for privacy review.
- Operational records are not anonymous merely because direct identifiers are excluded; timestamps and location may still identify visits in a small cohort.

## Tests conducted

- Public aggregate validation (monthly totals and same-month ratios)
- Defensive timestamp cleaning and field minimization on **synthetic** workbook data
- End-to-end generation of baseline/KPI figures
- Python source compilation

These tests verify the released implementation using known aggregate values and synthetic attendance records. They do **not** establish accuracy of the original internal dataset, official institutional outcomes, or causal effect of administrative changes.
