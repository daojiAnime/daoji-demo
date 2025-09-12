"""
数据模型定义
提供统一的数据结构和类型安全的数据模型
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DataType(str, Enum):
    """数据类型枚举"""

    TEXT = "text"
    IMAGE = "image"
    TABLE = "table"
    JSON = "json"
    BINARY = "binary"
    AUDIO = "audio"
    VIDEO = "video"


class BaseDataModel(BaseModel):
    """基础数据模型

    所有数据类型的基础类，提供：
    - 唯一标识
    - 数据类型标记
    - 时间戳
    - 元数据存储
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="数据唯一标识")

    type: DataType = Field(description="数据类型")

    timestamp: datetime = Field(default_factory=datetime.now, description="创建时间")

    metadata: dict[str, Any] = Field(default_factory=dict, description="元数据")

    source: str | None = Field(None, description="数据来源")

    class Config:
        """Pydantic配置"""

        json_encoders = {datetime: lambda v: v.isoformat()}
        use_enum_values = True

    def add_metadata(self, key: str, value: Any) -> None:
        """添加元数据"""
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """获取元数据"""
        return self.metadata.get(key, default)

    def has_metadata(self, key: str) -> bool:
        """检查是否有指定元数据"""
        return key in self.metadata


class TextData(BaseDataModel):
    """文本数据模型"""

    type: DataType = DataType.TEXT

    content: str = Field(description="文本内容")

    language: str | None = Field(None, description="语言代码 (如: zh, en)")

    encoding: str = Field(default="utf-8", description="文本编码")

    word_count: int | None = Field(None, description="词数统计")

    def __init__(self, **data):
        super().__init__(**data)
        # 自动计算词数
        if self.word_count is None and self.content:
            self.word_count = len(self.content.split())

    def get_preview(self, max_length: int = 100) -> str:
        """获取文本预览"""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."

    def is_empty(self) -> bool:
        """检查文本是否为空"""
        return not self.content.strip()


class TableData(BaseDataModel):
    """表格数据模型"""

    type: DataType = DataType.TABLE

    headers: list[str] = Field(description="表头列表")

    rows: list[list[Any]] = Field(description="数据行列表")

    column_schema: dict[str, str] | None = Field(None, description="列数据类型定义")

    def __init__(self, **data):
        super().__init__(**data)
        # 验证数据一致性
        self._validate_data()

    def _validate_data(self):
        """验证表格数据一致性"""
        if not self.headers:
            raise ValueError("表头不能为空")

        header_count = len(self.headers)
        for i, row in enumerate(self.rows):
            if len(row) != header_count:
                raise ValueError(f"第{i+1}行数据列数({len(row)})与表头列数({header_count})不匹配")

    def get_row_count(self) -> int:
        """获取行数"""
        return len(self.rows)

    def get_column_count(self) -> int:
        """获取列数"""
        return len(self.headers)

    def get_column_data(self, column_name: str) -> list[Any]:
        """获取指定列的数据"""
        if column_name not in self.headers:
            raise ValueError(f"列 '{column_name}' 不存在")

        column_index = self.headers.index(column_name)
        return [row[column_index] for row in self.rows]

    def add_row(self, row: list[Any]) -> None:
        """添加数据行"""
        if len(row) != len(self.headers):
            raise ValueError(f"行数据列数({len(row)})与表头列数({len(self.headers)})不匹配")
        self.rows.append(row)

    def to_dict_list(self) -> list[dict[str, Any]]:
        """转换为字典列表格式"""
        return [dict(zip(self.headers, row, strict=False)) for row in self.rows]


class ImageData(BaseDataModel):
    """图像数据模型"""

    type: DataType = DataType.IMAGE

    file_path: str | None = Field(None, description="图像文件路径")

    data: bytes | None = Field(None, description="图像二进制数据")

    format: str | None = Field(None, description="图像格式 (jpg, png, gif等)")

    width: int | None = Field(None, description="图像宽度")

    height: int | None = Field(None, description="图像高度")

    size_bytes: int | None = Field(None, description="文件大小（字节）")

    def has_file(self) -> bool:
        """检查是否有文件路径"""
        return bool(self.file_path)

    def has_data(self) -> bool:
        """检查是否有二进制数据"""
        return bool(self.data)


class ProcessingResult(BaseModel):
    """数据处理结果模型"""

    success: bool = Field(description="处理是否成功")

    data: BaseDataModel | None = Field(None, description="处理后的数据")

    error: str | None = Field(None, description="错误信息")

    error_code: str | None = Field(None, description="错误代码")

    processing_time: float = Field(description="处理时间（秒）")

    processor_name: str | None = Field(None, description="处理器名称")

    warnings: list[str] = Field(default_factory=list, description="警告信息列表")

    def add_warning(self, warning: str) -> None:
        """添加警告信息"""
        self.warnings.append(warning)

    def has_warnings(self) -> bool:
        """检查是否有警告"""
        return len(self.warnings) > 0

    @classmethod
    def success_result(
        cls, data: BaseDataModel, processing_time: float, processor_name: str | None = None
    ) -> "ProcessingResult":
        """创建成功结果"""
        return cls(success=True, data=data, processing_time=processing_time, processor_name=processor_name)

    @classmethod
    def error_result(
        cls, error: str, processing_time: float, error_code: str | None = None, processor_name: str | None = None
    ) -> "ProcessingResult":
        """创建错误结果"""
        return cls(
            success=False,
            error=error,
            error_code=error_code,
            processing_time=processing_time,
            processor_name=processor_name,
        )
