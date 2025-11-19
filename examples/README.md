# MCP 客户端使用示例

本目录包含如何使用 spider-mcp-server 的完整示例代码。

## 📁 文件说明

- `quick_start.py` - 最简单的使用示例，演示核心API调用
- `mcp_client_tutorial.py` - 完整的教程，包含错误处理和最佳实践

## 🚀 快速开始

### 1. 安装依赖

```bash
# 在项目根目录
pip install -e .
```

### 2. 运行示例

```bash
# 快速开始示例
python examples/quick_start.py

# 完整教程
python examples/mcp_client_tutorial.py
```

## ⚠️ 重要注意事项

1. **返回值处理**: MCP 服务器返回的是 `CallToolResult` 对象，内容在 `result.content` 中
2. **路径配置**: 确保虚拟环境路径正确
3. **依赖安装**: 需要安装 crawl4ai 和浏览器驱动

## 🔧 核心要点

```python
# ✅ 正确的返回值处理
result = await session.call_tool("tool_name", params)
for content in result.content:  # 注意是 .content
    if content.type == "text":
        print(content.text)

# ❌ 错误的写法
for content in result:  # 这会出错！
    print(content.text)
```