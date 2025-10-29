"""
nb_log 基础示例 1: 简单的控制台日志

这个示例展示了 nb_log 最基本的用法：
- 创建日志器
- 输出不同级别的日志
- 彩色控制台输出
"""

from nb_log import get_logger

# 创建一个日志器，默认只输出到控制台
logger = get_logger("simple_demo")

# 输出不同级别的日志
logger.debug("这是 DEBUG 级别的日志 - 绿色")
logger.info("这是 INFO 级别的日志 - 青色")
logger.warning("这是 WARNING 级别的日志 - 黄色")
logger.error("这是 ERROR 级别的日志 - 洋红色")
logger.critical("这是 CRITICAL 级别的日志 - 红色")

# 日志支持格式化
user_id = 12345
action = "login"
logger.info(f"用户 {user_id} 执行了 {action} 操作")

# 使用传统的 % 格式化
logger.info("用户 %s 执行了 %s 操作", user_id, action)

# 使用 extra 参数添加额外信息
logger.info("用户操作", extra={"user_id": user_id, "action": action})

print("\n✅ 基础日志示例完成！")
print("💡 提示: 日志会显示文件名、行号，可以在 IDE 中点击跳转")
