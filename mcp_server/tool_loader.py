"""
工具加载器 - 自动扫描并返回所有 MCP 工具实例
遵循 MCP 服务器日志记录最佳实践，避免写入 stdout
"""
import os
import logging
import importlib.util
from pathlib import Path
from typing import List

from mcp_server.mcp_tool import MCPTool


def load_all_tools() -> List[MCPTool]:
    """
    自动扫描 tools 目录并加载所有工具
    """
    tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
    tools = []

    # 遍历工具目录
    for filename in os.listdir(tools_dir):
        if filename.endswith('_tool.py') and filename != '__init__.py':
            # 构建模块名称
            module_name = f"mcp_server.tools.{filename[:-3]}"  # 去掉 .py 后缀
            file_path = os.path.join(tools_dir, filename)

            try:
                # 动态导入模块
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None:
                    logging.error(f"Could not create module spec for {file_path}")
                    continue

                module = importlib.util.module_from_spec(spec)

                # 添加到 sys.modules 以避免重复导入问题
                import sys as sys_module
                sys_module.modules[module_name] = module

                spec.loader.exec_module(module)

                # 查找 create_*_tool 函数
                for attr_name in dir(module):
                    if attr_name.startswith('create_') and attr_name.endswith('_tool'):
                        create_func = getattr(module, attr_name)
                        if callable(create_func):
                            try:
                                tool_instance = create_func()
                                if isinstance(tool_instance, MCPTool):
                                    tools.append(tool_instance)
                                else:
                                    logging.warning(f"{attr_name} did not return an MCPTool instance: {type(tool_instance)}")
                            except Exception as e:
                                logging.exception(f"Error creating tool from {attr_name} in {file_path}: {e}")

            except ImportError as e:
                logging.error(f"Failed to import module {file_path}: {e}")
            except Exception as e:
                logging.exception(f"Unexpected error processing {file_path}: {e}")

    logging.info(f"Loaded {len(tools)} tools from {tools_dir}")
    return tools


def _scan_tools_directory_recursive(base_path: str, file_pattern: str = "*_tool.py") -> List[str]:
    """
    递归扫描工具目录，支持子目录
    """
    path = Path(base_path)
    tool_files = []

    for file_path in path.rglob(file_pattern):
        if file_path.is_file() and file_path.name != '__init__.py':
            tool_files.append(str(file_path))

    return tool_files


def load_all_tools_recursive() -> List[MCPTool]:
    """
    递归扫描 tools 目录（包括子目录）并加载所有工具
    """
    tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
    tool_files = _scan_tools_directory_recursive(tools_dir)

    tools = []

    for file_path in tool_files:
        # 生成唯一模块名以避免冲突
        rel_path = os.path.relpath(file_path, os.path.dirname(__file__))
        module_name = f"mcp_server.tools.{rel_path.replace(os.sep, '.').replace('.py', '')}"

        try:
            # 动态导入模块
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                logging.error(f"Could not create module spec for {file_path}")
                continue

            module = importlib.util.module_from_spec(spec)

            # 添加到 sys.modules 以避免重复导入问题
            import sys as sys_module
            sys_module.modules[module_name] = module

            spec.loader.exec_module(module)

            # 查找 create_*_tool 函数
            for attr_name in dir(module):
                if attr_name.startswith('create_') and attr_name.endswith('_tool'):
                    create_func = getattr(module, attr_name)
                    if callable(create_func):
                        try:
                            tool_instance = create_func()
                            if isinstance(tool_instance, MCPTool):
                                tools.append(tool_instance)
                            else:
                                logging.warning(f"{attr_name} did not return an MCPTool instance: {type(tool_instance)}")
                        except Exception as e:
                            logging.exception(f"Error creating tool from {attr_name} in {file_path}: {e}")

        except ImportError as e:
            logging.error(f"Failed to import module {file_path}: {e}")
        except Exception as e:
            logging.exception(f"Unexpected error processing {file_path}: {e}")

    logging.info(f"Recursively loaded {len(tools)} tools from {tools_dir} and subdirectories")
    return tools


def get_all_mcp_tools() -> List[MCPTool]:
    """
    获取所有 MCP 工具实例的便捷函数（使用递归扫描）
    """
    return load_all_tools_recursive()