# Daoji Core Framework

统一的模块化架构核心框架，为Daoji Demo项目提供标准化的配置管理、数据处理和模块管理功能。

## 特性

- 🔧 **类型安全的配置管理** - 基于Pydantic BaseSettings的配置系统
- 📊 **统一的数据模型** - 类型安全的数据结构和处理管道
- 🔌 **模块化架构** - 标准化的模块接口和注册管理
- 🛠️ **完整的工具支持** - 日志、异常处理等工具模块
- 🐍 **Python 3.12+兼容** - 现代Python特性支持

## 快速开始

### 安装依赖

```bash
# 确保已安装pydantic-settings
uv add pydantic-settings
```

### 基本使用

```python
from daoji_core import (
    ConfigManager, BaseConfig, 
    BaseModule, ModuleRegistry,
    BaseDataModel, DataPipeline, DataType, TextData
)

# 1. 配置管理
from daoji_core.config import AIConfig
ai_config = ConfigManager.register_config("ai", AIConfig)

# 2. 数据处理
text_data = TextData(content="Hello World", source="demo")
pipeline = DataPipeline("MyPipeline")
result = pipeline.process(text_data)

# 3. 模块管理
registry = ModuleRegistry.get_instance()
# 注册和管理自定义模块...
```

## 架构概览

```
daoji_core/
├── __init__.py          # 框架入口
├── config/              # 配置管理模块
│   ├── base.py         # 基础配置类
│   ├── manager.py      # 配置管理器
│   ├── ai.py           # AI服务配置
│   ├── aws.py          # AWS服务配置
│   └── web.py          # Web服务配置
├── data/               # 数据流模块
│   ├── models.py       # 数据模型定义
│   ├── pipeline.py     # 数据处理管道
│   └── interface.py    # 数据流接口
├── modules/            # 模块管理模块
│   ├── base.py         # 基础模块类
│   └── registry.py     # 模块注册器
└── utils/              # 工具模块
    ├── logging.py      # 日志工具
    └── exceptions.py   # 自定义异常
```

## 核心组件

### 配置管理

```python
from daoji_core.config import BaseConfig, ConfigManager

class MyConfig(BaseConfig):
    api_key: str = Field(description="API密钥")
    timeout: int = Field(default=30, description="超时时间")

# 注册配置
config = ConfigManager.register_config("my_service", MyConfig)
```

### 数据处理

```python
from daoji_core.data import DataProcessor, ProcessingResult

class MyProcessor(DataProcessor):
    def can_process(self, data):
        return data.type == DataType.TEXT
    
    def process(self, data):
        # 处理逻辑
        return ProcessingResult.success_result(data, 0.001, self.name)
```

### 模块开发

```python
from daoji_core.modules import BaseModule

class MyModule(BaseModule):
    def initialize(self):
        return True
    
    def cleanup(self):
        return True
    
    def get_supported_types(self):
        return [DataType.TEXT]
    
    def process_data(self, data):
        # 模块处理逻辑
        pass
```

## 示例

查看 `examples/framework_demo.py` 获取完整的使用示例。

```bash
python examples/framework_demo.py
```

## 设计决策

### 架构选择：模块化单体架构
- **优势**: 开发效率高，维护成本低，适合实验性项目
- **特点**: 统一部署，模块间松耦合，标准化接口

### 配置管理：基于Pydantic的配置类
- **优势**: 类型安全，自动验证，生态集成好
- **特点**: 环境变量支持，分层配置，热重载

### 数据流：数据模型+管道处理
- **优势**: 类型安全，处理灵活，易于扩展
- **特点**: 链式处理，错误处理，性能监控

## 版本

当前版本: 0.1.0

## 许可证

MIT License 