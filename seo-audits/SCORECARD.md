# SEO Scorecard — csoh.org

Track audit scores over time. Add a new row each time `/seo-audit` is run. Lower scores = regression; investigate.

| Date | Overall | Technical | On-Page | Content | Performance | Mobile/A11y | Critical | Warnings | Report |
|---|---|---|---|---|---|---|---|---|---|
| 2026-04-30 | **88** | 95 | 90 | 88 | 75 | 95 | 2 | 6 | [baseline](2026-04-30-baseline.md) |
| 2026-05-03 | **96** | 97 | 95 | 96 | 92 | 96 | 0 | 1 | [report](2026-05-03.md) |
| 2026-05-03 (rerun) | **96** | 95 | 96 | 97 | 93 | 96 | 1 | 1 | [report](2026-05-03-rerun.md) |

## How to use

1. Run `/seo-audit csoh.org` (uses the SearchFit SEO skill) or invoke the seo-auditor agent.
2. Save the full report as `seo-audits/YYYY-MM-DD.md`.
3. Append a row to the table above with the new scores.
4. Diff against the previous row — celebrate gains, investigate drops.

## External signals to track alongside this

- **Google Search Console** — impressions, clicks, average position, CTR (set up email alerts for coverage/index drops)
- **PageSpeed Insights / CrUX** — Core Web Vitals trend (LCP, INP, CLS) on the same set of pages each month
- **Bing Webmaster Tools** — secondary search source

The scores in this scorecard measure on-site/codebase health. Search Console measures actual ranking outcomes. Both matter.
