# Pydantic AI Context Engineering — Global Rules for AI Agent Development

This file contains the global rules and principles that apply to **ALL Pydantic AI agent development work**. These rules are specialized for building production‑grade AI agents with tools, memory, and structured outputs.

---

## 🔄 Pydantic AI Core Principles

### Agent Development Workflow
- Always start with **INITIAL.md** — define agent requirements before generating PRPs.
- Use the PRP pattern: **INITIAL.md → /generate-pydantic-ai-prp INITIAL.md → /execute-pydantic-ai-prp PRPs/filename.md**.
- Follow **validation loops** — each PRP must include agent testing with `TestModel`/`FunctionModel`.
- **Context is king** — include necessary Pydantic AI patterns, examples, and docs.
- **Keep it simple** — simple yet complete; avoid unnecessary complexity.
- **Avoid backward compatibility** for dead code. Remove duplicates rather than maintain legacy shims.
- **Avoid files > 500 lines** — split into modules as you approach the limit.
- **Avoid complex dependency graphs** — keep dependencies simple and testable.

### Research Methodology for AI Agents
- Web search extensively — research Pydantic AI patterns and best practices.
- Use **Archon MCP server** for RAG — query Pydantic AI docs and code examples.
- Study official documentation — **https://ai.pydantic.dev** is authoritative.
- Pattern extraction — identify reusable agent architectures and tool patterns.
- Gotcha documentation — async patterns, model limits, context management issues.

---

## 📚 Project Awareness & Context
- Use a **virtual environment** to run code and tests; create it if missing.
- Use consistent **Pydantic AI naming** and **agent structure patterns**.
- Follow established directory patterns: `agent.py`, `tools.py`, `models.py`, `dependencies.py`.
- Leverage Pydantic AI **examples** extensively before inventing new patterns.

---

## 🧱 Agent Structure & Modularity
- Never create files longer than **500 lines** — split into modules.
- Organize modules by responsibility:
  - `agent.py` — main agent definition and execution logic
  - `tools.py` — tool functions
  - `models.py` — Pydantic output models and dependency classes
  - `dependencies.py` — external service integrations and settings
- Use clear, consistent imports from `pydantic_ai`.
- **Environment variables** via `python-dotenv`; follow `examples/main_agent_reference/settings.py` pattern.
- Never hardcode sensitive information — always `.env` for API keys and config.

---

## 🤖 Pydantic AI Development Standards

### Agent Creation Patterns
- **Model‑agnostic design** — support OpenAI/Anthropic/Gemini, etc.
- **Dependency injection** — use `deps_type` for external services and context.
- **Structured outputs** — Pydantic models only when needed; otherwise default to string output.
- **Comprehensive system prompts** — static + dynamic instructions (but keep them concise).

### Tool Integration Standards
- Use `@agent.tool` for context‑aware tools with `RunContext[DepsType]`.
- Use `@agent.tool_plain` for simple tools without context dependencies.
- Validate parameters with Pydantic models.
- Handle tool errors gracefully — implement retry/backoff and recovery paths.

### Environment Variable Configuration (python‑dotenv + pydantic‑settings)
```python
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="API key for the LLM provider")
    llm_model: str = Field(default="gpt-4", description="Model name to use")
    llm_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the LLM API"
    )

def load_settings() -> Settings:
    load_dotenv()
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nMake sure to set LLM_API_KEY in your .env file"
        raise ValueError(error_msg) from e

def get_llm_model():
    settings = load_settings()
    provider = OpenAIProvider(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
    return OpenAIModel(settings.llm_model, provider=provider)
```

### Testing Standards for AI Agents
- Use **TestModel** for development — fast validation without API calls.
- Use **FunctionModel** for custom behavior in tests.
- Use **Agent.override()** to replace models in test contexts.
- Test **both sync and async** flows.
- Test **tool validation** — verify schemas and error handling.

---

## ✅ Task Management for AI Development
- Break development into clear steps with acceptance criteria.
- Mark tasks complete immediately after finishing implementations.
- Update task status in real time.
- **Test agent behavior before** marking tasks complete.

---

## 📎 Pydantic AI Coding Standards

### Agent Architecture
```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from .settings import load_settings, get_llm_model

@dataclass
class AgentDependencies:
    api_key: str
    session_id: str | None = None

settings = load_settings()

agent = Agent(
    get_llm_model(),
    deps_type=AgentDependencies,
    system_prompt="You are a helpful assistant..."
)

@agent.tool
async def example_tool(ctx: RunContext[AgentDependencies], query: str) -> str:
    return await external_api_call(ctx.deps.api_key, query)
```

### Security Best Practices
- API keys via `.env` — never commit keys.
- Always `load_dotenv()` in settings init.
- Validate and sanitize all user inputs.
- Rate limit external API use.
- Never leak sensitive info in errors.

