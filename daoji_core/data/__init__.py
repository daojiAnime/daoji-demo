"""
数据流管理模块
提供统一的数据模型、处理管道和流管理功能
"""

from .interface import DataFlowManager, DataModule
from .models import BaseDataModel, DataType, ProcessingResult, TableData, TextData
from .pipeline import DataPipeline, DataProcessor

__all__ = [
    "BaseDataModel",
    "DataType",
    "TextData",
    "TableData",
    "ProcessingResult",
    "DataProcessor",
    "DataPipeline",
    "DataModule",
    "DataFlowManager",
]
