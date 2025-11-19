#!/usr/bin/env python3
"""
Spider MCP 客户端快速开始示例
最简单的使用方式
"""

import asyncio
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置服务器连接参数（请根据实际路径调整）
PROJECT_ROOT = Path(__file__).parent.parent
SERVER_PARAMS = StdioServerParameters(
    command=str(PROJECT_ROOT / "venv" / "bin" / "python"),
    args=[str(PROJECT_ROOT / "spider_mcp_server" / "server.py")]
)

async def crawl_webpage_simple():
    """简单的网页爬取示例"""
    print("🕷️ 开始爬取网页...")
    
    # 创建输出目录
    output_dir = "./simple_output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 连接到MCP服务器
        async with stdio_client(SERVER_PARAMS) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化会话
                await session.initialize()
                
                # 调用爬虫工具
                result = await session.call_tool("crawl_web_page", {
                    "url": "https://github.com/unclecode/crawl4ai",
                    "save_path": output_dir
                })
                
                # ✅ 正确处理返回结果
                # MCP服务器返回的是 CallToolResult 对象，内容在 result.content 中
                for content in result.content:
                    if content.type == "text":
                        print(f"✅ 爬取结果: {content.text}")
                
    except Exception as e:
        print(f"❌ 爬取失败: {e}")

if __name__ == "__main__":
    asyncio.run(crawl_webpage_simple())