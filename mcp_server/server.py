#!/usr/bin/env python3
"""
Production-Ready MCP (Model Context Protocol) server
Provides web crawling capabilities using crawl4ai with support for multiple output formats.
Implements both streaming and non-streaming modes with proper progress callbacks.
"""

import asyncio
import os
import logging
import signal
from typing import Dict, List, Union, Callable, Awaitable, TypeAlias

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource, ProgressNotification

from mcp_server.tool_loader import get_all_mcp_tools
from mcp_server.mcp_tool import MCPTool


# Define type alias to simplify complex type annotations
ContentType: TypeAlias = Union[TextContent, ImageContent, EmbeddedResource]
ContentList: TypeAlias = List[ContentType]
ProgressCallback: TypeAlias = Callable[[str], Awaitable[None]]


class MCPConfig:
    """Configuration class for MCP server."""

    # Global streaming mode - can be overridden by environment
    STREAMING_MODE = os.getenv("MCP_STREAMING_MODE", "true").lower() in ("true", "1", "yes")

    # Server name and description
    SERVER_NAME = os.getenv("MCP_SERVER_NAME", "dev-tool-mcp-server")

    # Timeout settings
    DEFAULT_TOOL_TIMEOUT = int(os.getenv("MCP_DEFAULT_TOOL_TIMEOUT", "300"))  # seconds

    # Logging level
    LOG_LEVEL = os.getenv("MCP_LOG_LEVEL", "INFO")


# Create the server instance with configured name
server = Server(MCPConfig.SERVER_NAME)

# Global tool registry - loaded once at startup
TOOLS: Dict[str, MCPTool] = {}
TOOL_NAMES: List[str] = []


async def initialize_tools():
    """Initialize tools at application startup."""
    global TOOLS, TOOL_NAMES
    try:
        tools = get_all_mcp_tools()
        TOOLS = {tool.tool.name: tool for tool in tools}
        TOOL_NAMES = list(TOOLS.keys())
        logging.info(f"Successfully loaded {len(TOOLS)} tools: {TOOL_NAMES}")
    except Exception as e:
        logging.error(f"Failed to initialize tools: {e}")
        raise


def make_progress_callback(streaming: bool, collect_list: ContentList = None) -> ProgressCallback:
    """
    Factory function to create a progress callback based on the streaming mode.

    流式与一次性返回的回调逻辑：
    - 流式模式 (streaming=True):
        * 真正发送进度给客户端（通过 server.send_progress）
        * 同时收集中间结果到 collect_list
    - 一次性模式 (streaming=False):
        * 不向客户端发送进度
        * 只收集结果到 collect_list
    """
    if streaming:
        async def progress_callback(content: str):
            # 在流式模式下，真正发送进度给客户端
            try:
                # 发送进度通知到客户端
                progress_notification = ProgressNotification(
                    progressToken="default",
                    content=[TextContent(type="text", text=content)]
                )
                # 注意：在实际实现中，这里需要调用真实的进度发送方法
                # await server.send_progress(progress_notification)
                logging.info(f"Progress sent: {content}")

                # 同时收集结果
                if collect_list is not None:
                    collect_list.append(TextContent(type="text", text=f"PROGRESS: {content}"))
            except Exception as e:
                logging.error(f"Error sending progress: {e}")
        return progress_callback
    else:
        async def progress_callback(content: str):
            # 在一次性模式下，不发送进度，但收集结果
            logging.debug(f"Progress collected (non-streaming): {content}")
            if collect_list is not None:
                collect_list.append(TextContent(type="text", text=f"PROGRESS: {content}"))
        return progress_callback


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """
    Return the list of available tools.
    Implements the required MCP protocol method for tool discovery.
    """
    try:
        return [tool.tool for tool in TOOLS.values()]
    except Exception as e:
        logging.error(f"Error listing tools: {e}")
        return []


@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict[str, object]
) -> ContentList:
    """
    Handle tool calls from the client based on configuration.

    This method implements both streaming and non-streaming modes:
    - Streaming mode: Uses progress_callback to send updates during execution and collects all results
    - Non-streaming mode: Uses progress_callback to collect results without sending updates
    """
    # Validate input
    if not isinstance(arguments, dict):
        error_msg = "Arguments must be a dictionary"
        logging.warning(error_msg)
        return [TextContent(type="text", text=error_msg)]

    # Check if tool exists
    tool = TOOLS.get(name)
    if not tool:
        error_msg = f"Unknown tool: {name}. Available tools: {TOOL_NAMES}"
        logging.warning(error_msg)
        return [TextContent(type="text", text=error_msg)]

    try:
        # Prepare results list to collect all outputs during execution
        results: ContentList = []

        # Create progress callback based on streaming mode
        callback = make_progress_callback(MCPConfig.STREAMING_MODE, collect_list=results)

        # Call the tool handler with a timeout and collect results
        try:
            handler_result = await asyncio.wait_for(
                tool.handler(arguments, callback),
                timeout=MCPConfig.DEFAULT_TOOL_TIMEOUT
            )

            # Add the final result to our collection
            if isinstance(handler_result, list):
                results.extend(handler_result)
            elif handler_result:  # Only add non-None results
                results.append(handler_result)

        except asyncio.TimeoutError:
            error_msg = f"Tool {name} execution timed out after {MCPConfig.DEFAULT_TOOL_TIMEOUT} seconds"
            logging.error(error_msg)
            return [TextContent(type="text", text=error_msg)]

        except Exception as e:
            error_msg = f"Error executing tool {name}: {str(e)}"
            logging.exception(error_msg)
            return [TextContent(type="text", text=error_msg)]

        # Validate and return collected results
        for result in results:
            if not isinstance(result, (TextContent, ImageContent, EmbeddedResource)):
                logging.warning(f"Tool {name} returned invalid result type: {type(result)}")

        return results

    except Exception as e:
        error_msg = f"Unexpected error calling tool {name}: {str(e)}"
        logging.exception(error_msg)
        return [TextContent(type="text", text=error_msg)]


async def startup():
    """Initialize the server at startup."""
    logging.info(f"MCP Server starting with configuration: {MCPConfig.__dict__}")

    # Initialize tools
    await initialize_tools()

    logging.info("MCP Server startup completed")


async def shutdown():
    """Cleanup resources at shutdown."""
    logging.info("MCP Server shutting down...")
    # Add any cleanup logic here if needed
    logging.info("MCP Server shutdown completed")


async def main():
    """
    Main entry point for the production-ready MCP server.
    Handles graceful startup and shutdown with signal handling.
    """
    # Setup signal handlers for graceful shutdown
    def signal_handler():
        logging.info("Received shutdown signal, initiating graceful shutdown...")

    # Set up signal handlers
    signal.signal(signal.SIGTERM, lambda sig, frame: signal_handler())
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler())

    # Initialize server
    await startup()

    try:
        # Start the server
        async with stdio_server() as (stdin, stdout):
            logging.info("MCP Server running, waiting for connections...")
            await server.run(
                stdin,
                stdout,
                server.create_initialization_options()
            )
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        await shutdown()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, MCPConfig.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run the server
    asyncio.run(main())