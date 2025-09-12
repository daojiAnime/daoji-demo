"""
Web服务配置
提供Web相关服务的配置管理
"""

from pydantic import Field, validator

from .base import BaseConfig


class WebConfig(BaseConfig):
    """Web服务配置

    管理Web相关服务的配置：
    - FastAPI配置
    - Streamlit配置
    - CORS设置
    - 静态文件配置
    """

    # FastAPI配置
    fastapi_host: str = Field(default="127.0.0.1", description="FastAPI服务主机")

    fastapi_port: int = Field(default=8000, description="FastAPI服务端口")

    fastapi_reload: bool = Field(default=True, description="是否启用自动重载（开发模式）")

    fastapi_workers: int = Field(default=1, description="FastAPI工作进程数")

    # Streamlit配置
    streamlit_host: str = Field(default="127.0.0.1", description="Streamlit服务主机")

    streamlit_port: int = Field(default=8501, description="Streamlit服务端口")

    streamlit_theme: str = Field(default="light", description="Streamlit主题 (light/dark)")

    # API配置
    api_prefix: str = Field(default="/api/v1", description="API路径前缀")

    api_title: str = Field(default="Daoji Demo API", description="API标题")

    api_description: str = Field(default="Daoji Demo项目的统一API接口", description="API描述")

    api_version: str = Field(default="1.0.0", description="API版本")

    # CORS配置
    cors_origins: list[str] = Field(default=["*"], description="允许的CORS源")

    cors_methods: list[str] = Field(default=["GET", "POST", "PUT", "DELETE"], description="允许的HTTP方法")

    cors_headers: list[str] = Field(default=["*"], description="允许的请求头")

    # 静态文件配置
    static_dir: str = Field(default="static", description="静态文件目录")

    upload_dir: str = Field(default="uploads", description="文件上传目录")

    max_upload_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        description="最大上传文件大小（字节）",
    )

    # 安全配置
    secret_key: str | None = Field(None, description="应用密钥")

    access_token_expire_minutes: int = Field(default=30, description="访问令牌过期时间（分钟）")

    # 中间件配置
    enable_gzip: bool = Field(default=True, description="是否启用Gzip压缩")

    enable_rate_limit: bool = Field(default=False, description="是否启用速率限制")

    rate_limit_requests: int = Field(default=100, description="速率限制请求数")

    rate_limit_window: int = Field(default=60, description="速率限制时间窗口（秒）")

    class Config:
        """Pydantic配置"""

        env_prefix = "WEB_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    @validator("fastapi_port", "streamlit_port")
    def validate_port(cls, v):
        """验证端口号"""
        if not 1 <= v <= 65535:
            raise ValueError("端口号必须在1-65535之间")
        return v

    @validator("fastapi_workers")
    def validate_workers(cls, v):
        """验证工作进程数"""
        if v <= 0:
            raise ValueError("工作进程数必须大于0")
        return v

    @validator("streamlit_theme")
    def validate_theme(cls, v):
        """验证Streamlit主题"""
        if v not in ["light", "dark"]:
            raise ValueError("主题必须是light或dark")
        return v

    @validator("max_upload_size")
    def validate_upload_size(cls, v):
        """验证上传文件大小"""
        if v <= 0:
            raise ValueError("最大上传文件大小必须大于0")
        return v

    @validator("access_token_expire_minutes")
    def validate_token_expire(cls, v):
        """验证令牌过期时间"""
        if v <= 0:
            raise ValueError("令牌过期时间必须大于0")
        return v

    @validator("rate_limit_requests")
    def validate_rate_limit_requests(cls, v):
        """验证速率限制请求数"""
        if v <= 0:
            raise ValueError("速率限制请求数必须大于0")
        return v

    @validator("rate_limit_window")
    def validate_rate_limit_window(cls, v):
        """验证速率限制时间窗口"""
        if v <= 0:
            raise ValueError("速率限制时间窗口必须大于0")
        return v

    def get_fastapi_url(self) -> str:
        """获取FastAPI服务URL"""
        return f"http://{self.fastapi_host}:{self.fastapi_port}"

    def get_streamlit_url(self) -> str:
        """获取Streamlit服务URL"""
        return f"http://{self.streamlit_host}:{self.streamlit_port}"

    def get_cors_config(self) -> dict:
        """获取CORS配置"""
        return {
            "allow_origins": self.cors_origins,
            "allow_methods": self.cors_methods,
            "allow_headers": self.cors_headers,
            "allow_credentials": True,
        }

    def get_uvicorn_config(self) -> dict:
        """获取Uvicorn配置"""
        config = {
            "host": self.fastapi_host,
            "port": self.fastapi_port,
            "reload": self.fastapi_reload and self.is_development(),
        }

        if not self.is_development():
            config["workers"] = self.fastapi_workers

        return config
