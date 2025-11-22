#!/usr/bin/env python3
"""
Test script for browser service functionality.
"""

import asyncio
import json
from mcp_server.browser.browser_service import get_browser_service


async def test_browser_functions():
    """Test all browser service functions."""
    print("Initializing browser service...")
    browser_service = await get_browser_service()

    # Test URL
    test_url = "https://nextjs.org/"

    print(f"\n1. Testing get_page_content for {test_url}")
    try:
        content_result = await browser_service.get_page_content(test_url)
        # print(f"   content_result : {content_result} characters")
        print(f"   Status: {content_result.get('status')}")
        print(f"   Title: {content_result.get('title')[:50]}...")
        print(f"   Content length: {len(content_result.get('html', ''))} characters")
    except Exception as e:
        print(f"   Error: {str(e)}")

    print(f"\n2. Testing get_console_messages for {test_url}")
    try:
        console_result = await browser_service.get_console_messages(test_url)
        # print(f"   content_result : {console_result} characters")
        print(f"   Status: {console_result.get('status')}")
        print(f"   Console messages count: {len(console_result.get('console_messages', []))}")
    except Exception as e:
        print(f"   Error: {str(e)}")

    print(f"\n3. Testing get_network_requests for {test_url}")
    try:
        network_result = await browser_service.get_network_requests(test_url)
        # print(f"   content_result : {network_result} characters")
        print(f"   Status: {network_result.get('status')}")
        print(f"   Requests count: {network_result.get('total_requests')}")
        print(f"   Responses count: {network_result.get('total_responses')}")
    except Exception as e:
        print(f"   Error: {str(e)}")


def run_tests():
    """Run the browser tests."""
    asyncio.run(test_browser_functions())


if __name__ == "__main__":
    run_tests()