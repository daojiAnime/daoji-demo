"""
nb_log 基础示例 3: 多日志器管理

这个示例展示了如何使用多个独立的日志器：
- 为不同模块创建独立日志器
- 不同日志器使用不同配置
- 命名空间隔离
"""

from nb_log import get_logger

# 为数据库操作创建专用日志器
db_logger = get_logger(
    "database",
    log_filename="database.log",
    log_level_int=10,  # DEBUG 级别，记录所有操作
)

# 为 API 请求创建专用日志器
api_logger = get_logger(
    "api",
    log_filename="api_requests.log",
    log_level_int=20,  # INFO 级别
)

# 为业务逻辑创建日志器
business_logger = get_logger(
    "business",
    log_filename="business.log",
    log_level_int=30,  # WARNING 级别
)

# 模拟不同模块的日志记录
print("=== 数据库模块 ===")
db_logger.debug("连接数据库")
db_logger.info("执行 SQL 查询")
db_logger.debug("返回 100 行数据")

print("\n=== API 模块 ===")
api_logger.debug("这条 DEBUG 不会显示（日志级别设为 INFO）")
api_logger.info("收到 GET /api/users 请求")
api_logger.info("返回 200 OK")

print("\n=== 业务模块 ===")
business_logger.debug("这条不会显示")
business_logger.info("这条也不会显示")
business_logger.warning("库存不足警告")
business_logger.error("订单处理失败")

# 层级命名空间
parent_logger = get_logger("myapp")
child_logger = get_logger("myapp.module1")
grandchild_logger = get_logger("myapp.module1.submodule")

parent_logger.info("父日志器")
child_logger.info("子日志器")
grandchild_logger.info("孙日志器")

print("\n✅ 多日志器示例完成！")
print("\n💡 提示:")
print("  - 每个日志器可以有独立的日志级别")
print("  - 每个日志器可以输出到不同的文件")
print("  - 使用命名空间可以建立日志器层级关系")
print("\n📁 查看生成的日志文件:")
print("  - database.log (包含 DEBUG 及以上)")
print("  - api_requests.log (包含 INFO 及以上)")
print("  - business.log (包含 WARNING 及以上)")
