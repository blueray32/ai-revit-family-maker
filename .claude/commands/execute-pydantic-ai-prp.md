Here you go — a clean, ready-to-drop markdown for the slash command, same structure as your example:

# /slash Execute Pydantic AI Agent PRP

Implement a complete Pydantic AI agent using the PRP framework with comprehensive workflow management.

**PRP File:** `$ARGUMENTS`

---

## 🎯 Primary Directive

⚠️ **CRITICAL WORKFLOW:** This command implements a full agent creation workflow using the PRP as the primary planning document.

The workflow progresses through:

1) PRP Loading & Archon Setup  
2) Parallel Component Development (3 subagents)  
3) Agent Implementation  
4) Validation & Testing (1 subagent)  
5) Delivery & Documentation

---

## 🔄 Complete Agent Creation Workflow

### Agent Creation Location Rule
When implementing Pydantic AI agents via PRPs:

- **ALWAYS** create the agent in the **current working directory**  
- Planning files go in `./planning/` (relative to current directory)  
- Implementation files go in `./` (current directory)

---

## Phase 1: PRP Loading & Archon Integration 📋

**Actions:**

1. **Load and analyze the PRP file**
   - Read the specified Pydantic AI PRP file
   - Understand all agent requirements and research findings
   - Identify validation gates and success criteria
   - Review `examples/main_agent_reference` patterns for implementation guidance

2. **Initialize Archon Project Management**
   - Run `mcp__archon__health_check`
   - **If Archon is available:**
     - CREATE an Archon project for the agent being built
     - CREATE tasks in Archon for each workflow phase:
       - Task 1: “System Prompt Design” (Phase 2A — pydantic-ai-prompt-engineer)
       - Task 2: “Tool Development Planning” (Phase 2B — pydantic-ai-tool-integrator)
       - Task 3: “Dependency Configuration” (Phase 2C — pydantic-ai-dependency-manager)
       - Task 4: “Agent Implementation” (Phase 3 — main Claude Code)
       - Task 5: “Validation & Testing” (Phase 4 — pydantic-ai-validator)
       - Task 6: “Documentation & Delivery” (Phase 5 — main Claude Code)
   - **If Archon is not available:** use TodoWrite for local tracking

3. **ULTRATHINK about the implementation**
   - Break down agent development into smaller steps
   - Use the TodoWrite tool to create and track the implementation plan
   - Plan project structure following `main_agent_reference` patterns

---

## Phase 2: Parallel Component Development ⚡

> Execute **SIMULTANEOUSLY** (all three subagents work in parallel).  
> **Archon:** Update Tasks 1, 2, 3 to “doing” before parallel invocation.

**CRITICAL:** Use **parallel tool invocation** — when invoking multiple subagents, call all three Task tools **in a single message** to ensure true parallel execution.

### 2A: System Prompt Engineering
- **Subagent:** pydantic-ai-prompt-engineer  
- **Philosophy:** SIMPLE, CLEAR prompts (typically 100–300 words)  
- **Input:** The PRP file (pass the path; instruct the subagent to read it)  
- **Output:** `planning/prompts.md`  
- **⚠️ CRITICAL:** Output **MARKDOWN** file with prompt specifications, **NOT** Python code  
- **Contents:**
  - One simple static system prompt (100–300 words)
  - Skip dynamic prompts unless explicitly needed
  - Focus on essential behavior only

### 2B: Tool Development Planning
- **Subagent:** pydantic-ai-tool-integrator  
- **Philosophy:** MINIMAL tools — 2–3 essential functions only  
- **Input:** The PRP file (path; instruct the subagent to read it)  
- **Output:** `planning/tools.md`  
- **⚠️ CRITICAL:** Output **MARKDOWN** file with tool specifications, **NOT** Python code  
- **Contents:**
  - 2–5 essential tool specifications only
  - Simple parameters (1–4 per tool)
  - Basic error handling
  - Single-purpose tools

### 2C: Dependency Configuration Planning
- **Subagent:** pydantic-ai-dependency-manager  
- **Philosophy:** MINIMAL config — essential environment variables only  
- **Input:** The PRP file (path; instruct the subagent to read it)  
- **Output:** `planning/dependencies.md`  
- **⚠️ CRITICAL:** Output **MARKDOWN** file with dependency specifications, **NOT** Python code  
- **Contents:**
  - Essential environment variables only
  - Single model provider (no fallbacks)
  - Simple dataclass dependencies
  - Minimal Python packages

**Phase 2 Complete When:** All three subagents report completion.  
**Archon:** Mark Tasks 1, 2, 3 as “done” after subagents complete.

---

## Phase 3: Agent Implementation 🔨

- **Actor:** Main Claude Code (not a subagent)  
- **Archon:** Update Task 4 to “doing” before starting implementation

**Actions:**
1. Update Archon Task 4 “Agent Implementation” to status **doing**
2. **READ** the 4 critical files:
   - The original PRP file (requirements and validation gates)
   - `planning/prompts.md`
   - `planning/tools.md`
   - `planning/dependencies.md`
3. Use **Archon RAG** to search for Pydantic AI patterns and examples as needed
4. **IMPLEMENT** the actual Python code based on specifications:
   - Convert prompt specs → `prompts.py`
   - Convert tool specs → `tools.py`
   - Convert dependency specs → `settings.py`, `providers.py`, `dependencies.py`
