"""
配置管理器
提供统一的配置注册、获取和验证功能
"""

from typing import Any, TypeVar

from loguru import logger

from .base import BaseConfig

T = TypeVar("T", bound=BaseConfig)


class ConfigManager:
    """配置管理器

    提供统一的配置管理功能：
    - 配置类注册
    - 配置实例获取
    - 配置验证
    - 配置热重载
    """

    _configs: dict[str, BaseConfig] = {}
    _config_classes: dict[str, type[BaseConfig]] = {}

    @classmethod
    def register_config(cls, name: str, config_class: type[T]) -> T:
        """注册配置类并创建实例

        Args:
            name: 配置名称
            config_class: 配置类

        Returns:
            配置实例

        Raises:
            ValueError: 配置名称已存在
        """
        if name in cls._configs:
            logger.warning(f"配置 {name} 已存在，将被覆盖")

        try:
            config = config_class()
            cls._configs[name] = config
            cls._config_classes[name] = config_class
            logger.info(f"配置 {name} 注册成功")
            return config
        except Exception as e:
            logger.error(f"配置 {name} 注册失败: {e}")
            raise

    @classmethod
    def get_config(cls, name: str) -> BaseConfig:
        """获取配置实例

        Args:
            name: 配置名称

        Returns:
            配置实例

        Raises:
            ValueError: 配置未注册
        """
        if name not in cls._configs:
            raise ValueError(f"配置 {name} 未注册")
        return cls._configs[name]

    @classmethod
    def get_typed_config(cls, name: str, config_type: type[T]) -> T:
        """获取指定类型的配置实例

        Args:
            name: 配置名称
            config_type: 期望的配置类型

        Returns:
            配置实例

        Raises:
            ValueError: 配置未注册或类型不匹配
        """
        config = cls.get_config(name)
        if not isinstance(config, config_type):
            raise ValueError(f"配置 {name} 类型不匹配，期望 {config_type}，实际 {type(config)}")
        return config

    @classmethod
    def list_configs(cls) -> dict[str, str]:
        """列出所有已注册的配置

        Returns:
            配置名称到类型名称的映射
        """
        return {name: type(config).__name__ for name, config in cls._configs.items()}

    @classmethod
    def validate_all(cls) -> bool:
        """验证所有配置

        Returns:
            是否所有配置都有效
        """
        all_valid = True
        for name, config in cls._configs.items():
            try:
                # 触发Pydantic验证
                _ = config.model_dump()
                logger.debug(f"配置 {name} 验证通过")
            except Exception as e:
                logger.error(f"配置 {name} 验证失败: {e}")
                all_valid = False

        return all_valid

    @classmethod
    def reload_config(cls, name: str) -> bool:
        """重新加载指定配置

        Args:
            name: 配置名称

        Returns:
            是否重新加载成功
        """
        if name not in cls._config_classes:
            logger.error(f"配置 {name} 未注册，无法重新加载")
            return False

        try:
            config_class = cls._config_classes[name]
            new_config = config_class()
            cls._configs[name] = new_config
            logger.info(f"配置 {name} 重新加载成功")
            return True
        except Exception as e:
            logger.error(f"配置 {name} 重新加载失败: {e}")
            return False

    @classmethod
    def clear_all(cls):
        """清除所有配置（主要用于测试）"""
        cls._configs.clear()
        cls._config_classes.clear()
        logger.info("所有配置已清除")

    @classmethod
    def get_config_summary(cls) -> dict[str, Any]:
        """获取配置摘要信息

        Returns:
            配置摘要信息
        """
        summary: dict[str, Any] = {"total_configs": len(cls._configs), "configs": {}}

        for name, config in cls._configs.items():
            summary["configs"][name] = {
                "type": type(config).__name__,
                "environment": getattr(config, "environment", "unknown"),
                "debug": getattr(config, "debug", False),
            }

        return summary
