# Contributing to Context Engineering Hub

Help us build the definitive collection of AI coding resources for the Dynamous community! This guide shows you how to contribute new templates, tools, and improvements to the Context Engineering Hub.

## 🎯 What We're Building

The Context Engineering Hub follows strict patterns to ensure every resource is:
- **Immediately usable** - Copy-paste ready with working examples
- **Consistently documented** - Following established README templates
- **Properly tested** - All examples and commands verified working
- **Well categorized** - Clear organization for easy discovery

## 🚀 Quick Start for Contributors

1. **Fork the repository**
2. **Choose your contribution type** (see sections below)
3. **Follow the templates** for your contribution type
4. **Test everything works** as documented
5. **Submit a PR** with clear description

## 📋 Contribution Types

### 📝 PRP Templates
Complete development frameworks with AI context and validation.

**When to contribute:**
- Your template enables one-pass implementations
- It includes comprehensive examples and patterns
- It follows the established PRP methodology

**Structure required:**
```
prp-templates/
├── your-template-name/
│   ├── .claude/
│   ├── PRPs/
│   ├── CLAUDE.md
│   ├── README.md
│   └── copy_template.py
└── README.md (update with your addition)
```

### 🏛️ Global Rules
High-level behavioral guidelines for AI coding assistants.

**When to contribute:**
- You have rules that improve AI behavior across entire projects
- Your rules are additive (enhance rather than replace existing rules)
- They're tool-specific optimizations (MCP servers, IDEs, etc.)

**Structure required:**
```
global-rules/
├── your-rule-name/
│   ├── README.md
│   └── RULES.md (or CLAUDE.md, .cursorrules, .windsurfrules if AI-specific)
└── README.md (update with your addition)
```

**Note**: Some global rules may need different files for different AI coding assistants (like Archon having CLAUDE.md, .cursorrules, and .windsurfrules). Include the appropriate files for your target AI assistants.

### ⚡ Slash Commands
Custom automation for Claude Code workflows.

**When to contribute:**
- Your command automates repetitive development tasks
- It leverages parallel processing or complex workflows
- It's battle-tested in real development scenarios

**Structure required:**
```
slash-commands/
├── category-name/
│   ├── your-command.md
│   └── README.md (if creating new category)
└── README.md (update with your addition)
```

### 🔗 Claude Hooks
Automated workflows that execute at key moments during AI development.

**When to contribute:**
- Your hook provides useful automation or guardrails
- It follows security best practices
- It's broadly applicable across different projects

**Structure required:**
```
claude-hooks/
├── your-hook-name/
│   ├── hook.json
│   └── README.md
└── README.md (update with your addition)
```

### 🤖 Subagents
Specialized AI team members for specific development tasks.

**When to contribute:**
- Your subagent excels at a specific type of task
- It has clear, actionable descriptions for automatic invocation
- It's tested and provides consistent value

**Structure required:**
```
subagents/
├── your-agent-name/
│   ├── your-agent-name.md
│   └── README.md
└── README.md (update with your addition)
```

## 📚 README Updates Required

When you contribute a new resource, you must update the main README for that category. Here's exactly what to add:

### Global Rules README Update

Add to the "Available Global Rules" section in `global-rules/README.md`:

```markdown
### 🏛️ [Your Rule Name]
**For projects using [specific tool/framework] - use the README in `[directory]/` as a template for global rule READMEs**

[2-3 sentence description of what the rule establishes/ensures]

[View [Rule Name] Global Rules →](./[directory]/README.md)
```

### PRP Templates README Update

Add to the main repository README.md in the template overview section:

```markdown
### [Your Template Name]
[Brief description of what development framework/use case this template enables]
```

**Note**: Also create a comprehensive README.md in your template folder explaining the template's purpose, structure, and usage.

### Slash Commands README Update

Add to the appropriate category section in `slash-commands/README.md`:

```markdown
#### `/category:your-command-name`
[Single line description of what the command does]
```

### Claude Hooks README Update

Add to the "Available Hooks" section in `claude-hooks/README.md`:

```markdown
### your-hook-name
[Single line description of what the hook does and where it logs/acts]
```

### Subagents README Update

Add to the "Available Subagents" section in `subagents/README.md`:

```markdown
### your-agent-name
[Single line description of what the agent validates/does]
```

## ✅ Quality Standards

### Documentation Requirements

**Every contribution must include:**

1. **Working examples** - All AI coding resources must be copy-paste ready
2. **Clear when-to-use guidance** - Explicit scenarios for usage
3. **Complete installation steps** - From zero to working

### Testing Requirements

**Before submitting, verify:**

1. **All commands work** - Test every bash command in your README
2. **Examples are realistic** - Use actual scenarios, not placeholders
3. **Installation/integration succeeds** - Fresh environment test

## 🤝 Community Standards

### Code of Conduct

- **Be helpful** - Focus on practical, working solutions
- **Be specific** - Provide exact commands and examples
- **Be inclusive** - Welcome contributors of all skill levels
- **Be collaborative** - Work together to improve existing content

## 📞 Getting Help

- **GitHub Issues** - Use for bug reports
- **Dynamous Community Forum** - Use for general questions about using these AI coding resources
- **Office Hours** - Attend weekly community office hours for live help
- **Documentation** - Check existing READMEs for patterns and examples

## 🎖️ Recognition

Contributors get:
- **Attribution** in contributed content
- **Community recognition** for valuable additions
- **Maintainer opportunities** for consistent contributors

---

Remember: Every contribution makes AI coding more effective for the entire Dynamous community. Quality over quantity - one well-documented, tested resource is more valuable than many incomplete ones.