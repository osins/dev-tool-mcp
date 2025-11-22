"""
工具函数和日志配置模块
"""
import os
import logging
import sys
from pathlib import Path
from typing import Callable


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    为 MCP 服务器设置日志记录，确保日志写入 stderr 而不是 stdout
    """
    # 创建日志格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # 移除现有的处理器，避免重复
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 创建并配置 stderr 处理器
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    root_logger.addHandler(stderr_handler)

    # 如果指定了日志文件，也添加文件处理器
    if log_file:
        file_path = Path(log_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def save(path: str, name: str, s: str | bytes | bytearray | None, call: Callable[[str], None]):
    """
    保存文件内容到指定路径
    注意：这个函数不能使用 print，因为它是为 MCP 服务器设计的
    """
    # 使用日志记录而不是 print，以避免写入 stdout
    logging.info(f"Saving: {path}, {name}, {type(s).__name__ if s is not None else 'None'}")

    if s is None:
        return

    file: str = os.path.join(path, name)
    if isinstance(s, str):
        with open(file, 'w', encoding='utf-8') as f:
            _ = f.write(s)
    else:
        with open(file, 'wb') as f:
            _ = f.write(s)

    call(file)


# 设置默认日志记录
setup_logging()