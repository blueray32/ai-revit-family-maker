# PRP Quality Agent

A specialized quality assurance subagent that validates completed Product Requirement Prompts (PRPs) before execution to ensure one-pass implementation success.

## Purpose

This agent performs comprehensive pre-execution validation of PRPs to catch issues before implementation begins. It applies rigorous quality gates to ensure PRPs have everything needed for successful one-shot development.

## When to Use

✅ **Use when:**
- A PRP has been completed and needs quality validation
- Before starting implementation of a new feature
- You want to ensure PRP completeness and accuracy
- Preparing for high-stakes one-pass implementations

❌ **Don't use when:**
- Writing or drafting PRPs (use during creation, not validation)
- For simple tasks that don't require PRPs
- When you need execution validation (use prp-validation-gate-agent instead)

## Installation

1. **Copy to your project**:
   ```bash
   cp subagents/prp-quality-agent/prp-quality-agent.md .claude/agents/
   ```

2. **Automatic activation**: Claude will invoke this agent when you ask for PRP quality checks or validation.

## What It Validates

### Structural Validation
- Template compliance (all required sections present)
- Content completeness (no placeholder text)
- YAML context structure formatting

### Context Completeness  
- **"No Prior Knowledge" Test**: Could someone unfamiliar implement this successfully?
- Reference accessibility (URLs work, files exist)
- Codebase-specific constraints and gotchas

### Information Density
- Specific vs generic references
- Actionable implementation tasks
- Information-dense keywords from actual codebase

### Implementation Readiness
- Task dependency ordering
- Execution feasibility
- Anti-pattern coverage

### Validation Gates
- Command availability verification
- 4-level validation system structure
- Project-specific validation commands

## Usage Examples

```bash
# Claude will automatically route these to the quality agent:
"Please validate this PRP for quality before we implement it"
"Check if this PRP is ready for execution"
"Quality review the completed PRP in /path/to/prp.md"
```

## Quality Metrics

The agent provides scoring on a 10-point scale for:
- **Context Completeness**: Sufficient information for implementation
- **Information Density**: Specific, actionable guidance  
- **Implementation Readiness**: Clear, executable tasks
- **Validation Quality**: Proper testing framework

**Minimum 8/10 required for approval**

## Report Structure

The agent generates comprehensive reports including:
- ✅/❌ status for each validation area
- Specific line references for issues
- Actionable fix recommendations  
- Priority-based issue categorization
- Overall confidence score and approval status

## Key Features

### Reference Validation
- Tests all URLs for accessibility
- Verifies file references exist
- Validates section anchors in documentation

### Context Analysis
- Applies "No Prior Knowledge" test rigorously
- Checks for codebase-specific patterns
- Validates naming conventions and placement guidance

### Command Verification
- Tests validation command availability
- Ensures project-specific tooling exists
- Verifies test framework configuration

## Validation Guidelines

**Quality Standards:**
- All references must be specific and accessible
- Implementation tasks must be information-dense
- Context must enable zero-knowledge implementation
- Validation commands must be project-executable

## Typical Issues Found

- Generic references without specific examples
- Broken URLs or missing file references
- Placeholder text in critical sections
- Missing validation commands or tools
- Insufficient context for independent implementation

## Best Practices

1. **Run early**: Validate PRPs before starting implementation
2. **Address all issues**: Don't skip medium priority items
3. **Re-validate after fixes**: Ensure changes resolve all issues
4. **Use for templates**: Validate PRP templates themselves

---

This agent serves as your quality gatekeeper, ensuring PRPs meet the standards needed for successful one-pass implementation. Trust its thoroughness - it's designed to catch the subtle issues that derail implementations.