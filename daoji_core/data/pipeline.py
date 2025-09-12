"""
数据处理管道
提供链式数据处理和转换功能
"""

import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable

from .models import BaseDataModel, ProcessingResult

logger = logging.getLogger(__name__)


class DataProcessor(ABC):
    """数据处理器抽象基类

    定义数据处理器的标准接口：
    - 处理数据的核心方法
    - 检查是否可以处理特定数据
    - 处理器名称和描述
    """

    def __init__(self, name: str | None = None):
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(f"{__name__}.{self.name}")

    @abstractmethod
    def process(self, data: BaseDataModel) -> ProcessingResult:
        """处理数据

        Args:
            data: 输入数据

        Returns:
            处理结果
        """
        pass

    @abstractmethod
    def can_process(self, data: BaseDataModel) -> bool:
        """检查是否可以处理该数据

        Args:
            data: 输入数据

        Returns:
            是否可以处理
        """
        pass

    def get_description(self) -> str:
        """获取处理器描述"""
        return getattr(self, "__doc__", "") or f"{self.name} 数据处理器"

    def validate_input(self, data: BaseDataModel) -> bool:
        """验证输入数据

        Args:
            data: 输入数据

        Returns:
            是否有效
        """
        return data is not None

    def pre_process(self, data: BaseDataModel) -> BaseDataModel:
        """预处理钩子

        Args:
            data: 输入数据

        Returns:
            预处理后的数据
        """
        return data

    def post_process(self, result: ProcessingResult) -> ProcessingResult:
        """后处理钩子

        Args:
            result: 处理结果

        Returns:
            后处理后的结果
        """
        return result


class DataPipeline:
    """数据处理管道

    管理多个数据处理器的链式执行：
    - 处理器注册和管理
    - 顺序执行处理器
    - 错误处理和恢复
    - 处理过程监控
    """

    def __init__(self, name: str | None = None):
        self.name = name or "DataPipeline"
        self.processors: list[DataProcessor] = []
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        self.enable_parallel = False  # 未来可扩展并行处理

    def add_processor(self, processor: DataProcessor) -> "DataPipeline":
        """添加处理器

        Args:
            processor: 数据处理器

        Returns:
            管道实例（支持链式调用）
        """
        self.processors.append(processor)
        self.logger.info(f"添加处理器: {processor.name}")
        return self

    def remove_processor(self, processor_name: str) -> bool:
        """移除处理器

        Args:
            processor_name: 处理器名称

        Returns:
            是否成功移除
        """
        for i, processor in enumerate(self.processors):
            if processor.name == processor_name:
                removed = self.processors.pop(i)
                self.logger.info(f"移除处理器: {removed.name}")
                return True
        return False

    def clear_processors(self) -> None:
        """清空所有处理器"""
        self.processors.clear()
        self.logger.info("清空所有处理器")

    def get_processor_names(self) -> list[str]:
        """获取所有处理器名称"""
        return [processor.name for processor in self.processors]

    def process(self, data: BaseDataModel) -> ProcessingResult:
        """执行处理管道

        Args:
            data: 输入数据

        Returns:
            最终处理结果
        """
        if not self.processors:
            self.logger.warning("管道中没有处理器")
            return ProcessingResult.success_result(data=data, processing_time=0.0, processor_name=self.name)

        start_time = time.time()
        current_data = data
        processed_count = 0

        try:
            for processor in self.processors:
                if not processor.can_process(current_data):
                    self.logger.debug(f"处理器 {processor.name} 跳过数据类型 {current_data.type}")
                    continue

                self.logger.debug(f"执行处理器: {processor.name}")
                processor_start = time.time()

                try:
                    # 预处理
                    preprocessed_data = processor.pre_process(current_data)

                    # 核心处理
                    result = processor.process(preprocessed_data)

                    # 后处理
                    result = processor.post_process(result)

                    processor_time = time.time() - processor_start
                    self.logger.debug(f"处理器 {processor.name} 完成，耗时 {processor_time:.3f}s")

                    if not result.success:
                        self.logger.error(f"处理器 {processor.name} 处理失败: {result.error}")
                        return result

                    current_data = result.data or current_data
                    processed_count += 1

                except Exception as e:
                    processor_time = time.time() - processor_start
                    error_msg = f"处理器 {processor.name} 执行异常: {str(e)}"
                    self.logger.error(error_msg)

                    return ProcessingResult.error_result(
                        error=error_msg, processing_time=processor_time, processor_name=processor.name
                    )

            total_time = time.time() - start_time
            self.logger.info(f"管道处理完成，共执行 {processed_count} 个处理器，总耗时 {total_time:.3f}s")

            return ProcessingResult.success_result(
                data=current_data, processing_time=total_time, processor_name=self.name
            )

        except Exception as e:
            total_time = time.time() - start_time
            error_msg = f"管道执行异常: {str(e)}"
            self.logger.error(error_msg)

            return ProcessingResult.error_result(error=error_msg, processing_time=total_time, processor_name=self.name)

    def validate_pipeline(self) -> list[str]:
        """验证管道配置

        Returns:
            验证错误列表
        """
        errors = []

        if not self.processors:
            errors.append("管道中没有处理器")

        # 检查处理器名称重复
        names = [p.name for p in self.processors]
        duplicates = set([name for name in names if names.count(name) > 1])
        if duplicates:
            errors.append(f"处理器名称重复: {duplicates}")

        return errors

    def get_pipeline_info(self) -> dict:
        """获取管道信息"""
        return {
            "name": self.name,
            "processor_count": len(self.processors),
            "processors": [{"name": p.name, "description": p.get_description()} for p in self.processors],
        }


class ConditionalProcessor(DataProcessor):
    """条件处理器

    根据条件决定是否执行处理逻辑
    """

    def __init__(self, condition: Callable[[BaseDataModel], bool], processor: DataProcessor, name: str | None = None):
        super().__init__(name)
        self.condition = condition
        self.processor = processor

    def can_process(self, data: BaseDataModel) -> bool:
        """检查条件和内部处理器是否都可以处理"""
        return self.condition(data) and self.processor.can_process(data)

    def process(self, data: BaseDataModel) -> ProcessingResult:
        """条件满足时执行内部处理器"""
        if not self.condition(data):
            return ProcessingResult.success_result(data=data, processing_time=0.0, processor_name=self.name)

        return self.processor.process(data)


class ParallelProcessor(DataProcessor):
    """并行处理器（未来扩展）

    同时执行多个处理器并合并结果
    """

    def __init__(self, processors: list[DataProcessor], name: str | None = None):
        super().__init__(name)
        self.processors = processors

    def can_process(self, data: BaseDataModel) -> bool:
        """至少有一个处理器可以处理"""
        return any(p.can_process(data) for p in self.processors)

    def process(self, data: BaseDataModel) -> ProcessingResult:
        """顺序执行所有可用处理器（暂时不实现真正的并行）"""
        start_time = time.time()
        results = []

        for processor in self.processors:
            if processor.can_process(data):
                result = processor.process(data)
                results.append(result)
                if not result.success:
                    return result

        processing_time = time.time() - start_time

        # 简单返回最后一个成功结果
        if results:
            last_result = results[-1]
            last_result.processing_time = processing_time
            return last_result

        return ProcessingResult.success_result(data=data, processing_time=processing_time, processor_name=self.name)
