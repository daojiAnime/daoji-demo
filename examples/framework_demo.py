#!/usr/bin/env python3
"""
Daoji Core框架功能演示
展示配置管理、模块注册、数据处理等核心功能
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from daoji_core import (
    BaseDataModel,
    BaseModule,
    ConfigManager,
    DataPipeline,
    DataType,
    ModuleRegistry,
    ProcessingResult,
    TextData,
)
from daoji_core.config import AIConfig, AWSConfig, WebConfig
from daoji_core.data import DataProcessor


def demo_config_management():
    """演示配置管理功能"""
    print("\n🔧 配置管理演示")
    print("=" * 50)

    # 注册各种配置
    ai_config = ConfigManager.register_config("ai", AIConfig)
    aws_config = ConfigManager.register_config("aws", AWSConfig)
    web_config = ConfigManager.register_config("web", WebConfig)

    print(f"AI配置: {ai_config.default_chat_model}")
    print(f"AWS区域: {aws_config.aws_region}")
    print(f"Web端口: {web_config.fastapi_port}")

    # 列出所有配置
    configs = ConfigManager.list_configs()
    print(f"已注册配置: {configs}")

    # 验证配置
    is_valid = ConfigManager.validate_all()
    print(f"配置验证结果: {'✅ 通过' if is_valid else '❌ 失败'}")


class DemoProcessor(DataProcessor):
    """演示数据处理器"""

    def can_process(self, data: BaseDataModel) -> bool:
        return data.type == DataType.TEXT

    def process(self, data: BaseDataModel) -> ProcessingResult:
        if isinstance(data, TextData):
            # 简单的文本处理：转换为大写
            processed_content = data.content.upper()
            result_data = TextData(content=processed_content, source="DemoProcessor")
            return ProcessingResult.success_result(data=result_data, processing_time=0.001, processor_name=self.name)
        return ProcessingResult.error_result(error="不支持的数据类型", processing_time=0.0, processor_name=self.name)


class DemoModule(BaseModule):
    """演示模块"""

    def initialize(self) -> bool:
        self.logger.info("演示模块初始化")
        return True

    def cleanup(self) -> bool:
        self.logger.info("演示模块清理")
        return True

    def get_supported_types(self) -> list[DataType]:
        return [DataType.TEXT]

    def process_data(self, data: BaseDataModel) -> ProcessingResult:
        if isinstance(data, TextData):
            # 添加前缀
            processed_content = f"[DemoModule处理] {data.content}"
            result_data = TextData(content=processed_content, source="DemoModule")
            return ProcessingResult.success_result(data=result_data, processing_time=0.002, processor_name=self.name)
        return ProcessingResult.error_result(error="不支持的数据类型", processing_time=0.0, processor_name=self.name)


def demo_data_processing():
    """演示数据处理功能"""
    print("\n📊 数据处理演示")
    print("=" * 50)

    # 创建测试数据
    text_data = TextData(content="Hello, Daoji Core Framework!", source="demo")
    print(f"原始数据: {text_data.content}")

    # 创建处理管道
    pipeline = DataPipeline("DemoPipeline")
    pipeline.add_processor(DemoProcessor("TextUppercase"))

    # 处理数据
    result = pipeline.process(text_data)
    if result.success:
        print(f"处理结果: {result.data.content}")
        print(f"处理时间: {result.processing_time:.4f}秒")
    else:
        print(f"处理失败: {result.error}")


def demo_module_management():
    """演示模块管理功能"""
    print("\n🔧 模块管理演示")
    print("=" * 50)

    # 获取模块注册器
    registry = ModuleRegistry.get_instance()

    # 创建并注册演示模块
    demo_module = DemoModule("demo_module")
    success = registry.register_module(demo_module)
    print(f"模块注册: {'✅ 成功' if success else '❌ 失败'}")

    # 启动模块
    start_success = registry.start_module("demo_module")
    print(f"模块启动: {'✅ 成功' if start_success else '❌ 失败'}")

    # 列出模块
    modules = registry.list_modules()
    print(f"已注册模块: {modules}")

    # 获取健康状态
    health = registry.get_health_status()
    print(f"模块健康状态: {health}")

    # 测试数据处理
    text_data = TextData(content="测试模块处理", source="demo")
    module = registry.get_module("demo_module")
    if module:
        result = module.process_data(text_data)
        if result.success:
            print(f"模块处理结果: {result.data.content}")

    # 停止并注销模块
    registry.stop_module("demo_module")
    registry.unregister_module("demo_module")


def demo_framework_integration():
    """演示框架集成功能"""
    print("\n🚀 框架集成演示")
    print("=" * 50)

    # 1. 配置管理
    ai_config = ConfigManager.register_config("demo_ai", AIConfig)
    print("配置管理: ✅ AI配置已注册")

    # 2. 模块注册
    registry = ModuleRegistry.get_instance()
    demo_module = DemoModule("integration_demo", ai_config)
    registry.register_module(demo_module)
    registry.start_module("integration_demo")
    print("模块管理: ✅ 演示模块已启动")

    # 3. 数据处理
    pipeline = DataPipeline("IntegrationPipeline")
    pipeline.add_processor(DemoProcessor("Integration"))

    text_data = TextData(content="框架集成测试", source="integration")
    pipeline_result = pipeline.process(text_data)

    if pipeline_result.success:
        # 通过模块进一步处理
        if not pipeline_result.data:
            print("处理结果为空")
            return
        module_result = demo_module.process_data(pipeline_result.data)
        if module_result.success:
            print(f"集成处理结果: {module_result.data.content}")
            print(f"总处理时间: {pipeline_result.processing_time + module_result.processing_time:.4f}秒")

    # 清理
    registry.stop_module("integration_demo")
    registry.unregister_module("integration_demo")
    ConfigManager.clear_all()


def main():
    """主函数"""
    print("🎯 Daoji Core框架功能演示")
    print("=" * 60)

    try:
        # 演示各个功能模块
        demo_config_management()
        demo_data_processing()
        demo_module_management()
        demo_framework_integration()

        print("\n🎉 所有演示完成！")
        print("框架功能验证通过 ✅")

    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
