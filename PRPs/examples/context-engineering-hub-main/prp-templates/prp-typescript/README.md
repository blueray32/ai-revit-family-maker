# PRP TypeScript Template

**Drop PRPs into any existing TypeScript project for structured feature development**

This template provides the TypeScript-focused PRP (Product Requirement Prompt) framework that can be added to any TypeScript codebase. A PRP combines the structured approach of Product Requirements Documents with curated context and implementation guidance for AI coding assistants.

## 🚀 Quick Start

**Add to any existing or new TypeScript project in 30 seconds:**

```bash
# 1. Clone and copy the essentials
git clone https://github.com/dynamous-community/context-engineering-hub.git
cp -r context-engineering-hub/prp-templates/prp-typescript/PRPs/ your-project/
cp -r context-engineering-hub/prp-templates/prp-typescript/.claude/ your-project/

# 2. Start building features immediately
cd your-project

# 3. Start building with the PRP workflow
# Fill out PRPs/INITIAL.md with the TypeScript feature you want to create

# 4. Generate the PRP based on your detailed requirements
/prp-ts-create PRPs/INITIAL.md
# or simply pass the string
/prp-ts-create "Build a user authentication system with JWT tokens using TypeScript"

# IMPORTANT
# validate that the PRP content is aligned with your goals after generating!

# The PRP can also be created manually without the generate command, its important to understand the command is just a starting point, not a perfect solution.

# 5. Manually Read the PRP and make sure it is complete and accurate before proceeding.
/prp-ts-execute PRPs/user-authentication-system.md
```

**That's it!** You now have:

- ✅ TypeScript-specific PRP templates for structured feature requests
- ✅ Claude commands that research, plan, and implement TypeScript features
- ✅ A complete context engineering workflow for TypeScript projects

**Optional:** Copy `CLAUDE.md` for project-specific AI coding rules.

**Even simpler:** Just copy the `prp-templates/prp-typescript/` folder to your project root.

## 📚 Table of Contents

