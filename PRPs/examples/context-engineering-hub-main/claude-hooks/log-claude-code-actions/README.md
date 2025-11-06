# log-claude-code-actions Hook

A security and audit hook that logs every Bash command executed by Claude Code, providing complete visibility into AI-driven system interactions.

## Purpose

This hook creates an audit trail of all Bash commands executed during Claude Code sessions, essential for:
- **Security auditing** - Track exactly what commands were run
- **Debugging** - Understand command sequences that led to issues  
- **Compliance** - Maintain records for regulatory requirements
- **Learning** - Review how Claude approaches different tasks

## How It Works

The hook intercepts all Bash tool uses via the `PreToolUse` event and logs:
- The exact command being executed
- Command description (if Claude provides one)
- Timestamp (via file modification time)

All logs append to `~/.claude/bash-command-log.txt` for persistent tracking across sessions.

## Installation

1. **Copy the hook configuration** from `hook.json`

2. **Add to your Claude settings** (`~/.claude/settings.json`):
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             {
               "type": "command",
               "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
             }
           ]
         }
       ]
     }
   }
   ```

3. **Create the log file** (optional):
   ```bash
   touch ~/.claude/bash-command-log.txt
   ```

## Log Format

Each line in the log follows this format:
```
<command> - <description or "No description">
```

Example log entries:
```
git status - Check repository status
npm install - Install project dependencies  
rm -rf node_modules - No description
docker-compose up -d - Start services in background
```

## Usage Tips

### Viewing Recent Commands
```bash
tail -20 ~/.claude/bash-command-log.txt
```

### Searching for Specific Commands
```bash
grep "git" ~/.claude/bash-command-log.txt
```

### Adding Timestamps
For more detailed logging with timestamps, modify the command:
```json
{
  "command": "echo \"$(date '+%Y-%m-%d %H:%M:%S') - $(jq -r '.tool_input.command + \" - \" + (.tool_input.description // \"No description\")')\" >> ~/.claude/bash-command-log.txt"
}
```

### Rotating Logs
To prevent the log from growing too large:
```bash
# Add to crontab
0 0 * * 0 mv ~/.claude/bash-command-log.txt ~/.claude/bash-command-log.$(date +%Y%m%d).txt
```

## Security Considerations

- **Log contains sensitive data** - Commands may include paths, filenames, or operations
- **Secure the log file** - Consider restricting permissions: `chmod 600 ~/.claude/bash-command-log.txt`
- **Regular reviews** - Periodically check logs for unexpected commands
- **No passwords** - This hook doesn't capture stdin, so passwords remain secure
