"""
nb_log 配置示例 - 生产环境

这是一个适用于生产环境的 nb_log 配置文件。
将此文件重命名为 nb_log_config.py 并放在项目根目录即可生效。

生产环境特点：
- 日志级别较高（INFO），减少日志量
- 启用日志轮转，避免单个文件过大
- 集成外部服务（MongoDB、Elasticsearch、DingTalk）
- 关闭开发辅助功能
"""

import logging
import os

# ============================================================================
# 生产环境核心配置
# ============================================================================

# 日志级别 - 生产环境使用 INFO 级别，减少日志量
LOG_LEVEL_FILTER = logging.INFO

# 控制台输出 - 生产环境可以禁用背景色，减少输出
DEFAULUT_USE_COLOR_HANDLER = True  # 保留彩色，便于查看
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False  # 关闭背景色，减少视觉干扰
DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = False

# 开发辅助功能 - 生产环境全部关闭
AUTO_PATCH_PRINT = False  # 关闭 print 增强，避免性能影响
SHOW_PYCHARM_COLOR_SETINGS = False  # 不显示提示信息
SHOW_NB_LOG_LOGO = False  # 不显示 Logo
SHOW_IMPORT_NB_LOG_CONFIG_PATH = False  # 不显示配置路径

# 日志文件路径 - 生产环境使用标准日志目录
if os.name == "posix":  # Linux/Mac
    LOG_PATH = "/var/log/myapp"  # 标准日志目录
else:  # Windows
    LOG_PATH = "C:/logs/myapp"

# 文件处理器类型 - 生产环境使用多进程安全的处理器
LOG_FILE_HANDLER_TYPE = 6  # Type 6: 按日期和大小轮转，最推荐

# 文件大小和备份数 - 生产环境设置较大的值
LOG_FILE_SIZE = 100  # 100MB
LOG_FILE_BACKUP_COUNT = 10  # 保留 10 个备份文件

# 自动写入错误日志到单独文件 - 生产环境必须启用
AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = True

# 格式化模板 - 生产环境使用 JSON 格式，便于机器解析
FORMATTER_KIND = 8  # Template 8: JSON 格式，便于日志收集和分析

# Print 和系统输出重定向 - 生产环境建议禁用或重定向到文件
PRINT_WRTIE_FILE_NAME = None  # 不记录 print 输出
SYS_STD_FILE_NAME = None  # 不重定向系统输出

# ============================================================================
# 外部服务集成 - 生产环境配置
# ============================================================================

# MongoDB - 日志持久化存储
MONGO_URL = os.getenv("MONGO_LOG_URL", "mongodb://log-mongo:27017/logs")

# Elasticsearch - 日志搜索和分析
ELASTIC_HOST = os.getenv("ELASTIC_HOST", "elasticsearch")
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", "9200"))

# Kafka - 实时日志流
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKERS", "kafka:9092").split(",")
ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT = False

# DingTalk - 错误告警（从环境变量读取）
DING_TALK_TOKEN = os.getenv("DINGTALK_WEBHOOK_TOKEN")

# Email - 严重错误告警（从环境变量读取）
EMAIL_HOST = (os.getenv("SMTP_HOST", "smtp.company.com"), int(os.getenv("SMTP_PORT", "587")))
EMAIL_FROMADDR = os.getenv("SMTP_FROM", "alerts@company.com")
EMAIL_TOADDRS = tuple(os.getenv("ALERT_EMAILS", "admin@company.com").split(","))
EMAIL_CREDENTIALS = (os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))

# 环境标识
RUN_ENV = os.getenv("ENVIRONMENT", "production")

# Windows 批量输出优化
USE_BULK_STDOUT_ON_WINDOWS = True

# 根日志配置
ROOT_LOGGER_LEVEL = logging.WARNING  # 生产环境只记录警告及以上
ROOT_LOGGER_FILENAME = "root.log"
ROOT_LOGGER_FILENAME_ERROR = "root.error.log"

# 过滤词 - 可以过滤掉一些敏感信息或噪音日志
FILTER_WORDS_PRINT = []

# ============================================================================
# 安全和性能优化
# ============================================================================

# 日志敏感信息脱敏（示例）
# 在实际使用中，可以通过自定义 Filter 实现
# class SensitiveDataFilter(logging.Filter):
#     def filter(self, record):
#         # 脱敏处理
#         record.msg = record.msg.replace('password=xxx', 'password=***')
#         return True

# 日志采样（高流量场景）
# 可以实现日志采样，只记录一部分日志
# LOG_SAMPLING_RATE = 0.1  # 记录 10% 的日志

print("✅ 加载生产环境配置")
print(f"📁 日志目录: {LOG_PATH}")
print("🔍 日志级别: INFO")
print("📊 外部服务:")
print(f"  - MongoDB: {'启用' if MONGO_URL else '禁用'}")
print("  - Elasticsearch: 启用")
print("  - Kafka: 启用")
print(f"  - DingTalk: {'启用' if DING_TALK_TOKEN else '禁用'}")
print(f"  - Email: {'启用' if EMAIL_CREDENTIALS[0] else '禁用'}")
