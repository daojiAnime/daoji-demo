"""
nb_log 配置示例 - 开发环境

这是一个适用于开发环境的 nb_log 配置文件。
将此文件重命名为 nb_log_config.py 并放在项目根目录即可生效。
"""

import logging
from pathlib import Path

# ============================================================================
# 开发环境特点：详细日志、控制台优化、快速调试
# ============================================================================

# 日志级别 - 开发环境使用 DEBUG 级别，查看所有细节
LOG_LEVEL_FILTER = logging.DEBUG

# 控制台输出 - 启用彩色输出和背景色，便于区分
DEFAULUT_USE_COLOR_HANDLER = True  # 启用彩色输出
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = True  # 启用背景色块
DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = False  # 使用 nb_log 的 ColorHandler

# 增强功能 - 开发环境全部启用
AUTO_PATCH_PRINT = True  # 自动增强 print 函数
SHOW_PYCHARM_COLOR_SETINGS = True  # 显示 PyCharm 颜色设置提示
SHOW_NB_LOG_LOGO = True  # 显示 nb_log Logo
SHOW_IMPORT_NB_LOG_CONFIG_PATH = True  # 显示配置文件路径

# 日志文件路径 - 开发环境使用项目目录下的 logs 文件夹
LOG_PATH = Path(__file__).parent / "logs"

# 文件处理器类型 - 开发环境使用简单的日志记录
LOG_FILE_HANDLER_TYPE = 3  # Type 3: 单文件，无轮转（开发环境不需要轮转）

# 文件大小和备份数 - 开发环境设置较小的值
LOG_FILE_SIZE = 50  # 50MB（开发环境文件较小）
LOG_FILE_BACKUP_COUNT = 2  # 只保留 2 个备份

# 自动写入错误日志到单独文件
AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = True

# 格式化模板 - 使用包含详细信息的格式
FORMATTER_KIND = 5  # Template 5: 包含文件路径和行号，适合开发调试

# Print 和系统输出重定向
PRINT_WRTIE_FILE_NAME = Path(__file__).parent.name + ".print"
SYS_STD_FILE_NAME = Path(__file__).parent.name + ".std"

# 外部服务 - 开发环境通常不需要
# MongoDB
MONGO_URL = None  # 开发环境不使用 MongoDB

# Elasticsearch
ELASTIC_HOST = "127.0.0.1"
ELASTIC_PORT = 9200

# Kafka
KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]
ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT = False

# DingTalk - 开发环境不发送通知
DING_TALK_TOKEN = None

# Email - 开发环境不发送邮件
EMAIL_HOST = None
EMAIL_FROMADDR = None
EMAIL_TOADDRS = None
EMAIL_CREDENTIALS = None

# 环境标识
RUN_ENV = "development"

# Windows 批量输出优化（开发环境可以启用以提高性能）
USE_BULK_STDOUT_ON_WINDOWS = True

# 根日志级别
ROOT_LOGGER_LEVEL = logging.INFO
ROOT_LOGGER_FILENAME = "root.log"
ROOT_LOGGER_FILENAME_ERROR = "root.error.log"

# 过滤词（可以过滤掉一些不想看到的日志）
FILTER_WORDS_PRINT = []

print("✅ 加载开发环境配置")
print(f"📁 日志目录: {LOG_PATH}")
print("🔍 日志级别: DEBUG (显示所有日志)")
print("🎨 彩色输出: 已启用")
print("✨ Print 增强: 已启用")
