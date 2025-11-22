
import asyncio
import os
import json
import uuid
import aiohttp
import litellm

from datetime import datetime
from typing import Callable, List
from pydantic import BaseModel, Field
from crawl4ai.models import CrawlResult
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy

from mcp_server.utils import save


DEFAULT_INSTRUCTION = ""


def llm_config(
    instruction: str = "",
    save_screenshot: bool = False,
    save_pdf: bool = False,
    generate_markdown: bool = False
):
    """
    Configure LLM settings for crawling.

    Args:
        instruction: Instruction for the LLM
        save_screenshot: Whether to save screenshot
        save_pdf: Whether to save PDF
        generate_markdown: Whether to generate markdown

    Returns:
        CrawlerRunConfig with specified settings
    """
    # Create basic config
    config = CrawlerRunConfig()

    # Add LLM configuration if instruction is provided
    if instruction:
        config.llm_config = LLMConfig(
            provider="openai/gpt-4o-mini",  # Using a common provider
            model="gpt-4o-mini",
            extraction_strategy=LLMExtractionStrategy(instruction=instruction)
        )

    # Set other options based on parameters
    if save_screenshot:
        config.screenshot = True
    if save_pdf:
        config.pdf = True
    if generate_markdown:
        config.markdown = True

    return config


def crawl_config(
    instruction: str = "",
    save_screenshot: bool = False,
    save_pdf: bool = False,
    generate_markdown: bool = False
):
    return llm_config(instruction, save_screenshot, save_pdf, generate_markdown)

async def save_download_files_json(path: str, result: CrawlResult, call: Callable[[str], None]):
    if hasattr(result, 'downloaded_files') and result.downloaded_files:
        save(path, 'downloaded_files.json', json.dumps(result.downloaded_files), call)

        files_dir = os.path.join(path, 'files')
        os.makedirs(files_dir, exist_ok=True)

        # Download and save files from the downloaded files list to files subdirectory
        for file_info in result.downloaded_files:
            if 'url' in file_info and 'filename' in file_info:
                file_url = file_info['url']
                filename = file_info['filename']
                file_path = os.path.join(files_dir, filename)
                
                try:
                    # Use aiohttp to download file
                    async with aiohttp.ClientSession() as session:
                        async with session.get(file_url) as response:
                            if response.status == 200:
                                content = await response.read()
                                save(file_path, filename, content, call)
                except Exception as download_error:
                    print(f"Failed to download {file_url}: {download_error}")


