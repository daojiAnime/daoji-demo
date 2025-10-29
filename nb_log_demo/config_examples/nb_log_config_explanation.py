"""
nb_log 配置文件详解

这个文件详细解释了 nb_log 配置文件中的所有配置项。
仅供参考，不要直接使用此文件作为配置。
"""

import logging

# ============================================================================
# 1. 日志级别配置
# ============================================================================

# LOG_LEVEL_FILTER: 默认日志级别
# 可选值: logging.DEBUG(10), logging.INFO(20), logging.WARNING(30),
#        logging.ERROR(40), logging.CRITICAL(50)
# 开发环境建议: DEBUG 或 INFO
# 生产环境建议: INFO 或 WARNING
LOG_LEVEL_FILTER = logging.INFO

# ROOT_LOGGER_LEVEL: 根日志器的级别
# 影响所有没有明确设置级别的日志器
ROOT_LOGGER_LEVEL = logging.INFO

# ============================================================================
# 2. 控制台输出配置
# ============================================================================

# DEFAULUT_USE_COLOR_HANDLER: 是否使用彩色控制台输出
# True: 使用 nb_log 的 ColorHandler（彩色输出）
# False: 使用标准的 StreamHandler
DEFAULUT_USE_COLOR_HANDLER = True

# DISPLAY_BACKGROUD_COLOR_IN_CONSOLE: 是否显示背景色
# True: 日志级别会有背景色块
# False: 只有前景色（文字颜色）
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = True

# DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER: 是否使用 loguru 风格的控制台
# True: 使用 loguru 的格式化和颜色
# False: 使用 nb_log 的 ColorHandler
DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = False

# WHITE_COLOR_CODE: 白色文字的 ANSI 颜色码
# 37: 兼容旧版 PyCharm
# 97: 适用于新版 PyCharm (2023+)
WHITE_COLOR_CODE = 37

# ============================================================================
# 3. 增强功能配置
# ============================================================================

# AUTO_PATCH_PRINT: 是否自动增强 print 函数
# True: print 会显示时间戳、文件位置等信息
# False: print 保持原始行为
# 建议: 开发环境 True，生产环境 False
AUTO_PATCH_PRINT = True

# SHOW_PYCHARM_COLOR_SETINGS: 是否显示 PyCharm 颜色设置提示
# True: 首次运行时显示颜色配置建议
# False: 不显示
SHOW_PYCHARM_COLOR_SETINGS = False

# SHOW_NB_LOG_LOGO: 是否显示 nb_log 的 ASCII Logo
# True: 首次运行时显示
# False: 不显示
SHOW_NB_LOG_LOGO = True

# SHOW_IMPORT_NB_LOG_CONFIG_PATH: 是否显示配置文件加载路径
# True: 显示正在使用的配置文件路径
# False: 不显示
SHOW_IMPORT_NB_LOG_CONFIG_PATH = True

# ============================================================================
# 4. 文件日志配置
# ============================================================================

# LOG_PATH: 日志文件保存目录
# 可以是绝对路径或相对路径
# 如果目录不存在，会自动创建
LOG_PATH = "/pythonlogs"  # Linux/Mac 默认
# LOG_PATH = Path.home() / 'logs'  # 用户目录下的 logs 文件夹

# LOG_FILE_HANDLER_TYPE: 文件处理器类型
# 1: 多进程安全，按大小轮转（高性能，Windows 优化）
# 2: 多进程安全，按日期轮转
# 3: 单文件，无轮转（最简单）
# 4: WatchedFileHandler（配合 logrotate 使用，仅 Linux）
# 5: 第三方 ConcurrentRotatingFileHandler
# 6: 按日期和大小轮转（推荐，综合方案）
# 7: Loguru 文件处理器
LOG_FILE_HANDLER_TYPE = 6

# LOG_FILE_SIZE: 单个日志文件的最大大小（MB）
# 超过此大小会创建新文件（对支持大小轮转的处理器有效）
LOG_FILE_SIZE = 100

# LOG_FILE_BACKUP_COUNT: 保留的备份文件数量
# 超过此数量的旧文件会被删除
LOG_FILE_BACKUP_COUNT = 10

# DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER
# 是否默认添加多进程安全的文件处理器（即使没有指定 log_filename）
DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER = False

# AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE
# 是否自动将 ERROR 级别以上的日志写入单独的文件
# True: 自动创建 xxx.error.log 文件
# False: 不创建
AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = True

# ROOT_LOGGER_FILENAME: 根日志器的日志文件名
ROOT_LOGGER_FILENAME = "root.log"

# ROOT_LOGGER_FILENAME_ERROR: 根日志器的错误日志文件名
ROOT_LOGGER_FILENAME_ERROR = "root.error.log"

# ============================================================================
# 5. Print 和系统输出重定向
# ============================================================================

# PRINT_WRTIE_FILE_NAME: print 输出重定向的文件名
# None: 不重定向 print 输出到文件
# 字符串: 将 print 输出保存到该文件（每天一个文件）
PRINT_WRTIE_FILE_NAME = "project.print"

# SYS_STD_FILE_NAME: 系统标准输出（stdout/stderr）重定向的文件名
# None: 不重定向
# 字符串: 将所有控制台输出保存到该文件
SYS_STD_FILE_NAME = "project.std"

# USE_BULK_STDOUT_ON_WINDOWS: Windows 系统是否使用批量输出
# True: 使用批量写入，提高性能（Windows I/O 较慢）
# False: 直接写入
USE_BULK_STDOUT_ON_WINDOWS = True

# ============================================================================
# 6. 日志格式化配置
# ============================================================================

# FORMATTER_KIND: 使用的格式化模板编号
# 1: 中文标签格式
# 2: 标准格式，包含函数名
# 3: Traceback 风格，可跳转
# 4: 包含文件路径，可跳转
# 5: 推荐格式，路径:行号 (推荐使用)
# 6: 紧凑格式
# 7: 简短格式，文件名:行号
# 8: JSON 格式（适合机器解析）
# 9: 包含进程/线程 ID + 完整路径
# 10: 包含进程/线程 ID + 文件名
# 11: 包含进程/线程 ID + IP/主机名
FORMATTER_KIND = 5

# FORMATTER_DICT: 格式化模板字典（可以自定义）
# 这是一个字典，键是模板编号，值是 logging.Formatter 对象
# 可以自己添加新的模板
FORMATTER_DICT = {
    # 示例：自定义格式
    12: logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
}

# ============================================================================
# 7. 外部服务集成配置
# ============================================================================

# MongoDB 配置
MONGO_URL = None  # MongoDB 连接字符串
# 示例: 'mongodb://user:password@localhost:27017/logs'

# Elasticsearch 配置
ELASTIC_HOST = "127.0.0.1"
ELASTIC_PORT = 9200

# Kafka 配置
KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]
ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT = False

# DingTalk 配置
DING_TALK_TOKEN = None  # DingTalk webhook token
# 示例: '3dd0eexxxxxadab014bd604XXXXXXXXXXXX'

# Email 配置
EMAIL_HOST = ("smtp.example.com", 587)
EMAIL_FROMADDR = "sender@example.com"
EMAIL_TOADDRS = ("recipient1@example.com", "recipient2@example.com")
EMAIL_CREDENTIALS = ("username", "password")

# ============================================================================
# 8. 其他配置
# ============================================================================

# RUN_ENV: 运行环境标识
# 用于区分不同环境的日志配置
RUN_ENV = "development"  # 或 'production', 'staging', 'test'

# FILTER_WORDS_PRINT: 要过滤的关键词列表
# 包含这些关键词的日志不会被输出
FILTER_WORDS_PRINT = []
# 示例: ['password', 'secret', 'token']

# ============================================================================
# 配置优先级说明
# ============================================================================
"""
nb_log 的配置优先级（从高到低）：

1. 函数参数
   logger = get_logger('name', log_level_int=10)
   
2. 环境变量
   export LOG_PATH=/custom/path
   
3. nb_log_config.py（用户配置文件）
   放在项目根目录，自动加载
   
4. nb_log_config_default.py（默认配置）
   nb_log 包内置的默认值

使用建议：
- 开发环境：使用 nb_log_config.py，设置详细的日志级别
- 生产环境：使用环境变量 + nb_log_config.py，敏感信息用环境变量
- 临时调试：使用函数参数，快速改变某个日志器的行为
"""

# ============================================================================
# 完整的配置示例
# ============================================================================

print(__doc__)