- [What is Context Engineering?](#what-is-context-engineering)
- [Template Structure](#template-structure)
- [Step-by-Step Guide](#step-by-step-guide)
- [Writing Effective INITIAL.md Files](#writing-effective-initialmd-files)
- [The PRP Workflow](#the-prp-workflow)
- [TypeScript-Specific Features](#typescript-specific-features)
- [Best Practices](#best-practices)

## What Makes PRPs Different?

PRPs go beyond traditional prompts by providing:

- **Structured Context**: Complete TypeScript codebase patterns and conventions
- **Implementation Guidance**: Specific architectural decisions and TypeScript tool choices
- **Validation Gates**: Automated testing and quality checks with TypeScript compilation
- **Examples**: Real TypeScript code patterns for AI to follow

## Template Structure

```
prp-typescript/
├── .claude/
│   ├── commands/
│   │   ├── prp-ts-create.md    # Generates comprehensive TypeScript PRPs
│   │   └── prp-ts-execute.md   # Executes PRPs to implement TypeScript features
│   └── settings.local.json     # Claude Code permissions
├── PRPs/
│   ├── templates/
│   │   └── prp_base_typescript.md  # Base template for TypeScript PRPs
│   ├── examples/               # Your TypeScript code examples (critical!)
│   ├── ai_docs/                # TypeScript library docs for AI to search
│   ├── INITIAL.md             # Template for TypeScript feature requests
│   ├── INITIAL_EXAMPLE.md     # Example TypeScript feature request
│   └── EXAMPLE_typescript_prp.md  # Example of complete TypeScript PRP
├── CLAUDE.md                  # Global rules for AI assistant
└── README.md                 # This file
```

## Step-by-Step Guide

### 1. Set Up Global Rules (CLAUDE.md)

The `CLAUDE.md` file contains project-wide rules that the AI assistant will follow in every conversation. The template includes:

- **Project awareness**: Reading planning docs, checking tasks
- **Code structure**: File size limits, module organization for TypeScript
- **Testing requirements**: Unit test patterns with Jest/Vitest, coverage expectations
- **Style conventions**: TypeScript preferences, formatting rules, linting
- **Documentation standards**: TSDoc formats, commenting practices

**You can use the provided template as-is or customize it for your TypeScript project.**

### 2. Create Your Initial Feature Request

Edit `INITIAL.md` to describe what you want to build:

```markdown
## FEATURE:

[Describe what you want to build - be specific about functionality and TypeScript requirements]

## EXAMPLES:

[List any example files in the PRPs/examples/ folder and explain how they should be used]

## DOCUMENTATION:

[Include links to relevant documentation, TypeScript APIs, or library resources]

## OTHER CONSIDERATIONS:

[Mention any gotchas, specific TypeScript requirements, or things AI assistants commonly miss]
```

**See `INITIAL_EXAMPLE.md` for a complete example.**

### 3. Generate the PRP

PRPs (Product Requirements Prompts) are comprehensive implementation blueprints that include:

- Complete context and documentation
- TypeScript-specific implementation steps with validation
- Error handling patterns
- Test requirements with TypeScript

They are similar to PRDs (Product Requirements Documents) but are crafted more specifically to instruct an AI coding assistant working with TypeScript.

Run in Claude Code:

```bash
/prp-ts-create INITIAL.md
```

**Note:** The slash commands are custom commands defined in `.claude/commands/`. You can view their implementation:

- `.claude/commands/prp-ts-create.md` - See how it researches and creates TypeScript PRPs
- `.claude/commands/prp-ts-execute.md` - See how it implements TypeScript features from PRPs

The `$ARGUMENTS` variable in these commands receives whatever you pass after the command name (e.g., `INITIAL.md` or `PRPs/your-feature.md`).

This command will:

1. Read your TypeScript feature request
2. Research the codebase for TypeScript patterns
3. Search for relevant TypeScript documentation
4. Create a comprehensive PRP in `PRPs/your-feature-name.md`

### 4. Execute the PRP

Once generated, execute the PRP to implement your TypeScript feature:

```bash
/prp-ts-execute PRPs/your-feature-name.md
```

The AI coding assistant will:

1. Read all context from the PRP
2. Create a detailed TypeScript implementation plan
3. Execute each step with TypeScript compilation validation
4. Run tests and fix any issues
5. Ensure all success criteria are met

## Writing Effective INITIAL.md Files

### Key Sections Explained

**FEATURE**: Be specific and comprehensive

- ❌ "Build a web API"
- ✅ "Build a TypeScript Express API with type-safe routing, JWT authentication, input validation using Zod, and PostgreSQL integration with Prisma ORM"

**EXAMPLES**: Leverage the PRPs/examples/ folder

- Place relevant TypeScript code patterns in `PRPs/examples/`
- Reference specific files and patterns to follow
- Explain what TypeScript aspects should be mimicked

**DOCUMENTATION**: Include all relevant resources

- TypeScript documentation URLs
- Library guides (Express, React, etc.)
- API documentation
- Database schemas

**OTHER CONSIDERATIONS**: Capture important details

- TypeScript version requirements
- Build tool preferences (Vite, Webpack, etc.)
- Testing framework preferences
- Common TypeScript pitfalls
- Performance requirements

## The PRP Workflow

### How /prp-ts-create Works

The command follows this process:

1. **Research Phase**
   - Analyzes your TypeScript codebase for patterns
   - Searches for similar TypeScript implementations
   - Identifies TypeScript conventions to follow

2. **Documentation Gathering**
   - Fetches relevant TypeScript API docs
   - Includes library documentation
   - Adds TypeScript-specific gotchas and quirks

3. **Blueprint Creation**
   - Creates step-by-step TypeScript implementation plan
   - Includes TypeScript compilation validation gates
   - Adds test requirements with TypeScript

4. **Quality Check**
   - Scores confidence level (1-10)
   - Ensures all TypeScript context is included

### How /prp-ts-execute Works

1. **Load Context**: Reads the entire TypeScript PRP
2. **Plan**: Creates detailed task list using TodoWrite
3. **Execute**: Implements each TypeScript component
4. **Validate**: Runs TypeScript compilation, tests and linting
5. **Iterate**: Fixes any TypeScript issues found
6. **Complete**: Ensures all requirements met

## TypeScript-Specific Features

This template includes specialized support for:

- **Type Safety**: Comprehensive type definitions and interfaces
- **Modern TypeScript**: Latest language features and best practices
- **Build Tools**: Integration with popular TypeScript build systems
- **Testing**: TypeScript-aware testing patterns
- **Linting**: ESLint + TypeScript rules and configurations
- **Documentation**: TSDoc and type-aware documentation

## Best Practices

### TypeScript Development Standards

- Use strict TypeScript configuration
- Implement proper type definitions for all APIs
- Follow established naming conventions for types and interfaces
- Use generic types where appropriate
- Implement proper error handling with typed errors

### Project Structure

- Organize types in dedicated files or folders
- Use barrel exports for clean imports
- Separate business logic from framework code
- Implement proper dependency injection patterns

See `PRPs/EXAMPLE_typescript_prp.md` for a complete example of what gets generated.