# HALT — governance preflight (P2 engineer session)

**Date (authoritative):** 2026-04-12  
**Rule:** AGENTS.md input validation; EAA Portfolio Governance v8.3

## Trigger

Required manuscript input absent per `eaa_system/attachment_requirements.json` → `paper-2.required_files` includes `manuscript.pdf OR manuscript.docx`.

## Missing path (exact)

`c:\Users\Walter.Brown\EAA_Portfolio\ethical-alpha-audit-paper-2-threshold-justification\inputs\manuscript.docx`  
*(or equivalently `inputs/manuscript.pdf` in the same directory)*

## Verified present

- `inputs/supplementary.pdf`
- `inputs/experiment_pack/` (directory)

## Additional note (snapshot drift; escalate at portfolio level)

`eaa_system/system_snapshot.json` lists `repos.P2.commit` as `null` and `phase` as `not-started`, while this repository `main` is at `b6be862a2372bc19626f9e5021ab8235e455b709`. Update snapshot binding in a portfolio-administered session if required.

## Action

Stop P2 engineer session. Add manuscript to `inputs/`, re-run preflight in a new agent session.
