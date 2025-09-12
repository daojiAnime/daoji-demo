"""
Daoji Core Framework
统一的模块化架构核心框架
"""

__version__ = "0.1.0"

from .config import BaseConfig, ConfigManager
from .data import BaseDataModel, DataPipeline, DataType, ProcessingResult, TextData
from .modules import BaseModule, ModuleRegistry

__all__ = [
    "ConfigManager",
    "BaseConfig",
    "BaseModule",
    "ModuleRegistry",
    "BaseDataModel",
    "DataType",
    "TextData",
    "ProcessingResult",
    "DataPipeline",
]
