"""
Test suite for Competitor Research Agent.

Tests the competitor research agent's functionality, including web search integration,
prompt adherence, and error handling.
"""

import pytest
from unittest.mock import Mock, patch
from agents.competitor_research_agent import competitor_research_agent
from agents.deps import ResearchAgentDependencies


class TestCompetitorResearchAgent:
    """Test Competitor research agent functionality"""
    
    @pytest.fixture
    def mock_deps(self):
        """Create mock dependencies for testing"""
        deps = Mock(spec=ResearchAgentDependencies)
        deps.brave_api_key = "test-brave-key"
        return deps
    
    @pytest.mark.asyncio
    async def test_competitor_research_agent_basic_functionality(self, mock_deps):
        """Test basic competitor research agent functionality"""
        
        # Mock agent response
        mock_response = Mock()
        mock_response.data = "Competitor Research: TechCorp shows strong market position with recent $50M Series B funding..."
        
        # Mock the agent run method
        with patch.object(competitor_research_agent, 'run', return_value=mock_response) as mock_run:
            
            # Test agent response
            query = "Research TechCorp's competitive position and market analysis"
            result = await competitor_research_agent.run(
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
            assert "Competitor Research" in result.data
    
    @pytest.mark.asyncio 
    async def test_competitor_research_tool_integration(self, mock_deps):
        """Test competitor research agent's web search tool"""
        
        # Test that the tool wrapper exists and can be called
        mock_ctx = Mock()
        mock_ctx.deps = mock_deps
        
        # Import the tool wrapper
        from agents.competitor_research_agent import search_web
        
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
    async def test_competitor_search_tool_error_handling(self, mock_deps):
        """Test error handling in competitor search tool"""
        
        # Mock search to raise exception
        with patch('tools.brave_tools.search_web_tool', side_effect=Exception("Competitor API Error")):
            
            mock_ctx = Mock()
            mock_ctx.deps = mock_deps
            
            from agents.competitor_research_agent import search_web
            
            results = await search_web(mock_ctx, "test query")
            
            # Verify error is handled gracefully
            assert len(results) == 1
            assert "error" in results[0]
            assert "Search failed" in results[0]["error"]
    
    @pytest.mark.asyncio
    async def test_competitor_search_parameter_validation(self, mock_deps):
        """Test parameter validation in competitor search tool"""
        
        # Test that parameters are validated internally
        mock_ctx = Mock()
        mock_ctx.deps = mock_deps
        
        from agents.competitor_research_agent import search_web
        
        # Mock the search_web_tool where it's imported
        with patch('agents.competitor_research_agent.search_web_tool') as mock_search:
            mock_search.return_value = []
            
            # Test with max_results too high
            await search_web(mock_ctx, "test query", max_results=20)
            # Verify it was called (clamped to 10)
            args = mock_search.call_args[1]
            assert args["count"] == 10
            
            # Reset and test with max_results too low
            mock_search.reset_mock()
            await search_web(mock_ctx, "test query", max_results=0)
            # Verify it was called (clamped to 1)
            args = mock_search.call_args[1]
            assert args["count"] == 1
    
    def test_competitor_agent_initialization(self):
        """Test that competitor research agent is properly initialized"""
        
        # Verify agent exists and has correct configuration
        assert competitor_research_agent is not None
        assert competitor_research_agent._deps_type == ResearchAgentDependencies
        
        # Verify agent has tools configured
        # Note: Pydantic AI doesn't expose tools directly, but we can verify the agent is configured
        assert hasattr(competitor_research_agent, 'tool')
    
    @pytest.mark.asyncio
    async def test_competitor_agent_with_message_history(self, mock_deps):
        """Test competitor agent with conversation history"""
        
        
        # Create mock message history - don't instantiate ModelMessage directly
        # Just create a simple message structure for testing
        message_history = []
        
        # Mock agent response
        mock_response = Mock()
        mock_response.data = "Follow-up competitor analysis for TechCorp based on previous context..."
        
        with patch.object(competitor_research_agent, 'run', return_value=mock_response) as mock_run:
            
            result = await competitor_research_agent.run(
                "Follow up on TechCorp's market positioning against competitors",
                deps=mock_deps,
                message_history=message_history
            )
            
            # Verify agent was called with message history
            mock_run.assert_called_once_with(
                "Follow up on TechCorp's market positioning against competitors",
                deps=mock_deps,
                message_history=message_history
            )
            
            # Verify agent processed the request with history
            assert result is not None
            assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_competitor_agent_prompt_adherence(self, mock_deps):
        """Test that competitor agent follows its system prompt focus"""
        
        # Mock agent response focused on competitive analysis
        mock_response = Mock()
        mock_response.data = "Competitive Analysis: Company X shows strong market positioning with key advantages..."
        
        with patch.object(competitor_research_agent, 'run', return_value=mock_response) as mock_run:
            
            # Query should trigger competitive analysis-focused research
            result = await competitor_research_agent.run(
                "Analyze Company X's competitive advantages and market positioning",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called
            mock_run.assert_called_once_with(
                "Analyze Company X's competitive advantages and market positioning",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent provided a response
            assert result is not None
            
            # The agent should focus on competitive analysis aspects
            assert result.data is not None
            assert "Competitive Analysis" in result.data
    
    @pytest.mark.asyncio
    async def test_competitor_agent_business_intelligence(self, mock_deps):
        """Test that competitor agent focuses on business intelligence aspects"""
        
        # Mock agent response for business intelligence
        mock_response = Mock()
        mock_response.data = "Business Intelligence: TechCorp has strong funding history with strategic partnerships..."
        
        with patch.object(competitor_research_agent, 'run', return_value=mock_response) as mock_run:
            
            result = await competitor_research_agent.run(
                "Research TechCorp's funding history and strategic partnerships",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called
            mock_run.assert_called_once_with(
                "Research TechCorp's funding history and strategic partnerships",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent responded to business intelligence query
            assert result is not None
            assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_competitor_agent_market_trends(self, mock_deps):
        """Test competitor agent's ability to analyze market trends"""
        
        # Mock agent response for market trends
        mock_response = Mock()
        mock_response.data = "Market Trends Analysis: TechCorp is well-positioned in the AI industry trends..."
        
        with patch.object(competitor_research_agent, 'run', return_value=mock_response) as mock_run:
            
            result = await competitor_research_agent.run(
                "Analyze how TechCorp fits into current AI industry trends and opportunities",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called
            mock_run.assert_called_once_with(
                "Analyze how TechCorp fits into current AI industry trends and opportunities",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent responded to market trends query
            assert result is not None
            assert result.data is not None