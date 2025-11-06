## FEATURE:

Build an intelligent AI assistant that combines traditional RAG with knowledge graph capabilities to provide comprehensive insights. The agent leverages vector similarity search via PostgreSQL with pgvector, hybrid search combining semantic and keyword matching with TSVector in PostgreSQL, and relationship-based reasoning through Neo4j with Graphiti. This creates a powerful multi-layered search system that understands semantic content, keyword relevance, and entity relationships for superior information retrieval and analysis.

You'll need to copy over (with the cp command, you have to actually copy over everything and keep the same folder structure) everything in examples/rag_pipeline because the RAG pipeline is already set up. Look at sql/schema.sql to understand the database structure and the functions for regular and hybrid search. Use the SQL functions provided in schema.sql for vector and hybrid search. You'll want to use asyncpg to create the database connection and have an environment variable in .env.example for the DATABASE_URL.

Build a nice CLI for the agent as well like we have in main_agent_reference. Use Archon for the Pydantic AI documentation + main_agent_reference to guide your implementation. Keep the agent simple - minimal tools, a single LLM determined by an environment variable you put in .env.example, include just the functionality that is crucial for the agent to be powerful but concise.

## TOOLS:

- **vector_search(query: str, limit: int = 10) -> List[Dict]**: Performs pure semantic similarity search across document chunks using pgvector embeddings. Returns chunks with content, similarity scores, document metadata, and source information.

- **graph_search(query: str) -> List[Dict]**: Searches the knowledge graph in Neo4j for entities, relationships, and temporal facts. Returns structured facts with UUIDs, validity periods, and source node references.

- **hybrid_search(query: str, limit: int = 10, text_weight: float = 0.3) -> List[Dict]**: Performs combined semantic vector search AND keyword search using PostgreSQL's TSVector for full-text search. The text_weight parameter controls the balance between semantic similarity and keyword matching. Returns chunks ranked by combined score.

- **perform_comprehensive_search(query: str, use_vector: bool = True, use_graph: bool = True, limit: int = 10) -> Dict**: The master search function that combines vector search results with knowledge graph results in parallel. Returns both vector_results and graph_results, allowing the agent to leverage both document chunks and entity relationships simultaneously.

- **get_document(document_id: str) -> Dict**: Retrieves complete document content with metadata when full context is needed.

- **list_documents(limit: int = 20, offset: int = 0) -> List[Dict]**: Lists available documents with metadata for browsing and discovery.

- **get_entity_relationships(entity_name: str, depth: int = 2) -> List[Dict]**: Traverses the knowledge graph to find relationships for a specific entity up to specified depth.

- **get_entity_timeline(entity_name: str, start_date: Optional[str], end_date: Optional[str]) -> List[Dict]**: Retrieves temporal information about an entity within a date range.

## DEPENDENCIES

- **search_preferences**: Dictionary containing configuration for search behavior (use_vector: bool, use_graph: bool, default_limit: int)
- **Database connections**: AsyncPG connection pool for PostgreSQL, Neo4j driver for graph database (handled internally via db_utils and graph_utils)
- **Embedding client**: OpenAI-compatible embedding API client for generating vector embeddings

## SYSTEM PROMPT(S)

You are an intelligent AI assistant with access to multiple search systems: a vector database for semantic search, TSVector for keyword matching, and a knowledge graph for entity relationships. Your primary capabilities include:
1. Vector search for pure semantic similarity 
2. Hybrid search combining semantic and keyword matching using PostgreSQL's TSVector
3. Knowledge graph search for relationships and temporal facts in Neo4j
4. Comprehensive search that runs vector and graph searches in parallel
5. Full document retrieval when detailed context is needed

When answering questions, always search for relevant information before responding. Use hybrid_search when you need both semantic understanding and specific keyword matches. Use perform_comprehensive_search when you need to combine document chunks with entity relationships. Cite your sources by mentioning document titles and specific facts. Consider temporal aspects as some information may be time-sensitive. Look for relationships and connections between entities.

Your responses should be accurate and based on available data, well-structured and easy to understand, comprehensive while remaining concise, and transparent about information sources. Use the knowledge graph tool only when the user asks about relationships between two or more entities in the same question. Otherwise, use vector or hybrid search for document retrieval.

## EXAMPLES:

- examples/basic_chat_agent - Basic chat agent with conversation memory
- examples/tool_enabled_agent - Tool-enabled agent with web search capabilities  
- examples/structured_output_agent - Structured output agent for data validation
- examples/testing_examples - Testing examples with TestModel and FunctionModel
- examples/main_agent_reference - Best practices for building Pydantic AI agents
- examples/rag_pipeline - RAG ingestion and also very important SQL DB and Graph DB util fils in utils/

## DOCUMENTATION:

- Pydantic AI Official Documentation: https://ai.pydantic.dev/
- Agent Creation Guide: https://ai.pydantic.dev/agents/
- Tool Integration: https://ai.pydantic.dev/tools/
- Testing Patterns: https://ai.pydantic.dev/testing/
- Model Providers: https://ai.pydantic.dev/models/
- Use Archon MCP server to query for Pydantic AI and Graphiti documentation and code examples

## OTHER CONSIDERATIONS:

- Use environment variables for API key configuration instead of hardcoded model strings
- Keep agents simple - default to string output unless structured output is specifically needed
- Follow the main_agent_reference patterns for configuration and providers
- Always include comprehensive testing with TestModel for development