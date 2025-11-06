# LangGraph State Management Patterns

## State Schema Design

### TypedDict Approach (Recommended)
TypedDict provides the best performance for most LangGraph applications:

```python
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    # Message history with concatenation reducer
    messages: Annotated[list[BaseMessage], operator.add]
    
    # Simple fields without reducers (last write wins)
    current_user: str
    session_id: str
    
    # Lists that should concatenate
    research_results: Annotated[list[dict], operator.add]
    
    # Custom data structures
    metadata: dict
```

### Pydantic BaseModel Approach
Use when runtime validation is required:

```python
from pydantic import BaseModel, Field
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class ValidatedState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_id: str = Field(..., description="Unique user identifier")
    confidence_score: float = Field(ge=0.0, le=1.0, description="AI confidence")
    
    class Config:
        arbitrary_types_allowed = True  # Required for LangChain messages
```

### MessagesState Shortcut
Built-in state for message-focused applications:

```python
from langgraph.graph import MessagesState

# Use directly
workflow = StateGraph(MessagesState)

# Or extend with additional fields
class ExtendedMessagesState(MessagesState):
    user_context: str
    processing_step: int
```

## State Reducers

### Built-in Reducers

#### operator.add - Concatenation
Most common reducer for lists and sequences:

```python
# List concatenation
messages: Annotated[list[BaseMessage], operator.add]
results: Annotated[list[dict], operator.add]

# String concatenation (careful with this)
accumulated_text: Annotated[str, operator.add]
```

#### add_messages - Message-Specific
Specialized reducer for LangChain messages:

```python
from langgraph.graph import add_messages

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    # add_messages handles message deduplication and ID management
```

### Custom Reducers

#### Dictionary Merging
```python
def merge_dicts(left: dict, right: dict) -> dict:
    """Merge dictionaries, with right values taking precedence."""
    result = left.copy()
    result.update(right)
    return result

class StateWithDictMerging(TypedDict):
    config: Annotated[dict, merge_dicts]
    user_preferences: Annotated[dict, merge_dicts]
```

#### List Deduplication
```python
def dedupe_list(left: list, right: list) -> list:
    """Combine lists while removing duplicates."""
    combined = left + right
    return list(dict.fromkeys(combined))  # Preserves order

class StateWithDeduplication(TypedDict):
    unique_items: Annotated[list[str], dedupe_list]
```

#### Numeric Operations
```python
def sum_values(left: int, right: int) -> int:
    return left + right

def max_value(left: float, right: float) -> float:
    return max(left, right)

class NumericState(TypedDict):
    total_count: Annotated[int, sum_values]
    max_confidence: Annotated[float, max_value]
```

## State Update Patterns

### Partial Updates
Nodes return partial state updates that are merged:

```python
async def research_node(state: AgentState) -> dict:
    # Only update specific fields
    research_data = await perform_research(state["query"])
    
    return {
        "research_results": [{"source": "web", "data": research_data}],
        "processing_step": "research_complete"
    }
```

### Conditional Updates
Update state based on conditions:

```python
async def conditional_node(state: AgentState) -> dict:
    updates = {"processed": True}
    
    if state.get("confidence_score", 0) > 0.8:
        updates["high_confidence"] = True
        updates["ready_for_action"] = True
    
    return updates
```

### Message Management
Proper message handling patterns:

```python
async def agent_node(state: AgentState) -> dict:
    messages = state["messages"]
    last_message = messages[-1]
    
    # Create response message
    response = await llm.ainvoke(messages)
    
    # Return message update (operator.add will concatenate)
    return {"messages": [response]}
```

## Multi-Agent State Coordination

### Shared State Access
All agents access the same state schema:

```python
class MultiAgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    
    # Agent coordination fields
    current_agent: str
    agent_results: Annotated[list[dict], operator.add]
    
    # Shared context
    user_context: dict
    task_progress: dict
```

### Agent-Specific State Isolation
Prevent agent interference through careful state design:

```python
class IsolatedAgentState(TypedDict):
    # Shared communication
    messages: Annotated[list[BaseMessage], operator.add]
    
    # Agent-specific results (namespaced)
    research_agent_results: Annotated[list[dict], operator.add]
    analysis_agent_results: Annotated[list[dict], operator.add]
    synthesis_agent_results: Annotated[list[dict], operator.add]
    
    # Coordination
    active_agents: list[str]
    completed_tasks: Annotated[list[str], operator.add]
```

### Concurrent State Updates
Handle parallel agent execution safely:

```python
async def parallel_agent_a(state: MultiAgentState) -> dict:
    # Agent A updates its specific fields
    return {
        "agent_results": [{"agent": "A", "result": "data_a"}],
        "completed_tasks": ["task_a"]
    }

async def parallel_agent_b(state: MultiAgentState) -> dict:
    # Agent B updates its specific fields
    return {
        "agent_results": [{"agent": "B", "result": "data_b"}], 
        "completed_tasks": ["task_b"]
    }

# Both agents can run in parallel - operator.add will merge results
```

## State Persistence Patterns

### Memory-Based Persistence
For development and simple applications:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# State persists across invocations for same thread
config = {"configurable": {"thread_id": "user_123"}}
```

### Database Persistence
For production applications:

```python
from langgraph.checkpoint.postgres import PostgresCheckpointer

# Production checkpointer with database
checkpointer = PostgresCheckpointer.from_conn_string(
    "postgresql://user:pass@localhost:5432/langgraph"
)
graph = workflow.compile(checkpointer=checkpointer)
```

### Custom Checkpointing
Implement custom persistence logic:

```python
from langgraph.checkpoint.base import BaseCheckpointSaver

class RedisCheckpointer(BaseCheckpointSaver):
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def aput(self, config, checkpoint):
        # Store checkpoint in Redis
        pass
    
    async def aget(self, config):
        # Retrieve checkpoint from Redis  
        pass
```

## State Debugging and Inspection

### State Visualization
Debug state changes during development:

```python
async def debug_node(state: MyState) -> dict:
    print(f"Current state: {state}")
    
    # Process normally
    result = await my_processing_logic(state)
    
    print(f"State updates: {result}")
    return result
```

### State History Tracking
Track state evolution over time:

```python
class TrackedState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    state_history: Annotated[list[dict], operator.add]

async def tracking_node(state: TrackedState) -> dict:
    # Add current state snapshot to history
    state_snapshot = {
        "timestamp": datetime.now().isoformat(),
        "node": "tracking_node",
        "message_count": len(state.get("messages", []))
    }
    
    return {
        "state_history": [state_snapshot],
        "messages": [AIMessage(content="Processing complete")]
    }
```

## Performance Optimization

### Efficient State Design
- Use TypedDict over Pydantic when validation isn't critical
- Keep state objects lean - avoid storing large data structures
- Use appropriate reducers to prevent unbounded state growth

### Memory Management
- Implement state cleanup for long-running workflows
- Consider state compression for large message histories
- Monitor memory usage in production deployments

### Serialization Considerations
- State must be serializable for checkpointing
- Avoid complex objects that don't serialize well
- Use JSON-compatible data types when possible

## Common Patterns and Anti-Patterns

### ✅ Good Patterns
- Use descriptive field names in state schema
- Implement proper reducers for list fields
- Keep state updates focused and minimal
- Use TypedDict for performance-critical applications

### ❌ Anti-Patterns  
- Storing non-serializable objects in state
- Creating deeply nested state structures
- Ignoring reducer functions for list fields
- Modifying state directly instead of returning updates

This comprehensive state management approach enables building robust, scalable multi-agent systems with proper data flow, persistence, and debugging capabilities.