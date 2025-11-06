"""
Unit tests for the tool functions (Brave search).

Tests Brave search tool functionality used by all research agents.
"""

import pytest
from unittest.mock import MagicMock, patch
import httpx

from tools.brave_tools import search_web_tool


class TestBraveSearchTool:
    """Test cases for Brave search tool functionality"""

    @pytest.mark.asyncio
    async def test_search_web_tool_success(self):
        """Test successful Brave search"""
        mock_response_data = {
            "web": {
                "results": [
                    {
                        "title": "Test Result 1",
                        "url": "https://example.com/1",
                        "description": "First test result"
                    },
                    {
                        "title": "Test Result 2", 
                        "url": "https://example.com/2",
                        "description": "Second test result"
                    }
                ]
            }
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await search_web_tool(
                api_key="test-api-key",
                query="test query",
                count=2
            )
            
            # Verify results
            assert len(result) == 2
            assert result[0]["title"] == "Test Result 1"
            assert result[0]["url"] == "https://example.com/1"
            assert result[0]["description"] == "First test result"
            assert result[0]["score"] == 1.0  # First result gets highest score
            
            assert result[1]["score"] == 0.95  # Second result gets lower score

    @pytest.mark.asyncio
    async def test_search_web_tool_invalid_api_key(self):
        """Test Brave search with invalid API key"""
        with pytest.raises(ValueError, match="Brave API key is required"):
            await search_web_tool(
                api_key="",
                query="test query"
            )
        
        with pytest.raises(ValueError, match="Brave API key is required"):
            await search_web_tool(
                api_key=None,
                query="test query"
            )

    @pytest.mark.asyncio
    async def test_search_web_tool_empty_query(self):
        """Test Brave search with empty query"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            await search_web_tool(
                api_key="test-api-key",
                query=""
            )
        
        with pytest.raises(ValueError, match="Query cannot be empty"):
            await search_web_tool(
                api_key="test-api-key",
                query=None
            )

    @pytest.mark.asyncio
    async def test_search_web_tool_count_validation(self):
        """Test Brave search count parameter validation"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"web": {"results": []}}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            # Test upper bound (tool limits to max 10)
            await search_web_tool(
                api_key="test-api-key",
                query="test",
                count=25
            )
            
            # Check that the actual API call used count=10 (max limit)
            call_args = mock_client.return_value.__aenter__.return_value.get.call_args
            assert call_args[1]["params"]["count"] == 10
            
            # Test lower bound
            await search_web_tool(
                api_key="test-api-key", 
                query="test",
                count=0
            )
            
            call_args = mock_client.return_value.__aenter__.return_value.get.call_args
            assert call_args[1]["params"]["count"] == 1

    @pytest.mark.asyncio
    async def test_search_web_tool_api_errors(self):
        """Test Brave search API error handling"""
        test_cases = [
            (401, "Invalid Brave API key"),
            (429, "Rate limit exceeded. Check your Brave API quota."),
            (500, "Brave API returned 500:")
        ]
        
        for status_code, expected_error in test_cases:
            mock_response = MagicMock()
            mock_response.status_code = status_code
            mock_response.text = "Error details"
            
            with patch('httpx.AsyncClient') as mock_client:
                mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
                
                with pytest.raises(Exception) as exc_info:
                    await search_web_tool(
                        api_key="test-api-key",
                        query="test query"
                    )
                
                assert expected_error in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_search_web_tool_request_error(self):
        """Test Brave search request error handling"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.RequestError("Network error")
            
            with pytest.raises(Exception, match="Request failed: Network error"):
                await search_web_tool(
                    api_key="test-api-key",
                    query="test query"
                )

    @pytest.mark.asyncio
    async def test_search_web_tool_with_offset(self):
        """Test Brave search with offset parameter"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"web": {"results": []}}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            await search_web_tool(
                api_key="test-api-key",
                query="test query",
                count=5,
                offset=10
            )
            
            # Verify offset was included in request
            call_args = mock_client.return_value.__aenter__.return_value.get.call_args
            params = call_args[1]["params"]
            assert params["offset"] == 10
            assert params["count"] == 5


