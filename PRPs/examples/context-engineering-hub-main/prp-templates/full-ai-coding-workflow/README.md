# AI Coding Workshop: The Full AI Development Workflow

Welcome to the complete 4-hour workshop to transform you into a well-equipped agentic engineer! This guide teaches you my entire workflow for building anything with AI coding assistants using proven methodologies and context engineering strategies.

## 🎯 The Three-Step Process

This workshop centers on a fundamental principle: **successful AI coding requires a structured approach**. We'll master three essential phases:

<p align="center">
  <img src="images/AICoding3Steps.png" alt="AI Coding Three-Step Process" width="900"/>
</p>

### 1. **Planning** 📋
The most critical step where you "sharpen your axe." We spend significant time here because proper planning determines project success. You'll learn context engineering and see how the PRP framework naturally emerges as the solution for structured AI development.

### 2. **Implementation** 🏗️  
Execute your structured plan using AI coding assistants with proper context, documentation, and validation loops. Transform planning documents into working code systematically.

### 3. **Validation** ✅
Validate outputs through automated testing and human oversight. Learn to be a validation gate yourself - understanding fundamentals while leveraging AI to accelerate development.

## 🚀 Quick Start with Template

Get started with this complete PRP template (for building AI agents) in just 2 minutes:

```bash
# Clone the context engineering repository
git clone https://github.com/dynamous-community/context-engineering-hub.git
cd context-engineering-hub/prp-templates/full-ai-coding-workflow

# 1. Copy this template to your new project
python copy_template.py /path/to/my-project

# 2. Navigate to your project
cd /path/to/my-project

# 3. Start building with the PRP workflow
# Fill out PRPs/INITIAL.md with your requirements

# 4. Generate comprehensive PRP
/generate-pydantic-ai-prp PRPs/INITIAL.md

# 5. Execute the PRP to build your agent
/execute-pydantic-ai-prp PRPs/generated_prp.md
```

## 🧠 Context Engineering: The Four Pillars

<table border="0">
<tr>
<td width="35%" valign="top">
<img src="images/ContextEngineering.png" alt="Context Engineering Four Pillars" width="100%"/>
</td>
<td width="65%" valign="top">

Successful AI coding relies on **Context Engineering** - giving your AI system everything it needs to succeed. This consists of four foundational pillars:

**1. RAG (Retrieval-Augmented Generation)**  
Access to real-time documentation and codebase knowledge through web search, Archon (detailed later), and other tools. Prevents hallucinations by grounding responses in verified information.

**2. Task Management**  
Structured tracking of development work via Archon, Claude Taskmaster MCP, and built-in tools like TodoWrite. Maintains focus and provides visibility into progress throughout complex projects.

**3. Memory**  
Persistent context across sessions including conversation history, project state, and architectural decisions. Enables coherent multi-step workflows without repetitive explanations.

**4. Prompt Engineering**  
Structured approaches like the PRP framework (our focus), Claude Flow, and the BMAD Method that guide AI behavior. Determines output quality and ensures reproducible results.

</td>
</tr>
</table>

## 🤖 AI Coding Assistant Compatibility

While this workshop focuses on Claude Code (the most agentic and powerful AI coding assistant that can execute PRPs end-to-end), these context engineering strategies work with any AI coding assistant. The PRP framework, global rules, and example-driven approaches are universal principles that enhance development across all platforms.

## 📦 What We're Building

Throughout this workshop, we'll build a **Hybrid RAG Agent** that showcases three powerful retrieval strategies:

- **Knowledge Graph Retrieval**: Using Graphiti with Neo4j for structured relationship data
- **Semantic Similarity Search**: Leveraging PGVector with PostgreSQL for contextual understanding  
- **Hybrid Search**: Combining TSVector with PostgreSQL for keyword-based retrieval

**Core Technologies:**
- **Agent Framework**: Pydantic AI for robust Python AI agent development
- **Backend**: Graphiti + Neo4j for knowledge graph operations
- **Database**: PostgreSQL with PGVector and TSVector extensions
- **AI Assistant**: Claude Code for agentic terminal-based development

---

## 📚 Planning: The Foundation of Success

### 📝 Prompt Progression

Understanding how to craft effective prompts is the first step toward mastering AI coding assistants. The `PromptProgression/` folder demonstrates the evolution from vague "vibe coding" to comprehensive context engineering, showing exactly what goes into a production-ready prompt.

<details>
<summary><strong>Deep Dive: From Bad Prompts to Perfect PRPs</strong></summary>

### The Problem with Vague Prompts

Starting with `bad_prompt.md`, we see common issues:
- ❌ **Vague Requirements**: "word counter tool", "maybe add argparse" 
- ❌ **Zero Context**: No existing patterns or implementation guidance
- ❌ **No Validation**: No testing approach or success criteria
- ❌ **Ambiguous Scope**: "modular so I can reuse parts" - what constitutes modularity?

**Expected Outcome**: 60-80% implementation requiring multiple iterations.

### The Evolution Journey

The progression through task_prompt_1.md to task_prompt_8_prp.md shows systematic improvements:

