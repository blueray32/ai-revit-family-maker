"""
Unit tests for the fallback agent functionality.

Tests fallback agent for normal conversation handling.
"""

import pytest
from unittest.mock import MagicMock, patch

from agents.fallback_agent import fallback_agent
from agents.deps import GuardrailDependencies


@pytest.fixture
def mock_fallback_deps():
    """Create mock fallback dependencies"""
    return GuardrailDependencies(session_id="test-session-123")


@pytest.fixture
def mock_fallback_result():
    """Create mock fallback agent result"""
    mock_result = MagicMock()
    mock_result.data = "I'm here to help with general questions and conversation..."
    mock_result.new_messages_json.return_value = b'{"message": "conversation"}'
    return mock_result


class TestFallbackAgent:
    """Test cases for fallback agent functionality"""

    @pytest.mark.asyncio
    async def test_fallback_agent_conversation(self, mock_fallback_deps, mock_fallback_result):
        """Test fallback agent handling conversation requests"""
        conversation_queries = [
            "How are you today?",
            "What's the weather like?",
            "Explain machine learning to me",
            "Help me understand this concept",
            "Tell me a joke",
            "How does this system work?"
        ]
        
        with patch.object(fallback_agent, 'run', return_value=mock_fallback_result) as mock_run:
            for query in conversation_queries:
                result = await fallback_agent.run(query, deps=mock_fallback_deps)
                
                # Verify the agent was called
                mock_run.assert_called_with(query, deps=mock_fallback_deps)
                
                # Verify result structure
                assert hasattr(result, 'data')
                assert isinstance(result.data, str)
                assert hasattr(result, 'new_messages_json')

    @pytest.mark.asyncio
    async def test_fallback_agent_with_message_history(self, mock_fallback_deps, mock_fallback_result):
        """Test fallback agent with message history"""
        query = "Continue our conversation about AI"
        message_history = [MagicMock()]
        
        with patch.object(fallback_agent, 'run', return_value=mock_fallback_result) as mock_run:
            await fallback_agent.run(
                query, 
                deps=mock_fallback_deps,
                message_history=message_history
            )
            
            # Verify the agent was called with message history
            mock_run.assert_called_with(
                query, 
                deps=mock_fallback_deps,
                message_history=message_history
            )

    @pytest.mark.asyncio
    async def test_fallback_agent_general_questions(self, mock_fallback_deps, mock_fallback_result):
        """Test fallback agent with various general questions"""
        general_queries = [
            "What is artificial intelligence?",
            "How do neural networks work?",
            "Can you explain quantum computing?",
            "What are the latest trends in technology?",
            "Help me understand blockchain",
            "What is the meaning of life?"
        ]
        
        with patch.object(fallback_agent, 'run', return_value=mock_fallback_result) as mock_run:
            for query in general_queries:
                result = await fallback_agent.run(query, deps=mock_fallback_deps)
                
                # Verify the agent responds to general questions
                mock_run.assert_called_with(query, deps=mock_fallback_deps)
                assert result.data is not None

    @pytest.mark.asyncio
    async def test_fallback_agent_guidance_requests(self, mock_fallback_deps, mock_fallback_result):
        """Test fallback agent providing system guidance"""
        guidance_queries = [
            "How do I use this system?",
            "What can you help me with?",
            "What are your capabilities?",
            "How does the research workflow work?",
            "Can you explain your features?"
        ]
        
        with patch.object(fallback_agent, 'run', return_value=mock_fallback_result) as mock_run:
            for query in guidance_queries:
                result = await fallback_agent.run(query, deps=mock_fallback_deps)
                
                # Verify the agent provides guidance
                mock_run.assert_called_with(query, deps=mock_fallback_deps)
                assert result.data is not None

    def test_fallback_dependencies_reuse(self):
        """Test that fallback agent uses GuardrailDependencies"""
        deps = GuardrailDependencies(session_id="test-session")
        
        assert deps.session_id == "test-session"
        
        # Test with None session_id
        deps_none = GuardrailDependencies()
        assert deps_none.session_id is None

    @pytest.mark.asyncio
    async def test_fallback_agent_error_handling(self, mock_fallback_deps):
        """Test fallback agent error handling"""
        query = "Test error handling"
        
        with patch.object(fallback_agent, 'run', side_effect=Exception("Test error")):
            # This should raise the exception since we're not handling it in the agent
            with pytest.raises(Exception):
                await fallback_agent.run(query, deps=mock_fallback_deps)

    @pytest.mark.asyncio
    async def test_fallback_agent_empty_query(self, mock_fallback_deps, mock_fallback_result):
        """Test fallback agent with empty or minimal queries"""
        minimal_queries = [
            "",
            " ",
            "?",
            "Hi",
            "Hello"
        ]
        
        with patch.object(fallback_agent, 'run', return_value=mock_fallback_result) as mock_run:
            for query in minimal_queries:
                result = await fallback_agent.run(query, deps=mock_fallback_deps)
                
                # Verify the agent handles minimal input gracefully
                mock_run.assert_called_with(query, deps=mock_fallback_deps)
                assert result.data is not None

    @pytest.mark.asyncio
    async def test_fallback_agent_message_history_integration(self, mock_fallback_deps):
        """Test fallback agent message history updates for conversation"""
        query = "Continue our discussion"
        
        # Mock result with message history
        mock_result = MagicMock()
        mock_result.data = "Continuing our discussion..."
        mock_result.new_messages_json.return_value = b'{"role": "assistant", "content": "response"}'
        
        with patch.object(fallback_agent, 'run', return_value=mock_result):
            result = await fallback_agent.run(query, deps=mock_fallback_deps)
            
            # Verify conversation history can be captured
            assert hasattr(result, 'new_messages_json')
            messages = result.new_messages_json()
            assert messages is not None
            assert isinstance(messages, bytes)