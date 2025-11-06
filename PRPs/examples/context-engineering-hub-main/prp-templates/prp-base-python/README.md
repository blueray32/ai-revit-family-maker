# PRP Base Template

**Drop PRPs into any existing project for structured feature development**

This template provides the universal PRP (Product Requirement Prompt) framework that can be added to any codebase. A PRP combines the structured approach of Product Requirements Documents with curated context and implementation guidance for AI coding assistants.

## 🚀 Quick Start

**Add to any existing or new project in 30 seconds:**

```bash
# 1. Clone and copy the essentials
git clone https://github.com/dynamous-community/context-engineering-hub.git
cp -r context-engineering-hub/prp-templates/prp-base-python/PRPs/ your-project/
cp -r context-engineering-hub/prp-templates/prp-base-python/.claude/ your-project/

# 2. Start building features immediately
cd your-project

# 3. Start building with the PRP workflow
# Fill out PRPs/INITIAL.md with the agent you want to create

# 4. Generate the PRP based on your detailed requirements
/generate-pydantic-ai-prp PRPs/INITIAL.md
# or simply pass the string
/generate-prp "Build a user authentication system with JWT tokens"

# IMPORTANT
# validate that the PRP content is aligned with your goals after generating!

# The PRP can also be created manually without the generate command, its important to understand the command is just a starting point, not a perfect solution.

# 3. Manually Read the PRP and make sure it is complete and accurate before proceeding.
/execute-prp PRPs/user-authentication-system.md
```

**That's it!** You now have:

- ✅ PRP templates for structured feature requests
- ✅ Claude commands that research, plan, and implement features
- ✅ A complete context engineering workflow

**Optional:** Copy `CLAUDE.md` for project-specific AI coding rules.

**Even simpler:** Just copy the `prp-templates/prp-base-python/` folder to your project root.

## 📚 Table of Contents

- [What is Context Engineering?](#what-is-context-engineering)
- [Template Structure](#template-structure)
- [Step-by-Step Guide](#step-by-step-guide)
- [Writing Effective INITIAL.md Files](#writing-effective-initialmd-files)
- [The PRP Workflow](#the-prp-workflow)
- [Using Examples Effectively](#using-examples-effectively)
- [Best Practices](#best-practices)

## What Makes PRPs Different?

PRPs go beyond traditional prompts by providing:

- **Structured Context**: Complete codebase patterns and conventions
- **Implementation Guidance**: Specific architectural decisions and tool choices
- **Validation Gates**: Automated testing and quality checks
- **Examples**: Real code patterns for AI to follow

## Template Structure

```
prp-base-python/
├── .claude/
│   ├── commands/
│   │   ├── generate-prp.md    # Generates comprehensive PRPs
│   │   └── execute-prp.md     # Executes PRPs to implement features
│   └── settings.local.json    # Claude Code permissions
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md       # Base template for PRPs
│   ├── examples/             # Your code examples (critical!)
│   ├── ai_docs/              # Library docs for AI to search
│   ├── INITIAL.md           # Template for feature requests
│   ├── INITIAL_EXAMPLE.md   # Example feature request
│   └── EXAMPLE_multi_agent_prp.md  # Example of complete PRP
├── CLAUDE.md                # Global rules for AI assistant
└── README.md               # This file
```

## Step-by-Step Guide

### 1. Set Up Global Rules (CLAUDE.md)

The `CLAUDE.md` file contains project-wide rules that the AI assistant will follow in every conversation. The template includes:

- **Project awareness**: Reading planning docs, checking tasks
- **Code structure**: File size limits, module organization
- **Testing requirements**: Unit test patterns, coverage expectations
- **Style conventions**: Language preferences, formatting rules
- **Documentation standards**: Docstring formats, commenting practices

**You can use the provided template as-is or customize it for your project.**

### 2. Create Your Initial Feature Request

Edit `INITIAL.md` to describe what you want to build:

```markdown
## FEATURE:

[Describe what you want to build - be specific about functionality and requirements]

## EXAMPLES:

[List any example files in the PRPs/examples/ folder and explain how they should be used]

## DOCUMENTATION:

[Include links to relevant documentation, APIs, or MCP server resources]

## OTHER CONSIDERATIONS:

[Mention any gotchas, specific requirements, or things AI assistants commonly miss]
```

**See `INITIAL_EXAMPLE.md` for a complete example.**

### 3. Generate the PRP

PRPs (Product Requirements Prompts) are comprehensive implementation blueprints that include:

- Complete context and documentation
- Implementation steps with validation
- Error handling patterns
- Test requirements

They are similar to PRDs (Product Requirements Documents) but are crafted more specifically to instruct an AI coding assistant.

Run in Claude Code:

```bash
/generate-prp INITIAL.md
```

**Note:** The slash commands are custom commands defined in `.claude/commands/`. You can view their implementation:

- `.claude/commands/generate-prp.md` - See how it researches and creates PRPs
- `.claude/commands/execute-prp.md` - See how it implements features from PRPs

The `$ARGUMENTS` variable in these commands receives whatever you pass after the command name (e.g., `INITIAL.md` or `PRPs/your-feature.md`).

This command will:

1. Read your feature request
2. Research the codebase for patterns
3. Search for relevant documentation
4. Create a comprehensive PRP in `PRPs/your-feature-name.md`

### 4. Execute the PRP

Once generated, execute the PRP to implement your feature:

```bash
/execute-prp PRPs/your-feature-name.md
```

The AI coding assistant will:

1. Read all context from the PRP
2. Create a detailed implementation plan
3. Execute each step with validation
4. Run tests and fix any issues
5. Ensure all success criteria are met

## Writing Effective INITIAL.md Files

### Key Sections Explained

**FEATURE**: Be specific and comprehensive

- ❌ "Build a web scraper"
- ✅ "Build an async web scraper using BeautifulSoup that extracts product data from e-commerce sites, handles rate limiting, and stores results in PostgreSQL"

**EXAMPLES**: Leverage the PRPs/examples/ folder

- Place relevant code patterns in `PRPs/examples/`
- Reference specific files and patterns to follow
- Explain what aspects should be mimicked

**DOCUMENTATION**: Include all relevant resources

- API documentation URLs
- Library guides
- MCP server documentation
- Database schemas

**OTHER CONSIDERATIONS**: Capture important details

- Authentication requirements
- Rate limits or quotas
- Common pitfalls
- Performance requirements

## The PRP Workflow

### How /generate-prp Works

The command follows this process:

1. **Research Phase**
   - Analyzes your codebase for patterns
   - Searches for similar implementations
   - Identifies conventions to follow

2. **Documentation Gathering**
   - Fetches relevant API docs
   - Includes library documentation
   - Adds gotchas and quirks

3. **Blueprint Creation**
   - Creates step-by-step implementation plan
   - Includes validation gates
   - Adds test requirements

4. **Quality Check**
   - Scores confidence level (1-10)
   - Ensures all context is included

### How /execute-prp Works

1. **Load Context**: Reads the entire PRP
2. **Plan**: Creates detailed task list using TodoWrite
3. **Execute**: Implements each component
4. **Validate**: Runs tests and linting
5. **Iterate**: Fixes any issues found
6. **Complete**: Ensures all requirements met

See `PRPs/EXAMPLE_multi_agent_prp.md` for a complete example of what gets generated.