1. **Basic Specificity** (task_prompt_1): Single function focus, clear input/output
2. **Structured Format** (task_prompt_2): ACTION patterns, validation commands
3. **Task Chaining** (task_prompt_3): Multiple related tasks with progressive validation
4. **Infrastructure Focus** (task_prompt_4): Testing framework and dependency management
5. **Modular Architecture** (task_prompt_5): Clean separation of concerns
6. **Feature Extensions** (task_prompt_6): Systematic integration patterns
7. **Context References** (task_prompt_7): Documentation and security patterns
8. **Complete PRP** (task_prompt_8): Everything needed for one-pass success

### Key Techniques Progression

**Success Rate Evolution**: 20% → 40% → 60% → 75% → 85% → 95%

Each improvement adds specific engineering techniques:
- Direct instruction → Structured task format
- Single tasks → Task chaining
- Basic requirements → Context engineering
- Simple validation → Progressive validation gates
- Basic implementation → Anti-pattern prevention

### The PRP Difference

The final PRP (task_prompt_8) includes:
- ✅ **Complete Context Engineering**: Comprehensive documentation references
- ✅ **One-Pass Implementation**: Everything needed upfront
- ✅ **Progressive Validation**: Multi-tier verification strategy
- ✅ **Anti-Pattern Prevention**: Explicit guidance on what to avoid
- ✅ **LLM Trust Engineering**: Minimal parsing, error transparency
- ✅ **Architecture-First Design**: Clean separation with patterns

This progression naturally leads us to understand why PRP is the optimal solution for AI coding.

</details>

### 🎯 PRP Framework

The PRP (Product Requirements Prompt) framework is a structured methodology that combines traditional PRD elements with AI-critical layers, enabling one-pass implementation success through comprehensive context engineering. The approach differs based on whether you're building new functionality or enhancing existing codebases.

<p align="center">
  <img src="images/PRPSteps.png" alt="PRP Framework Process" width="900"/>
</p>

<details>
<summary><strong>Deep Dive: Mastering the PRP Framework</strong></summary>

### What is PRP?

Created by Rasmus Widing, a product manager who has been diving deep into AI coding for over a year now, PRP provides everything an AI needs to deliver production-ready software.

### Core Components

**PRP = PRD + Curated Codebase Intelligence + Agent Runbook**

The framework includes:
- **Business Context**: Domain, requirements, and success criteria
- **Technical Context**: File paths, library versions, code patterns, architecture, and best practices
- **Implementation Blueprint**: Step-by-step development approach
- **Validation Framework**: Testing strategy and acceptance criteria

### PRP Structure

```markdown
## Goal
[What needs to be built - specific end state]

## Why
[Business justification and user value]

## What
[Detailed feature specification with success criteria]

## All Needed Context
- Documentation links and references
- File paths and existing code patterns  
- Library versions and gotchas
- Architecture constraints

## Implementation Blueprint
[Step-by-step development approach]

## Validation Loop
[Testing strategy and acceptance criteria]
```

### Why PRP Works

- **Comprehensive Context**: LLMs perform better with complete information
- **Reduced Iterations**: Minimal back-and-forth clarifications
- **Production Ready**: Includes testing and validation from the start
- **Flexible Approach**: Adapts to both new and existing codebases

### Two Workflows: New vs Existing Codebases

#### For New Projects/Greenfield Development

The INITIAL.md approach works best when building from scratch:

1. **Create INITIAL.md** with your requirements
2. **Run /generate-pydantic-ai-prp** to research and create PRP
3. **Review generated PRP** for completeness
4. **Execute with /execute-pydantic-ai-prp** for implementation

The INITIAL.md structure for new projects:
- **FEATURE**: Specific description of what to build
- **EXAMPLES**: Reference implementations from examples/ folder
- **DOCUMENTATION**: Links to relevant resources
- **OTHER CONSIDERATIONS**: Gotchas and special requirements

Added sections for building AI agents specifically:
- **TOOLS**: Required functionality and interfaces
- **DEPENDENCIES**: External services and configurations
- **SYSTEM PROMPTS**: Instructions for agent behavior

#### For Existing Codebases

When working with existing code, use a discovery-first approach:

1. **Codebase Investigation** (`/primer slash command or telling it to look at key files explicity`):
   - AI analyzes existing architecture and patterns
   - Identifies relevant components and dependencies
   - Documents current implementation approaches

2. **Research & Planning Phase**:
   - Collaborate with AI, for example: "I'm looking to implement X, please investigate my codebase and think hard about our options, write a report on your findings in MD format"
   - Generate investigation reports documenting findings
   - Web search + Archon MCP for best practices and similar implementations
   - Back-and-forth discussions to refine approach

3. **PRP Creation for Features**:
   - Once confident in approach: `/generate-pydantic-ai-prp "create a PRP following your findings report and our planning"`
   - Create smaller, focused PRPs for individual features rather than monolithic documents
   - Each PRP should target specific functionality (e.g., "Add OAuth provider", "Implement caching layer")

