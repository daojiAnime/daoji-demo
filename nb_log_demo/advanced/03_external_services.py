"""
nb_log 高级示例 3: 外部服务集成

这个示例展示了如何将日志发送到外部服务：
- MongoDB 文档存储
- Elasticsearch 搜索分析
- Kafka 流处理
- DingTalk 团队通知
- Email 邮件告警

注意: 运行前需要确保相应的服务已启动
"""

print("=== nb_log 外部服务集成示例 ===\n")
print("⚠️  注意: 需要相应服务运行才能正常工作\n")

# ========================================
# 1. MongoDB 集成 - 结构化日志存储
# ========================================
print("=== 1. MongoDB 集成 ===")
print("用途: 将日志作为文档存储，便于查询和分析")
print("配置示例:")
print("""
mongo_logger = get_logger(
    'mongo_app',
    mongo_url='mongodb://localhost:27017/logs',
    log_filename='app.log'
)
mongo_logger.info('这条日志会同时写入文件和 MongoDB')
""")
print("MongoDB 文档结构:")
print("""
{
  "time": "2024-01-15 10:30:25",
  "name": "mongo_app",
  "file_path": "/path/to/file.py",
  "func_name": "main",
  "line_no": 42,
  "log_level": "INFO",
  "detail_msg": "这条日志..."
}
""")
print()

# ========================================
# 2. Elasticsearch 集成 - 日志搜索和分析
# ========================================
print("=== 2. Elasticsearch 集成 ===")
print("用途: 全文搜索和日志分析")
print("配置示例:")
print("""
es_logger = get_logger(
    'es_app',
    is_add_elastic_handler=True,
    log_filename='app.log'
)
es_logger.info('这条日志会被索引到 Elasticsearch')
""")
print("特点:")
print("  - 自动批量写入（性能优化）")
print("  - 支持全文搜索")
print("  - 可以与 Kibana 集成进行可视化分析")
print()

# ========================================
# 3. Kafka 集成 - 实时日志流
# ========================================
print("=== 3. Kafka 集成 ===")
print("用途: 日志流处理和实时分析")
print("配置示例:")
print("""
kafka_logger = get_logger(
    'kafka_app',
    is_add_kafka_handler=True,
    log_filename='app.log'
)
kafka_logger.info('这条日志会发送到 Kafka')
""")
print("特点:")
print("  - 支持高吞吐量日志")
print("  - 可以被多个消费者订阅")
print("  - 适合微服务架构")
print()

# ========================================
# 4. DingTalk 集成 - 团队实时通知
# ========================================
print("=== 4. DingTalk 集成 ===")
print("用途: 错误告警实时通知到钉钉")
print("配置示例:")
print("""
dingtalk_logger = get_logger(
    'alert_app',
    ding_talk_token='your_webhook_token_here',
    ding_talk_time_interval=60,  # 60秒内最多发送一次
    log_level_int=40  # 只发送 ERROR 级别及以上
)
dingtalk_logger.error('严重错误：数据库连接失败！')
""")
print("特点:")
print("  - 内置频率控制，避免刷屏")
print("  - 适合生产环境错误告警")
print("  - 支持 @ 特定成员")
print()

# ========================================
# 5. Email 集成 - 邮件告警
# ========================================
print("=== 5. Email 集成 ===")
print("用途: 通过邮件发送严重错误告警")
print("配置示例:")
print("""
from nb_log.log_manager import MailHandlerConfig

mail_config = MailHandlerConfig(
    mailhost=('smtp.gmail.com', 587),
    fromaddr='alert@company.com',
    toaddrs=('admin@company.com', 'team@company.com'),
    subject='生产环境错误告警',
    credentials=('username', 'password'),
    is_use_ssl=True,
    mail_time_interval=3600  # 1小时最多一封
)

email_logger = get_logger(
    'email_alert',
    is_add_mail_handler=True,
    mail_handler_config=mail_config,
    log_level_int=50  # 只发送 CRITICAL 级别
)
email_logger.critical('系统严重错误，需要立即处理！')
""")
print()

# ========================================
# 6. 多服务组合使用
# ========================================
print("=== 6. 多服务组合使用 ===")
print("在生产环境中，通常会组合使用多个服务:")
print("""
prod_logger = get_logger(
    'production',
    # 本地文件
    log_filename='prod.log',
    error_log_filename='prod_errors.log',
    
    # MongoDB 存储
    mongo_url='mongodb://prod-mongo:27017/logs',
    
    # Elasticsearch 搜索
    is_add_elastic_handler=True,
    
    # Kafka 流处理
    is_add_kafka_handler=True,
    
    # 钉钉告警（只发送错误）
    ding_talk_token='webhook_token',
    ding_talk_time_interval=300,  # 5分钟
    
    # 邮件告警（只发送严重错误）
    is_add_mail_handler=True,
    log_level_int=20  # INFO 级别
)

# 不同级别的日志会路由到不同的服务
prod_logger.info('用户登录')  # → 文件、MongoDB、ES、Kafka
prod_logger.error('支付失败')  # → 所有服务 + 钉钉
prod_logger.critical('数据库崩溃')  # → 所有服务 + 钉钉 + 邮件
""")
print()

print("✅ 外部服务集成示例完成！")
print("\n💡 使用建议:")
print("  📁 文件: 所有日志都保存，供离线分析")
print("  💾 MongoDB: 结构化存储，便于查询")
print("  🔍 Elasticsearch: 全文搜索，配合 Kibana 可视化")
print("  🌊 Kafka: 实时流处理，支持多个消费者")
print("  💬 DingTalk: 实时错误告警，团队协作")
print("  📧 Email: 严重错误告警，确保看到")
print("\n⚡ 性能提示:")
print("  - 外部服务使用后台线程，不阻塞主程序")
print("  - 内置队列和批量操作，高效处理")
print("  - 频率控制防止服务过载")
