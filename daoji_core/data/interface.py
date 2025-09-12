"""
数据流接口定义
提供模块间数据交换的标准接口和管理器
"""

import logging
from typing import Protocol, runtime_checkable

from .models import BaseDataModel, DataType, ProcessingResult
from .pipeline import DataPipeline

logger = logging.getLogger(__name__)


@runtime_checkable
class DataModule(Protocol):
    """数据模块接口协议

    定义所有数据处理模块必须实现的标准接口：
    - 数据处理方法
    - 支持的数据类型
    - 模块信息
    """

    def process_data(self, data: BaseDataModel) -> ProcessingResult:
        """处理数据的标准接口

        Args:
            data: 输入数据

        Returns:
            处理结果
        """
        ...

    def get_supported_types(self) -> list[DataType]:
        """获取支持的数据类型

        Returns:
            支持的数据类型列表
        """
        ...

    def get_module_info(self) -> dict[str, str]:
        """获取模块信息

        Returns:
            模块信息字典
        """
        ...


class DataFlowManager:
    """数据流管理器

    管理模块间的数据流转：
    - 模块注册和发现
    - 数据路由和分发
    - 处理管道管理
    - 流程监控和日志
    """

    def __init__(self):
        self.modules: dict[str, DataModule] = {}
        self.pipeline = DataPipeline("GlobalPipeline")
        self.logger = logging.getLogger(__name__)
        self._routing_rules: dict[DataType, list[str]] = {}

    def register_module(self, name: str, module: DataModule) -> None:
        """注册数据模块

        Args:
            name: 模块名称
            module: 模块实例

        Raises:
            ValueError: 模块不符合协议或名称已存在
        """
        if not isinstance(module, DataModule):
            raise ValueError(f"模块 {name} 不符合 DataModule 协议")

        if name in self.modules:
            self.logger.warning(f"模块 {name} 已存在，将被覆盖")

        self.modules[name] = module
        self.logger.info(f"注册模块: {name}")

        # 自动设置路由规则
        self._setup_routing_for_module(name, module)

    def unregister_module(self, name: str) -> bool:
        """注销模块

        Args:
            name: 模块名称

        Returns:
            是否成功注销
        """
        if name in self.modules:
            del self.modules[name]
            self.logger.info(f"注销模块: {name}")
            self._cleanup_routing_for_module(name)
            return True
        return False

    def get_module(self, name: str) -> DataModule | None:
        """获取模块实例

        Args:
            name: 模块名称

        Returns:
            模块实例或None
        """
        return self.modules.get(name)

    def list_modules(self) -> dict[str, dict[str, str]]:
        """列出所有已注册的模块

        Returns:
            模块名称到模块信息的映射
        """
        return {name: module.get_module_info() for name, module in self.modules.items()}

    def route_data(self, data: BaseDataModel, target_module: str) -> ProcessingResult:
        """路由数据到指定模块

        Args:
            data: 输入数据
            target_module: 目标模块名称

        Returns:
            处理结果
        """
        if target_module not in self.modules:
            return ProcessingResult.error_result(
                error=f"模块 {target_module} 未注册", processing_time=0.0, error_code="MODULE_NOT_FOUND"
            )

        module = self.modules[target_module]

        # 检查模块是否支持该数据类型
        supported_types = module.get_supported_types()
        if data.type not in supported_types:
            return ProcessingResult.error_result(
                error=f"模块 {target_module} 不支持数据类型 {data.type}",
                processing_time=0.0,
                error_code="UNSUPPORTED_DATA_TYPE",
            )

        try:
            # 先通过全局管道预处理
            pipeline_result = self.pipeline.process(data)
            if not pipeline_result.success:
                return pipeline_result

            # 发送到目标模块
            self.logger.debug(f"路由数据到模块: {target_module}")
            result = module.process_data(pipeline_result.data)

            self.logger.debug(f"模块 {target_module} 处理完成")
            return result

        except Exception as e:
            error_msg = f"路由到模块 {target_module} 时发生异常: {str(e)}"
            self.logger.error(error_msg)
            return ProcessingResult.error_result(error=error_msg, processing_time=0.0, error_code="ROUTING_ERROR")

    def auto_route_data(self, data: BaseDataModel) -> list[ProcessingResult]:
        """自动路由数据到所有支持的模块

        Args:
            data: 输入数据

        Returns:
            所有模块的处理结果列表
        """
        results = []

        # 获取支持该数据类型的模块
        compatible_modules = self._get_compatible_modules(data.type)

        if not compatible_modules:
            self.logger.warning(f"没有模块支持数据类型 {data.type}")
            return results

        # 先通过全局管道预处理
        pipeline_result = self.pipeline.process(data)
        if not pipeline_result.success:
            results.append(pipeline_result)
            return results

        # 发送到所有兼容模块
        for module_name in compatible_modules:
            try:
                module = self.modules[module_name]
                result = module.process_data(pipeline_result.data)
                results.append(result)
                self.logger.debug(f"自动路由到模块 {module_name} 完成")
            except Exception as e:
                error_result = ProcessingResult.error_result(
                    error=f"自动路由到模块 {module_name} 失败: {str(e)}",
                    processing_time=0.0,
                    error_code="AUTO_ROUTING_ERROR",
                )
                results.append(error_result)

        return results

    def set_routing_rule(self, data_type: DataType, module_names: list[str]) -> None:
        """设置数据类型的路由规则

        Args:
            data_type: 数据类型
            module_names: 目标模块名称列表
        """
        self._routing_rules[data_type] = module_names
        self.logger.info(f"设置路由规则: {data_type} -> {module_names}")

    def get_routing_rules(self) -> dict[DataType, list[str]]:
        """获取所有路由规则"""
        return self._routing_rules.copy()

    def get_pipeline(self) -> DataPipeline:
        """获取全局处理管道"""
        return self.pipeline

    def validate_modules(self) -> dict[str, list[str]]:
        """验证所有模块

        Returns:
            模块名称到错误列表的映射
        """
        validation_results = {}

        for name, module in self.modules.items():
            errors = []

            try:
                # 检查必需方法
                if not hasattr(module, "process_data"):
                    errors.append("缺少 process_data 方法")

                if not hasattr(module, "get_supported_types"):
                    errors.append("缺少 get_supported_types 方法")

                if not hasattr(module, "get_module_info"):
                    errors.append("缺少 get_module_info 方法")

                # 检查支持的数据类型
                supported_types = module.get_supported_types()
                if not isinstance(supported_types, list):
                    errors.append("get_supported_types 必须返回列表")

                # 检查模块信息
                module_info = module.get_module_info()
                if not isinstance(module_info, dict):
                    errors.append("get_module_info 必须返回字典")

            except Exception as e:
                errors.append(f"验证异常: {str(e)}")

            validation_results[name] = errors

        return validation_results

    def get_flow_statistics(self) -> dict[str, int]:
        """获取数据流统计信息

        Returns:
            统计信息字典
        """
        return {
            "total_modules": len(self.modules),
            "total_routing_rules": len(self._routing_rules),
            "pipeline_processors": len(self.pipeline.processors),
        }

    def _setup_routing_for_module(self, name: str, module: DataModule) -> None:
        """为模块设置自动路由规则"""
        try:
            supported_types = module.get_supported_types()
            for data_type in supported_types:
                if data_type not in self._routing_rules:
                    self._routing_rules[data_type] = []
                if name not in self._routing_rules[data_type]:
                    self._routing_rules[data_type].append(name)
        except Exception as e:
            self.logger.warning(f"为模块 {name} 设置路由规则失败: {e}")

    def _cleanup_routing_for_module(self, name: str) -> None:
        """清理模块的路由规则"""
        for data_type, module_names in self._routing_rules.items():
            if name in module_names:
                module_names.remove(name)

    def _get_compatible_modules(self, data_type: DataType) -> list[str]:
        """获取支持指定数据类型的模块列表"""
        compatible = []
        for name, module in self.modules.items():
            try:
                if data_type in module.get_supported_types():
                    compatible.append(name)
            except Exception as e:
                self.logger.warning(f"检查模块 {name} 兼容性失败: {e}")
        return compatible
