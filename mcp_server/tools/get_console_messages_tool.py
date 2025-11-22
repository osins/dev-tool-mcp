"""
Get Console Messages Tool - 获取控制台消息工具
"""
import json
from typing import Callable, Awaitable

from mcp.types import Tool, TextContent
from mcp_server.mcp_tool import MCPTool
from mcp_server.browser.browser_service import get_browser_service


class StreamingContext:
    """Streaming context for sending progress updates."""
    
    def __init__(self):
        self.outputs = []

    async def send_output(self, content):
        """Send output to the client."""
        self.outputs.extend(content)


def create_get_console_messages_tool() -> MCPTool:
    """创建 GetConsoleMessagesTool 实例"""
    tool = Tool(
        name="get_console_messages",
        description="Capture console output information from specified URL webpage (including logs, warnings, errors, etc.)",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the web page to get console messages from"
                },
                "wait_for_selector": {
                    "type": "string",
                    "description": "Optional CSS selector to wait for before getting console messages"
                },
                "wait_timeout": {
                    "type": "integer",
                    "description": "Wait timeout in milliseconds, default 30000",
                    "default": 30000
                }
            },
            "required": ["url"]
        }
    )

    async def handler(arguments: dict, progress_callback: Callable[[str], Awaitable[None]]) -> list:
        try:
            # 验证输入参数
            if not isinstance(arguments, dict):
                raise TypeError("Arguments must be a dictionary")
            
            # 从参数中提取并验证字段
            url = arguments.get("url", "")
            wait_for_selector = arguments.get("wait_for_selector")
            wait_timeout = arguments.get("wait_timeout", 30000)
            
            # 验证必需参数
            if not url:
                raise ValueError("URL is required")
            
            # 验证 URL 格式
            if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
                raise ValueError("Invalid URL format")
            
            # 验证 wait_for_selector 格式
            if wait_for_selector is not None and not isinstance(wait_for_selector, str):
                raise ValueError("wait_for_selector must be a string or null")
            
            # 验证 wait_timeout 格式和范围
            if not isinstance(wait_timeout, int):
                raise ValueError("wait_timeout must be an integer")
            if wait_timeout < 0 or wait_timeout > 300000:  # 最大限制5分钟
                raise ValueError("wait_timeout must be between 0 and 300000 milliseconds")
            
            # 验证 URL 长度限制
            if len(url) > 2048:  # URL 长度限制
                raise ValueError("URL exceeds maximum length of 2048 characters")
            
            # 创建流式上下文
            ctx = StreamingContext()

            # 定义进度回调函数
            async def wrapped_progress_callback(msg: str):
                await ctx.send_output([TextContent(type="text", text=f"PROGRESS: {msg}")])

            browser_service = await get_browser_service()

            # 执行业务逻辑
            result = await browser_service.get_console_messages(
                url, wait_for_selector, wait_timeout,
                progress_callback=wrapped_progress_callback
            )
            
            # 验证结果格式
            if not isinstance(result, (dict, list, str)):
                raise ValueError("Result from get_console_messages is not in expected format")
            
            # 添加最终结果到输出
            await ctx.send_output([TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))])
            
            # 返回所有在执行过程中收集的输出
            return ctx.outputs
        
        except ValueError as e:
            # 处理值错误
            error_msg = f"Value Error in get_console_messages tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except TypeError as e:
            # 处理类型错误
            error_msg = f"Type Error in get_console_messages tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            # 处理其他异常
            error_msg = f"Unexpected error in get_console_messages tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    return MCPTool(tool=tool, handler=handler)