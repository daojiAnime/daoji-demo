"""
基础模块定义
提供所有功能模块的基础抽象类和通用功能
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from ..config import BaseConfig
from ..data import BaseDataModel, DataModule, DataType, ProcessingResult


class BaseModule(ABC, DataModule):
    """基础模块抽象类

    所有功能模块的基础类，提供：
    - 标准的模块接口
    - 配置管理
    - 日志记录
    - 生命周期管理
    - 数据处理接口
    """

    def __init__(self, name: str, config: BaseConfig | None = None):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{name}")
        self._initialized = False
        self._running = False

    @abstractmethod
    def initialize(self) -> bool:
        """初始化模块

        Returns:
            是否初始化成功
        """
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """清理模块资源

        Returns:
            是否清理成功
        """
        pass

    @abstractmethod
    def process_data(self, data: BaseDataModel) -> ProcessingResult:
        """处理数据（实现DataModule协议）

        Args:
            data: 输入数据

        Returns:
            处理结果
        """
        pass

    @abstractmethod
    def get_supported_types(self) -> list[DataType]:
        """获取支持的数据类型（实现DataModule协议）

        Returns:
            支持的数据类型列表
        """
        pass

    def get_module_info(self) -> dict[str, str]:
        """获取模块信息（实现DataModule协议）

        Returns:
            模块信息字典
        """
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "status": self.get_status(),
            "description": self.get_description(),
            "version": self.get_version(),
        }

    def get_description(self) -> str:
        """获取模块描述"""
        return getattr(self, "__doc__", "") or f"{self.name} 模块"

    def get_version(self) -> str:
        """获取模块版本"""
        return getattr(self, "__version__", "1.0.0")

    def get_status(self) -> str:
        """获取模块状态"""
        if not self._initialized:
            return "未初始化"
        elif self._running:
            return "运行中"
        else:
            return "已停止"

    def start(self) -> bool:
        """启动模块

        Returns:
            是否启动成功
        """
        if not self._initialized:
            if not self.initialize():
                self.logger.error(f"模块 {self.name} 初始化失败")
                return False
            self._initialized = True

        if self._running:
            self.logger.warning(f"模块 {self.name} 已在运行")
            return True

        try:
            if self._start_internal():
                self._running = True
                self.logger.info(f"模块 {self.name} 启动成功")
                return True
            else:
                self.logger.error(f"模块 {self.name} 启动失败")
                return False
        except Exception as e:
            self.logger.error(f"模块 {self.name} 启动异常: {e}")
            return False

    def stop(self) -> bool:
        """停止模块

        Returns:
            是否停止成功
        """
        if not self._running:
            self.logger.warning(f"模块 {self.name} 未在运行")
            return True

        try:
            if self._stop_internal():
                self._running = False
                self.logger.info(f"模块 {self.name} 停止成功")
                return True
            else:
                self.logger.error(f"模块 {self.name} 停止失败")
                return False
        except Exception as e:
            self.logger.error(f"模块 {self.name} 停止异常: {e}")
            return False

    def restart(self) -> bool:
        """重启模块

        Returns:
            是否重启成功
        """
        self.logger.info(f"重启模块: {self.name}")
        return self.stop() and self.start()

    def is_initialized(self) -> bool:
        """检查是否已初始化"""
        return self._initialized

    def is_running(self) -> bool:
        """检查是否正在运行"""
        return self._running

    def validate_config(self) -> list[str]:
        """验证配置

        Returns:
            验证错误列表
        """
        errors = []

        if self.config is None:
            errors.append("配置未设置")
        else:
            try:
                # 触发Pydantic验证
                self.config.dict()
            except Exception as e:
                errors.append(f"配置验证失败: {e}")

        return errors

    def get_health_status(self) -> dict[str, Any]:
        """获取健康状态

        Returns:
            健康状态信息
        """
        return {
            "name": self.name,
            "initialized": self._initialized,
            "running": self._running,
            "config_valid": len(self.validate_config()) == 0,
            "supported_types": self.get_supported_types(),
        }

    def _start_internal(self) -> bool:
        """内部启动逻辑（子类可重写）

        Returns:
            是否启动成功
        """
        return True

    def _stop_internal(self) -> bool:
        """内部停止逻辑（子类可重写）

        Returns:
            是否停止成功
        """
        return True

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()
        self.cleanup()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', status='{self.get_status()}')"


class SimpleModule(BaseModule):
    """简单模块实现

    提供基础的模块实现，适用于简单的数据处理场景
    """

    def __init__(
        self,
        name: str,
        supported_types: list[DataType],
        process_func: Callable | None = None,
        config: BaseConfig | None = None,
    ):
        super().__init__(name, config)
        self._supported_types = supported_types
        self._process_func = process_func

    def initialize(self) -> bool:
        """初始化简单模块"""
        self.logger.info(f"初始化简单模块: {self.name}")
        return True

    def cleanup(self) -> bool:
        """清理简单模块"""
        self.logger.info(f"清理简单模块: {self.name}")
        return True

    def get_supported_types(self) -> list[DataType]:
        """获取支持的数据类型"""
        return self._supported_types

    def process_data(self, data: BaseDataModel) -> ProcessingResult:
        """处理数据"""
        if data.type not in self._supported_types:
            return ProcessingResult.error_result(
                error=f"不支持的数据类型: {data.type}", processing_time=0.0, error_code="UNSUPPORTED_TYPE"
            )

        if self._process_func is None:
            return ProcessingResult.success_result(data=data, processing_time=0.0, processor_name=self.name)

        try:
            import time

            start_time = time.time()
            result_data = self._process_func(data)
            processing_time = time.time() - start_time

            return ProcessingResult.success_result(
                data=result_data or data, processing_time=processing_time, processor_name=self.name
            )
        except Exception as e:
            return ProcessingResult.error_result(
                error=f"处理异常: {str(e)}", processing_time=0.0, error_code="PROCESSING_ERROR"
            )