Note: You can still use a markdown first approach like we do with INITIAL.md for new codebases. The main difference is your examples will be more focused on parts of the existing codebase versus external documentation and web search (there will still be some of that but less).

### Example: Adding Authentication to Existing App

```bash
# 1. Investigate existing codebase
/primer

# 2. Research and plan
"Investigate our current user management and session handling. 
I want to add OAuth2 authentication. Write a report on integration options."

# 3. After research and discussion
/prp-create "Create PRP for adding Google OAuth2 provider following your report with the session management patterns 
we discovered in src/auth/"

# 4. Execute focused PRP (AFTER validating!)
/execute-pydantic-ai-prp PRPs/oauth2-google-provider.md
```

</details>

### ⚙️ Global Rules

Global rules (CLAUDE.md) define foundational principles that remain constant across your entire codebase. This is where you define all best practices, styles, architecture, and patterns of development you want the coding agent to **always** follow. Think of it like the primary system prompt for your AI coding assistant.

<details>
<summary><strong>Deep Dive: Mastering Global Rules and CLAUDE.md</strong></summary>

### What Are Global Rules?

Global rules are project-wide instructions that Claude Code (and other AI assistants) automatically load into context. Unlike PRP which is task-specific, global rules establish permanent behavioral patterns and coding standards.

### CLAUDE.md File Hierarchy

Claude reads files in this order:
1. **Current Directory** (`./CLAUDE.md`) - Project-specific rules
2. **Parent Directories** - Up to repository root for monorepos
3. **Home Directory** (`~/.claude/CLAUDE.md`) - Spans across all projects
4. **Local Override** (`./CLAUDE.local.md`) - Uncommitted personal settings

### What Belongs in Global Rules

**Architecture & Patterns**:
- Design principles (SOLID, DRY, KISS)
- Architectural patterns (MVC, microservices, event-driven)
- Module organization and file structure
- Dependency injection patterns

**Coding Standards**:
- Naming conventions (camelCase, snake_case, PascalCase)
- Code formatting rules (indentation, line length)
- Comment and documentation standards
- Import organization

**Development Practices**:
- Error handling patterns
- Logging conventions
- Security requirements (never hardcode secrets)
- Testing approach (TDD, unit/integration split)

**Anti-Patterns to Avoid (Claude Loves These Things, so Prompt to Avoid Them!)**:
- ❌ Over-engineering simple solutions
- ❌ Backward compatibility for new projects
- ❌ Creating files over 500 lines
- ❌ Mixing concerns in single modules
- ❌ Skipping validation and tests

### Best Practices for CLAUDE.md

**Keep It Concise**: Write for Claude, not onboarding a junior dev
```markdown
# BAD: Long narrative
The project uses React for the frontend framework because we believe...

# GOOD: Direct bullet point
- Frontend: React 18 with TypeScript
```

**Be Specific About Behaviors**:
```markdown
# Project Awareness
- Always read PLANNING.md at conversation start
- Check TASK.md before starting new work
- Mark tasks complete immediately after finishing

# Code Structure
- Never create files > 500 lines
- Split into modules when approaching limit
- Group by feature, not file type
```

**Include Utility Patterns**:
```markdown
# Common Patterns
- Database connections: Use connection pooling via db_pool
- API calls: Always use async/await with proper error handling
- File I/O: Use pathlib for cross-platform compatibility
```

### Advanced Features

**File Importing**:
```markdown
<!-- Load entire file content -->
![[path/to/patterns.md]]

<!-- Reference without loading -->
See authentication patterns in: docs/auth.md
```

**Dynamic Updates**:
Press `#` in Claude Code to add new rules on the fly:
```
# Always use pytest for testing, never unittest
```

### Global Rules vs PRP Context

| Global Rules | PRP Context |
|-------------|-------------|
| Permanent patterns | Task-specific requirements |
| Architecture principles | Feature implementation details |
| Coding standards | One-time configurations |
| Security requirements | Project-specific gotchas |
| Testing approach | Specific validation gates |

### Cross-Platform Compatibility

Other AI assistants use different filenames:
- **Cursor**: `.cursorrules`
- **Windsurf**: `.windsurfrules`
- **Continue**: `.continue/config.json`

The principles remain the same - include as system instructions or context files.

</details>

### 🌐 Archon Integration

Archon serves as the command center for AI coding assistants, providing a sophisticated knowledge and task management system. We as the humans manage the knowledge, tasks, and documents through a sleek UI, and the AI coding assistant accesses and manages the same knowledge, tasks, and documents through the MCP server.

Archon knowledge used for this workshop:
- **Pydantic AI**: https://ai.pydantic.dev/llms-full.txt
- **Graphiti**: https://help.getzep.com/graphiti/getting-started/welcome

<details>
<summary><strong>Deep Dive: Leveraging Archon for AI Development</strong></summary>

### What is Archon?

