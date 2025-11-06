# PRP Base Experimental Template

**Advanced PRPs with quality validation and implementation precision standards**

This experimental template provides cutting-edge PRP (Product Requirement Prompt) patterns with enhanced quality validation, precision standards, and advanced implementation methodologies. Built for teams pushing the boundaries of context engineering and AI-assisted development.

## 🚀 Quick Start

**Add experimental PRP capabilities to any project in 30 seconds:**

```bash
# 1. Clone and copy the experimental essentials
git clone https://github.com/dynamous-community/context-engineering-hub.git
cp -r context-engineering-hub/prp-templates/prp-base-experimental/PRPs/ your-project/
cp -r context-engineering-hub/prp-templates/prp-base-experimental/.claude/ your-project/

# 2. Start building with experimental features
cd your-project

# 3. Use the advanced PRP workflow with quality validation
# Fill out PRPs/INITIAL.md with your feature requirements

# 4. Generate a high-precision PRP
/generate-prp-experimental PRPs/INITIAL.md
# or pass requirements directly
/generate-prp-experimental "Build a distributed caching system with Redis clustering"

# 5. IMPORTANT: Quality validate before execution
/prp-quality-check PRPs/your-generated-prp.md

# 6. Execute only after quality approval
/execute-prp-experimental PRPs/your-validated-prp.md
```

**That's it!** You now have:

- ✅ Advanced PRP templates with precision implementation standards
- ✅ Built-in quality validation and approval workflows
- ✅ 4-level validation system with creative testing approaches
- ✅ Implementation-focused patterns with dependency ordering
- ✅ Context completeness validation ("No Prior Knowledge" test)

**Optional:** Copy `CLAUDE.md` for project-specific experimental AI coding rules.

**Even simpler:** Just copy the `prp-templates/prp-base-experimental/` folder to your project root.

## 📚 Table of Contents

