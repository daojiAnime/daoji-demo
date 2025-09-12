"""
AI服务配置
提供AI相关服务的配置管理
"""

from pydantic import Field, validator

from .base import BaseConfig


class AIConfig(BaseConfig):
    """AI服务配置

    管理AI相关服务的配置：
    - OpenAI API配置
    - 模型设置
    - 缓存配置
    - NLP模型配置
    """

    # OpenAI配置
    openai_api_key: str | None = Field(None, description="OpenAI API密钥")

    openai_base_url: str = Field(default="https://api.openai.com/v1", description="OpenAI API基础URL")

    openai_organization: str | None = Field(None, description="OpenAI组织ID")

    # 默认模型设置
    default_chat_model: str = Field(default="gpt-3.5-turbo", description="默认聊天模型")

    default_embedding_model: str = Field(default="text-embedding-ada-002", description="默认嵌入模型")

    # 模型参数
    default_temperature: float = Field(default=0.7, description="默认温度参数")

    default_max_tokens: int | None = Field(default=None, description="默认最大令牌数")

    # 缓存配置
    model_cache_dir: str = Field(default="./models", description="模型缓存目录")

    enable_model_cache: bool = Field(default=True, description="是否启用模型缓存")

    cache_ttl: int = Field(default=3600, description="缓存生存时间（秒）")

    # NLP模型配置
    gliner_model_name: str = Field(default="urchade/gliner_base", description="GLiNER模型名称")

    gliner_device: str = Field(default="cpu", description="GLiNER运行设备 (cpu/cuda)")

    # 请求配置
    request_timeout: int = Field(default=60, description="API请求超时时间（秒）")

    max_retries: int = Field(default=3, description="最大重试次数")

    # 支持的模型列表
    supported_chat_models: list[str] = Field(
        default=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "gpt-4o"], description="支持的聊天模型列表"
    )

    class Config:
        """Pydantic配置"""

        env_prefix = "AI_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    @validator("default_temperature")
    def validate_temperature(cls, v):
        """验证温度参数"""
        if not 0 <= v <= 2:
            raise ValueError("温度参数必须在0-2之间")
        return v

    @validator("default_max_tokens")
    def validate_max_tokens(cls, v):
        """验证最大令牌数"""
        if v is not None and v <= 0:
            raise ValueError("最大令牌数必须大于0")
        return v

    @validator("cache_ttl")
    def validate_cache_ttl(cls, v):
        """验证缓存TTL"""
        if v <= 0:
            raise ValueError("缓存TTL必须大于0")
        return v

    @validator("request_timeout")
    def validate_timeout(cls, v):
        """验证请求超时时间"""
        if v <= 0:
            raise ValueError("请求超时时间必须大于0")
        return v

    @validator("max_retries")
    def validate_retries(cls, v):
        """验证重试次数"""
        if v < 0:
            raise ValueError("重试次数不能为负数")
        return v

    def has_openai_key(self) -> bool:
        """检查是否配置了OpenAI API密钥"""
        return bool(self.openai_api_key)

    def get_openai_config(self) -> dict:
        """获取OpenAI客户端配置"""
        config = {
            "base_url": self.openai_base_url,
            "timeout": self.request_timeout,
        }

        if self.openai_api_key:
            config["api_key"] = self.openai_api_key

        if self.openai_organization:
            config["organization"] = self.openai_organization

        return config

    def get_model_params(self, **overrides) -> dict:
        """获取模型参数

        Args:
            **overrides: 覆盖的参数

        Returns:
            模型参数字典
        """
        params = {
            "model": self.default_chat_model,
            "temperature": self.default_temperature,
        }

        if self.default_max_tokens:
            params["max_tokens"] = self.default_max_tokens

        # 应用覆盖参数
        params.update(overrides)
        return params

    def is_model_supported(self, model_name: str) -> bool:
        """检查模型是否支持"""
        return model_name in self.supported_chat_models
