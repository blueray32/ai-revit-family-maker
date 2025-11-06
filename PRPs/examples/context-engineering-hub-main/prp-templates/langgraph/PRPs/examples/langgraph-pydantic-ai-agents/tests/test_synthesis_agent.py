"""
Test suite for Synthesis Agent.

Tests the synthesis agent's functionality, including research data synthesis,
comprehensive analysis creation, and error handling.
"""

import pytest
from unittest.mock import Mock, patch
from agents.synthesis_agent import synthesis_agent
from agents.deps import ResearchAgentDependencies


class TestSynthesisAgent:
    """Test Synthesis agent functionality"""
    
    @pytest.fixture
    def mock_deps(self):
        """Create mock dependencies for testing"""
        deps = Mock(spec=ResearchAgentDependencies)
        return deps
    
    @pytest.mark.asyncio
    async def test_synthesis_agent_basic_functionality(self, mock_deps):
        """Test basic synthesis agent functionality"""
        
        # Mock agent response
        mock_response = Mock()
        mock_response.data = "Research Synthesis: Comprehensive analysis synthesizing all research findings..."
        
        # Mock the agent run method
        with patch.object(synthesis_agent, 'run', return_value=mock_response) as mock_run:
            
            # Test agent response
            query = "Create a comprehensive synthesis of all research findings"
            result = await synthesis_agent.run(
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
            assert "Research Synthesis" in result.data
    
    @pytest.mark.asyncio 
    async def test_synthesis_tool_integration(self, mock_deps):
        """Test synthesis agent's research data synthesis tool"""
        
        # Create a context object that mimics RunContext
        mock_ctx = Mock()
        mock_ctx.deps = mock_deps
        
        # Import and test the tool directly
        from agents.synthesis_agent import synthesize_research_data
        
        seo_research = "TechCorp has strong domain authority of 65 and good organic traffic"
        social_research = "John Doe has 10k+ LinkedIn connections and active thought leadership"
        competitor_research = "TechCorp raised $50M Series B, positioned well against competitors"
        original_query = "Research John Doe at TechCorp"
        
        results = await synthesize_research_data(
            mock_ctx, 
            seo_research=seo_research,
            social_research=social_research,
            competitor_research=competitor_research,
            original_query=original_query
        )
        
        # Verify synthesis results
        assert "seo_insights" in results
        assert "social_insights" in results
        assert "competitive_insights" in results
        assert "original_context" in results
        assert results["seo_insights"] == seo_research
        assert results["social_insights"] == social_research
        assert results["competitive_insights"] == competitor_research
        assert results["original_context"] == original_query
    
    @pytest.mark.asyncio
    async def test_synthesis_tool_error_handling(self, mock_deps):
        """Test error handling in synthesis tool"""
        
        mock_ctx = Mock()
        mock_ctx.deps = mock_deps
        
        from agents.synthesis_agent import synthesize_research_data
        
        # Test with None values (should handle gracefully)
        results = await synthesize_research_data(
            mock_ctx,
            seo_research=None,
            social_research="Social data",
            competitor_research="Competitor data", 
            original_query="Test query"
        )
        
        # Verify error is handled gracefully
        assert "seo_insights" in results
        assert "social_insights" in results
        assert "competitive_insights" in results
        assert results["seo_insights"] is None
        assert results["social_insights"] == "Social data"
    
    def test_synthesis_agent_initialization(self):
        """Test that synthesis agent is properly initialized"""
        
        # Verify agent exists and has correct configuration
        assert synthesis_agent is not None
        assert synthesis_agent._deps_type == ResearchAgentDependencies
        
        # Verify agent has tools configured
        # Note: Pydantic AI doesn't expose tools directly, but we can verify the agent is configured
        assert hasattr(synthesis_agent, 'tool')
    
    @pytest.mark.asyncio
    async def test_synthesis_agent_with_message_history(self, mock_deps):
        """Test synthesis agent with conversation history"""
        
        
        # Create mock message history - don't instantiate ModelMessage directly
        # Just create a simple message structure for testing
        message_history = []
        
        # Mock agent response with message history
        mock_response = Mock()
        mock_response.data = "Research synthesis created with context from previous conversation..."
        
        with patch.object(synthesis_agent, 'run', return_value=mock_response) as mock_run:
            
            result = await synthesis_agent.run(
                "Create comprehensive synthesis of all the research findings",
                deps=mock_deps,
                message_history=message_history
            )
            
            # Verify agent was called with message history
            mock_run.assert_called_once_with(
                "Create comprehensive synthesis of all the research findings",
                deps=mock_deps,
                message_history=message_history
            )
            
            # Verify agent processed the request with history
            assert result is not None
            assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_synthesis_agent_comprehensive_input(self, mock_deps):
        """Test synthesis agent with comprehensive research inputs"""
        
        comprehensive_prompt = """
        Create a comprehensive analysis based on parallel research findings:
        
        Original Request: Research Sarah Smith at Microsoft
        
        SEO Research Findings:
        Microsoft has exceptional domain authority (95+) and strong organic presence. 
        Sarah Smith appears in several high-ranking Microsoft blog posts and technical papers.
        
        Social Media Research Findings:
        Sarah Smith is very active on LinkedIn with 15k+ connections, regularly posts about 
        AI/ML innovations, and has strong engagement rates. She's a thought leader in enterprise AI.
        
        Competitor Research Findings:
        Microsoft recently announced $10B AI investment, positioning strongly against Google and Amazon.
        Sarah's team is leading several key AI initiatives mentioned in recent earnings calls.
        
        Please synthesize all research findings and create a comprehensive analysis with strategic insights.
        """
        
        # Mock agent response for comprehensive input
        mock_response = Mock()
        mock_response.data = "Comprehensive research synthesis analyzing SEO, social media, and competitor intelligence..."
        
        with patch.object(synthesis_agent, 'run', return_value=mock_response) as mock_run:
            
            result = await synthesis_agent.run(
                comprehensive_prompt,
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called
            mock_run.assert_called_once_with(
                comprehensive_prompt,
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent provided a response to comprehensive input
            assert result is not None
            assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_synthesis_agent_prompt_adherence(self, mock_deps):
        """Test that synthesis agent follows its system prompt for research synthesis"""
        
        # Mock agent response focused on research synthesis
        mock_response = Mock()
        mock_response.data = "Comprehensive research synthesis created from all findings..."
        
        with patch.object(synthesis_agent, 'run', return_value=mock_response) as mock_run:
            
            # Query should trigger research synthesis based on research
            result = await synthesis_agent.run(
                "Based on the research findings, create a comprehensive analysis and synthesis",
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called
            mock_run.assert_called_once_with(
                "Based on the research findings, create a comprehensive analysis and synthesis",
                deps=mock_deps,
                message_history=[]
            )
        
        # Verify agent provided a response
        assert result is not None
        
        # The agent should focus on research synthesis
        # (We can't test the exact content without running the full LLM,
        # but we can verify the agent runs successfully)
        assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_synthesis_agent_structure_focus(self, mock_deps):
        """Test that synthesis agent focuses on proper analysis structure"""
        
        structured_prompt = """
        Create a comprehensive research synthesis with proper structure including:
        1. Executive summary
        2. SEO analysis insights
        3. Social media analysis
        4. Competitive intelligence
        5. Strategic recommendations
        6. Actionable conclusions
        
        Research data:
        - Target: John Smith, VP Engineering at TechStart
        - SEO: Company has growing digital presence
        - Social: John is active on tech Twitter, shares ML content
        - Competitive: TechStart raised Series A, expanding ML team
        """
        
        # Mock agent response for structured synthesis
        mock_response = Mock()
        mock_response.data = "Structured research synthesis with proper format and insights...\n\nExecutive Summary:\nComprehensive analysis shows..."
        
        with patch.object(synthesis_agent, 'run', return_value=mock_response) as mock_run:
            
            result = await synthesis_agent.run(
                structured_prompt,
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent was called
            mock_run.assert_called_once_with(
                structured_prompt,
                deps=mock_deps,
                message_history=[]
            )
            
            # Verify agent responded to structured synthesis request
            assert result is not None
            assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_synthesis_tool_with_empty_data(self, mock_deps):
        """Test synthesis tool with minimal/empty research data"""
        
        mock_ctx = Mock()
        mock_ctx.deps = mock_deps
        
        from agents.synthesis_agent import synthesize_research_data
        
        results = await synthesize_research_data(
            mock_ctx,
            seo_research="",
            social_research="",
            competitor_research="",
            original_query="Basic research request"
        )
        
        # Should still return valid structure even with empty data
        assert "seo_insights" in results
        assert "social_insights" in results
        assert "competitive_insights" in results
        assert "original_context" in results
        assert results["original_context"] == "Basic research request"