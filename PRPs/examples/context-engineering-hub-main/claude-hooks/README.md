# Claude Code Hooks Collection

Automated workflows and guardrails for Claude Code that execute at key moments during AI-assisted development.

## 🎯 Purpose

Claude Code hooks provide deterministic control over your AI coding workflow. Unlike relying on prompts, hooks guarantee specific actions happen at the right time - from logging commands to enforcing code quality standards.

## 🚀 Quick Start

### Installation

1. **Add to your settings**:
   ```bash
   # Edit ~/.claude/settings.json or .claude/settings.local.json
   ```

3. **Configure the hook** by adding the hook configuration from `hook.json` to your settings file.

## 📋 Available Hooks

### log-claude-code-actions
Logs all Bash commands executed by Claude Code to `~/.claude/bash-command-log.txt` for audit and review.

## 🛠️ How Hooks Work

### Hook Events

Hooks can trigger at these key moments:

| Event | When It Fires | Common Uses |
|-------|--------------|-------------|
| `PreToolUse` | Before any tool runs | Validation, logging, blocking |
| `PostToolUse` | After successful tool completion | Formatting, linting, notifications |
| `UserPromptSubmit` | When user submits a prompt | Context injection, preprocessing |
| `SessionStart` | When Claude Code starts | Environment setup, initialization |
| `Stop` | When Claude finishes responding | Cleanup, summary generation |
| `PreCompact` | Before context compaction | State preservation |
| `Notification` | On specific notifications | Custom alerts, integrations |

### Configuration Structure

```json
{
  "hooks": {
    "EventType": [
      {
        "matcher": "ToolName|Regex",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

### Exit Code Behavior

- **0**: Continue normally
- **Non-zero**: Block the action (for PreToolUse)
- **JSON output**: Advanced control with `continue`, `stopReason`, `suppressOutput`

## 💡 Creating Your Own Hooks

### Basic Hook Template

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'File modified: $CLAUDE_TOOL_INPUT' | jq -r .file_path"
          }
        ]
      }
    ]
  }
}
```

### Available Environment Variables

- `$CLAUDE_PROJECT_DIR` - Current project directory
- `$CLAUDE_TOOL_NAME` - Name of the tool being used
- `$CLAUDE_TOOL_INPUT` - JSON input to the tool
- `$CLAUDE_EVENT_TYPE` - Type of event triggering the hook

### Advanced Hook with JSON Response

```bash
#!/bin/bash
# check-style.sh

file=$(echo "$CLAUDE_TOOL_INPUT" | jq -r .file_path)
if ! eslint "$file" > /dev/null 2>&1; then
  echo '{"continue": false, "stopReason": "ESLint errors found. Please fix before proceeding."}'
  exit 0
fi
echo '{"continue": true}'
```

## 🔒 Security Best Practices

1. **Validate inputs**: Always sanitize data from `$CLAUDE_TOOL_INPUT`
2. **Use absolute paths**: Avoid path traversal vulnerabilities
3. **Quote variables**: Prevent shell injection with proper quoting
4. **Limit permissions**: Run hooks with minimal required privileges
5. **Log actions**: Keep audit trails of hook executions

## 🎨 Hook Ideas

### Code Quality Enforcement
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-and-lint.sh"
  }]
}
```

### Test-Driven Development Guard
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/tdd-check.sh"
  }]
}
```

### Git Commit Validation
```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "grep -q '^git commit' <<< \"$CLAUDE_TOOL_INPUT\" && $CLAUDE_PROJECT_DIR/.claude/hooks/validate-commit.sh"
  }]
}
```

### Security Scanner
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "semgrep --config=auto --json \"$file\" || echo '{\"continue\": false, \"stopReason\": \"Security issues detected\"}'"
  }]
}
```

## 🚦 Hook Categories

- **🔍 Auditing**: Log actions, track changes
- **✅ Quality**: Enforce standards, run linters
- **🛡️ Security**: Scan for vulnerabilities, validate inputs
- **🔄 Workflow**: Automate repetitive tasks
- **📊 Analytics**: Gather metrics, usage patterns
