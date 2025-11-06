# Generate LiveKit Agents PRP

Generate a comprehensive Product Requirement Prompt (PRP) for implementing LiveKit Agents voice AI features based on project requirements. This command specializes in realtime voice AI patterns, turn detection, tool integration, and multi-agent workflows.

## Usage
```
/generate-livekit-prp <path-to-INITIAL.md>
```

## Process

1. **Read Requirements**
   - Parse the INITIAL.md feature request
   - Extract voice AI requirements
   - Identify agent behaviors and tools needed
   - Determine deployment target (Cloud/Custom)

2. **ULTRATHINK - Voice AI Architecture**
   - Design voice pipeline (STT-LLM-TTS vs Realtime)
   - Plan turn detection strategy
   - Design tool integration patterns
   - Map multi-agent workflows if needed
   - Consider interruption handling

3. **Research Voice AI Patterns**
   **USE Archon MCP extensively if available:**
   ```
   - perform_rag_query("LiveKit [specific-feature]", source_domain="docs.livekit.io")
   - search_code_examples("[feature] implementation", source_domain="docs.livekit.io")
   ```
   
   **Research areas:**
   - Voice pipeline configuration (providers, models)
   - Turn detection and interruption patterns
   - Tool definition with @function_tool
   - Multi-agent handoff patterns
   - Testing strategies with judges
   - Deployment configurations

4. **Generate Specialized PRP**
   Create complete PRP with:
   - **Goal**: Voice AI implementation objectives
   - **Architecture**: AgentSession and Agent design
   - **Voice Pipeline**: STT-LLM-TTS configuration
   - **Tools**: Function definitions and MCP integration
   - **Workflows**: Multi-agent patterns if applicable
   - **Testing**: Behavioral validation with judges
   - **Deployment**: LiveKit Cloud or custom setup
   - **Examples**: Working code from documentation
   - **Validation**: Test commands with UV

5. **Include LiveKit Patterns**
   - Agent lifecycle methods (on_enter, on_exit)
   - Session event handlers
   - RoomInputOptions for noise cancellation
   - Provider selection matrix
   - Error handling patterns
   - State management

6. **Add Implementation Blueprint**
   ```yaml
   Phase 1 - Agent Setup:
     - Initialize UV project
     - Configure AgentSession
     - Define Agent class
     - Set up providers
   
   Phase 2 - Core Features:
     - Implement tools
     - Add conversation flows
     - Handle interruptions
     - Multi-agent handoffs
   
   Phase 3 - Testing:
     - Unit tests for tools
     - Behavioral tests with judges
     - Console mode testing
   
   Phase 4 - Deployment:
     - Dockerfile creation
     - livekit.toml config
     - Environment variables
     - LiveKit Cloud deploy
   ```

7. **Define Success Criteria**
   - [ ] Agent responds naturally to voice input
   - [ ] Turn detection works smoothly
   - [ ] Tools execute correctly
   - [ ] Interruptions handled gracefully
   - [ ] Tests pass with judges
   - [ ] Deploys to LiveKit Cloud

## Template Structure

IMPORTANT: Follow `PRPs/templates/prp_livekit_base.md` for the structure for the PRP.

## Validation Requirements

The generated PRP must include:
- [ ] Complete voice pipeline configuration
- [ ] Agent class implementation
- [ ] Tool definitions with proper types
- [ ] Testing scenarios with judges
- [ ] Deployment configuration
- [ ] Environment variable list
- [ ] UV commands for all operations
- [ ] Error handling patterns
- [ ] Performance optimization tips
- [ ] Common gotchas and solutions

## Output

Save the generated PRP to: `PRPs/[feature-name]-livekit-agent.md`

The PRP should be immediately executable with:
```bash
/execute-livekit-prp PRPs/[feature-name]-livekit-agent.md
```