"""
Browser service for MCP server using Playwright to provide web page content,
console messages, and network requests information.
"""

import asyncio
import re
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, Page, Route, Response
import json
import urllib.parse


class BrowserService:
    """Encapsulates browser automation functionality using Playwright."""

    def __init__(self):
        self._playwright = None
        self._browser = None
        self._pages = {}  # Store context information for different pages

    async def initialize(self):
        """Initialize Playwright and launch browser."""
        if self._playwright is None:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu',
                    '--disable-web-security'
                ]
            )

    async def close(self):
        """Close browser and cleanup resources."""
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def _create_page_with_context(self) -> Page:
        """Create a new browser page with context."""
        if not self._browser:
            await self.initialize()

        page = await self._browser.new_page()
        return page

    def _sanitize_url(self, url: str) -> str:
        """Sanitize URL to prevent potential security issues."""
        # Basic URL length check
        if len(url) > 2048:
            raise ValueError("URL too long")

        # Validate URL format and ensure it starts with http:// or https://
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme:
            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('/'):
                raise ValueError("Relative URLs are not supported")
            else:
                url = 'https://' + url
        elif parsed.scheme not in ['http', 'https']:
            raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

        # Validate URL format
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc:
            raise ValueError("Invalid URL: missing netloc")

        # Check for potential dangerous characters or protocols
        if re.search(r'[<>"\']', url):
            raise ValueError("Invalid characters in URL")

        return url

    async def get_page_content(self, url: str, wait_for_selector: Optional[str] = None,
                              wait_timeout: int = 30000, progress_callback=None) -> Dict[str, Any]:
        """
        Get the content of a web page by the specified URL

        Args:
            url: The URL of the target page
            wait_for_selector: Optional CSS selector to wait for a specific element to appear
            wait_timeout: Wait timeout time (milliseconds), default 30 seconds
            progress_callback: Optional callback function to report progress

        Returns:
            Dictionary containing page content
        """
        page = None
        try:
            # Validate and clean URL
            sanitized_url = self._sanitize_url(url)

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Opening page...")
                else:
                    progress_callback("Opening page...")

            # Create new page
            page = await self._create_page_with_context()

            # Set page load timeout
            page.set_default_timeout(wait_timeout)

            # Visit page
            response = await page.goto(sanitized_url, wait_until="domcontentloaded")

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Page loaded, waiting for selector...")
                else:
                    progress_callback("Page loaded, waiting for selector...")

            # If selector is specified, wait for it to appear
            if wait_for_selector:
                try:
                    await page.wait_for_selector(wait_for_selector, state="visible", timeout=wait_timeout)
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Selector element found...")
                        else:
                            progress_callback("Selector element found...")

                except:
                    # If wait times out, continue getting content
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Waiting for selector timed out, continuing processing...")
                        else:
                            progress_callback("Waiting for selector timed out, continuing processing...")

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Extracting DOM content...")
                else:
                    progress_callback("Extracting DOM content...")

            # Get page title
            title = await page.title()

            # Get page HTML content
            html_content = await page.content()

            # Get page text content
            text_content = await page.text_content('body')

            # Get page metadata
            meta_elements = await page.eval_on_selector_all('meta',
                'elements => elements.map(el => ({name: el.name || el.property, content: el.content}))')

            # Get page links
            links = await page.eval_on_selector_all('a',
                'elements => elements.map(el => ({text: el.innerText, href: el.href}))')

            # Get page images
            images = await page.eval_on_selector_all('img',
                'elements => elements.map(el => ({src: el.src, alt: el.alt}))')

            result = {
                "url": sanitized_url,
                "status": response.status if response else None,
                "title": title,
                "html": html_content,
                "text": text_content,
                "meta": meta_elements,
                "links": links,
                "images": images,
                "timestamp": asyncio.get_event_loop().time()
            }

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Processing complete...")
                else:
                    progress_callback("Processing complete...")

            return result

        except Exception as e:
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback(f"Error occurred during processing: {str(e)}")
                else:
                    progress_callback(f"Error occurred during processing: {str(e)}")
            return {
                "url": url,
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time()
            }
        finally:
            if page:
                await page.close()

    async def get_console_messages(self, url: str, wait_for_selector: Optional[str] = None,
                                  wait_timeout: int = 30000, progress_callback=None) -> Dict[str, Any]:
        """
        Get console messages from the specified page

        Args:
            url: The URL of the target page
            wait_for_selector: Optional CSS selector to wait for a specific element to appear
            wait_timeout: Wait timeout time (milliseconds), default 30 seconds
            progress_callback: Optional callback function to report progress

        Returns:
            Dictionary containing console messages
        """
        page = None
        console_messages = []

        def handle_console_msg(msg):
            """Callback function to handle console messages"""
            try:
                # Get message type and text
                message_type = msg.type
                text = msg.text
                location = {
                    "url": msg.page.url if msg.page else "unknown",
                    "line_number": getattr(msg, 'line_number', 0),
                    "column_number": getattr(msg, 'column_number', 0)
                }

                # If message includes error stack, try to get it
                stack = getattr(msg, 'stack', None)

                console_messages.append({
                    "type": message_type,
                    "text": text,
                    "location": location,
                    "stack": stack,
                    "timestamp": asyncio.get_event_loop().time()
                })
            except Exception as e:
                console_messages.append({
                    "type": "error",
                    "text": f"Error processing console message: {str(e)}",
                    "location": {},
                    "stack": None,
                    "timestamp": asyncio.get_event_loop().time()
                })

        try:
            # Validate and clean URL
            sanitized_url = self._sanitize_url(url)

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Opening page to capture console messages...")
                else:
                    progress_callback("Opening page to capture console messages...")

            # Create new page
            page = await self._create_page_with_context()

            # Set page load timeout
            page.set_default_timeout(wait_timeout)

            # Listen for console messages
            page.on("console", handle_console_msg)

            # Visit page
            response = await page.goto(sanitized_url, wait_until="domcontentloaded")

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Page loaded, waiting for selector...")
                else:
                    progress_callback("Page loaded, waiting for selector...")

            # If selector is specified, wait for it to appear
            if wait_for_selector:
                try:
                    await page.wait_for_selector(wait_for_selector, state="visible", timeout=wait_timeout)
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Selector element found...")
                        else:
                            progress_callback("Selector element found...")
                except:
                    # If wait times out, continue getting content
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Waiting for selector timed out, continuing processing...")
                        else:
                            progress_callback("Waiting for selector timed out, continuing processing...")

            # Wait extra time to capture more console messages
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Capturing console messages...")
                else:
                    progress_callback("Capturing console messages...")
            await page.wait_for_timeout(3000)

            result = {
                "url": sanitized_url,
                "status": response.status if response else None,
                "console_messages": console_messages,
                "timestamp": asyncio.get_event_loop().time()
            }

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Console message capture completed...")
                else:
                    progress_callback("Console message capture completed...")

            return result

        except Exception as e:
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback(f"Error occurred during processing: {str(e)}")
                else:
                    progress_callback(f"Error occurred during processing: {str(e)}")
            return {
                "url": url,
                "error": str(e),
                "console_messages": console_messages,  # Return collected messages even if error occurs
                "timestamp": asyncio.get_event_loop().time()
            }
        finally:
            if page:
                await page.close()

    async def get_network_requests(self, url: str, wait_for_selector: Optional[str] = None,
                                  wait_timeout: int = 30000, progress_callback=None) -> Dict[str, Any]:
        """
        Get a list of all network requests made when loading the specified page

        Args:
            url: The URL of the target page
            wait_for_selector: Optional CSS selector to wait for a specific element to appear
            wait_timeout: Wait timeout time (milliseconds), default 30 seconds
            progress_callback: Optional callback function to report progress

        Returns:
            Dictionary containing network request information
        """
        page = None
        requests_list = []
        responses_list = []

        async def handle_request(route):
            """Callback function to handle requests"""
            try:
                request = route.request
                request_info = {
                    "url": request.url,
                    "method": request.method,
                    "resource_type": request.resource_type,
                    "frame_url": request.frame.url if request.frame else None,
                    "headers": dict(request.headers),
                    "timestamp": asyncio.get_event_loop().time()
                }
                requests_list.append(request_info)
                # Continue with the request
                await route.continue_()
            except Exception as e:
                requests_list.append({
                    "error": f"Error processing request: {str(e)}",
                    "timestamp": asyncio.get_event_loop().time()
                })
                await route.continue_()

        def handle_response(response):
            """Callback function to handle responses"""
            try:
                response_info = {
                    "url": response.url,
                    "status": response.status,
                    "status_text": response.status_text,
                    "headers": dict(response.headers),
                    "request_headers": dict(response.request.headers) if response.request else {},
                    "content_type": response.headers.get('content-type', ''),
                    "content_length": response.headers.get('content-length', ''),
                    "timestamp": asyncio.get_event_loop().time()
                }
                responses_list.append(response_info)
            except Exception as e:
                responses_list.append({
                    "error": f"Error processing response: {str(e)}",
                    "url": response.url if response else "unknown",
                    "timestamp": asyncio.get_event_loop().time()
                })

        try:
            # Validate and clean URL
            sanitized_url = self._sanitize_url(url)

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Opening page to capture network requests...")
                else:
                    progress_callback("Opening page to capture network requests...")

            # Create new page
            page = await self._create_page_with_context()

            # Set page load timeout
            page.set_default_timeout(wait_timeout)

            # Enable request interception to capture requests
            await page.route("**/*", handle_request)

            # Listen for responses
            page.on("response", handle_response)

            # Visit page
            response = await page.goto(sanitized_url, wait_until="networkidle")

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Page loaded, waiting for selector...")
                else:
                    progress_callback("Page loaded, waiting for selector...")

            # If selector is specified, wait for it to appear
            if wait_for_selector:
                try:
                    await page.wait_for_selector(wait_for_selector, state="visible", timeout=wait_timeout)
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Selector element found...")
                        else:
                            progress_callback("Selector element found...")
                except:
                    # If wait times out, continue getting content
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Waiting for selector timed out, continuing processing...")
                        else:
                            progress_callback("Waiting for selector timed out, continuing processing...")

            # Wait extra time to capture more network requests
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Capturing network requests...")
                else:
                    progress_callback("Capturing network requests...")
            await page.wait_for_timeout(3000)

            result = {
                "url": sanitized_url,
                "status": response.status if response else None,
                "requests": requests_list,
                "responses": responses_list,
                "total_requests": len(requests_list),
                "total_responses": len(responses_list),
                "timestamp": asyncio.get_event_loop().time()
            }

            # Send progress update
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Network request capture completed...")
                else:
                    progress_callback("Network request capture completed...")

            return result

        except Exception as e:
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback(f"Error occurred during processing: {str(e)}")
                else:
                    progress_callback(f"Error occurred during processing: {str(e)}")
            return {
                "url": url,
                "error": str(e),
                "requests": requests_list,
                "responses": responses_list,
                "total_requests": len(requests_list),
                "total_responses": len(responses_list),
                "timestamp": asyncio.get_event_loop().time()
            }
        finally:
            if page:
                await page.close()


# Global browser service instance
_browser_service = None

async def get_browser_service():
    """Get the browser service instance"""
    global _browser_service
    if _browser_service is None:
        _browser_service = BrowserService()
        await _browser_service.initialize()
    return _browser_service