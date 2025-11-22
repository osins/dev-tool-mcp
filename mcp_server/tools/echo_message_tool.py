"""
Echo Message Tool - 回显消息工具
"""
import json
from typing import Callable, Awaitable

from mcp.types import Tool, TextContent
from mcp_server.mcp_tool import MCPTool


def create_echo_message_tool() -> MCPTool:
    """创建 EchoMessageTool 实例"""
    tool = Tool(
        name="echo_message",
        description="Echo tool that returns user-provided information as-is",
        inputSchema={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to echo back"
                }
            },
            "required": ["message"]
        }
    )

    async def handler(arguments: dict, progress_callback: Callable[[str], Awaitable[None]]) -> list:
        try:
            # 验证输入参数
            if not isinstance(arguments, dict):
                raise TypeError("Arguments must be a dictionary")
            
            # 从参数中提取并验证字段
            message = arguments.get("message", "")
            
            # 验证 message 参数
            if not isinstance(message, str):
                raise ValueError(f"Expected 'message' to be a string, got {type(message).__name__}")
            
            # 验证 message 长度限制
            if len(message) > 10000:  # 限制消息长度为10000字符
                raise ValueError("Message parameter exceeds maximum length of 10000 characters")
            
            # 执行业务逻辑
            result = message
            
            return [TextContent(type="text", text=result)]
        
        except ValueError as e:
            # 处理值错误
            error_msg = f"Value Error in echo_message tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except TypeError as e:
            # 处理类型错误
            error_msg = f"Type Error in echo_message tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            # 处理其他异常
            error_msg = f"Unexpected error in echo_message tool: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    return MCPTool(tool=tool, handler=handler)