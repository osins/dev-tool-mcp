from typing import Callable, Awaitable
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

class MCPTool:
    """
    精简并可生产部署的 MCP Tool 封装：
    - Tool 由调用方显式构建
    - MCPTool 自动验证 Tool 的合法性
    - handler 需要符合强类型签名
    """
    def __init__(
        self,
        tool: Tool,
        handler: Callable[
            [dict, Callable[[str], Awaitable[None]]],
            Awaitable[list[TextContent | ImageContent | EmbeddedResource]]
        ]
    ):
        if not isinstance(tool, Tool):
            raise TypeError("tool 必须是 mcp.types.Tool 的实例")
        
        if not callable(handler):
            raise TypeError("handler 必须是可调用对象")
        
        self.tool = tool
        self.handler = handler