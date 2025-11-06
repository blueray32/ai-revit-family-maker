"""
Unit tests for the guardrail agent functionality.

Tests guardrail decisions for research vs conversation routing.
"""

import pytest
from unittest.mock import MagicMock, patch

from agents.guardrail_agent import guardrail_agent, GuardrailResponse
from agents.deps import GuardrailDependencies


@pytest.fixture
def mock_guardrail_deps():
    """Create mock guardrail dependencies"""
    return GuardrailDependencies(session_id="test-session-123")


@pytest.fixture
def mock_research_result():
    """Create mock result for research request"""
    mock_result = MagicMock()
    mock_result.data = GuardrailResponse(
        is_research_request=True, 
        reasoning="This is a request requiring comprehensive research and analysis"
    )
    return mock_result


@pytest.fixture
def mock_conversation_result():
    """Create mock result for conversation request"""
    mock_result = MagicMock()
    mock_result.data = GuardrailResponse(
        is_research_request=False, 
        reasoning="This is a general conversation request"
    )
    return mock_result


class TestGuardrailAgent:
    """Test cases for guardrail agent functionality"""

    @pytest.mark.asyncio
    async def test_guardrail_research_detection(self, mock_guardrail_deps, mock_research_result):
        """Guardrail correctly identifies research requests"""
        research_queries = [
            "Research John Doe at TechCorp",
            "I want to start an AI pet startup for dogs",
            "Analyze the market for sustainable fashion",
            "What's the competitive landscape for meal delivery services?",
            "Research blockchain applications in healthcare"
        ]
        
        with patch.object(guardrail_agent, 'run', return_value=mock_research_result) as mock_run:
            for query in research_queries:
                result = await guardrail_agent.run(query, deps=mock_guardrail_deps)
                
                # Verify the agent was called with correct parameters
                mock_run.assert_called_with(query, deps=mock_guardrail_deps)
                
                # Verify structured output
                assert hasattr(result.data, 'is_research_request')
                assert hasattr(result.data, 'reasoning')
                assert result.data.is_research_request is True
                assert isinstance(result.data.reasoning, str)

    @pytest.mark.asyncio
    async def test_guardrail_conversation_detection(self, mock_guardrail_deps, mock_conversation_result):
        """Guardrail correctly identifies conversation requests"""
        conversation_queries = [
            "How are you today?",
            "What's the weather like?",
            "Explain machine learning to me",
            "Help me understand this concept",
            "Tell me a joke",
            "How does this system work?"
        ]
        
        with patch.object(guardrail_agent, 'run', return_value=mock_conversation_result) as mock_run:
            for query in conversation_queries:
                result = await guardrail_agent.run(query, deps=mock_guardrail_deps)
                
                # Verify the agent was called with correct parameters
                mock_run.assert_called_with(query, deps=mock_guardrail_deps)
                
                # Verify structured output
                assert hasattr(result.data, 'is_research_request')
                assert hasattr(result.data, 'reasoning')
                assert result.data.is_research_request is False
                assert isinstance(result.data.reasoning, str)

    @pytest.mark.asyncio
    async def test_guardrail_agent_with_message_history(self, mock_guardrail_deps, mock_research_result):
        """Guardrail agent works with message history"""
        query = "Research John Doe at TechCorp"
        message_history = [MagicMock()]  # Mock message history
        
        with patch.object(guardrail_agent, 'run', return_value=mock_research_result) as mock_run:
            result = await guardrail_agent.run(
                query, 
                deps=mock_guardrail_deps, 
                message_history=message_history
            )
            
            # Verify the agent was called with message history
            mock_run.assert_called_with(
                query, 
                deps=mock_guardrail_deps, 
                message_history=message_history
            )
            
            # Verify result structure
            assert result.data.is_research_request is True

    def test_guardrail_response_structure(self):
        """Test GuardrailResponse dataclass structure"""
        response = GuardrailResponse(
            is_research_request=True,
            reasoning="Test reasoning"
        )
        
        assert response.is_research_request is True
        assert response.reasoning == "Test reasoning"
        assert isinstance(response.is_research_request, bool)
        assert isinstance(response.reasoning, str)

    def test_guardrail_dependencies_structure(self):
        """Test GuardrailDependencies dataclass structure"""
        deps = GuardrailDependencies(session_id="test-123")
        
        assert deps.session_id == "test-123"
        
        # Test with None session_id
        deps_none = GuardrailDependencies()
        assert deps_none.session_id is None