### Common Pydantic AI Gotchas
- Be consistent with **async/await**.
- Respect **model context limits**.
- Keep dependency graphs **simple and well‑typed**.
- Always implement **retry/fallback** for tools.
- Prefer **stateless tools** to simplify context/state.

---

## 🔍 Research Standards for AI Agents
- Use **Archon MCP server** with RAG for docs and examples.
- Study official examples — **ai.pydantic.dev/examples**.
- Know provider‑specific features/limits.
- Document integration patterns (LLM, storage, external APIs).

---

## 🎯 Implementation Standards for AI Agents
- Follow the **PRP workflow** — don’t skip validation.
- Test with **TestModel** first.
- Reuse proven patterns (don’t reinvent).
- Include comprehensive error handling for tool/model failures.
- Test streaming where relevant.

---

## 🚫 Anti‑Patterns to Avoid
- ❌ Skipping tests (TestModel/FunctionModel).
- ❌ Hardcoding model strings — always env‑driven.
- ❌ Using `result_type` unless structured output is required.
- ❌ Mixing async/sync carelessly.
- ❌ Building complex dependency webs.
- ❌ Neglecting tool error handling.
- ❌ Skipping input validation.

---

## 🔧 Tool Usage Standards
- Use web search to research Pydantic AI and provider docs.
- Follow slash‑command patterns and agent workflows.
- Use validation loops to ensure quality each step.
- Test with **multiple providers** for compatibility.

---

## 🧪 Testing & Reliability
- Create comprehensive tests for tools, outputs, and failures.
- Validate behavior with **TestModel** before real models.
- Include edge cases for tool failures and provider outages.
- Test both structured and unstructured outputs.
- Validate DI in test contexts.

---

## Addendum — Revit/BIM Global Rules (Family Maker)

### Version & Compatibility
- **Target Revit versions are explicit** (e.g., 2024, 2025). No mixed‑version artifacts.
- **Template immutability**: pin family templates by SHA/URL; record `TEMPLATE_ID` + hash in outputs.

### Naming, Categories, Parameters
- **Family naming**: `Company_Category_Subtype_v{semver}.rfa` (e.g., `Bluewave_Furniture_Chair_v0.3.rfa`).
- **Type Catalogs**: if used, enforce `FamilyName.txt` with CSV header and unit suffixes.
- **Category is mandatory**; refuse generation if ambiguous.
- **Shared parameters**: prefer **Shared Parameter GUIDs**; keep a `shared_parameters.txt` under version control.
- **Parameter prefixes**: `DIM_`, `MTRL_`, `ID_`, `CTRL_`; avoid duplicates and type/instance confusion.
- **Units**: Revit internal = **feet**. Convert inputs; never assume metric. Round to sane tolerances (±0.5 mm).

### Geometry & Constraints Quality
- Use **reference planes**, labeled dims, locked constraints; avoid free geometry.
- **Flex test** every family: min/nominal/max parameter sets regenerate without errors.
- Keep mesh imports **light**; prefer parametric forms when possible.
- Avoid nested families unless justified; prevent bloat and circular refs.

### APS / Design Automation (Forge)
- Credentials are **env‑only**; never commit.
- Log **activity alias**, **bundle version**, **input/output URIs** per job.
- Define **max parallel jobs**; implement retry with backoff.
- Save `.rfa` + **JSON manifest** (parameters, units, template hash, Revit version).

### Image‑to‑3D (Optional)
- Import only meshes with **clear license**; store license URL in manifest.
- Always add a **scale** parameter; validate real‑world size after import.
- If AI reconstruction confidence is low, **fall back** to parametric template + prompt.

### Testing & Validation (must pass before release)
- **Golden tests**:
  - Text‑only: door/window/table → expected parameters exist with correct units/values.
  - Image‑only: mesh imported, scale param works, file size under budget.
  - Hybrid: text drives params; image drives shape; **flex test** passes.
- Determinism: fix seeds where applicable; pin template versions.
- CI: reject families exceeding **size budget** (e.g., 1–3 MB) or failing flex tests.

### Security, IP, and Privacy
- No confidential models/images to third‑party services without approval.
- Strip EXIF/PII from images before external calls.
- Errors must not leak paths, keys, or project names.

### Performance Budgets
- Family open time < 1 s for common types.
- Geometry simplification rules for production families.
- Ensure referenced materials exist; otherwise default to safe materials.

### Operational Runbooks
- **Fallback** if APS down: local Revit + pyRevit/RevitPythonShell runner.
- **Rollback**: store prior working artifact; releases are atomic.
- **Telemetry** (opt‑in): job ID, duration, template hash, outcome.

### Required Environment Variables (documented, not committed)
- `MODEL`, `OPENAI_API_KEY`
- `APS_CLIENT_ID`, `APS_CLIENT_SECRET`
- `APS_DA_ACTIVITY`, `APS_DA_BUNDLE_ALIAS`
- `APS_TEMPLATE_URL` (or template catalog service)
- `OUTPUT_BUCKET_OR_PATH`
