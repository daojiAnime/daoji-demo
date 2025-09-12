"""
日志工具
提供统一的日志配置和管理功能
"""

import logging
import logging.config
import sys
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    format_string: str | None = None,
    log_file: str | None = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> None:
    """设置日志配置

    Args:
        level: 日志级别
        format_string: 日志格式字符串
        log_file: 日志文件路径
        max_bytes: 日志文件最大大小
        backup_count: 备份文件数量
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 基础配置
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"standard": {"format": format_string, "datefmt": "%Y-%m-%d %H:%M:%S"}},
        "handlers": {
            "console": {"class": "logging.StreamHandler", "level": level, "formatter": "standard", "stream": sys.stdout}
        },
        "root": {"level": level, "handlers": ["console"]},
    }

    # 添加文件处理器
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level,
            "formatter": "standard",
            "filename": log_file,
            "maxBytes": max_bytes,
            "backupCount": backup_count,
            "encoding": "utf-8",
        }
        config["root"]["handlers"].append("file")

    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """获取日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        日志记录器实例
    """
    return logging.getLogger(name)


def configure_module_logging(
    module_name: str, level: str | None = None, handlers: list | None = None
) -> logging.Logger:
    """为特定模块配置日志

    Args:
        module_name: 模块名称
        level: 日志级别
        handlers: 处理器列表

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(module_name)

    if level:
        logger.setLevel(getattr(logging, level.upper()))

    if handlers:
        # 清除现有处理器
        logger.handlers.clear()
        # 添加新处理器
        for handler in handlers:
            logger.addHandler(handler)

    return logger


def create_file_handler(
    log_file: str,
    level: str = "INFO",
    format_string: str | None = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Handler:
    """创建文件处理器

    Args:
        log_file: 日志文件路径
        level: 日志级别
        format_string: 格式字符串
        max_bytes: 最大文件大小
        backup_count: 备份数量

    Returns:
        文件处理器
    """
    from logging.handlers import RotatingFileHandler

    # 确保目录存在
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")

    handler.setLevel(getattr(logging, level.upper()))

    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    return handler


def create_console_handler(level: str = "INFO", format_string: str | None = None) -> logging.Handler:
    """创建控制台处理器

    Args:
        level: 日志级别
        format_string: 格式字符串

    Returns:
        控制台处理器
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper()))

    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    return handler
