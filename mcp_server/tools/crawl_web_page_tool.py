"""
Crawl Web Page Tool - 爬取网页工具
"""
import json
from typing import Callable, Awaitable

from mcp.types import Tool, TextContent
from mcp_server.mcp_tool import MCPTool
from mcp_server.crawl.crawl import crawl_web_page, DEFAULT_INSTRUCTION


class StreamingContext:
    """Streaming context for sending progress updates."""
    
    def __init__(self):
        self.outputs = []

    async def send_output(self, content):
        """Send output to the client."""
        self.outputs.extend(content)


def create_crawl_web_page_tool() -> MCPTool:
    """创建 CrawlWebPageTool 实例"""
    tool = Tool(
        name="crawl_web_page",
        description="Crawl web page content and save in multiple formats (HTML, JSON, PDF, screenshots) while downloading file resources from the page",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the web page to crawl"
                },
                "save_path": {
                    "type": "string",
                    "description": "The base file path to save the crawled content and downloaded files"
                },
                "instruction": {
                    "type": "string",
                    "description": "The instruction to use for the LLM"
                },
                "save_screenshot": {
                    "type": "boolean",
                    "description": "Save a screenshot of the page",
                    "default": False
                },
                "save_pdf": {
                    "type": "boolean",
                    "description": "Save a PDF of the page",
                    "default": False
                },
                "generate_markdown": {
                    "type": "boolean",
                    "description": "Generate a Markdown representation of the page",
                    "default": False
                }
            },
            "required": ["url", "save_path"]
        }
    )

    async def handler(arguments: dict, progress_callback: Callable[[str], Awaitable[None]]) -> list:
        try:
            # 验证输入参数
            if not isinstance(arguments, dict):
                raise TypeError("Arguments must be a dictionary")
            
            # 从参数中提取并验证字段
            url = arguments.get("url", "")
            save_path = arguments.get("save_path", "")
            instruction = arguments.get("instruction", DEFAULT_INSTRUCTION)
            save_screenshot = arguments.get("save_screenshot", False)
            save_pdf = arguments.get("save_pdf", False)
            generate_markdown = arguments.get("generate_markdown", False)
            
            # 验证必需参数
            if not url:
                raise ValueError("URL is required")
            if not save_path:
                raise ValueError("Save path is required")
            
            # 验证 URL 格式
            if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
                raise ValueError("Invalid URL format")
            
            # 验证 save_path 格式
            if not isinstance(save_path, str) or len(save_path) == 0:
                raise ValueError("Invalid save path format")
            
            # 验证布尔参数
            if not isinstance(save_screenshot, bool):
                raise ValueError("save_screenshot must be a boolean")
            if not isinstance(save_pdf, bool):
                raise ValueError("save_pdf must be a boolean")
            if not isinstance(generate_markdown, bool):
                raise ValueError("generate_markdown must be a boolean")
            
            # 验证 instruction 格式
            if not isinstance(instruction, str):
                raise ValueError("instruction must be a string")
            
            # 验证 URL 和 save_path 长度限制
            if len(url) > 2048:  # URL 长度限制
                raise ValueError("URL exceeds maximum length of 2048 characters")
            if len(save_path) > 4096:  # 路径长度限制
                raise ValueError("Save path exceeds maximum length of 4096 characters")
            
            # 创建流式上下文
            ctx = StreamingContext()

            # 定义进度回调函数
            async def wrapped_progress_callback(msg: str):
                await ctx.send_output([TextContent(type="text", text=f"PROGRESS: {msg}")])

            # 执行业务逻辑
            result = await crawl_web_page(
                url, save_path, instruction, save_screenshot,
                save_pdf, generate_markdown, progress_callback=wrapped_progress_callback
            )
            
            # 添加最终结果到输出
            await ctx.send_output([TextContent(type="text", text=result)])
            
            # 返回所有在执行过程中收集的输出
            return ctx.outputs
        
        except ValueError as e:
            # 处理值错误
            error_msg = f"Value Error in crawl_web_page tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except TypeError as e:
            # 处理类型错误
            error_msg = f"Type Error in crawl_web_page tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            # 处理其他异常
            error_msg = f"Unexpected error in crawl_web_page tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    return MCPTool(tool=tool, handler=handler)