[Archon](https://archon.diy) is the knowledge and task management backbone for AI coding assistants. It provides a sleek interface to manage knowledge, context, and tasks while functioning as an MCP server for AI collaboration.

### Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Frontend UI     │    │ Server (API)    │    │ MCP Server      │    │ Agents Service  │
│ React + Vite    │◄──►│ FastAPI +       │◄──►│ Lightweight     │◄──►│ PydanticAI      │
│ Port 3737       │    │ SocketIO        │    │ HTTP Wrapper    │    │ Port 8052       │
│                 │    │ Port 8181       │    │ Port 8051       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                                        │
                                └────────────────┬───────────────────────┘
                                                 ▼
                                       ┌─────────────────┐
                                       │ Database        │
                                       │ Supabase        │
                                       │ PostgreSQL      │
                                       │ PGVector        │
                                       └─────────────────┘
```

### Core Features

**Knowledge Management**:
- **Smart Web Crawling**: Automatically crawls documentation sites
- **Document Processing**: PDF, Word, markdown with intelligent chunking
- **Vector Search**: Advanced semantic search with contextual embeddings
- **Hybrid Search**: Combines vector and keyword matching

**Task Management**:
- Project creation and organization
- Task tracking with status updates
- Document versioning and history
- Feature tracking and dependencies

### MCP Integration

Archon provides MCP tools for comprehensive functionality, including:

**RAG Operations**:
- `perform_rag_query`: Search knowledge base with reranking
- `search_code_examples`: Find relevant code patterns
- `get_available_sources`: List indexed documentation

**Project Management**:
- `create_project`: Initialize new projects
- `list_projects`: View all projects
- `update_project`: Modify project details

**Task Operations**:
- `create_task`: Add new tasks with dependencies
- `list_tasks`: Filter by status, project, assignee
- `update_task`: Change status, assignee, priority

### Workflow Integration

**Setup in Claude Code**:
```bash
# Add Archon MCP server
claude mcp add archon http://localhost:8051/mcp

# Or when in a dev container: claude mcp add archon http://host.docker.internal:8051/mcp

# Verify connection
claude mcp list
```

**Using Archon in PRPs**:
```yaml
# In your PRP context section
mcp: Archon
query: "Pydantic AI agent patterns"
why: Get latest documentation and examples
```

**Feature-Level Project Management**:

Archon projects can represent individual features within your existing codebase, not just entire applications. This granular approach provides focused context and tracking:

```bash
# Example: One codebase, multiple feature projects
MyApp/
  ├── Project: "OAuth2 Integration" (Archon project for auth feature)
  │   ├── Task 1: Research existing auth patterns
  │   ├── Task 2: Design OAuth2 provider interface
  │   ├── Task 3: Implement Google provider
  │   └── Task 4: Add tests and documentation
  │
  ├── Project: "Search Enhancement" (Archon project for search feature)
  │   ├── Task 1: Analyze current search implementation
  │   ├── Task 2: Design vector search integration
  │   └── Task 3: Implement hybrid search
  │
  └── Project: "Performance Optimization" (Archon project for optimization)
      ├── Task 1: Profile database queries
      ├── Task 2: Implement caching layer
      └── Task 3: Add connection pooling
```

**Task Management Flow (New Project)**:
1. Create project for your development
2. Generate tasks from PRP requirements
3. Update task status as you progress
4. Use RAG for documentation lookup
5. Track feature completion

**Task Management Flow (Existing Code)**:
1. Create project for each major feature or enhancement
2. Break feature into granular tasks (investigation, design, implementation, testing)
3. Update task status as you progress (todo → doing → review → done)
4. Use RAG for documentation lookup specific to that feature domain
5. Track feature completion

### Benefits for AI Development

- **Centralized Context**: Single source of truth for all documentation
- **Team Collaboration**: Shared knowledge base and task tracking
- **Advanced RAG**: Semantic search with reranking for better results
- **Version Control**: Track document and requirement changes
- **Real-time Updates**: Live collaboration via Socket.IO

### Current Status

Archon is in beta with active development. Join the community in [GitHub](https://github.com/coleam00/Archon) for updates and contributions.

</details>

---

## 🏗️ Implementation: Building with AI

### 🐳 Dev Containers

Dev containers provide isolated, reproducible development environments that enable "YOLO mode" - allowing AI assistants to perform any action safely without affecting your host system.

<details>
<summary><strong>Deep Dive: Safe Development with Dev Containers</strong></summary>

### Why Dev Containers?

Dev containers solve the "destructive AI" problem - enabling rapid experimentation while maintaining safety through containerization. This allows Claude Code to operate with full permissions in an isolated environment.

### Security Features

Our dev container provides:
- **Network Isolation**: Custom firewall restricts outbound connections
- **Whitelisted Domains**: Only approved services (GitHub, npm, Anthropic)
- **Pre-installed Tools**: Claude Code, GitHub CLI, development utilities
- **Secure Environment**: Built on Node.js 20 with security patches

### Setup Process

1. **Prerequisites**:
   - Install [Docker](https://www.docker.com/)
   - Install VS Code (or Cursor/Windsurf)

2. **Activate Container**:
   - Press `F1` or `Ctrl/Cmd + Shift + P`
   - Select "Dev Containers: Reopen in Container"
   - OR click blue button in bottom-left → "Reopen in Container"

3. **Wait for Build** (first time ~3-5 minutes)

4. **Open Terminal**: `Ctrl + J` or Terminal → New Terminal

5. **Run in YOLO Mode**:
   ```bash
   claude --dangerously-skip-permissions
   ```

Note: If you are running the dev container for the first time, you'll have to go through the Claude Code authentication process.

### Configuration Structure

```
.devcontainer/
├── devcontainer.json    # VS Code configuration
├── Dockerfile          # Container image definition
└── init-firewall.sh    # Security script
```

### Network Security

The `init-firewall.sh` script implements:
```bash
# Allow only specific domains (add more domains that you want Claude Code to be able to search through)
ALLOWED_DOMAINS=(
  "github.com"
  "api.github.com"
  "api.anthropic.com"
  "registry.npmjs.org"
)

# Block all other outbound traffic
iptables -P OUTPUT DROP
```

</details>

### ⚡ Slash Commands

Slash commands provide reusable workflows that eliminate repetitive tasks and ensure consistent implementation patterns across your development process.

<details>
<summary><strong>Deep Dive: Automating with Slash Commands</strong></summary>

### What Are Slash Commands?

Slash commands are reusable prompt templates stored in `.claude/commands/` that automate complex workflows. They accept arguments via `$ARGUMENTS` and execute consistent, tested procedures.

### Core PRP Commands

**`/generate-pydantic-ai-prp`**:
```markdown
# Generate comprehensive PRP from initial requirements
# Usage: /generate-pydantic-ai-prp PRPs/INITIAL.md

Process:
1. Read initial requirements
2. Research codebase patterns
3. Search documentation with Archon
4. Create structured PRP
5. Include validation gates
```

**`/execute-pydantic-ai-prp`**:
```markdown
# Implement complete agent from PRP
# Usage: /execute-pydantic-ai-prp PRPs/agent.md

Process:
1. Load PRP context
2. Create task list with TodoWrite
3. Implement components
4. Run validation gates
5. Fix any issues
```

### Custom Command Structure

```markdown
# Command: analyze-codebase
# Description: Comprehensive repository analysis

## Arguments
- $ARGUMENTS: Path to analyze (default: current directory)

## Steps
1. Read project structure
2. Analyze dependencies
3. Identify patterns
4. Generate summary

## Validation
- Verify all files readable
- Check for .gitignore patterns
- Validate dependency versions

## Output
- ANALYSIS.md with findings
- Recommendations for improvements
```

### Command Best Practices

**Use Variables**:
```markdown
# Good - flexible
$ARGUMENTS
$PROJECT_PATH
$CONFIG_FILE

# Bad - hardcoded
PRPs/specific-file.md
/home/user/project
config.json
```

**Include Validation**:
```markdown
## Validation Gates
- [ ] Tests pass: pytest
- [ ] Linting clean: ruff check
- [ ] Types correct: mypy
```

**Provide Context**:
```markdown
## Context References
- Read: PLANNING.md
- Check: TASK.md
- Use: examples/patterns/
```

### Creating Custom Commands

1. **Create file**: `.claude/commands/my-command.md`
2. **Define structure**:
   ```markdown
   # Command: my-workflow
   Description here
   
   ## Steps
   1. First action
   2. Second action
   
   ## Validation
   - Check results
   ```

3. **Use in Claude Code**: `/my-workflow arguments`

### Cross-Platform Usage

Other AI assistants can use commands as regular prompts:
```bash
# In Cursor/Windsurf
# Copy command content and paste with arguments
```

</details>

### 🤖 Subagents

Subagents enable specialized AI collaboration through a structured team approach, where each agent focuses on their domain expertise for optimal results.

<details>
<summary><strong>Deep Dive: Orchestrating AI Subagents</strong></summary>

### Subagent Architecture

Our workflow demonstrates parallel and sequential agent collaboration:

```
           User Request
                ↓
    [Phase 1: PRP Generation]
                ↓
    [Phase 2: Parallel Execution]
           ↙    ↓    ↘
    Prompt   Tool    Dependency
    Engineer Integrator Manager
           ↘    ↓    ↙
    [Phase 3: Implementation]
           Claude Code
                ↓
    [Phase 4: Validation]
         Validator Agent
```

### Specialized Agent Roles

**Prompt Engineer** (`pydantic-ai-prompt-engineer`):
- Creates system prompts (100-300 words)
- Focuses on clear, concise instructions
- Outputs: `planning/prompts.md`

**Tool Integrator** (`pydantic-ai-tool-integrator`):
- Designs 2-5 essential tools
- Defines parameters and error handling
- Outputs: `planning/tools.md`

**Dependency Manager** (`pydantic-ai-dependency-manager`):
- Plans environment variables
- Configures model providers
- Outputs: `planning/dependencies.md`

**Validator** (`pydantic-ai-validator`):
- Creates comprehensive test suites
- Validates against PRP requirements
- Outputs: `tests/` directory

### Subagent Configuration

Each subagent has specialized context:

```markdown
# .claude/agents/pydantic-ai-prompt-engineer.md

You are a system prompt specialist for Pydantic AI agents.

## Your Role
- Create clear, focused system prompts
- Keep prompts 100-300 words
- Focus on essential behavior only

## Input
- PRP document with requirements

## Output
- planning/prompts.md with specifications
- MARKDOWN only, no Python code
```

### Communication Protocol

**Input Standards**:
- Pass paths to files the subagent needs to read
- Include Archon project ID if available
- Specify output paths clearly

**Output Standards**:
- Markdown specifications (not code)
- Structured format for parsing
- Clear success/failure indicators

### Best Practices

**Keep Agents Focused**:
- Single responsibility per agent
- Clear input/output contracts
- No overlapping concerns

**Enable Parallel Work**:
- Independent task design
- No shared state during execution
- Combine results after completion

**Validate Continuously**:
- Each agent self-validates
- Main agent validates integration
- Validator agent final check

</details>

### 🏗️ Building the RAG Agent

Our workshop's practical implementation showcases a sophisticated hybrid RAG agent combining multiple retrieval strategies for comprehensive knowledge access.

<details>
<summary><strong>Deep Dive: Hybrid RAG Agent Architecture</strong></summary>

### System Overview

Our agent combines three retrieval strategies:

```
User Query
     ↓
[Pydantic AI Agent]
     ↓
┌────────────────────────────────────┐
│        Retrieval Layer             │
├────────────┬───────────┬───────────┤
│  Vector    │  Hybrid   │  Graph    │
│  Search    │  Search   │  Search   │
├────────────┼───────────┼───────────┤
│ PGVector   │ TSVector  │  Neo4j    │
│ PostgreSQL │PostgreSQL │ Graphiti  │
└────────────┴───────────┴───────────┘
```

### Core Components

**Vector Search (Semantic)**:
```python
async def vector_search(query: str, limit: int = 10):
    """Pure semantic similarity using pgvector"""
    embedding = await generate_embedding(query)
    return await db.vector_search(embedding, limit)
```

**Hybrid Search (Semantic + Keyword)**:
```python
async def hybrid_search(
    query: str, 
    limit: int = 10,
    text_weight: float = 0.3
):
    """Combined pgvector + tsvector search"""
    embedding = await generate_embedding(query)
    return await db.hybrid_search(
        embedding=embedding,
        query_text=query,
        limit=limit,
        text_weight=text_weight  # Balance semantic vs keyword
    )
```

**Graph Search (Relationships)**:
```python
async def graph_search(query: str):
    """Knowledge graph traversal with Neo4j"""
    return await graphiti.search(query)
```

**Comprehensive Search (All Combined)**:
```python
async def perform_comprehensive_search(
    query: str,
    use_vector: bool = True,
    use_graph: bool = True,
    limit: int = 10
):
    """Master function combining all strategies"""
    tasks = []
    if use_vector:
        tasks.append(vector_search(query, limit))
    if use_graph:
        tasks.append(graph_search(query))
    
    results = await asyncio.gather(*tasks)
    return combine_results(results)
```

### PostgreSQL Schema

```sql
-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chunks with embeddings
CREATE TABLE chunks (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id),
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI dimension
    metadata JSONB,
    -- Full text search
    search_vector tsvector GENERATED ALWAYS AS 
        (to_tsvector('english', content)) STORED
);