5. Create complete agent implementation:
   - Combine all components into `agent.py`
   - Wire up dependencies and tools
   - Create main execution file
6. Structure final project:

├── agent.py           # Main agent
├── settings.py        # Configuration
├── providers.py       # Model providers
├── dependencies.py    # Dependencies
├── tools.py           # Tool implementations
├── prompts.py         # System prompts
├── init.py        # Package init
├── requirements.txt   # Python deps
├── .env.example       # Environment template
└── README.md          # Usage documentation

7. Update Archon Task 4 to status **done** when implementation completes

---

## Phase 4: Validation & Testing ✅

- **Subagent:** pydantic-ai-validator  
- **Trigger:** Automatic after implementation  
- **Archon:** Update Task 5 to “doing” before invoking validator

**Actions:**
1. Update Archon Task 5 “Validation & Testing” to status **doing**
2. Invoke validator subagent with:
- The original PRP file path (tell the subagent to read it for the validation gates)
- Path to implemented agent code
- Archon project ID (if available)
3. Validator will:
- Create a comprehensive test suite based on the PRP validation gates
- Validate against PRP requirements and validation gates
- Run tests with **TestModel**
- Generate a validation report
4. **Output:** `tests/`

├── test_agent.py
├── test_tools.py
├── test_integration.py
├── test_validation.py
├── conftest.py
└── VALIDATION_REPORT.md

5. Update Archon Task 5 to status **done** after validation completes

**Success Criteria:**
- All PRP validation gates pass  
- Core functionality tested  
- Error handling verified  
- Performance acceptable

---

## Phase 5: Delivery & Documentation 📦

- **Actor:** Main Claude Code  
- **Archon:** Update Task 6 to “doing” before final documentation

**Final Actions:**
1. Update Archon Task 6 “Documentation & Delivery” to status **doing**
2. Generate a comprehensive `README.md`
3. Create usage examples based on PRP use cases
4. Document API endpoints (if applicable)
5. Provide deployment instructions
6. Run final validation checks from PRP
7. Update Archon Task 6 to status **done**
8. Add final notes to Archon project about agent capabilities
9. **Summary report to user** with:
- Archon project link (if available)
- Implementation status
- Test results
- Any deviations from PRP

---

## 📋 Archon Task Management Protocol

**Task Creation Flow**  
When Archon is available, create all workflow tasks immediately after loading PRP:

```python
# After creating Archon project
tasks = [
 {"title": "System Prompt Design", "assignee": "pydantic-ai-prompt-engineer"},
 {"title": "Tool Development Planning", "assignee": "pydantic-ai-tool-integrator"},
 {"title": "Dependency Configuration", "assignee": "pydantic-ai-dependency-manager"},
 {"title": "Agent Implementation", "assignee": "Claude Code"},
 {"title": "Validation & Testing", "assignee": "pydantic-ai-validator"},
 {"title": "Documentation & Delivery", "assignee": "Claude Code"},
]
# Create all tasks with status="todo" initially

Task Status Updates
	•	Set to doing immediately before starting each phase
	•	Set to done immediately after phase completes successfully
	•	Add notes if a phase encounters issues or deviations
	•	Never have multiple tasks in doing status (except during parallel Phase 2)

Subagent Communication
	•	Always pass the PRP content and Archon project ID to subagents:
	•	Include in the prompt: “Use PRP: [full PRP content]”
	•	Include in the prompt: “Use Archon Project ID: [project-id]” (if available)
	•	Subagents should reference the PRP for requirements and validation gates

⸻

🎭 Subagent Invocation Rules

Automatic Invocation

# Phase 2 — Parallel automatic
parallel_invoke([
  "pydantic-ai-prompt-engineer",
  "pydantic-ai-tool-integrator",
  "pydantic-ai-dependency-manager"
])

# Phase 4 — Automatic after implementation
invoke("pydantic-ai-validator")

Manual Override
Users can explicitly request specific subagents:
	•	“Use the prompt engineer to refine the system prompt.”
	•	“Have the tool integrator add web search capabilities.”
	•	“Run the validator again with updated tests.”

⸻

🔍 Monitoring & Debugging

Progress Tracking — Claude Code should provide status updates:
	•	✅ Phase 1: PRP Loaded and Analyzed
	•	⏳ Phase 2: Building Components (3 subagents working…)
	•	✅ Prompts: Complete
	•	✅ Tools: Complete
	•	⏳ Dependencies: In progress…
	•	⏳ Phase 3: Implementation pending…
	•	⏳ Phase 4: Validation pending…

⸻

Pydantic AI-Specific Patterns to Follow
	•	Configuration: Use environment-based setup like main_agent_reference
	•	Output: Default to string output; only use result_type when validation is needed
	•	Tools: Use @agent.tool with RunContext for dependency injection
	•	Testing: Include TestModel validation for development
	•	Security: Environment variables for API keys; proper error handling
	•	PRP Adherence: Follow all validation gates and success criteria from the PRP

Note: The PRP serves as the single source of truth for requirements. All subagents and implementation phases must reference and validate against the PRP specifications.

Want me to drop this into `.claude/commands/execute-pydantic-ai-agent-prp.md` in your workspace?