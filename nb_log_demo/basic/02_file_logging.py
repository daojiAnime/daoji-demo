"""
nb_log 基础示例 2: 文件日志

这个示例展示了如何将日志输出到文件：
- 同时输出到控制台和文件
- 自动创建日志目录
- 日志文件轮转
"""

from nb_log import get_logger

# 创建一个输出到文件的日志器
# log_filename: 指定日志文件名
logger = get_logger("file_demo", log_filename="demo_app.log")

logger.info("这条日志会同时输出到控制台和文件")
logger.debug("调试信息也会被记录")
logger.warning("警告信息")

# 带有错误级别的单独文件
logger_with_error = get_logger("app_with_error", log_filename="app.log", error_log_filename="app_errors.log")

logger_with_error.info("这是普通日志，只写入 app.log")
logger_with_error.error("这是错误日志，会同时写入 app.log 和 app_errors.log")

# 自定义日志文件大小
# 注意：备份文件数量由配置文件中的 LOG_FILE_BACKUP_COUNT 控制
logger_custom = get_logger(
    "custom_rotation",
    log_filename="custom.log",
    log_file_size=10,  # 10MB（当文件达到10MB时会自动轮转）
    log_file_handler_type=1,  # 使用多进程安全的文件处理器
)

for i in range(10):
    logger_custom.info(f"这是第 {i+1} 条日志消息")

print("\n✅ 文件日志示例完成！")
print("📁 日志文件位置:")
print("  - Linux/Mac: ~/pythonlogs/")
print("  - Windows: C:/pythonlogs/")
print("\n💡 提示:")
print("  - 日志文件会自动轮转（按大小或时间）")
print("  - 默认保留最近 10 个备份文件")
print("  - 备份数量可在 nb_log_config.py 中通过 LOG_FILE_BACKUP_COUNT 配置")
