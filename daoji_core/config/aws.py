"""
AWS服务配置
提供AWS相关服务的配置管理
"""

from pydantic import Field, validator

from .base import BaseConfig


class AWSConfig(BaseConfig):
    """AWS服务配置

    管理AWS相关服务的配置：
    - 访问凭证
    - 区域设置
    - 服务端点
    - Lightsail特定配置
    """

    # AWS凭证
    aws_access_key_id: str | None = Field(None, description="AWS访问密钥ID")

    aws_secret_access_key: str | None = Field(None, description="AWS秘密访问密钥")

    aws_session_token: str | None = Field(None, description="AWS会话令牌（临时凭证）")

    # 区域和端点
    aws_region: str = Field(default="us-east-1", description="AWS区域")

    aws_endpoint_url: str | None = Field(None, description="自定义AWS端点URL（用于本地测试）")

    # Lightsail特定配置
    lightsail_instance_name: str | None = Field(None, description="Lightsail实例名称")

    lightsail_region: str | None = Field(None, description="Lightsail区域（如果与AWS区域不同）")

    # 连接配置
    connect_timeout: int = Field(default=60, description="连接超时时间（秒）")

    read_timeout: int = Field(default=60, description="读取超时时间（秒）")

    max_retries: int = Field(default=3, description="最大重试次数")

    class Config:
        """Pydantic配置"""

        env_prefix = "AWS_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    @validator("aws_region")
    def validate_region(cls, v):
        """验证AWS区域格式"""
        if v and not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("AWS区域格式无效")
        return v

    @validator("connect_timeout", "read_timeout")
    def validate_timeout(cls, v):
        """验证超时时间"""
        if v <= 0:
            raise ValueError("超时时间必须大于0")
        return v

    @validator("max_retries")
    def validate_retries(cls, v):
        """验证重试次数"""
        if v < 0:
            raise ValueError("重试次数不能为负数")
        return v

    def get_lightsail_region(self) -> str:
        """获取Lightsail区域，如果未设置则使用AWS区域"""
        return self.lightsail_region or self.aws_region

    def has_credentials(self) -> bool:
        """检查是否配置了AWS凭证"""
        return bool(self.aws_access_key_id and self.aws_secret_access_key)

    def get_boto3_config(self) -> dict:
        """获取boto3客户端配置"""
        config = {
            "region_name": self.aws_region,
        }

        if self.aws_endpoint_url:
            config["endpoint_url"] = self.aws_endpoint_url

        return config

    def get_credentials_dict(self) -> dict:
        """获取凭证字典"""
        credentials = {}

        if self.aws_access_key_id:
            credentials["aws_access_key_id"] = self.aws_access_key_id

        if self.aws_secret_access_key:
            credentials["aws_secret_access_key"] = self.aws_secret_access_key

        if self.aws_session_token:
            credentials["aws_session_token"] = self.aws_session_token

        return credentials
