"""
自定义异常类
提供框架特定的异常类型
"""


class DaojiCoreError(Exception):
    """Daoji Core框架基础异常类"""

    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ConfigError(DaojiCoreError):
    """配置相关异常"""

    def __init__(self, message: str, config_name: str = None, error_code: str = "CONFIG_ERROR"):
        super().__init__(message, error_code)
        self.config_name = config_name

    def __str__(self) -> str:
        if self.config_name:
            return f"配置错误 [{self.config_name}]: {self.message}"
        return f"配置错误: {self.message}"


class ModuleError(DaojiCoreError):
    """模块相关异常"""

    def __init__(self, message: str, module_name: str = None, error_code: str = "MODULE_ERROR"):
        super().__init__(message, error_code)
        self.module_name = module_name

    def __str__(self) -> str:
        if self.module_name:
            return f"模块错误 [{self.module_name}]: {self.message}"
        return f"模块错误: {self.message}"


class DataError(DaojiCoreError):
    """数据处理相关异常"""

    def __init__(self, message: str, data_type: str = None, error_code: str = "DATA_ERROR"):
        super().__init__(message, error_code)
        self.data_type = data_type

    def __str__(self) -> str:
        if self.data_type:
            return f"数据错误 [{self.data_type}]: {self.message}"
        return f"数据错误: {self.message}"


class ValidationError(DaojiCoreError):
    """验证异常"""

    def __init__(self, message: str, field_name: str = None, error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, error_code)
        self.field_name = field_name

    def __str__(self) -> str:
        if self.field_name:
            return f"验证错误 [{self.field_name}]: {self.message}"
        return f"验证错误: {self.message}"


class ProcessingError(DaojiCoreError):
    """处理异常"""

    def __init__(self, message: str, processor_name: str = None, error_code: str = "PROCESSING_ERROR"):
        super().__init__(message, error_code)
        self.processor_name = processor_name

    def __str__(self) -> str:
        if self.processor_name:
            return f"处理错误 [{self.processor_name}]: {self.message}"
        return f"处理错误: {self.message}"
