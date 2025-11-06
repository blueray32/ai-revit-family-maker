# PRP Templates - Context Engineering Hub

> **A PRP is PRD + curated codebase intelligence + agent/runbook—the minimum viable packet an AI needs to plausibly ship production-ready code on the first pass.**

Based on https://github.com/Wirasm/PRPs-agentic-eng

A collection of PRP templates for different use cases. Each template provides the context engineering framework to help AI coding assistants deliver production-ready code on the first pass.

## 🚀 Templates Overview

### 🔧 [prp-base-python](./prp-base-python/) - Python PRP Template

**Drop into any existing Python project**

Add comprehensive context engineering to any Python codebase in 30 seconds.

```bash
# Quick start
git clone https://github.com/dynamous-community/context-engineering-hub.git
cp -r context-engineering-hub/prp-templates/prp-base-python/PRPs/ your-project/
cp -r context-engineering-hub/prp-templates/prp-base-python/.claude/ your-project/
```

**Perfect for:** Adding structured feature development to existing Python projects

---

### 🌐 [mcp-server](./mcp-server/) - MCP Server Project Starter

**Complete MCP server with TypeScript, auth, and database tools**

Full project template for building Model Context Protocol servers.

```bash
# Quick start
git clone https://github.com/dynamous-community/context-engineering-hub.git
cp -r context-engineering-hub/prp-templates/mcp-server/ your-mcp-project/
cd your-mcp-project && npm install
```

**Perfect for:** Building MCP servers with authentication, database tools, and testing

---

### 🤖 [pydantic-ai](./pydantic-ai/) - Pydantic AI Agent Starter

**Multi-agent Python project with structured outputs**

Complete project template for building Pydantic AI agents with tools and validation.

```bash
# Quick start
git clone https://github.com/dynamous-community/context-engineering-hub.git
cp -r context-engineering-hub/prp-templates/pydantic-ai/ your-agent-project/
```

**Perfect for:** Building Python AI agents with structured outputs and tool integration

---

### 📝 [prp-typescript](./prp-typescript/) - TypeScript PRP Template

**TypeScript-focused PRP framework**

Specialized template for TypeScript projects with type-safe patterns and build integration.

```bash
# Quick start
git clone https://github.com/dynamous-community/context-engineering-hub.git
cp -r context-engineering-hub/prp-templates/prp-typescript/PRPs/ your-project/
cp -r context-engineering-hub/prp-templates/prp-typescript/.claude/ your-project/
```

**Perfect for:** TypeScript applications with strict type checking and modern build tools

---

### 🧪 [prp-base-experimental](./prp-base-experimental/) - Experimental PRP Template

**Advanced PRPs with quality validation**

Cutting-edge template with quality validation agents and precision implementation standards.

```bash
# Quick start
git clone https://github.com/dynamous-community/context-engineering-hub.git
cp -r context-engineering-hub/prp-templates/prp-base-experimental/PRPs/ your-project/
cp -r context-engineering-hub/prp-templates/prp-base-experimental/.claude/ your-project/
```

**Perfect for:** Teams pushing the boundaries of context engineering with advanced validation

---

### ⚙️ [template-generator](./template-generator/) - PRP Template Generator

**Generate new PRP templates for any use case**

Meta-template that generates custom PRP templates for new domains and frameworks.

```bash
# Quick start
git clone https://github.com/dynamous-community/context-engineering-hub.git
cd context-engineering-hub/prp-templates/template-generator/
/generate-prp "Create a PRP template for FastAPI microservices"
```

**Perfect for:** Creating specialized PRP templates for new frameworks or domains

## 🎯 Which Template Should You Use?

| Use Case                       | Template                                          | Type            |
| ------------------------------ | ------------------------------------------------- | --------------- |
| Add PRPs to Python project     | [prp-base-python](./prp-base-python/)             | Drop-in         |
| Add PRPs to TypeScript project | [prp-typescript](./prp-typescript/)               | Drop-in         |
| Advanced quality validation    | [prp-base-experimental](./prp-base-experimental/) | Drop-in         |
| Build MCP server               | [mcp-server](./mcp-server/)                       | Project starter |
| Build Python AI agents         | [pydantic-ai](./pydantic-ai/)                     | Project starter |
| Create custom PRP template     | [template-generator](./template-generator/)       | Meta-template   |

## 🏗️ Consistent Template Structure

Each template follows this structure:

```
template-name/
├── .claude/
│   ├── commands/              # Custom Claude Code commands
│   └── settings.local.json    # Permissions and settings
├── PRPs/
│   ├── templates/             # Base PRP templates
│   ├── examples/              # Code examples (critical for AI!)
│   ├── INITIAL.md            # Feature request template
│   └── ai_docs/              # Documentation context (when needed)
├── CLAUDE.md                 # Project-specific AI rules
└── README.md                 # Template-specific documentation
```

## Best Practices

### 1. Be Explicit in your initial request

- Create a detailed description of the feature you want to implement.
- Create it in INITIAL.md or a similar format (you can also fill out the top part of the PRP template)
- Don't assume the AI knows your preferences.
- Include specific requirements and constraints
- Reference examples liberally

### 2. Provide Comprehensive Examples

- Detailed relevant examples = better implementations
- Show both what to do AND what not to do

### 3. Use Validation Gates

- PRPs include test commands that must pass
- AI will iterate until all validations succeed
- This ensures working code on first try

### 4. Leverage Documentation

- Include official API docs
- Add MCP server resources
- Reference specific documentation sections

### 5. Customize CLAUDE.md

- Add your conventions
- Include project-specific rules
- Define coding standards

### What to Include in Examples

1. **Code Structure Patterns**
   - How you organize modules
   - Import conventions
   - Class/function patterns

2. **Testing Patterns**
   - Test file structure
   - Mocking approaches
   - Assertion styles

3. **Integration Patterns**
   - API client implementations
   - Database connections
   - Authentication flows

4. **CLI Patterns**
   - Argument parsing
   - Output formatting
   - Error handling
