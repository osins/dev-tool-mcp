# MCP Dev Tool Server

An MCP (Model Context Protocol) development tool server based on [crawl4ai](https://github.com/unclecode/crawl4ai) and Playwright that provides powerful web crawling, content extraction, and browser automation capabilities.

## 🚀 Features

- **Intelligent Web Crawling**: Efficient web content extraction based on crawl4ai
- **LLM Enhanced Extraction**: Integrated large language models for intelligent content understanding and structured extraction
- **Multi-Format Output**: Supports HTML, Markdown, JSON, PDF, and PNG formats
- **Smart Content Extraction**: Uses LLMExtractionStrategy for semantic content extraction
- **Flexible Configuration**: Supports both traditional CSS selector extraction and LLM intelligent extraction modes
- **Screenshot Generation**: Automatically generates webpage screenshots
- **PDF Export**: Exports webpage content to PDF format
- **Content Filtering**: Uses PruningContentFilter to optimize content extraction
- **Structured Data Extraction**: Supports JsonCssExtractionStrategy for precise data extraction
- **File Downloading**: Automatically downloads and saves referenced files
- **Multi-Model Support**: Supports Ollama, OpenAI, Claude and other LLM providers
- **Environment Variable Configuration**: Flexible model configuration and switching mechanisms
- **MCP Protocol Compliant**: Full compatibility with MCP standards, integrable with MCP-enabled clients
- **Browser Automation**: Advanced browser capabilities powered by Playwright
- **Page Content Analysis**: Get complete HTML, text, metadata, links, and images
- **Console Message Capture**: Monitor JavaScript logs, warnings, and errors
- **Network Request Tracking**: Record all network requests and responses made by pages
- **Real-time Streaming**: Stream processing status and intermediate results

## 📦 Installation

### Requirements

- Python 3.8+
- Virtual environment recommended
- **LLM Dependencies**:
  - `litellm` - Unified multi-model LLM interface
  - Ollama or other LLM providers (optional, for intelligent content extraction)
- **Browser Dependencies**:
  - Chrome/Chromium (crawl4ai requires it)
  - Playwright (automatically installed)

### Installation Steps

1. **Clone repository**
```bash
git clone https://github.com/osins/dev-tool-mcp.git
cd dev-tool-mcp
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -e .
```

## 🔧 MCP Service Configuration

### Claude Desktop Configuration Example

Add the following configuration to Claude Desktop's configuration file:

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
      "description": "MCP development tool server using crawl4ai for web crawling and content extraction"
    }
  }
}
```

### General MCP Client Configuration

If you use other MCP clients, you can use the following general configuration:

```json
{
  "servers": {
    "dev-tool-crawler": {
      "name": "Dev Tool Crawler Server",
      "description": "Web crawling and content extraction server",
      "command": "/path/to/dev-tool-mcp/venv/bin/python",
      "args": [
        "/path/to/dev-tool-mcp/mcp_server/server.py"
      ],
      "timeout": 30000
    }
  }
}
```

### 📋 Configuration Notes

**Direct script execution is all you need:**
- No environment variables needed
- No need to use `-m` parameter
- Python automatically handles relative imports
- Most simple and reliable configuration

### 🤖 LLM Configuration Options

To enable LLM enhancement features, set the following environment variables:

```bash
# Enable LLM mode
export CRAWL_MODE=llm

# LLM Provider Configuration
export LLAMA_PROVIDER="ollama/qwen2.5-coder:latest"  # Default value
export LLAMA_API_TOKEN="your_api_token"             # Optional, required by some providers
export LLAMA_BASE_URL="http://localhost:11434"       # Optional, custom API endpoint
export LLAMA_MAX_TOKENS=4096                         # Optional, max tokens
```

**Supported LLM Providers:**
- **Ollama**: `ollama/model-name` (local deployment)
- **OpenAI**: `openai/gpt-4` / `openai/gpt-3.5-turbo`
- **Claude**: `anthropic/claude-3-sonnet`
- **Other**: All providers supported via litellm

## 🛠️ MCP Protocol Usage Guide

### Client Development Based on MCP Protocol

This project is based on the [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) protocol and provides standardized tool call interfaces. Here are the key points for writing MCP clients:

#### 1. MCP Connection Establishment

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure server parameters
server_params = StdioServerParameters(
    command="/path/to/venv/bin/python",  # Python interpreter path
    args=["/path/to/server.py"]         # Server script path
)

# Establish stdio connection
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()  # Initialize session
```

