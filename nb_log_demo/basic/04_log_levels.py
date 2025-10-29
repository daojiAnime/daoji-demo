"""
nb_log 基础示例 4: 日志级别控制

这个示例展示了日志级别的使用：
- 理解不同日志级别
- 动态调整日志级别
- 使用日志级别过滤信息
"""

import logging

from nb_log import get_logger

print("=== 日志级别说明 ===")
print("DEBUG(10)    - 详细的调试信息")
print("INFO(20)     - 一般信息")
print("WARNING(30)  - 警告信息")
print("ERROR(40)    - 错误信息")
print("CRITICAL(50) - 严重错误")
print()

# 创建不同级别的日志器
print("=== 1. DEBUG 级别（显示所有日志）===")
logger_debug = get_logger("debug_demo", log_level_int=logging.DEBUG)
logger_debug.debug("✅ DEBUG 可见")
logger_debug.info("✅ INFO 可见")
logger_debug.warning("✅ WARNING 可见")
logger_debug.error("✅ ERROR 可见")

print("\n=== 2. INFO 级别（过滤 DEBUG）===")
logger_info = get_logger("info_demo", log_level_int=logging.INFO)
logger_info.debug("❌ DEBUG 不可见")
logger_info.info("✅ INFO 可见")
logger_info.warning("✅ WARNING 可见")
logger_info.error("✅ ERROR 可见")

print("\n=== 3. WARNING 级别（只显示警告和错误）===")
logger_warning = get_logger("warning_demo", log_level_int=logging.WARNING)
logger_warning.debug("❌ DEBUG 不可见")
logger_warning.info("❌ INFO 不可见")
logger_warning.warning("✅ WARNING 可见")
logger_warning.error("✅ ERROR 可见")

print("\n=== 4. ERROR 级别（只显示错误）===")
logger_error = get_logger("error_demo", log_level_int=logging.ERROR)
logger_error.debug("❌ DEBUG 不可见")
logger_error.info("❌ INFO 不可见")
logger_error.warning("❌ WARNING 不可见")
logger_error.error("✅ ERROR 可见")
logger_error.critical("✅ CRITICAL 可见")

# 实际应用场景
print("\n=== 实际应用场景 ===")

# 开发环境：使用 DEBUG 级别，查看详细信息
dev_logger = get_logger("app", log_level_int=logging.DEBUG)
print("\n开发环境（DEBUG 级别）:")
dev_logger.debug("连接数据库")
dev_logger.debug("执行 SQL: SELECT * FROM users")
dev_logger.info("查询成功，返回 10 条记录")

# 生产环境：使用 INFO 或 WARNING 级别，减少日志量
prod_logger = get_logger("app_prod", log_level_int=logging.INFO)
print("\n生产环境（INFO 级别）:")
prod_logger.debug("这些调试信息在生产环境不会显示")
prod_logger.info("用户登录成功")
prod_logger.warning("API 响应时间超过 1 秒")
prod_logger.error("数据库连接失败")

print("\n✅ 日志级别示例完成！")
print("\n💡 最佳实践:")
print("  - 开发环境使用 DEBUG 或 INFO 级别")
print("  - 生产环境使用 INFO 或 WARNING 级别")
print("  - DEBUG: 详细的调试信息（如 SQL 语句）")
print("  - INFO: 重要的业务操作（如用户登录）")
print("  - WARNING: 需要注意的情况（如性能问题）")
print("  - ERROR: 错误情况（如异常、失败）")
print("  - CRITICAL: 严重错误（如系统崩溃）")