async def crawl_web_page(
    url: str,
    path: str,
    instruction:str = "",
    save_screenshot: bool = False,
    save_pdf: bool = False,
    generate_markdown: bool = False,
    progress_callback=None
) -> str:
    """
    Crawl a web page and save content in multiple formats (HTML, JSON, PDF, screenshot) with downloaded files.

    Args:
        url: The URL of the web page to crawl
        save_path: The base file path to save the crawled content and downloaded files
        progress_callback: Optional callback function to report progress

    Returns:
        str: Success message or error message
    """
    if not url:
        return "URL is required for crawling"

    if not path:
        return "Save path is required for saving content"

    try:
        # Send progress update
        if progress_callback:
            if asyncio.iscoroutinefunction(progress_callback):
                await progress_callback("Launching browser...")
            else:
                # If it's not a coroutine function, we need to handle it differently
                try:
                    result = progress_callback("Launching browser...")
                    if asyncio.iscoroutine(result):
                        await result
                except:
                    # If callback raises an error, just ignore it to maintain compatibility
                    pass

        # Configure browser and crawler
        browser_config = BrowserConfig(headless=True, java_script_enabled=True)

        # Use crawl4ai to crawl the web page
        async with AsyncWebCrawler(config=browser_config) as crawler:
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback("Crawling page...")
                else:
                    try:
                        result = progress_callback("Crawling page...")
                        if asyncio.iscoroutine(result):
                            await result
                    except:
                        pass

            result = await crawler.arun(url=url, config=crawl_config(
                instruction,
                save_screenshot,
                save_pdf,
                generate_markdown
            ))

            if result.success:
                # Send progress update
                if progress_callback:
                    if asyncio.iscoroutinefunction(progress_callback):
                        await progress_callback("Crawl completed, starting to process content...")
                    else:
                        try:
                            result = progress_callback("Crawl completed, starting to process content...")
                            if asyncio.iscoroutine(result):
                                await result
                        except:
                            pass

                # Create directories
                path = f"{path}/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                os.makedirs(path, exist_ok=True)
                files_dir = os.path.join(path, 'files')
                os.makedirs(files_dir, exist_ok=True)

                saved_files = []

                # 1. Save HTML file
                if result.html:
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Saving HTML file...")
                        else:
                            try:
                                result = progress_callback("Saving HTML file...")
                                if asyncio.iscoroutine(result):
                                    await result
                            except:
                                pass
                    save(path, 'output.html', result.html, lambda s: saved_files.append(s))

                # 2. Save JSON file (extracted_content or full result)
                json_content = None
                json_filename = 'output.json'

                # Try to save LLM extracted content as JSON if available
                if hasattr(result, 'extracted_content') and result.extracted_content:
                    json_content = result.extracted_content
                # Otherwise save the full crawl result as JSON
                else:
                    # Create a dictionary representation of the crawl result
                    crawl_result_dict = {
                        'success': result.success,
                        'url': result.url,
                        'html': result.html[:1000] + "..." if result.html and len(result.html) > 1000 else result.html,  # Truncate long HTML
                        'screenshot': bool(result.screenshot),
                        'pdf': bool(result.pdf),
                        'markdown': {
                            'raw_markdown': result.markdown.raw_markdown[:1000] + "..." if result.markdown and result.markdown.raw_markdown and len(result.markdown.raw_markdown) > 1000 else (result.markdown.raw_markdown if result.markdown else None),
                            'links': getattr(result.markdown, 'links', []) if result.markdown else [],
                            'metadata': getattr(result.markdown, 'metadata', {}) if result.markdown else {}
                        } if result.markdown else None,
                        'error_message': result.error_message,
                        'extra_info': result.extra_info if hasattr(result, 'extra_info') else {}
                    }
                    json_content = crawl_result_dict

                if json_content:
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Generating JSON content...")
                        else:
                            try:
                                result = progress_callback("Generating JSON content...")
                                if asyncio.iscoroutine(result):
                                    await result
                            except:
                                pass
                    print("output json:", json_content)
                    save(path, json_filename, json.dumps(json_content, ensure_ascii=False, indent=2), lambda s: saved_files.append(s))

                # 3. Save screenshot file
                if save_screenshot and result.screenshot:
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Generating screenshot...")
                        else:
                            try:
                                result = progress_callback("Generating screenshot...")
                                if asyncio.iscoroutine(result):
                                    await result
                            except:
                                pass
                    save(path, 'output.png', result.screenshot, lambda s: saved_files.append(s))

                # 4. Save PDF file
                if save_pdf and result.pdf:
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Generating PDF...")
                        else:
                            try:
                                result = progress_callback("Generating PDF...")
                                if asyncio.iscoroutine(result):
                                    await result
                            except:
                                pass
                    save(path, 'output.pdf', result.pdf, lambda s: saved_files.append(s))

                # 5. Save Markdown file
                if generate_markdown and hasattr(result, 'markdown') and result.markdown:
                    if progress_callback:
                        if asyncio.iscoroutinefunction(progress_callback):
                            await progress_callback("Generating Markdown...")
                        else:
                            try:
                                result = progress_callback("Generating Markdown...")
                                if asyncio.iscoroutine(result):
                                    await result
                            except:
                                pass
                    save(path, 'raw_markdown.md', result.markdown.raw_markdown, lambda s: saved_files.append(s))

                # 6. Save downloaded files as JSON
                if progress_callback:
                    if asyncio.iscoroutinefunction(progress_callback):
                        await progress_callback("Processing downloaded files...")
                    else:
                        try:
                            result = progress_callback("Processing downloaded files...")
                            if asyncio.iscoroutine(result):
                                await result
                        except:
                            pass
                await save_download_files_json(path, result, lambda s: saved_files.append(s))

                if progress_callback:
                    if asyncio.iscoroutinefunction(progress_callback):
                        await progress_callback(f"Final result JSON output...")
                    else:
                        try:
                            result = progress_callback(f"Final result JSON output...")
                            if asyncio.iscoroutine(result):
                                await result
                        except:
                            pass

                return f"Successfully crawled {url} and saved {len(saved_files)} files to {path}"
            else:
                if progress_callback:
                    if asyncio.iscoroutinefunction(progress_callback):
                        await progress_callback(f"Crawl failed: {result.error_message}")
                    else:
                        try:
                            result = progress_callback(f"Crawl failed: {result.error_message}")
                            if asyncio.iscoroutine(result):
                                await result
                        except:
                            pass
                print("Error:", result.error_message)
                return f"Failed to crawl URL: {result.error_message}"
    except Exception as e:
        if progress_callback:
            if asyncio.iscoroutinefunction(progress_callback):
                await progress_callback(f"An error occurred: {str(e)}")
            else:
                try:
                    result = progress_callback(f"An error occurred: {str(e)}")
                    if asyncio.iscoroutine(result):
                        await result
                except:
                    pass
        return f"Error crawling URL or saving files: {str(e)}"


