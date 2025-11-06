# Archon Global Rules

## Overview

The Archon Global Rules establish a task-driven development workflow for AI coding assistants when working with projects that use the [Archon MCP Server](https://github.com/dynamous-community/workshops/tree/main/archon-v2-alpha). These rules ensure that AI assistants leverage Archon's powerful knowledge base and task management capabilities to deliver better, more organized code.

## When to Use These Rules

✅ **Use when:**
- Your project has Archon MCP server connected
- You want task-driven development with built-in knowledge management
- You need AI to research before implementing
- You want organized project and feature tracking
- You prefer systematic progress tracking

❌ **Don't use when:**
- Working on simple scripts or one-off tasks
- Archon MCP server is not available

The when to use/when not to use is a bit silly here but I want the Archon global rules README to be a template for global rule READMEs going forward, and this section is important for most rules!

## Core Philosophy

The Archon Global Rules implement three key principles:

### 1. 🎯 Task-First Development
Every coding action starts with checking current tasks. No code is written without understanding what task it fulfills.

### 2. 📚 Research-Driven Implementation
Before implementing any feature, the AI searches Archon's knowledge base for best practices, patterns, and examples.

### 3. 🔄 Continuous Progress Tracking
Tasks move through clear states (todo → doing → review → done) with real-time updates.

## Key Behaviors These Rules Enable

### Task Management Integration
```
User: "Add authentication to the app"
AI: [Checks Archon for existing auth tasks]
    [Creates specific tasks if none exist]
    [Researches auth patterns in knowledge base]
    [Implements based on research]
    [Updates task status throughout]
```

### Knowledge-Driven Coding
```
User: "Implement rate limiting"
AI: [Searches: "rate limiting best practices"]
    [Searches: "Express.js rate limiting implementation"]
    [Reviews code examples]
    [Implements using discovered patterns]
```

### Project Organization
```
User: "Let's work on the payment system"
AI: [Gets project features]
    [Lists all payment-related tasks]
    [Identifies highest priority task]
    [Begins systematic implementation]
```

## Compatibility Notes

### Works Well With:
- ✅ PRP templates (enhances their effectiveness)
- ✅ Project-specific CLAUDE.md rules
- ✅ Other MCP servers (as long as Archon is primary for tasks)
- ✅ Standard development workflows

### Potential Conflicts:
- ⚠️ Other task management systems (choose one primary system)
- ⚠️ Workflows that discourage planning
- ⚠️ Extremely rapid prototyping scenarios

## Expected AI Behavior Changes

### Before Archon Rules:
```
User: "Build a user dashboard"
AI: [Immediately starts coding]
    [Creates files based on assumptions]
    [Might miss important patterns]
```

### After Archon Rules:
```
User: "Build a user dashboard"
AI: [Checks current project tasks]
    [Searches "dashboard UI patterns"]
    [Searches "user dashboard examples"]
    [Creates atomic tasks for dashboard features]
    [Implements based on research]
    [Updates progress at each step]
```

## Customization

You can adjust these rules by:

1. **Modifying research depth** - Adjust `match_count` parameters
2. **Changing task granularity** - Define what constitutes a single task
3. **Adjusting status workflow** - Add custom statuses if needed
4. **Feature organization** - Define your own feature categories

## Troubleshooting

### AI Not Using Archon
- Ensure Archon MCP server is running
- Verify the global rules are properly included
- Check that rules appear early in CLAUDE.md

### Too Much Research
- Reduce `match_count` in queries
- Focus on specific technical queries
- Skip research for trivial tasks

### Task Overhead
- Batch related small changes into single tasks
- Use features to group related work
- Archive outdated tasks regularly

## Example Workflows

### New Feature Development
1. AI creates feature-grouped tasks
2. Researches architecture patterns
3. Implements incrementally
4. Updates task status continuously
5. Moves to next priority task

### Bug Fixing
1. AI checks for existing bug tasks
2. Researches error patterns
3. Implements fix based on findings
4. Marks task for review
5. Documents solution

### Refactoring
1. AI analyzes current implementation
2. Researches better patterns
3. Creates refactoring tasks
4. Implements improvements systematically
5. Ensures nothing breaks