-- Indexes for performance
CREATE INDEX chunks_embedding_idx ON chunks 
    USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX chunks_search_idx ON chunks 
    USING GIN (search_vector);
```

### Ingestion Pipeline

1. **Document Processing**:
   - Semantic chunking with LLM
   - Metadata extraction
   - Entity recognition

2. **Embedding Generation**:
   - OpenAI/Ollama/Gemini support
   - Batch processing for efficiency
   - Caching for repeated content

3. **Knowledge Graph Building**:
   - Entity extraction with Graphiti
   - Relationship mapping
   - Temporal awareness

### System Prompts

```python
SYSTEM_PROMPT = """You are an intelligent AI assistant with access to:
1. Vector search for semantic similarity
2. Hybrid search combining semantic and keywords (TSVector)
3. Knowledge graph for entity relationships
4. Comprehensive search combining all approaches

Use hybrid_search for semantic + keyword needs.
Use perform_comprehensive_search for complete analysis.
Use graph search only for entity relationships.
"""
```

### Performance Optimizations

- **Connection Pooling**: AsyncPG for PostgreSQL
- **Embedding Cache**: Reuse computed embeddings
- **Batch Operations**: Process multiple queries
- **Index Optimization**: IVFFlat for vectors, GIN for text
- **Query Planning**: Parallel execution strategies

</details>

### 🎭 Honorable Mentions

Additional features that enhance your AI coding workflow but aren't essential for the core development process.

<details>
<summary><strong>Deep Dive: Advanced Features</strong></summary>

### Claude Hooks

Hooks are automation triggers that execute custom commands based on specific events in your Claude Code workflow.

**Available Hook Events**:
- **PreToolUse/PostToolUse**: Before/after tool execution
- **UserPromptSubmit**: When user submits a prompt
- **SessionStart/SessionEnd**: Session lifecycle events
- **Stop/SubagentStop**: Interruption events

**Example Hook Configuration** (in `.claude/settings.local.json`):
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "ruff check --fix"
      }]
    }],
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.sh"
      }]
    }]
  }
}
```

