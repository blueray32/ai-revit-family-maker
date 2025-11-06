# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Context Engineering Hub - a collection of battle-tested PRP (Product Requirement Prompt) templates for different use cases. PRPs combine PRDs with curated codebase intelligence and agent runbooks to help AI coding assistants deliver production-ready code.

## Architecture

### Template Structure

All templates follow a consistent structure:

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
├── src/[use_cases]           # Source code starter if applicable to use case
└── README.md                 # Template-specific documentation
```

### Available Templates

1. **prp-base-python** - Universal PRP template for any existing project
2. **mcp-server** - Complete MCP server with TypeScript, auth, and database tools
3. **pydantic-ai** - Multi-agent Python project with structured outputs
4. **template-generator** - Meta-template for generating custom PRP templates

## Development Commands

### Template Management

```bash
# Copy templates to new projects
python prp-templates/mcp-server/copy_template.py <target-directory>
python prp-templates/pydantic-ai/copy_template.py <target-directory>

# Use template generator
cd prp-templates/template-generator/
/generate-prp "Create a PRP template for [framework/domain]"
```

## Key Implementation Details

### Context Engineering Principles

- **Examples are critical** - Accurate and relevant examples = better AI implementations
- **Validation gates** - PRPs include test commands that must pass
- **Comprehensive context** - Include documentation, patterns, and constraints
- **Progressive refinement** - AI iterates until all validations succeed

## Important Notes

- **Never commit secrets** - Use environment variables and .env files
- **Follow KISS principle** - Simple solutions over complex ones
- **Trust the prompt** - PRPs contain comprehensive context for AI
- **Examples drive quality** - Include representative code patterns
- **Validate continuously** - Use test commands throughout development
