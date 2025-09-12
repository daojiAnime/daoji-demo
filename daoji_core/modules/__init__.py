"""
模块管理系统
提供统一的模块接口和注册管理功能
"""

from .base import BaseModule
from .registry import ModuleRegistry

__all__ = [
    "BaseModule",
    "ModuleRegistry",
]
