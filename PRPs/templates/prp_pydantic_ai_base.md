# PRP — Pydantic AI Base

## Objective
Define a minimal, robust agent with clear tools, small surface area, and env-driven configuration.

## Inputs
- Natural language prompt and/or image path.
- Optional dimensions and category hints.

## Outputs
- A generated Revit family (.rfa) or an actionable error explaining what’s missing.

## Steps
1) Validate inputs; if ambiguous, ask targeted questions.
2) Choose mode: parametric (template) vs image-based mesh.
3) Generate via APS Design Automation activity.
4) Save artifact; report path and key parameters.

## Guardrails
- No secrets in code; use `.env`.
- Keep tools minimal and deterministic.
- Tests must pass before release.
