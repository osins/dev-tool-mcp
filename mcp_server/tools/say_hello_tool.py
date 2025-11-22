"""
Say Hello Tool - 问候工具
"""
import json
from typing import Callable, Awaitable

from mcp.types import Tool, TextContent
from mcp_server.mcp_tool import MCPTool


def create_say_hello_tool() -> MCPTool:
    """创建 SayHelloTool 实例"""
    tool = Tool(
        name="say_hello",
        description="A simple greeting tool that returns personalized messages to users",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name to greet, defaults to World",
                    "default": "World"
                }
            },
            "required": []
        }
    )

    async def handler(arguments: dict, progress_callback: Callable[[str], Awaitable[None]]) -> list:
        try:
            # 验证输入参数
            if not isinstance(arguments, dict):
                raise TypeError("Arguments must be a dictionary")
            
            # 从参数中提取并验证字段
            name = arguments.get("name", "World")
            
            # 验证 name 参数
            if name is not None and not isinstance(name, str):
                raise ValueError(f"Expected 'name' to be a string, got {type(name).__name__}")
            
            # 验证 name 长度限制
            if name and len(name) > 100:
                raise ValueError("Name parameter exceeds maximum length of 100 characters")
            
            # 执行业务逻辑
            result = f"Hello, {name}!"
            
            return [TextContent(type="text", text=result)]
        
        except ValueError as e:
            # 处理值错误
            error_msg = f"Value Error in say_hello tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except TypeError as e:
            # 处理类型错误
            error_msg = f"Type Error in say_hello tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            # 处理其他异常
            error_msg = f"Unexpected error in say_hello tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    return MCPTool(tool=tool, handler=handler)