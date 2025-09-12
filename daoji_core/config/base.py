"""
基础配置类
提供所有模块配置的基础类和通用功能
"""

from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """环境类型枚举"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class BaseConfig(BaseSettings):
    """基础配置类

    所有模块配置的基础类，提供通用的配置功能：
    - 环境管理
    - 调试模式
    - 日志配置
    - 自动环境变量读取
    """

    # 环境配置
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="运行环境")

    debug: bool = Field(default=False, description="调试模式开关")

    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)")

    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="日志格式")

    # 项目信息
    project_name: str = Field(default="Daoji Demo", description="项目名称")

    version: str = Field(default="0.1.0", description="项目版本")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def is_development(self) -> bool:
        """检查是否为开发环境"""
        return self.environment == Environment.DEVELOPMENT

    def is_production(self) -> bool:
        """检查是否为生产环境"""
        return self.environment == Environment.PRODUCTION

    def get_env_file(self) -> str:
        """获取环境特定的配置文件路径"""
        return f".env.{self.environment.value}"