- [What Makes This Experimental?](#what-makes-this-experimental)
- [Advanced Features](#advanced-features)
- [Template Structure](#template-structure)
- [Quality Validation System](#quality-validation-system)
- [Precision Implementation Standards](#precision-implementation-standards)
- [4-Level Validation Framework](#4-level-validation-framework)
- [Best Practices](#best-practices)

## What Makes This Experimental?

This template pushes beyond traditional PRPs with:

- **Quality Validation Agent**: Automated PRP quality checking before execution
- **Precision Standards**: Implementation-focused templates with exact specifications
- **Context Completeness Testing**: "No Prior Knowledge" validation methodology
- **4-Level Validation System**: Progressive validation from syntax to creative testing
- **Implementation Blueprints**: Dependency-ordered task specifications
- **Information Density**: Anti-generic patterns with maximum actionability

## Advanced Features

### Quality Validation System

Built-in PRP quality assurance agent that validates:

- **Structural Completeness**: All required sections present and populated
- **Context Accessibility**: URLs and file references are valid and accessible
- **Information Density**: No generic references, maximum specificity
- **Implementation Readiness**: Tasks are actionable with proper dependencies
- **Validation Command Testing**: Project-specific commands are available

### Precision Implementation Standards

- **Implementation-Focused Templates**: Task-oriented rather than documentation-focused
- **Dependency Ordering**: Clear task dependencies and execution order
- **Exact Specifications**: File paths, class names, method signatures included
- **Pattern References**: Specific existing code patterns to follow
- **Anti-Pattern Guidelines**: Explicit guidance on what to avoid

### Context Completeness Validation

The revolutionary "No Prior Knowledge" test:

> "Could someone unfamiliar with this codebase implement this successfully using only this PRP?"

This test ensures PRPs contain everything needed for successful implementation without external context or assumptions.

## Template Structure

```
prp-base-experimental/
├── .claude/
│   ├── commands/
│   │   ├── generate-prp-experimental.md    # Advanced PRP generation
│   │   ├── execute-prp-experimental.md     # Precision implementation
│   │   └── prp-quality-check.md           # Quality validation agent
│   └── settings.local.json                # Enhanced permissions
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md                    # Implementation-focused template
│   ├── examples/                          # Advanced code examples
│   ├── ai_docs/                           # Specialized documentation
│   ├── prp-readme.md                      # Quality validation agent spec
│   ├── INITIAL.md                         # Feature request template
│   └── INITIAL_EXAMPLE.md                 # Advanced example
├── CLAUDE.md                              # Experimental AI rules
└── README.md                             # This file
```

## Quality Validation System

### Phase 1: Structural Validation

- **Template Structure Check**: Verify all required sections present
- **Content Completeness**: Ensure no placeholder content remains
- **YAML Context Validation**: Verify proper formatting and structure

### Phase 2: Context Completeness Validation

- **"No Prior Knowledge" Test**: Critical completeness assessment
- **Reference Accessibility**: Validate all URLs and file references
- **Context Quality Assessment**: Ensure codebase-specific constraints included

### Phase 3: Information Density Validation

- **Specificity Check**: Flag generic references and vague guidance
- **Actionability Assessment**: Verify implementation tasks are executable
- **Pattern Verification**: Confirm referenced patterns actually exist

### Phase 4: Implementation Readiness Validation

- **Task Dependency Analysis**: Verify proper ordering and dependencies
- **Execution Feasibility Check**: Confirm tasks are implementable as written
- **Validation Gates Dry-Run**: Test command availability without execution

### Quality Report Generation

Comprehensive validation report with:

- ✅/❌ Status for each validation phase
- Specific line references for issues found
- Actionable fix recommendations
- Quality metrics scoring (minimum 8/10 for approval)
- Final approval/rejection decision with reasoning

## Precision Implementation Standards

### Implementation-Focused Template Features

**Goal Section Enhancement**:
- Feature Goal, Deliverable, Success Definition (no placeholders allowed)
- User Persona with specific use cases and pain points
- Measurable success criteria

**Context Completeness Requirements**:
- YAML-structured references with specific why/pattern/gotcha details
- Current and desired codebase tree structures
- Known gotchas and library quirks with examples

**Implementation Blueprint**:
- Data models and structure specifications
- Dependency-ordered implementation tasks
- Exact naming conventions and file placement
- Integration points with specific configuration changes

### 4-Level Validation Framework

**Level 1: Syntax & Style (Immediate Feedback)**
```bash
ruff check src/{new_files} --fix
mypy src/{new_files}
ruff format src/{new_files}
```

**Level 2: Unit Tests (Component Validation)**
```bash
uv run pytest src/services/tests/test_{domain}_service.py -v
uv run pytest src/tools/tests/test_{action}_{resource}.py -v
```

**Level 3: Integration Testing (System Validation)**
```bash
# Service startup and health checks
uv run python main.py &
curl -f http://localhost:8000/health
# Feature-specific endpoint testing
# MCP server validation if applicable
```

**Level 4: Creative & Domain-Specific Validation**
```bash
# Creative validation approaches:
playwright-mcp --test-user-journey
docker-mcp --build --test --cleanup
database-mcp --validate-schema --test-queries
# Performance, security, load testing as needed
```

## Writing Effective Experimental PRPs

### Enhanced INITIAL.md Structure

**FEATURE**: Ultra-specific with technology stack
- ❌ "Build a caching system"
- ✅ "Build a distributed Redis-based caching system with cluster failover, TTL management, and Prometheus metrics integration"

**EXAMPLES**: Pattern-specific references
- Reference exact files with specific patterns to follow
- Include anti-patterns to avoid
- Explain why certain approaches were chosen

**DOCUMENTATION**: Section-anchored URLs
- Include direct links to specific documentation sections
- Add gotchas and quirks from real usage
- Reference integration-specific considerations

**OTHER CONSIDERATIONS**: Implementation constraints
- Library version requirements
- Performance benchmarks
- Security considerations
- Scalability requirements

### Advanced PRP Workflow

**1. Enhanced Research Phase**
- Deep codebase pattern analysis
- Technology stack compatibility assessment
- Performance and scalability consideration integration

**2. Quality-First Generation**
- Implementation task dependency mapping
- Validation command verification
- Anti-pattern identification and avoidance guidance

**3. Mandatory Quality Gate**
- Automated quality validation before execution approval
- Context completeness verification
- Implementation readiness confirmation

**4. Precision Execution**
- Progressive validation at each implementation step
- Creative testing approaches
- Quality metrics tracking throughout

## Best Practices

### Experimental Development Standards

- **Always validate quality before execution** - Use `/prp-quality-check` mandatory gate
- **Follow dependency ordering strictly** - Implement tasks in specified sequence  
- **Test at each validation level** - Don't skip progressive validation steps
- **Reference specific patterns** - No generic "similar to existing" references
- **Include creative validation** - Level 4 testing pushes beyond standard approaches

### Advanced Context Engineering

- **Apply "No Prior Knowledge" test rigorously** - Assume zero prior context
- **Maximize information density** - Every reference must be specific and actionable
- **Validate reference accessibility** - All URLs and files must be reachable
- **Include implementation constraints** - Real-world gotchas and limitations

### Quality Standards

- **Minimum 8/10 confidence score** for PRP approval
- **Zero placeholder content** allowed in generated PRPs
- **All validation commands must be project-specific** and verified working
- **Context must be complete and self-contained** for implementation success

This experimental template represents the cutting edge of context engineering methodology, designed for teams ready to push the boundaries of AI-assisted development precision and quality.