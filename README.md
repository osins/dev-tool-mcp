# MCP Spider Server

An MCP (Model Context Protocol) spider server based on [crawl4ai](https://github.com/unclecode/crawl4ai) that provides powerful web crawling and content extraction capabilities.

## 🚀 Features

- **Intelligent Web Crawling**: Use crawl4ai for efficient web content extraction
- **Multi-format Output**: Support HTML, Markdown, JSON, PDF, and PNG formats
- **Screenshot Function**: Automatic webpage screenshot generation
- **PDF Export**: Export webpage content as PDF files
- **Content Filtering**: Use PruningContentFilter to optimize content extraction
- **Structured Data Extraction**: Support JsonCssExtractionStrategy for precise data extraction
- **File Downloads**: Automatically download and save referenced files
- **MCP Protocol Support**: Fully compatible with MCP standard, integrable with MCP-supporting clients

## 📦 Installation

### Requirements

- Python 3.8+
- Virtual environment recommended

### Installation Steps

1. **Clone repository**
```bash
git clone https://github.com/osins/crawler-mcp-server.git
cd crawler-mcp-server
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
    "spider": {
      "command": "/path/to/crawler-mcp-server/venv/bin/python",
      "args": [
        "/path/to/crawler-mcp-server/spider_mcp_server/server.py"
      ],
      "description": "MCP spider server using crawl4ai for web crawling and content extraction"
    }
  }
}
```

### General MCP Client Configuration

If you use other MCP clients, you can use the following general configuration:

```json
{
  "servers": {
    "spider-crawler": {
      "name": "Spider Crawler Server",
      "description": "Web crawling and content extraction server",
      "command": "/path/to/crawler-mcp-server/venv/bin/python",
      "args": [
        "/path/to/crawler-mcp-server/spider_mcp_server/server.py"
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

## 🛠️ Available Tools

### 1. `crawl_web_page`

Crawl webpage content from the specified URL and save in multiple formats.

**Parameters:**
- `url` (string, required): The webpage URL to crawl
- `save_path` (string, required): The directory path to save crawled content

**Features:**
- Automatic webpage screenshot (PNG)
- PDF export generation
- Raw Markdown content extraction
- Cleaned/filtered Markdown content
- Structured data extraction (JSON)
- HTML content preservation
- Downloaded files processing

**Example usage:**
```python
# Crawl webpage and save to specified directory
result = await session.call_tool("crawl_web_page", {
    "url": "https://example.com",
    "save_path": "./output_directory"
})
```

### 2. `say_hello`

Simple greeting tool for testing server connectivity.

**Parameters:**
- `name` (string, optional): Name to greet, defaults to "World"

**Example usage:**
```python
result = await session.call_tool("say_hello", {
    "name": "Alice"
})
```

### 3. `echo_message`

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
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def crawl_example():
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="/path/to/crawler-mcp-server/venv/bin/python",
        args=["/path/to/crawler-mcp-server/spider_mcp_server/server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()
            
            # Crawl webpage
            result = await session.call_tool("crawl_web_page", {
                "url": "https://github.com/unclecode/crawl4ai",
                "save_path": "./crawl_results"
            })
            
            print("Crawling completed!")
            for content in result:
                if hasattr(content, 'text'):
                    print(f"Result: {content.text}")

# Run example
asyncio.run(crawl_example())
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
    print(f"Crawled: {url}")
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
```

### Test Directory Structure

```
test/
├── test_complete_crawler.py    # Full integration test
├── test_hello.py             # Hello/echo functionality
├── test_server.py            # MCP server protocol
├── test_crawl.py             # Core crawling logic
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
crawler-mcp-server/
├── spider_mcp_server/          # Main package
│   ├── __init__.py            # Package initialization
│   ├── server.py              # MCP server implementation
│   ├── crawl.py              # Crawling logic and file handling
│   └── utils.py              # Utility functions for file I/O
├── test/                     # Test suite
├── test_output/              # Test output directory
├── typings/                  # Type stubs for crawl4ai
├── pyproject.toml            # Project configuration
└── README.md                # This file
```

## 📚 API Reference

### Core Classes and Functions

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

## 🎯 Configuration Details

### CSS Extraction Strategy

The crawler uses a pre-configured CSS extraction schema:

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

Uses `PruningContentFilter` with these settings:
- `threshold`: 0.35 (dynamic threshold)
- `min_word_threshold`: 3
- `threshold_type`: "dynamic"

### Browser Configuration

- Headless mode enabled
- JavaScript enabled
- Bypass cache for fresh content

## ⚠️ Important Notes

1. **Rate Limiting**: Please control crawling frequency reasonably to avoid excessive pressure on target websites
2. **robots.txt**: Please comply with robots.txt rules of target websites
3. **Legal Compliance**: Ensure crawling behavior complies with relevant laws, regulations and website terms of use
4. **Browser Requirements**: crawl4ai requires a browser engine (Chrome/Chromium) to be installed on the system
5. **Memory Usage**: Large screenshots and PDFs may consume significant memory and disk space

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
- [Project Package](https://pypi.org/project/spider-mcp/)

## 📞 Support

If you encounter problems or have suggestions:

1. **Check Issues**: [GitHub Issues](https://github.com/osins/crawler-mcp-server/issues)
2. **Create New Issue**: Report bugs or request features
3. **Test First**: Run `python test/test_complete_crawler.py` to verify setup

## 🎮 CLI Entry Point

The package includes a CLI entry point:

```bash
# After installation
spider-mcp
```

This is equivalent to running:
```bash
python -m spider_mcp_server.server
```

---

**Made with ❤️ using crawl4ai and MCP**

*Current Version: 0.1.0*