#### 2. Tool Calls and Result Handling

**⚠️ Important: MCP Return Value Structure**

The MCP server returns a `CallToolResult` object, with the actual content in `result.content`:

```python
# ❌ Incorrect approach (common error)
for content in result:  # result is not iterable
    print(content.text)

# ✅ Correct approach
result = await session.call_tool("tool_name", {"param": "value"})
for content in result.content:  # Access content attribute
    if content.type == "text":  # Check content type
        print(content.text)
```

#### 3. Tool Interfaces for This Project

**Available Tools:**
- `say_hello` - Test connection
- `echo_message` - Echo message
- `crawl_web_page` - Web page crawling
- `get_page_content` - Get page content by URL
- `get_console_messages` - Get console messages from page
- `get_network_requests` - Get network requests made by page

**crawl_web_page Tool Parameters:**
```python
{
    "url": "https://example.com",           # URL to crawl
    "save_path": "./output_directory"       # Save path
}
```

**Return Value Handling:**
```python
result = await session.call_tool("crawl_web_page", {
    "url": "https://github.com/unclecode/crawl4ai",
    "save_path": "./results"
})

# Parse return results correctly
for content in result.content:
    if content.type == "text":
        message = content.text
        print(f"Crawling result: {message}")

        # Message format example:
        # "Successfully crawled https://github.com/unclecode/crawl4ai and saved 8 files to ./results/20231119-143022"
```

#### 4. Error Handling Best Practices

```python
async def safe_crawl(session: ClientSession, url: str, save_path: str):
    try:
        result = await session.call_tool("crawl_web_page", {
            "url": url,
            "save_path": save_path
        })

        # Check return results
        if result.content:
            for content in result.content:
                if content.type == "text":
                    if "Failed to crawl" in content.text:
                        print(f"❌ Crawling failed: {content.text}")
                    else:
                        print(f"✅ Crawling successful: {content.text}")
        else:
            print("❌ No return result received")

    except Exception as e:
        print(f"❌ Tool call failed: {e}")
```

## 🛠️ Available Tools

### 1. `crawl_web_page`

Crawl webpage content from the specified URL and save in multiple formats. Supports both traditional CSS extraction and LLM-enhanced extraction modes.

**Parameters:**
- `url` (string, required): The webpage URL to crawl
- `save_path` (string, required): The directory path to save crawled content
- `instruction` (string, optional): The instruction to use for the LLM (default: DEFAULT_INSTRUCTION)
- `save_screenshot` (boolean, optional): Save a screenshot of the page (default: False)
- `save_pdf` (boolean, optional): Save a PDF of the page (default: False)
- `generate_markdown` (boolean, optional): Generate a Markdown representation of the page (default: False)

**Features:**
- Automatic webpage screenshot (PNG)
- PDF export generation
- Raw Markdown content extraction
- Cleaned/filtered Markdown content
- Structured data extraction (JSON)
- HTML content preservation
- Downloaded files processing
- **LLM Intelligent Extraction** (enabled when CRAWL_MODE=llm is set):
  - Semantic content understanding
  - Automatic removal of navigation, ads and other non-main content
  - Structured Markdown output
  - Support for multiple LLM providers

**Example usage:**
```python
# Traditional crawling mode
result = await session.call_tool("crawl_web_page", {
    "url": "https://example.com",
    "save_path": "./output_directory"
})

# LLM enhanced mode (set environment variables)
os.environ["CRAWL_MODE"] = "llm"
os.environ["LLAMA_PROVIDER"] = "ollama/qwen2.5-coder:latest"
os.environ["LLAMA_BASE_URL"] = "http://localhost:11434"
```

### 2. `get_page_content`

Get the content of a web page by URL and analyze it in real-time.

**Parameters:**
- `url` (string, required): The URL of the web page to get content from
- `wait_for_selector` (string, optional): Optional CSS selector to wait for before getting content
- `wait_timeout` (integer, optional): Wait timeout in milliseconds, default 30000

