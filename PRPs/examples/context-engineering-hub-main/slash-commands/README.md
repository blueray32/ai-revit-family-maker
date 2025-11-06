# Custom Slash Commands Collection

A curated collection of powerful custom slash commands for Claude Code that automate complex development workflows, from code reviews to rapid prototyping.

## 🎯 Purpose

These custom slash commands transform repetitive development tasks into single-command workflows. They leverage Claude Code's capabilities for parallel processing, deep code analysis, and intelligent automation.

## 🚀 Quick Start

Place these commands in your project's `.claude/commands/` directory or in `~/.claude/commands/` for global access.

```bash
# Project-specific
.claude/commands/code-quality/review-general.md

# Global (all projects)
~/.claude/commands/code-quality/review-general.md
```

## 📋 Available Commands

### Code Quality

#### `/code-quality:refactor-simple`

Quick refactoring analysis for Python code focusing on function complexity and cross-feature imports.

#### `/code-quality:review-general`

Comprehensive code review covering quality, patterns, security, and testing with structured issue reporting.

#### `/code-quality:review-staged-unstaged`

Reviews both staged and unstaged changes with focus on Python/Pydantic patterns and security.

#### `/code-quality:TS-review-general`

Comprehensive TypeScript/Astro codebase review covering architecture, patterns, performance, and security.

#### `/code-quality:TS-review-staged-unstaged`

Reviews staged/unstaged TypeScript files focusing on strict typing and framework-specific patterns.

### Development Workflows

#### `/development:create-pr`

Creates well-structured pull requests with proper branch management, conventional commits, and comprehensive PR templates.

#### `/development:debug-RCA`

Systematic debugging and root cause analysis with reproduction steps, isolation strategies, and documented fixes.

#### `/development:new-dev-branch`

Simple workflow to create new development branch from latest develop.

#### `/development:onboarding`

Generates comprehensive onboarding documentation including ONBOARDING.md, QUICKSTART.md, and README suggestions.

#### `/development:prime-core`

Primes Claude with core project knowledge by analyzing structure, dependencies, and key files.

#### `/development:smart-commit`

Analyzes changes and creates conventional commits with appropriate types (feat/fix/docs/etc).

### Git Operations

#### `/git-operations:conflict-resolver-general`

Expert merge conflict resolution with intelligent change combination and semantic conflict detection.

#### `/git-operations:conflict-resolver-specific [strategy]`

Targeted conflict resolution with strategies: safe, aggressive, test, ours, theirs.

#### `/git-operations:smart-resolver`

Intelligent conflict resolution with pre-resolution branch analysis and post-resolution verification.

### Rapid Development (Experimental)

#### `/rapid-development:create-base-prp-parallel`

Creates comprehensive PRPs using 4 parallel research agents for codebase patterns, technical research, testing, and documentation.

#### `/rapid-development:create-planning-parallel`

Transforms ideas into complete PRDs using parallel agents for market intelligence, technical feasibility, UX research, and best practices.

#### `/rapid-development:hackathon-prp-parallel`

**Power command**: Deploys 25 parallel agents for 40-minute hackathon implementations with attempting "production-ready" code.

#### `/rapid-development:hackathon-research`

Evaluates multiple solution approaches using 15 concurrent research agents with quantitative scoring.

#### `/rapid-development:parallel-prp-creation`

Creates 2-5 parallel PRP variations focusing on different aspects (Performance, Security, Maintainability, etc).

#### `/rapid-development:prp-analyze-run`

Post-execution analysis capturing lessons learned, success metrics, and improvement suggestions.

#### `/rapid-development:prp-validate`

Pre-flight validation ensuring all PRP dependencies and references are available.

#### `/rapid-development:user-story-rapid`

Creates detailed implementation plans for separate backend/frontend projects with API contract planning.

## 💡 Usage Examples

```bash
# Quick refactor check
/code-quality:refactor-simple

# Create a PR with all the bells and whistles
/development:create-pr

# Resolve complex merge conflicts
/git-operations:smart-resolver

# Rapid prototype with 25 agents
/rapid-development:hackathon-prp-parallel Build a real-time chat app

# TypeScript code review
/code-quality:TS-review-general
```

## 🛠️ Creating Your Own Commands

Basic template:

```markdown
---
description: What your command does
allowed-tools: Edit, Read, Bash
argument-hint: [optional-arguments]
---

# Command Instructions

Your detailed instructions for Claude Code.
Use $ARGUMENTS to reference user input.
```