### Output Styles

Customize how Claude Code responds by modifying its system prompt for different contexts.

**Built-in Styles**:
- **Default**: Standard software engineering focus
- **Explanatory**: Adds educational "Insights" sections
- **Learning**: Collaborative mode with `TODO(human)` markers

**Usage**:
```bash
# Access style menu
/output-style

# Set specific style
/output-style explanatory
```

**Custom Styles**:
Create custom styles with `/output-style:new` and save to `~/.claude/output-styles/`:
```markdown
---
name: concise
description: Brief, focused responses
---
Be extremely concise. No explanations unless asked.
Focus on implementation, not theory.
```

### Advanced MCP Servers

Beyond Archon, integrate specialized MCP servers:

- **Puppeteer**: Browser automation and testing
- **Supabase**: Real-time database operations
- **Neon**: Serverless PostgreSQL
- **Sentry**: Error monitoring
- **Playwright**: E2E testing automation

### Parallel Development

Use Git worktrees for multiple simultaneous implementations:

```bash
# Create parallel branches
/prep-parallel feature-name 3

# Execute in parallel
/execute-parallel feature-name plan.md 3

# Compare and merge best
git merge feature-name-2
```

</details>

---

## ✅ Validation: Ensuring Quality

### 🔍 Validation Gates

Comprehensive validation ensures code quality through multi-tier testing strategies and automated quality gates that prevent progression until all criteria are met.

