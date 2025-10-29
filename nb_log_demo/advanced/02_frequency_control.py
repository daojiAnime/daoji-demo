"""
nb_log 高级示例 2: 频率控制（防刷屏）

这个示例展示了如何使用频率控制防止日志刷屏：
- 在循环中控制日志频率
- 避免重复日志淹没有用信息
- 基于位置的频率控制
"""

import time

from nb_log import get_logger
from nb_log.frequency_control_log import FrequencyControlLog

logger = get_logger("frequency_demo")

print("=== 1. 无频率控制的日志（会刷屏）===\n")

# 模拟一个循环任务，没有频率控制
print("运行 10 秒，观察日志刷屏...")
start_time = time.time()
count = 0
while time.time() - start_time < 3:  # 运行 3 秒
    logger.info(f"任务执行中... 第 {count} 次")
    count += 1
    time.sleep(0.1)

print(f"\n❌ 问题: 产生了 {count} 条日志，刷屏严重！\n")
time.sleep(1)

print("=== 2. 使用频率控制（5秒间隔）===\n")

# 使用频率控制包装器
fc_logger = FrequencyControlLog(logger, interval=5)

print("运行 10 秒，日志会被限制在每 5 秒一次...")
start_time = time.time()
count = 0
while time.time() - start_time < 10:
    # 同样的代码，但日志会被限制
    fc_logger.info(f"任务执行中... 第 {count} 次")
    count += 1
    time.sleep(0.1)

print(f"\n✅ 效果: 虽然执行了 {count} 次，但只输出了 2-3 条日志！\n")
time.sleep(1)

print("=== 3. 不同位置的频率控制互不影响 ===\n")

fc_logger = FrequencyControlLog(logger, interval=3)

print("两个不同位置的日志会独立计算频率...")
for i in range(10):
    # 位置 1: 这里的日志 3 秒一次
    fc_logger.info("位置 1 的日志")

    time.sleep(0.5)

    # 位置 2: 这里的日志也是 3 秒一次，但独立计算
    fc_logger.warning("位置 2 的日志")

    time.sleep(0.5)

print("\n✅ 两个位置的日志独立控制频率\n")
time.sleep(1)

print("=== 4. 实际应用场景 ===\n")

# 场景 1: 监控循环任务
print("场景 1: 监控循环任务（避免日志爆炸）")
monitor_logger = FrequencyControlLog(logger, interval=10)

for i in range(20):
    # 每秒执行一次，但日志 10 秒才记录一次
    monitor_logger.info("监控任务运行正常")
    time.sleep(0.5)

print()

# 场景 2: API 请求日志
print("场景 2: API 请求日志（相同接口限制频率）")
api_logger = FrequencyControlLog(logger, interval=5)

# 模拟多次 API 调用
for i in range(10):
    api_logger.info("GET /api/users - 200 OK")
    time.sleep(0.3)

print("\n=== 5. 不同日志级别都支持频率控制 ===\n")

fc_logger = FrequencyControlLog(logger, interval=3)

# 所有日志级别都支持
for i in range(15):
    fc_logger.debug("Debug 消息")
    fc_logger.info("Info 消息")
    fc_logger.warning("Warning 消息")
    fc_logger.error("Error 消息")
    time.sleep(0.3)

print("\n✅ 频率控制示例完成！")
print("\n💡 使用建议:")
print("  - 监控任务: 使用 60 秒或更长的间隔")
print("  - 循环处理: 使用 10-30 秒间隔")
print("  - API 日志: 使用 5-10 秒间隔")
print("  - 频繁的调试日志: 使用频率控制避免刷屏")
print("\n📌 注意:")
print("  - 频率控制基于代码位置（文件+行号）")
print("  - 相同位置的日志共享频率限制")
print("  - 不同位置的日志独立计算")
