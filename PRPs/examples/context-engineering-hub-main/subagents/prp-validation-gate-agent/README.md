# PRP Validation Gate Agent

A specialized execution agent that runs validation checklists from PRPs to verify that implementations meet all specified requirements and success criteria.

## Purpose

This agent executes the "Final Validation Checklist" from completed PRPs to systematically verify that implementation work has successfully met all requirements. It provides comprehensive pass/fail reporting on technical, functional, and quality criteria.

## When to Use

✅ **Use when:**
- Implementation work is complete and needs validation
- You want to verify PRP success criteria are met
- Running final checks before considering a feature done
- Need detailed validation reports for stakeholders

❌ **Don't use when:**
- PRP hasn't been implemented yet
- For validating PRP quality (use prp-quality-agent instead)
- During active development (use for final validation only)
- For general code review (this is requirements-specific)

## Installation

1. **Copy to your project**:
   ```bash
   cp subagents/prp-validation-gate-agent/prp-validation-gate-agent.md .claude/agents/
   ```

2. **Automatic activation**: Claude will invoke this agent when you request PRP validation execution.

## What It Validates

### Technical Validation
- **Test Execution**: Runs all test commands from PRP checklist
- **Linting Validation**: Executes linting commands and reports issues  
- **Type Checking**: Runs type checkers and reports errors
- **Additional Commands**: Any other technical validation specified in PRP

### Feature Implementation
- **Goal Achievement**: Verifies Feature Goal end state is reached
- **Deliverable Confirmation**: Checks concrete deliverable exists and works
- **Success Criteria**: Validates each success criterion from PRP "What" section
- **Manual Testing**: Executes manual test commands and verifies responses

### Code Quality Assessment
- **Pattern Compliance**: Ensures implementation follows existing patterns
- **Anti-Pattern Avoidance**: Checks none of the specified anti-patterns exist
- **Dependency Management**: Verifies proper imports and dependencies
- **File Placement**: Confirms correct directory structure and naming

### Documentation & Deployment
- **Code Documentation**: Verifies self-documenting code and required docs
- **Environment Configuration**: Checks config integration is complete
- **Deployment Readiness**: Ensures production-ready implementation

## Usage Examples

```bash
# Claude will automatically route these to the validation gate agent:
"Run the validation checklist from prp/authentication-feature.md"
"Execute final validation for the user dashboard PRP"
"Check if the implementation meets all PRP requirements"
```

**Note**: You must provide the exact relative file path to the PRP when requesting validation.

## Report Structure

The agent generates detailed validation reports with:

### Technical Results
- Command execution status (✅/❌)
- Specific error messages and failure details
- Test results summary with issue identification

### Feature Validation
- Goal achievement verification
- Success criteria status per requirement
- Manual testing results with expected vs actual

### Quality Assessment  
- Pattern compliance status
- Anti-pattern violation detection
- Code organization and naming validation

### Summary & Recommendations
- Overall pass/fail status
- Critical issues requiring immediate attention
- Next steps for resolving failures
- Confidence level in implementation

## Key Features

### Exact Command Execution
- Runs validation commands exactly as specified in PRP
- Captures and reports actual command output
- Provides specific error details, not generic failures

### Requirements Traceability
- Validates against PRP requirements, not generic standards
- Cross-references implementation with original success criteria
- Ensures all deliverables match PRP specifications

### Actionable Reporting
- Specific file/line references for issues
- Fix recommendations based on error patterns
- References to PRP patterns and gotchas for guidance

## Execution Guidelines

**The agent always:**
- Executes validation commands exactly as written in PRP
- Provides specific failure details with error messages
- Validates against PRP criteria, not assumptions
- Reports both successes and failures clearly

**The agent never:**
- Skips validation steps that "seem fine"
- Executes commands not in the PRP checklist
- Provides vague failure descriptions
- Makes assumptions about pass/fail criteria

## Common Validation Results

### Typical Passes
- All tests execute successfully
- Linting reports clean code
- Feature goals demonstrably achieved
- Manual testing matches expected outputs

### Common Failures
- Test failures due to missing edge cases
- Linting errors from style violations
- Type checking failures from incorrect annotations
- Feature incomplete relative to success criteria

## Best Practices

1. **Complete implementation first**: Only run after all coding is done
2. **Fix all critical issues**: Address failures before considering complete
3. **Provide exact PRP paths**: Agent needs specific file references
4. **Review reports thoroughly**: Don't skip minor issues
5. **Re-run after fixes**: Validate that corrections resolve issues

## Integration with Development Flow

```
PRP Creation → Implementation → Validation Gate → Success
                     ↑              ↓
                Fix Issues ← Report Failures
```

---

This agent serves as your implementation verification checkpoint, ensuring that completed work actually fulfills the original PRP requirements. It's the definitive answer to "Did we build what we said we would build?"