**Returns:**
JSON object containing:
- `url`: Requested URL
- `status`: HTTP status code
- `title`: Page title
- `html`: Page HTML content
- `text`: Page text content
- `meta`: Page metadata
- `links`: Page link list
- `images`: Page image list
- `timestamp`: Operation timestamp

### 3. `get_console_messages`

Get console messages from a web page by URL (logs, warnings, errors).

**Parameters:**
- `url` (string, required): The URL of the web page to get console messages from
- `wait_for_selector` (string, optional): Optional CSS selector to wait for before getting console messages
- `wait_timeout` (integer, optional): Wait timeout in milliseconds, default 30000

**Returns:**
JSON object containing:
- `url`: Requested URL
- `status`: HTTP status code
- `console_messages`: List of console messages, each containing type, text, location and stack info
- `timestamp`: Operation timestamp

### 4. `get_network_requests`

Get network requests made by a web page by URL.

**Parameters:**
- `url` (string, required): The URL of the web page to get network requests from
- `wait_for_selector` (string, optional): Optional CSS selector to wait for before getting network requests
- `wait_timeout` (integer, optional): Wait timeout in milliseconds, default 30000

**Returns:**
JSON object containing:
- `url`: Requested URL
- `status`: HTTP status code
- `requests`: Request list, each request contains URL, method, resource type, etc.
- `responses`: Response list, each response contains URL, status code, header info, etc.
- `total_requests`: Total request count
- `total_responses`: Total response count
- `timestamp`: Operation timestamp

### 5. `say_hello`

Simple greeting tool for testing server connectivity.

**Parameters:**
- `name` (string, optional): Name to greet, defaults to "World"

**Example usage:**
```python
result = await session.call_tool("say_hello", {
    "name": "Alice"
})
```

### 6. `echo_message`

Echo messages back to test communication.

**Parameters:**
- `message` (string, required): The message to echo

**Example usage:**
```python
result = await session.call_tool("echo_message", {
    "message": "Hello MCP!"
})
```

## 📁 Output File Structure

After crawling, the following files will be generated in the specified output directory:

```
output_directory/
├── output.html              # Complete HTML content
├── output.json              # Structured data (CSS-extracted JSON)
├── output.png               # Webpage screenshot
├── output.pdf               # PDF version of the page
├── raw_markdown.md          # Raw markdown extraction
├── fit_markdown.md          # Cleaned/filtered markdown
├── downloaded_files.json    # List of downloaded files (if any)
└── files/                   # Downloaded files directory (if any)
```

## 🔍 Usage Examples

### Basic Web Crawling

```python
import asyncio
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def crawl_example():
    # Configure server connection parameters (adjust paths as needed)
    project_root = Path("/path/to/your/dev-tool-mcp")
    server_params = StdioServerParameters(
        command=str(project_root / "venv" / "bin" / "python"),
        args=[str(project_root / "mcp_server" / "server.py")]
    )

    # Create output directory
    output_dir = "./crawl_results"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Connect to MCP server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize session
                await session.initialize()

                # Call crawling tool
                result = await session.call_tool("crawl_web_page", {
                    "url": "https://github.com/unclecode/crawl4ai",
                    "save_path": output_dir
                })

                # ✅ Correct return value handling
                # MCP server returns CallToolResult object, content is in result.content
                for content in result.content:
                    if content.type == "text":
                        print(f"✅ Crawling result: {content.text}")

    except Exception as e:
        print(f"❌ Crawling failed: {e}")

# Run example
asyncio.run(crawl_example())
```

### Browser Content Analysis

```python
# Get complete page content
result = await session.call_tool("get_page_content", {
    "url": "https://nextjs.org",
    "wait_for_selector": "main",
    "wait_timeout": 15000
})

# Get console messages (useful for detecting JavaScript errors)
console_result = await session.call_tool("get_console_messages", {
    "url": "https://example.com",
    "wait_for_selector": ".app-loaded",
    "wait_timeout": 10000
})

# Get network requests (useful for API tracking)
network_result = await session.call_tool("get_network_requests", {
    "url": "https://api.example.com",
    "wait_for_selector": "[data-loaded=true]",
    "wait_timeout": 20000
})
```

