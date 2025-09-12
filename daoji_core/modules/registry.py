"""
模块注册器
提供模块的注册、发现和管理功能
"""

import logging
from typing import Any, Optional

from .base import BaseModule

logger = logging.getLogger(__name__)


class ModuleRegistry:
    """模块注册器

    管理所有模块的注册、发现和生命周期：
    - 模块注册和注销
    - 模块发现和查找
    - 批量操作
    - 依赖管理
    """

    _instance: Optional["ModuleRegistry"] = None
    _modules: dict[str, BaseModule] = {}
    _module_types: dict[str, type[BaseModule]] = {}

    def __new__(cls) -> "ModuleRegistry":
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = logging.getLogger(__name__)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "ModuleRegistry":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_module(self, module: BaseModule) -> bool:
        """注册模块

        Args:
            module: 模块实例

        Returns:
            是否注册成功
        """
        if not isinstance(module, BaseModule):
            self.logger.error(f"模块必须继承自BaseModule: {type(module)}")
            return False

        name = module.name
        if name in self._modules:
            self.logger.warning(f"模块 {name} 已存在，将被覆盖")

        self._modules[name] = module
        self._module_types[name] = type(module)
        self.logger.info(f"注册模块: {name} ({type(module).__name__})")
        return True

    def unregister_module(self, name: str) -> bool:
        """注销模块

        Args:
            name: 模块名称

        Returns:
            是否注销成功
        """
        if name not in self._modules:
            self.logger.warning(f"模块 {name} 不存在")
            return False

        module = self._modules[name]

        # 停止模块
        if module.is_running():
            module.stop()

        # 清理资源
        module.cleanup()

        # 从注册表移除
        del self._modules[name]
        del self._module_types[name]

        self.logger.info(f"注销模块: {name}")
        return True

    def get_module(self, name: str) -> BaseModule | None:
        """获取模块实例

        Args:
            name: 模块名称

        Returns:
            模块实例或None
        """
        return self._modules.get(name)

    def get_module_type(self, name: str) -> type[BaseModule] | None:
        """获取模块类型

        Args:
            name: 模块名称

        Returns:
            模块类型或None
        """
        return self._module_types.get(name)

    def list_modules(self) -> list[str]:
        """列出所有已注册的模块名称

        Returns:
            模块名称列表
        """
        return list(self._modules.keys())

    def list_module_info(self) -> dict[str, dict[str, Any]]:
        """列出所有模块的详细信息

        Returns:
            模块信息字典
        """
        return {name: module.get_module_info() for name, module in self._modules.items()}

    def find_modules_by_type(self, module_type: type[BaseModule]) -> list[BaseModule]:
        """根据类型查找模块

        Args:
            module_type: 模块类型

        Returns:
            匹配的模块列表
        """
        return [module for module in self._modules.values() if isinstance(module, module_type)]

    def find_modules_by_status(self, running: bool) -> list[BaseModule]:
        """根据运行状态查找模块

        Args:
            running: 是否运行中

        Returns:
            匹配的模块列表
        """
        return [module for module in self._modules.values() if module.is_running() == running]

    def start_module(self, name: str) -> bool:
        """启动指定模块

        Args:
            name: 模块名称

        Returns:
            是否启动成功
        """
        module = self.get_module(name)
        if module is None:
            self.logger.error(f"模块 {name} 不存在")
            return False

        return module.start()

    def stop_module(self, name: str) -> bool:
        """停止指定模块

        Args:
            name: 模块名称

        Returns:
            是否停止成功
        """
        module = self.get_module(name)
        if module is None:
            self.logger.error(f"模块 {name} 不存在")
            return False

        return module.stop()

    def restart_module(self, name: str) -> bool:
        """重启指定模块

        Args:
            name: 模块名称

        Returns:
            是否重启成功
        """
        module = self.get_module(name)
        if module is None:
            self.logger.error(f"模块 {name} 不存在")
            return False

        return module.restart()

    def start_all_modules(self) -> dict[str, bool]:
        """启动所有模块

        Returns:
            模块名称到启动结果的映射
        """
        results = {}
        for name, module in self._modules.items():
            try:
                results[name] = module.start()
            except Exception as e:
                self.logger.error(f"启动模块 {name} 异常: {e}")
                results[name] = False

        return results

    def stop_all_modules(self) -> dict[str, bool]:
        """停止所有模块

        Returns:
            模块名称到停止结果的映射
        """
        results = {}
        for name, module in self._modules.items():
            try:
                results[name] = module.stop()
            except Exception as e:
                self.logger.error(f"停止模块 {name} 异常: {e}")
                results[name] = False

        return results

    def validate_all_modules(self) -> dict[str, list[str]]:
        """验证所有模块

        Returns:
            模块名称到验证错误列表的映射
        """
        validation_results = {}

        for name, module in self._modules.items():
            try:
                errors = module.validate_config()
                validation_results[name] = errors
            except Exception as e:
                validation_results[name] = [f"验证异常: {str(e)}"]

        return validation_results

    def get_health_status(self) -> dict[str, dict[str, Any]]:
        """获取所有模块的健康状态

        Returns:
            模块健康状态信息
        """
        health_status = {}

        for name, module in self._modules.items():
            try:
                health_status[name] = module.get_health_status()
            except Exception as e:
                health_status[name] = {"name": name, "error": str(e), "healthy": False}

        return health_status

    def get_registry_statistics(self) -> dict[str, Any]:
        """获取注册表统计信息

        Returns:
            统计信息字典
        """
        running_count = len(self.find_modules_by_status(True))
        stopped_count = len(self.find_modules_by_status(False))

        type_counts = {}
        for module in self._modules.values():
            module_type = type(module).__name__
            type_counts[module_type] = type_counts.get(module_type, 0) + 1

        return {
            "total_modules": len(self._modules),
            "running_modules": running_count,
            "stopped_modules": stopped_count,
            "module_types": type_counts,
        }

    def clear_registry(self) -> None:
        """清空注册表（主要用于测试）"""
        # 停止所有模块
        self.stop_all_modules()

        # 清理所有模块
        for module in self._modules.values():
            try:
                module.cleanup()
            except Exception as e:
                self.logger.error(f"清理模块异常: {e}")

        # 清空注册表
        self._modules.clear()
        self._module_types.clear()
        self.logger.info("清空模块注册表")

    def export_module_config(self) -> dict[str, dict[str, Any]]:
        """导出所有模块配置

        Returns:
            模块配置字典
        """
        configs = {}

        for name, module in self._modules.items():
            if module.config is not None:
                try:
                    configs[name] = module.config.dict()
                except Exception as e:
                    self.logger.error(f"导出模块 {name} 配置失败: {e}")
                    configs[name] = {"error": str(e)}
            else:
                configs[name] = {}

        return configs

    def __len__(self) -> int:
        """返回注册的模块数量"""
        return len(self._modules)

    def __contains__(self, name: str) -> bool:
        """检查模块是否已注册"""
        return name in self._modules

    def __iter__(self):
        """迭代所有模块"""
        return iter(self._modules.values())

    def __repr__(self) -> str:
        return f"ModuleRegistry(modules={len(self._modules)})"
