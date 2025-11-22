# MCP 开发工具服务器

基于 [crawl4ai](https://github.com/unclecode/crawl4ai) 和 Playwright 的 MCP (Model Context Protocol) 开发工具服务器，提供强大的网络爬取、内容提取和浏览器自动化功能。

## 🚀 特性

- **智能网络爬虫**: 基于 crawl4ai 的高效网页内容提取
- **LLM 增强提取**: 集成大语言模型，支持智能内容理解和结构化提取
- **多格式输出**: 支持 HTML、Markdown、JSON、PDF 和 PNG 格式
- **智能内容提取**: 使用 LLMExtractionStrategy 进行基于语义的内容提取
- **灵活配置**: 支持传统 CSS 选择器提取和 LLM 智能提取两种模式
- **截图功能**: 自动生成网页截图
- **PDF 导出**: 将网页内容导出为 PDF 文件
- **内容过滤**: 使用 PruningContentFilter 优化内容提取
- **结构化数据提取**: 支持 JsonCssExtractionStrategy 精确数据提取
- **文件下载**: 自动下载并保存引用文件
- **多模型支持**: 支持 Ollama、OpenAI、Claude 等多种 LLM 提供商
- **环境变量配置**: 灵活的模型配置和切换机制
- **MCP 协议支持**: 完全兼容 MCP 标准，可集成到支持 MCP 的客户端
- **浏览器自动化**: Playwright 驱动的高级浏览器功能
- **页面内容分析**: 获取完整的 HTML、文本、元数据、链接和图片
- **控制台消息捕获**: 监控 JavaScript 日志、警告和错误
- **网络请求跟踪**: 记录页面发起的所有网络请求和响应
- **实时流式处理**: 实时流式处理状态和中间结果

## 📦 安装

### 环境要求

- Python 3.8+
- 推荐使用虚拟环境
- **LLM 依赖项**:
  - `litellm` - 统一的多模型 LLM 接口
  - Ollama 或其他 LLM 提供商（可选，用于智能内容提取）
- **浏览器依赖项**:
  - Chrome/Chromium（crawl4ai 需要）
  - Playwright（自动安装）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/osins/dev-tool-mcp.git
cd dev-tool-mcp
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -e .
```

## 🔧 MCP 服务配置

### Claude Desktop 配置示例

将以下配置添加到 Claude Desktop 的配置文件中：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "dev-tool": {
      "command": "/path/to/dev-tool-mcp/venv/bin/python",
      "args": [
        "/path/to/dev-tool-mcp/mcp_server/server.py"
      ],
      "description": "使用 crawl4ai 进行网页爬取和内容提取的 MCP 开发工具服务器"
    }
  }
}
```

### 通用 MCP 客户端配置

如果使用其他 MCP 客户端，可使用以下通用配置：

```json
{
  "servers": {
    "dev-tool-crawler": {
      "name": "开发工具爬取服务器",
      "description": "网页爬取和内容提取服务器",
      "command": "/path/to/dev-tool-mcp/venv/bin/python",
      "args": [
        "/path/to/dev-tool-mcp/mcp_server/server.py"
      ],
      "timeout": 30000
    }
  }
}
```

### 📋 配置说明

**直接脚本执行即可:**
- 无需环境变量
- 无需使用 `-m` 参数
- Python 自动处理相对导入
- 最简单最可靠的配置

### 🤖 LLM 配置选项

为启用 LLM 增强功能，可设置以下环境变量：

```bash
# 启用 LLM 模式
export CRAWL_MODE=llm

# LLM 提供商配置
export LLAMA_PROVIDER="ollama/qwen2.5-coder:latest"  # 默认值
export LLAMA_API_TOKEN="your_api_token"             # 可选，某些提供商需要
export LLAMA_BASE_URL="http://localhost:11434"       # 可选，自定义 API 端点
export LLAMA_MAX_TOKENS=4096                         # 可选，最大 token 数
```

**支持的 LLM 提供商:**
- **Ollama**: `ollama/model-name` (本地部署)
- **OpenAI**: `openai/gpt-4` / `openai/gpt-3.5-turbo`
- **Claude**: `anthropic/claude-3-sonnet`
- **其他**: 通过 litellm 支持的所有提供商

## 🛠️ MCP 协议使用指南

### 基于 MCP 协议的客户端开发

此项目基于 [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) 协议，提供标准化工具调用接口。编写 MCP 客户端的关键要点如下：

#### 1. MCP 连接建立

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置服务器参数
server_params = StdioServerParameters(
    command="/path/to/venv/bin/python",  # Python 解释器路径
    args=["/path/to/server.py"]         # 服务器脚本路径
)

# 建立 stdio 连接
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()  # 初始化会话
```

#### 2. 工具调用和结果处理

**⚠️ 重要: MCP 返回值结构**

MCP 服务器返回 `CallToolResult` 对象，实际内容在 `result.content` 中：

```python
# ❌ 错误方法（常见错误）
for content in result:  # result 不可迭代
    print(content.text)

# ✅ 正确方法
result = await session.call_tool("tool_name", {"param": "value"})
for content in result.content:  # 访问 content 属性
    if content.type == "text":  # 检查内容类型
        print(content.text)
```

#### 3. 此项目可用的工具接口

**可用工具:**
- `say_hello` - 测试连通性
- `echo_message` - 回显消息
- `crawl_web_page` - 网页爬取
- `get_page_content` - 通过 URL 获取页面内容
- `get_console_messages` - 获取页面控制台消息
- `get_network_requests` - 获取页面发起的网络请求

**crawl_web_page 工具参数:**
```python
{
    "url": "https://example.com",           # 要爬取的 URL
    "save_path": "./output_directory"       # 保存路径
}
```

**返回值处理:**
```python
result = await session.call_tool("crawl_web_page", {
    "url": "https://github.com/unclecode/crawl4ai",
    "save_path": "./results"
})

# 正确解析返回结果
for content in result.content:
    if content.type == "text":
        message = content.text
        print(f"爬取结果: {message}")

        # 消息格式示例:
        # "Successfully crawled https://github.com/unclecode/crawl4ai and saved 8 files to ./results/20231119-143022"
```

#### 4. 错误处理最佳实践

```python
async def safe_crawl(session: ClientSession, url: str, save_path: str):
    try:
        result = await session.call_tool("crawl_web_page", {
            "url": url,
            "save_path": save_path
        })

        # 检查返回结果
        if result.content:
            for content in result.content:
                if content.type == "text":
                    if "Failed to crawl" in content.text:
                        print(f"❌ 爬取失败: {content.text}")
                    else:
                        print(f"✅ 爬取成功: {content.text}")
        else:
            print("❌ 未收到返回结果")

    except Exception as e:
        print(f"❌ 工具调用失败: {e}")
```

## 🛠️ 可用工具

### 1. `crawl_web_page`

从指定 URL 爬取网页内容，并以多种格式保存。支持传统 CSS 提取和 LLM 增强提取模式。

**参数:**
- `url` (string, required): 要爬取的网页 URL
- `save_path` (string, required): 保存爬取内容的目录路径
- `instruction` (string, optional): 用于 LLM 的指令 (默认: DEFAULT_INSTRUCTION)
- `save_screenshot` (boolean, optional): 保存页面截图 (默认: False)
- `save_pdf` (boolean, optional): 保存页面 PDF (默认: False)
- `generate_markdown` (boolean, optional): 生成页面 Markdown 表示 (默认: False)

**功能:**
- 自动网页截图 (PNG)
- PDF 导出生成
- 原始 Markdown 内容提取
- 清洁/过滤的 Markdown 内容
- 结构化数据提取 (JSON)
- HTML 内容保存
- 下载文件处理
- **LLM 智能提取** (当设置 CRAWL_MODE=llm 时启用):
  - 基于语义的内容理解
  - 自动去除导航、广告等非主要内容
  - 结构化的 Markdown 输出
  - 支持多种 LLM 提供商

**示例用法:**
```python
# 传统爬取模式
result = await session.call_tool("crawl_web_page", {
    "url": "https://example.com",
    "save_path": "./output_directory"
})

# LLM 增强模式 (设置环境变量)
os.environ["CRAWL_MODE"] = "llm"
os.environ["LLAMA_PROVIDER"] = "ollama/qwen2.5-coder:latest"
os.environ["LLAMA_BASE_URL"] = "http://localhost:11434"
```

### 2. `get_page_content`

通过 URL 获取网页内容并实时分析。

**参数:**
- `url` (string, required): 要获取内容的网页 URL
- `wait_for_selector` (string, optional): 获取内容前等待特定元素的 CSS 选择器
- `wait_timeout` (integer, optional): 等待超时时间（毫秒），默认 30000

**返回:**
包含以下字段的 JSON 对象：
- `url`: 请求的 URL
- `status`: HTTP 状态码
- `title`: 页面标题
- `html`: 页面 HTML 内容
- `text`: 页面文本内容
- `meta`: 页面元数据
- `links`: 页面链接列表
- `images`: 页面图片列表
- `timestamp`: 操作时间戳

### 3. `get_console_messages`

通过 URL 从网页获取控制台消息 (日志、警告、错误)。

**参数:**
- `url` (string, required): 要获取控制台消息的网页 URL
- `wait_for_selector` (string, optional): 获取控制台消息前等待特定元素的 CSS 选择器
- `wait_timeout` (integer, optional): 等待超时时间（毫秒），默认 30000

**返回:**
包含以下字段的 JSON 对象：
- `url`: 请求的 URL
- `status`: HTTP 状态码
- `console_messages`: 控制台消息列表，每条消息包含类型、文本、位置和堆栈信息
- `timestamp`: 操作时间戳

### 4. `get_network_requests`

通过 URL 获取页面发起的网络请求。

**参数:**
- `url` (string, required): 要获取网络请求的网页 URL
- `wait_for_selector` (string, optional): 获取网络请求前等待特定元素的 CSS 选择器
- `wait_timeout` (integer, optional): 等待超时时间（毫秒），默认 30000

**返回:**
包含以下字段的 JSON 对象：
- `url`: 请求的 URL
- `status`: HTTP 状态码
- `requests`: 请求列表，每个请求包含 URL、方法、资源类型等信息
- `responses`: 响应列表，每个响应包含 URL、状态码、头信息等
- `total_requests`: 总请求数
- `total_responses`: 总响应数
- `timestamp`: 操作时间戳

### 5. `say_hello`

用于测试服务器连通性的简单问候工具。

**参数:**
- `name` (string, optional): 要问候的名字，默认为 "World"

**示例用法:**
```python
result = await session.call_tool("say_hello", {
    "name": "Alice"
})
```

### 6. `echo_message`

用于测试通信的回显消息工具。

**参数:**
- `message` (string, required): 要回显的消息

**示例用法:**
```python
result = await session.call_tool("echo_message", {
    "message": "Hello MCP!"
})
```

## 📁 输出文件结构

爬取完成后，将在指定的输出目录中生成以下文件：

```
output_directory/
├── output.html              # 完整 HTML 内容
├── output.json              # 结构化数据 (CSS 提取的 JSON)
├── output.png               # 网页截图
├── output.pdf               # 网页的 PDF 版本
├── raw_markdown.md          # 原始 markdown 提取
├── fit_markdown.md          # 清洁/过滤的 markdown
├── downloaded_files.json    # 下载文件列表 (如有)
└── files/                   # 下载文件目录 (如有)
```

## 🔍 使用示例

### 基本网页爬取

```python
import asyncio
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def crawl_example():
    # 配置服务器连接参数 (根据需要调整路径)
    project_root = Path("/path/to/your/dev-tool-mcp")
    server_params = StdioServerParameters(
        command=str(project_root / "venv" / "bin" / "python"),
        args=[str(project_root / "mcp_server" / "server.py")]
    )

    # 创建输出目录
    output_dir = "./crawl_results"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # 连接 MCP 服务器
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化会话
                await session.initialize()

                # 调用爬取工具
                result = await session.call_tool("crawl_web_page", {
                    "url": "https://github.com/unclecode/crawl4ai",
                    "save_path": output_dir
                })

                # ✅ 正确的返回值处理
                # MCP 服务器返回 CallToolResult 对象，内容在 result.content 中
                for content in result.content:
                    if content.type == "text":
                        print(f"✅ 爬取结果: {content.text}")

    except Exception as e:
        print(f"❌ 爬取失败: {e}")

# 运行示例
asyncio.run(crawl_example())
```

### 浏览器内容分析

```python
# 获取完整页面内容
result = await session.call_tool("get_page_content", {
    "url": "https://nextjs.org",
    "wait_for_selector": "main",
    "wait_timeout": 15000
})

# 获取控制台消息 (检测 JavaScript 错误很有用)
console_result = await session.call_tool("get_console_messages", {
    "url": "https://example.com",
    "wait_for_selector": ".app-loaded",
    "wait_timeout": 10000
})

# 获取网络请求 (API 跟踪很有用)
network_result = await session.call_tool("get_network_requests", {
    "url": "https://api.example.com",
    "wait_for_selector": "[data-loaded=true]",
    "wait_timeout": 20000
})
```

### 批量爬取多个网页

```python
urls = [
    "https://example.com",
    "https://github.com",
    "https://stackoverflow.com"
]

for i, url in enumerate(urls):
    result = await session.call_tool("crawl_web_page", {
        "url": url,
        "save_path": f"./results/crawl_{i+1}"
    })

    # ✅ 正确的返回值处理
    for content in result.content:
        if content.type == "text":
            print(f"爬取完成: {url} - {content.text}")

    # 添加延迟以避免过于频繁的请求
    await asyncio.sleep(2)
```

### LLM 增强爬取示例

```python
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def llm_enhanced_crawl():
    # 配置 LLM 环境变量
    os.environ["CRAWL_MODE"] = "llm"
    os.environ["LLAMA_PROVIDER"] = "ollama/qwen2.5-coder:latest"
    os.environ["LLAMA_BASE_URL"] = "http://localhost:11434"

    # 配置服务器连接
    server_params = StdioServerParameters(
        command="/path/to/venv/bin/python",
        args=["/path/to/mcp_server/server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # LLM 增强爬取
            result = await session.call_tool("crawl_web_page", {
                "url": "https://example.com/article",
                "save_path": "./llm_results"
            })

            for content in result.content:
                if content.type == "text":
                    print(f"LLM 增强爬取结果: {content.text}")

asyncio.run(llm_enhanced_crawl())
```

## 🧪 开发和测试

### 运行测试

项目包含全面的测试套件：

```bash
# 运行完整爬虫测试，带真实文件输出
python test/test_complete_crawler.py

# 运行单个组件测试
python test/test_hello.py      # 测试 hello/echo 功能
python test/test_server.py     # 测试 MCP 服务器功能
python test/test_crawl.py      # 测试爬取功能
python test/test_complete.py    # 测试完整工作流程
python test/test_browser.py     # 测试浏览器自动化功能
```

### 测试目录结构

```
test/
├── test_complete_crawler.py    # 完整集成测试
├── test_hello.py             # Hello/echo 功能
├── test_server.py            # MCP 服务器协议
├── test_crawl.py             # 核心爬取逻辑
├── test_browser.py           # 浏览器自动化测试
└── test_complete.py          # 端到端工作流程
```

### 开发模式

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 项目使用 pyright 进行类型检查 (在 pyproject.toml 中配置)
# 未配置其他 linting 工具
```

## 📚 项目结构

```
dev-tool-mcp/
├── mcp_server/          # 主包
│   ├── __init__.py            # 包初始化
│   ├── server.py              # MCP 服务器实现
│   ├── crawl.py              # 爬取逻辑和文件处理
│   ├── llm.py                # LLM 配置和提取策略
│   ├── browser/              # 浏览器自动化模块
│   │   ├── __init__.py       # 浏览器模块初始化
│   │   ├── browser_service.py # 浏览器服务实现
│   │   └── README.md         # 浏览器模块文档
│   └── utils.py              # 文件 I/O 实用函数
├── test/                     # 测试套件
│   ├── test_litellm_ollama.py # LLM 集成测试
│   ├── test_browser.py       # 浏览器功能测试
│   └── ...                   # 其他测试文件
├── test_output/              # 测试输出目录
├── typings/                  # crawl4ai 的类型存根
├── pyproject.toml            # 项目配置
└── README.md                # 此文件
```

## 📚 API 参考

### 核心类和函数

#### `llm_config()` 函数 (`llm.py`)
配置 LLM 增强爬取策略。

**参数:**
- `instruction` (str): 提取指令，默认为专门优化的网页内容提取指令

**返回:**
- `CrawlerRunConfig`: 配置了 LLM 提取策略的爬取配置

**特性:**
- 支持 litellm 的所有提供商
- 自动分块处理大型内容
- 智能内容过滤和结构化输出
- 可配置的温度和 token 参数

#### `save()` 函数 (`utils.py`)
使用适当编码处理将内容保存到文件。

**参数:**
- `path`: 目录路径
- `name`: 文件名
- `s`: 内容 (字符串、字节或字节数组)
- `call`: 附有保存文件路径的回调函數

#### `saveJson()` 函数 (`crawl.py`)
异步函數，用于保存下载的文件信息并处理文件下载。

**功能:**
- 保存 `downloaded_files.json` 和文件元数据
- 将引用的文件下载并保存到 `files/` 子目录
- 失败下载的错误处理

#### `crawl_config()` 函数 (`crawl.py`)
动态选择爬取配置，根据环境变量决定是否启用 LLM 模式。

**环境变量:**
- `CRAWL_MODE=llm`: 启用 LLM 增强提取
- 其他值: 使用传统 CSS 选择器提取

### 浏览器服务函数

#### `get_page_content()` (`browser_service.py`)
获取包含 HTML、文本、元数据、链接和图片的完整页面内容。

**参数:**
- `url` (string, required): 目标页面 URL
- `wait_for_selector` (string, optional): 获取内容前等待特定元素
- `wait_timeout` (int, optional): 等待超时时间（毫秒）(默认 30000)
- `progress_callback` (callable, optional): 可选进度回调

#### `get_console_messages()` (`browser_service.py`)
捕获来自网页的控制台消息 (日志、警告、错误)。

**参数:**
- `url` (string, required): 目标页面 URL
- `wait_for_selector` (string, optional): 获取控制台消息前等待特定元素
- `wait_timeout` (int, optional): 等待超时时间（毫秒）(默认 30000)
- `progress_callback` (callable, optional): 可选进度回调

#### `get_network_requests()` (`browser_service.py`)
记录由网页发起的所有网络请求和响应。

**参数:**
- `url` (string, required): 目标页面 URL
- `wait_for_selector` (string, optional): 获取网络请求前等待特定元素
- `wait_timeout` (int, optional): 等待超时时间（毫秒）(默认 30000)
- `progress_callback` (callable, optional): 可选进度回调

## 🎯 配置说明

### LLM 提取策略

启用 LLM 模式时，使用以下智能提取配置：

**默认提取指令:**
```
You are a **Web Content Extraction Assistant**. Your task is to extract the **complete, clean, and precise main text content** from a given web page...
```

**LLM 配置参数:**
- `provider`: 通过 `LLAMA_PROVIDER` 环境变量配置
- `api_token`: 通过 `LLAMA_API_TOKEN` 环境变量配置
- `base_url`: 通过 `LLAMA_BASE_URL` 环境变量配置
- `max_tokens`: 默认 4096，可通过 `LLAMA_MAX_TOKENS` 调整
- `temperature`: 0.1 (确保输出稳定性)
- `chunk_token_threshold`: 1400 (分块处理阈值)
- `apply_chunking`: true (启用内容分块)

### CSS 提取策略

传统模式使用预配置的 CSS 提取模式：

```javascript
{
  "baseSelector": "body",
  "fields": [
    {"name": "title", "selector": "h2", "type": "text"},
    {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"},
    {"name": "p", "selector": "p", "type": "text"}
  ]
}
```

### 内容过滤

使用 `PruningContentFilter` 配置：
- `threshold`: 0.35 (动态阈值)
- `min_word_threshold`: 3
- `threshold_type`: "dynamic"

### 浏览器配置

- 无头模式启用
- JavaScript 启用
- 绕过缓存获取新内容
- Playwright 驱动的自动化
- 实时内容监控

## ⚠️ 重要注意事项

1. **频率限制**: 请合理控制爬取频率，避免对目标网站造成过度压力
2. **robots.txt**: 请遵守目标网站的 robots.txt 规则
3. **法律合规**: 确保爬取行为符合相关法律、法规和网站条款
4. **浏览器要求**: crawl4ai 要求在系统上安装浏览器引擎 (Chrome/Chromium)
5. **内存使用**: 大型截图和 PDF 可能会消耗大量内存和磁盘空间
6. **安全性**: URL 验证防止访问 localhost 和内网地址
7. **流式处理**: 长操作期间实时流式传输进度更新

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

此项目使用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- [crawl4ai 官方文档](https://github.com/unclecode/crawl4ai)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Claude Desktop 文档](https://docs.anthropic.com/claude/docs/overview)
- [LiteLLM 文档](https://docs.litellm.ai/)
- [Ollama 文档](https://github.com/ollama/ollama)
- [Playwright 文档](https://playwright.dev/)
- [项目包](https://pypi.org/project/dev-tool-mcp/)

## 📞 支持

如果遇到问题或有建议：

1. **检查 Issues**: [GitHub Issues](https://github.com/osins/dev-tool-mcp/issues)
2. **创建新 Issue**: 报告错误或请求功能
3. **先测试**: 运行 `python test/test_complete_crawler.py` 以验证设置

## 🎮 CLI 入口点

包包含一个 CLI 入口点：

```bash
# 安装后
dev-tool-mcp
```

这相当于运行：
```bash
python -m mcp_server.server
```

## 🛠️ 可用工具

---

**使用 crawl4ai、Playwright 和 MCP 制作 ❤️**

*当前版本: 0.1.0*