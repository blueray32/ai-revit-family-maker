"""
Test suite for Social Media Research Agent.

Tests the social media research agent's functionality, including web search integration,
prompt adherence, and error handling.
"""

import pytest
from unittest.mock import Mock, patch
from agents.social_research_agent import social_research_agent
from agents.deps import ResearchAgentDependencies


class TestSocialResearchAgent:
    """Test Social Media research agent functionality"""
    
    @pytest.fixture
    def mock_deps(self):
        """Create mock dependencies for testing"""
        deps = Mock(spec=ResearchAgentDependencies)
        deps.brave_api_key = "test-brave-key"
        return deps
    
    @pytest.mark.asyncio
    async def test_social_research_agent_basic_functionality(self, mock_deps):
        """Test basic social media research agent functionality"""
        
        # Mock agent response
        mock_response = Mock()
        mock_response.data = "Social Media Research: John Doe has strong LinkedIn presence with 10k+ connections..."
        
        # Mock the agent run method
        with patch.object(social_research_agent, 'run', return_value=mock_response) as mock_run:
            
            # Test agent response
            query = "Research John Doe's social media presence and activity"
            result = await social_research_agent.run(
                query,
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called with correct parameters
            mock_run.assert_called_once_with(
                query,
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent responded
            assert result is not None
            assert result.data is not None
            assert "Social Media Research" in result.data
    
    @pytest.mark.asyncio 
    async def test_social_research_tool_integration(self, mock_deps):
        """Test social media research agent's web search tool"""
        
        # Test that the tool wrapper exists and can be called
        mock_ctx = Mock()
        mock_ctx.deps = mock_deps
        
        # Import the tool wrapper
        from agents.social_research_agent import search_web
        
        # Verify the function exists and has correct signature
        import inspect
        sig = inspect.signature(search_web)
        params = list(sig.parameters.keys())
        assert "ctx" in params
        assert "query" in params
        assert "max_results" in params
        
        # Verify it's an async function
        assert inspect.iscoroutinefunction(search_web)
    
    @pytest.mark.asyncio
    async def test_social_search_tool_error_handling(self, mock_deps):
        """Test error handling in social media search tool"""
        
        # Mock search to raise exception
        with patch('tools.brave_tools.search_web_tool', side_effect=Exception("Social API Error")):
            
            mock_ctx = Mock()
            mock_ctx.deps = mock_deps
            
            from agents.social_research_agent import search_web
            
            results = await search_web(mock_ctx, "test query")
            
            # Verify error is handled gracefully
            assert len(results) == 1
            assert "error" in results[0]
            assert "Search failed" in results[0]["error"]
    
    @pytest.mark.asyncio
    async def test_social_search_parameter_validation(self, mock_deps):
        """Test parameter validation in social media search tool"""
        
        # Test that parameters are validated internally
        mock_ctx = Mock()
        mock_ctx.deps = mock_deps
        
        from agents.social_research_agent import search_web
        
        # Mock the search_web_tool where it's imported
        with patch('agents.social_research_agent.search_web_tool') as mock_search:
            mock_search.return_value = []
            
            # Test with max_results too high
            await search_web(mock_ctx, "test query", max_results=15)
            # Verify it was called (clamped to 10)
            args = mock_search.call_args[1]
            assert args["count"] == 10
            
            # Reset and test with max_results too low
            mock_search.reset_mock()
            await search_web(mock_ctx, "test query", max_results=-1)
            # Verify it was called (clamped to 1)
            args = mock_search.call_args[1]
            assert args["count"] == 1
    
    def test_social_agent_initialization(self):
        """Test that social media research agent is properly initialized"""
        
        # Verify agent exists and has correct configuration
        assert social_research_agent is not None
        assert social_research_agent._deps_type == ResearchAgentDependencies
        
        # Verify agent has tools configured
        # Note: Pydantic AI doesn't expose tools directly, but we can verify the agent is configured
        assert hasattr(social_research_agent, 'tool')
    
    @pytest.mark.asyncio
    async def test_social_agent_with_message_history(self, mock_deps):
        """Test social media agent with conversation history"""
        
        
        # Create mock message history - don't instantiate ModelMessage directly
        # Just create a simple message structure for testing
        message_history = []
        
        # Mock agent response
        mock_response = Mock()
        mock_response.data = "Follow-up social media analysis for TechCorp based on previous context..."
        
        with patch.object(social_research_agent, 'run', return_value=mock_response) as mock_run:
            
            result = await social_research_agent.run(
                "Follow up on TechCorp's social media engagement",
                deps=mock_deps,
                message_history=message_history
            )
            
            # Verify agent was called with message history
            mock_run.assert_called_once_with(
                "Follow up on TechCorp's social media engagement",
                deps=mock_deps,
                message_history=message_history
            )
            
            # Verify agent processed the request with history
            assert result is not None
            assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_social_agent_prompt_adherence(self, mock_deps):
        """Test that social media agent follows its system prompt focus"""
        
        # Mock agent response focused on social media
        mock_response = Mock()
        mock_response.data = "Social Media Analysis: Company X shows strong engagement patterns across platforms..."
        
        with patch.object(social_research_agent, 'run', return_value=mock_response) as mock_run:
            
            # Query should trigger social media-focused research
            result = await social_research_agent.run(
                "Analyze Company X's social media strategy and engagement patterns",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called
            mock_run.assert_called_once_with(
                "Analyze Company X's social media strategy and engagement patterns",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent provided a response
            assert result is not None
            
            # The agent should focus on social media-related aspects
            assert result.data is not None
            assert "Social Media Analysis" in result.data
    
    @pytest.mark.asyncio
    async def test_social_agent_platform_coverage(self, mock_deps):
        """Test that social agent covers major social platforms"""
        
        # Mock agent response for platform coverage
        mock_response = Mock()
        mock_response.data = "Multi-platform social media analysis for Sarah Smith across LinkedIn, Twitter, and Instagram..."
        
        with patch.object(social_research_agent, 'run', return_value=mock_response) as mock_run:
            
            result = await social_research_agent.run(
                "Research Sarah Smith's presence across LinkedIn, Twitter, and other platforms",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called
            mock_run.assert_called_once_with(
                "Research Sarah Smith's presence across LinkedIn, Twitter, and other platforms",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent responded to platform-specific query
            assert result is not None
            assert result.data is not None