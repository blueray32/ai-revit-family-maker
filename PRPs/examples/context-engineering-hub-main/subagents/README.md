# Claude Code Subagents Collection

Specialized AI team members that extend Claude Code's capabilities with task-specific expertise and dedicated context windows.

## 🎯 Purpose

Subagents are autonomous AI specialists that Claude Code can invoke automatically to handle specific types of tasks. They provide focused expertise, isolated context, and specialized tool access - like having a team of experts available on-demand.

## 🚀 Quick Start

### Installation

1. **Copy specific subagents to your project**:
   ```bash
   # Copy a single agent
   cp subagents/prp-quality-agent/prp-quality-agent.md .claude/agents/
   ```

2. **Verify installation**:
   ```bash
   # List available agents
   /agents
   ```

3. **Claude will automatically use them** when appropriate tasks arise.

## 📋 Available Subagents

### prp-quality-agent
Validates completed PRPs (Product Requirement Prompts) for quality and completeness before execution.

### prp-validation-gate-agent  
Executes validation checklists from PRPs to verify implementation meets all requirements.

## 🛠️ How Subagents Work

### Core Features

- **Automatic Invocation**: Claude intelligently routes tasks to appropriate specialists
- **Isolated Context**: Each subagent has its own context window and system prompt
- **Specialized Tools**: Subagents can be granted specific tool access
- **Task Focus**: Designed for specific workflows or problem domains

### Agent Structure

```markdown
---
name: agent-name
description: When this agent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all if omitted
model: sonnet              # Optional - sonnet, opus
---

Your agent's system prompt and instructions go here.
```

### The /agents Command

Use `/agents` to:
- View all available subagents
- Modify tool access for agents
- Create new custom agents interactively

## 💡 Creating Custom Subagents

### Basic Template

```markdown
---
name: code-reviewer
description: Use PROACTIVELY to review code changes for quality and security
tools: Read, Grep, WebSearch
---

You are a code review specialist. When you see code changes:
1. Check for security vulnerabilities
2. Verify code follows project patterns
3. Suggest improvements for readability
4. Ensure test coverage exists
```

### Best Practices

1. **Clear Descriptions**: Make the `description` field specific and action-oriented
2. **Proactive Keywords**: Use "PROACTIVELY" or "MUST BE USED" for automatic invocation
3. **Focused Scope**: Each agent should excel at one type of task
4. **Tool Selection**: Only grant tools the agent actually needs

## 🎨 Subagent Ideas

### Test Runner
```markdown
---
name: test-runner
description: Use PROACTIVELY to run tests after code changes
tools: Bash, Read, Edit
---
Run appropriate tests when code changes are made.
Fix simple test failures while preserving intent.
```

### Security Scanner
```markdown
---
name: security-scanner  
description: Scan for security vulnerabilities in new code
tools: Read, Grep, WebSearch, Bash
---
Analyze code for OWASP vulnerabilities.
Check for exposed secrets or credentials.
Verify secure coding practices.
```

### Documentation Writer
```markdown
---
name: doc-writer
description: Generate and update documentation
tools: Read, Write, Edit
---
Create clear documentation for new features.
Update existing docs when code changes.
Ensure examples are accurate and helpful.
```

## 🚦 Subagent Categories

- **🔍 Quality Assurance**: Code review, testing, validation
- **📝 Documentation**: README generation, API docs, examples
- **🛡️ Security**: Vulnerability scanning, secret detection
- **🏗️ Architecture**: Design review, pattern enforcement
- **📊 Analysis**: Performance profiling, complexity analysis