### Batch Crawling Multiple Webpages

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

    # ✅ Correct return value handling
    for content in result.content:
        if content.type == "text":
            print(f"Crawled: {url} - {content.text}")

    # Add delay to avoid too frequent requests
    await asyncio.sleep(2)
```

### LLM Enhanced Crawling Example

```python
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def llm_enhanced_crawl():
    # Configure LLM environment variables
    os.environ["CRAWL_MODE"] = "llm"
    os.environ["LLAMA_PROVIDER"] = "ollama/qwen2.5-coder:latest"
    os.environ["LLAMA_BASE_URL"] = "http://localhost:11434"

    # Configure server connection
    server_params = StdioServerParameters(
        command="/path/to/venv/bin/python",
        args=["/path/to/mcp_server/server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # LLM Enhanced Crawling
            result = await session.call_tool("crawl_web_page", {
                "url": "https://example.com/article",
                "save_path": "./llm_results"
            })

            for content in result.content:
                if content.type == "text":
                    print(f"LLM Enhanced Crawling Result: {content.text}")

asyncio.run(llm_enhanced_crawl())
```

## 🧪 Development and Testing

### Run Tests

The project includes a comprehensive test suite:

```bash
# Run complete crawler test with real file output
python test/test_complete_crawler.py

# Run individual component tests
python test/test_hello.py      # Test hello/echo functions
python test/test_server.py     # Test MCP server functionality
python test/test_crawl.py      # Test crawling functions
python test/test_complete.py    # Test complete workflow
python test/test_browser.py     # Test browser automation functions
```

### Test Directory Structure

```
test/
├── test_complete_crawler.py    # Full integration test
├── test_hello.py             # Hello/echo functionality
├── test_server.py            # MCP server protocol
├── test_crawl.py             # Core crawling logic
├── test_browser.py           # Browser automation tests
├── test/test_browser.py      # Browser functionality tests
└── test_complete.py          # End-to-end workflow
```

### Development Mode

```bash
# Install development dependencies
pip install -e ".[dev]"

# The project uses pyright for type checking (configured in pyproject.toml)
# No additional linting tools are configured
```

## 📚 Project Structure

```
dev-tool-mcp/
├── mcp_server/          # Main package
│   ├── __init__.py            # Package initialization
│   ├── server.py              # MCP server implementation
│   ├── crawl.py              # Crawling logic and file handling
│   ├── llm.py                # LLM configuration and extraction strategies
│   ├── browser/              # Browser automation module
│   │   ├── __init__.py       # Browser module init
│   │   ├── browser_service.py # Browser service implementation
│   │   └── README.md         # Browser module docs
│   └── utils.py              # Utility functions for file I/O
├── test/                     # Test suite
│   ├── test_litellm_ollama.py # LLM integration tests
│   ├── test_browser.py       # Browser functionality tests
│   └── ...                   # Other test files
├── test_output/              # Test output directory
├── typings/                  # Type stubs for crawl4ai
├── pyproject.toml            # Project configuration
└── README.md                # This file
```

## 📚 API Reference

### Core Classes and Functions

#### `llm_config()` function (`llm.py`)
Configure LLM enhanced crawling strategies.

**Parameters:**
- `instruction` (str): Extraction instruction, defaults to specially optimized web content extraction instruction

**Returns:**
- `CrawlerRunConfig`: Crawler configuration with LLM extraction strategy

**Features:**
- Supports all litellm providers
- Automatic chunking of large content
- Intelligent content filtering and structured output
- Configurable temperature and token parameters

#### `save()` function (`utils.py`)
Save content to files with proper encoding handling.

**Parameters:**
- `path`: Directory path
- `name`: Filename
- `s`: Content (string, bytes, or bytearray)
- `call`: Callback function with saved file path

#### `saveJson()` function (`crawl.py`)
Async function to save downloaded files information and handle file downloads.

**Features:**
- Saves `downloaded_files.json` with file metadata
- Downloads and saves referenced files to `files/` subdirectory
- Error handling for failed downloads

#### `crawl_config()` function (`crawl.py`)
Dynamically select crawling configuration, decide whether to enable LLM mode based on environment variables.

**Environment Variables:**
- `CRAWL_MODE=llm`: Enable LLM enhanced extraction
- Others: Use traditional CSS selector extraction

### Browser Service Functions

#### `get_page_content()` (`browser_service.py`)
Get complete page content including HTML, text, metadata, links, and images.

**Parameters:**
- `url` (string, required): Target page URL
- `wait_for_selector` (string, optional): Wait for specific element before getting content
- `wait_timeout` (int, optional): Wait timeout in milliseconds (default 30000)
- `progress_callback` (callable, optional): Optional progress callback

#### `get_console_messages()` (`browser_service.py`)
Capture console messages (logs, warnings, errors) from webpage.

**Parameters:**
- `url` (string, required): Target page URL
- `wait_for_selector` (string, optional): Wait for specific element before getting console messages
- `wait_timeout` (int, optional): Wait timeout in milliseconds (default 30000)
- `progress_callback` (callable, optional): Optional progress callback

#### `get_network_requests()` (`browser_service.py`)
Record all network requests and responses made by webpage.

**Parameters:**
- `url` (string, required): Target page URL
- `wait_for_selector` (string, optional): Wait for specific element before getting network requests
- `wait_timeout` (int, optional): Wait timeout in milliseconds (default 30000)
- `progress_callback` (callable, optional): Optional progress callback

## 🎯 Configuration Details

### LLM Extraction Strategy

When LLM mode is enabled, the following smart extraction configuration is used:

**Default Extraction Instruction:**
```
You are a **Web Content Extraction Assistant**. Your task is to extract the **complete, clean, and precise main text content** from a given web page...
```

**LLM Configuration Parameters:**
- `provider`: Configured via `LLAMA_PROVIDER` environment variable
- `api_token`: Configured via `LLAMA_API_TOKEN` environment variable
- `base_url`: Configured via `LLAMA_BASE_URL` environment variable
- `max_tokens`: Default 4096, adjustable via `LLAMA_MAX_TOKENS`
- `temperature`: 0.1 (ensure output stability)
- `chunk_token_threshold`: 1400 (chunking threshold)
- `apply_chunking`: true (enable content chunking)

### CSS Extraction Strategy

Traditional mode uses pre-configured CSS extraction patterns:

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

### Content Filtering

Using `PruningContentFilter` configuration:
- `threshold`: 0.35 (dynamic threshold)
- `min_word_threshold`: 3
- `threshold_type`: "dynamic"

### Browser Configuration

- Headless mode enabled
- JavaScript enabled
- Bypass cache for fresh content
- Playwright-powered automation
- Real-time content monitoring

## ⚠️ Important Notes

1. **Rate Limiting**: Please control crawling frequency reasonably to avoid excessive pressure on target websites
2. **robots.txt**: Please comply with robots.txt rules of target websites
3. **Legal Compliance**: Ensure crawling behavior complies with relevant laws, regulations and website terms of use
4. **Browser Requirements**: crawl4ai requires a browser engine (Chrome/Chromium) to be installed on the system
5. **Memory Usage**: Large screenshots and PDFs may consume significant memory and disk space
6. **Security**: URL validation prevents access to localhost and internal network addresses
7. **Streaming**: Progress updates are streamed in real-time during long operations

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project uses MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- [crawl4ai Official Documentation](https://github.com/unclecode/crawl4ai)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Claude Desktop Documentation](https://docs.anthropic.com/claude/docs/overview)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Playwright Documentation](https://playwright.dev/)
- [Project Package](https://pypi.org/project/dev-tool-mcp/)

## 📞 Support

If you encounter problems or have suggestions:

1. **Check Issues**: [GitHub Issues](https://github.com/osins/dev-tool-mcp/issues)
2. **Create New Issue**: Report bugs or request features
3. **Test First**: Run `python test/test_complete_crawler.py` to verify setup

## 🎮 CLI Entry Point

The package includes a CLI entry point:

```bash
# After installation
dev-tool-mcp
```

This is equivalent to running:
```bash
python -m mcp_server.server
```

## 🛠️ Available Tools

---

**Made with ❤️ using crawl4ai, Playwright, and MCP**

*Current Version: 0.1.0*