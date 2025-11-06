# /slash generate-pydantic-ai-prp

**Goal:** Create a new PRP from the base template, pre-filled for the current project.
**Inputs:** `name`, optional `output` path (default: `PRPs/INITIAL.md`).

**Behavior:**
- Loads `PRPs/templates/prp_pydantic_ai_base.md`
- Interpolates project vars (name, description)
- Writes result to `output`

**Success Output:** path to created PRP.