<details>
<summary><strong>Deep Dive: Multi-Tier Validation Strategy</strong></summary>

### Validation Levels

Our validation strategy progresses through five levels:

```
Level 1: Syntax & Style
    ↓ (must pass)
Level 2: Type Safety  
    ↓ (must pass)
Level 3: Unit Testing
    ↓ (must pass)
Level 4: Integration Testing
    ↓ (must pass)
Level 5: Human Review
```

### Level 1: Syntax & Style

**Automated Formatting**:
```bash
# Python
black src/ --check
isort src/ --check-only
ruff check src/

# JavaScript/TypeScript
eslint src/ --max-warnings 0
prettier --check "src/**/*.{js,ts,jsx,tsx}"
```

**Configuration** (`.ruff.toml`):
```toml
line-length = 100
target-version = "py311"

[lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]  # Line length handled by black
```

### Level 2: Type Safety

**Static Type Checking**:
```bash
# Python
mypy src/ --strict

# TypeScript
tsc --noEmit
```

**Type Coverage Requirements**:
```python
# mypy.ini
[mypy]
python_version = 3.11
strict = True
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### Level 3: Unit Testing

**Test Structure**:
```python
def test_vector_search():
    """Test semantic search functionality"""
    # Arrange
    query = "test query"
    mock_embedding = [0.1] * 1536
    
    # Act
    results = vector_search(query, limit=5)
    
    # Assert
    assert len(results) <= 5
    assert all(r.score >= 0 for r in results)
```

**Coverage Requirements**:
```bash
pytest tests/ -v --cov=src/ --cov-report=term-missing
# Minimum 80% coverage required
```

### Level 4: Integration Testing

**End-to-End Validation**:
```python
async def test_comprehensive_search_integration():
    """Test all retrieval strategies together"""
    # Setup test data
    await setup_test_database()
    await setup_test_graph()
    
    # Execute comprehensive search
    results = await perform_comprehensive_search(
        query="test entity relationships",
        use_vector=True,
        use_graph=True
    )
    
    # Validate results from all sources
    assert results["vector_results"]
    assert results["graph_results"]
    assert results["total_results"] > 0
```

### Level 5: Human Review

**Review Checklist**:
- [ ] Business logic correctness
- [ ] Edge case handling
- [ ] Security considerations
- [ ] Performance implications
- [ ] Documentation completeness

### Validation Gates in PRPs

Every PRP includes executable validation gates:

```yaml
validation_gates:
  syntax:
    - command: "ruff check src/ --fix"
      must_pass: true
    - command: "black src/ --check"
      must_pass: true
  
  types:
    - command: "mypy src/ --strict"
      must_pass: true
  
  tests:
    - command: "pytest tests/unit/ -v"
      must_pass: true
    - command: "pytest tests/integration/ -v"
      must_pass: true
  
  coverage:
    - command: "pytest --cov=src/ --cov-fail-under=80"
      must_pass: true
```

</details>

### 🤖 Validation Subagent

The validation subagent specializes in creating comprehensive test suites and ensuring all implementation meets PRP requirements through systematic validation. It's common and powerful to have a subagent in your project specifically for validation, and that's what we have in this workshop for building AI agents.

<details>
<summary><strong>Deep Dive: The Validation Specialist</strong></summary>

### Validation Agent Role

The `pydantic-ai-validator` subagent serves as the quality gatekeeper:

```
Implementation Complete
         ↓
