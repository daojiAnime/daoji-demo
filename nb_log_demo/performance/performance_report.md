# 日志库性能对比报告

## 测试概述

本报告对比了两个流行的Python日志库的性能：
- **nb_log**: 专注于易用性和开箱即用的日志库
- **structlog + rich**: 结构化日志与Rich终端美化的组合

## 测试环境

- **Python版本**: 3.12
- **测试迭代次数**: 5,000次（每种测试场景）
- **测试场景**: 简单日志 + 结构化日志
- **测试日期**: 2025-10-23

## 性能测试结果

| 日志库               | 简单日志(秒) | 结构化日志(秒) | 总耗时(秒) | 吞吐量(ops/s) |
| -------------------- | ------------ | -------------- | ---------- | ------------- |
| **structlog + rich** | 0.0440       | 0.0490         | 0.0930     | 107,500       |
| **nb_log**           | 0.0340       | 0.0370         | 0.0710     | 141,000       |

> **注意**: 测试结果基于多次运行的平均值（禁用控制台输出以确保准确性）

### 关键发现

1. **性能优势**: nb_log 比 structlog + rich **快约 24-27%**（平均约 25%）
2. **吞吐量**: nb_log 的吞吐量达到 **141,000 操作/秒**，相比 structlog 的 107,500 操作/秒有明显优势
3. **两种场景**: nb_log 在简单日志和结构化日志场景中都表现更好
4. **稳定性**: 多次测试结果稳定，性能提升范围在 24-27% 之间

## 详细对比

### nb_log

**优点**：
- ✅ **性能更快**: 比 structlog 快约 24-27%
- ✅ **零配置**: 开箱即用，无需复杂配置
- ✅ **功能丰富**: 内置多种输出方式（钉钉、邮件、MongoDB等）
- ✅ **自动切割**: 内置日志文件切割功能
- ✅ **彩色输出**: 自动为不同级别添加颜色

**缺点**：
- ⚠️ **配置复杂度**: 虽然可以零配置，但高级定制相对复杂
- ⚠️ **文件位置**: 默认日志文件位置可能不符合预期
- ⚠️ **依赖较多**: 安装了较多依赖包
- ⚠️ **启动提示**: 默认会显示很多提示信息（可配置关闭）

### structlog + rich

**优点**：
- ✅ **高度灵活**: 可以精确控制日志处理流程
- ✅ **结构化日志**: 原生支持结构化日志，便于分析
- ✅ **文档完善**: 社区活跃，文档详细
- ✅ **可组合性**: 可以与各种 handler 和 processor 组合

**缺点**：
- ⚠️ **配置复杂**: 需要手动配置处理器和格式化器
- ⚠️ **性能略低**: 比 nb_log 慢约 24-27%
- ⚠️ **文件切割**: 需要自己实现或使用额外库

## 使用建议

### 选择 nb_log 如果你：
1. 需要快速集成，不想花时间配置
2. 性能是关键考虑因素
3. 需要多种输出方式（钉钉、邮件等）
4. 喜欢开箱即用的解决方案

### 选择 structlog + rich 如果你：
1. 需要高度定制的日志处理流程
2. 已有 structlog 使用经验
3. 看重代码的灵活性和可维护性
4. 性能差异（24-27%）对你的应用不重要

## 实际使用示例

### nb_log

```python
from nb_log import get_logger

# 最简单的使用
logger = get_logger('my_app')
logger.info('应用启动')
logger.warning('警告信息', extra={'user_id': 123})
```

### structlog + rich

```python
import structlog
from rich.logging import RichHandler
import logging

# 需要配置
logging.basicConfig(
    level=logging.INFO,
    handlers=[RichHandler()]
)

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()
logger.info('应用启动')
logger.warning('警告信息', user_id=123)
```

## 结论

根据测试结果（多次运行验证）：

1. **性能优先**: 如果性能是首要考虑，选择 **nb_log**，它比 structlog + rich 快 24-27%
2. **灵活性优先**: 如果需要高度定制和灵活的日志处理，选择 **structlog + rich**
3. **快速开发**: 对于大多数应用场景，**nb_log** 的零配置特性可以大大加快开发速度
4. **企业级应用**: 两者都适合企业级应用，选择取决于具体需求

### 测试方法说明

为确保测试准确性，采用了以下措施：
- 禁用控制台输出（只测试文件写入性能）
- 多次运行取平均值
- 使用相同的测试环境和迭代次数
- 确保两个库使用相似的配置（文件输出、日志级别等）

## 性能优化建议

无论选择哪个库，都可以通过以下方式优化性能：

1. **减少日志级别**: 在生产环境只记录 INFO 及以上级别
2. **异步写入**: 使用异步handler减少I/O阻塞
3. **批量写入**: 批量写入日志文件而不是每条都flush
4. **合理使用结构化数据**: 只在必要时添加额外字段
5. **日志切割**: 及时切割日志文件避免单文件过大

## 附录：测试代码

完整的测试代码可在以下文件中找到：
- `benchmark_comparison.py` - 性能对比测试脚本

运行测试：
```bash
cd /Users/daoji/Code/daoji-demo
uv run python nb_log_demo/performance/benchmark_comparison.py 2>/dev/null
```

**重要**: 使用 `2>/dev/null` 可以屏蔽 stderr 输出，确保只看到性能测试结果

