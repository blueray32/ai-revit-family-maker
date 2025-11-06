"""
Test helpers for agent tests.

Provides common mocking utilities and fixtures.
"""

from unittest.mock import AsyncMock


def create_mock_search_web_tool():
    """Create a mock search_web_tool that behaves like the real one"""
    async def mock_search_web_tool(api_key, query, count):
        # Return empty results by default
        return []
    
    return AsyncMock(side_effect=mock_search_web_tool)