[Validation Subagent]
         ↓
    ┌────────────┐
    │Read PRP    │ → Extract validation gates
    │Read Code   │ → Analyze implementation
    │Create Tests│ → Generate test suite
    │Run Tests   │ → Execute validation
    │Report      │ → Document results
    └────────────┘
```

### Validation Agent Capabilities

**Test Generation**:
- Creates unit tests for all functions
- Generates integration tests for workflows
- Produces edge case scenarios
- Implements mock strategies

**Requirement Validation**:
- Maps PRP requirements to tests
- Ensures feature completeness
- Validates success criteria
- Checks anti-pattern avoidance

**Quality Assurance**:
- Coverage analysis
- Performance testing
- Security validation
- Documentation verification

### Agent Configuration

```markdown
# .claude/agents/pydantic-ai-validator.md

You are a validation specialist for Pydantic AI agents.

## Your Mission
Create comprehensive test suites that validate:
1. All PRP requirements are met
2. Validation gates pass
3. Edge cases are handled
4. Performance meets criteria

## Input
- PRP document with validation gates
- Implemented agent code
- Archon project ID (if available)

## Output
tests/
├── test_agent.py        # Agent behavior tests
├── test_tools.py        # Tool functionality
├── test_integration.py  # End-to-end workflows
├── test_validation.py   # PRP requirement checks
├── conftest.py         # Test fixtures
└── VALIDATION_REPORT.md # Results summary
```

### Test Generation Strategy

**Unit Test Template**:
```python
# Generated by validation agent
import pytest
from unittest.mock import Mock, patch
from pydantic_ai.models.test import TestModel

def test_tool_registration():
    """Verify all tools are properly registered"""
    assert len(agent.tools) == expected_tool_count
    assert all(hasattr(t, '__name__') for t in agent.tools)

def test_tool_parameters():
    """Validate tool parameter schemas"""
    for tool in agent.tools:
        schema = tool.get_schema()
        assert 'parameters' in schema
        assert schema['parameters']['type'] == 'object'

@pytest.mark.asyncio
async def test_agent_with_test_model():
    """Test agent behavior with TestModel"""
    test_model = TestModel()
    with agent.override(model=test_model):
        result = await agent.run("test query")
        assert result.output
        assert len(result.tool_calls) > 0
```

**Integration Test Pattern**:
```python
@pytest.mark.integration
async def test_full_workflow():
    """Validate complete agent workflow"""
    # Setup
    deps = AgentDependencies(session_id="test")
    
    # Execute
    result = await agent.run(
        "Find information about AI initiatives",
        deps=deps
    )
    
    # Validate
    assert result.output
    assert "vector_search" in [t.name for t in result.tool_calls]
    validate_response_format(result.output)
```

### Validation Report Format

```markdown
# Validation Report

## Summary
- Total Requirements: 15
- Passed: 14
- Failed: 1
- Coverage: 92%

## Requirement Validation

### ✅ Functional Requirements
- [x] Vector search implemented
- [x] Hybrid search working
- [x] Graph search integrated
- [x] Comprehensive search combines all

### ❌ Failed Requirements
- [ ] Performance: Search exceeds 1s timeout
  - Current: 1.3s average
  - Required: <1s
  - Recommendation: Add caching layer

## Test Results
...
```

</details>

---

## 🎓 Success Outcomes

After completing this workshop, you'll have:

✅ **Complete Template Repository**: Production-ready template with all workshop resources  
✅ **Hybrid RAG Agent**: Fully functional agent with three retrieval strategies  
✅ **PRP Mastery**: Structured approach to AI-assisted development  
✅ **Context Engineering Skills**: Professional-grade AI coding techniques  
✅ **Validation Expertise**: Quality assurance and testing automation

## 📂 Template Structure

```
full-ai-coding-workflow/
├── .claude/
│   ├── commands/              # Slash commands for automation
│   │   ├── generate-pydantic-ai-prp.md
│   │   └── execute-pydantic-ai-prp.md
│   ├── agents/               # Subagent configurations
│   │   ├── pydantic-ai-prompt-engineer.md
│   │   ├── pydantic-ai-tool-integrator.md
│   │   ├── pydantic-ai-dependency-manager.md
│   │   └── pydantic-ai-validator.md
│   └── settings.local.json   # Permissions configuration
├── .devcontainer/            # Dev container setup
│   ├── devcontainer.json
│   ├── Dockerfile
│   └── init-firewall.sh
├── PRPs/
│   ├── templates/            # Base PRP templates
│   │   └── prp_pydantic_ai_base.md
│   ├── examples/            # Reference implementations
│   └── INITIAL.md          # Starting point for PRPs
├── PromptProgression/       # Evolution from bad to perfect prompts
├── FullExample/            # Complete RAG agent implementation
├── CLAUDE.md              # Global rules for AI assistant
├── copy_template.py       # Template deployment script
└── README.md             # This comprehensive guide
```
