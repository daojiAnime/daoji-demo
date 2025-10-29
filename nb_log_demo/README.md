# nb_log Demo 示例集合

这个文件夹包含了 nb_log 的各种使用示例和配置参考。

## 文件夹结构

```
nb_log_demo/
├── README.md                    # 本文件
├── nb_log_marimo_demo.py        # 🎯 Marimo 交互式演示（⭐ 推荐！）
├── run_marimo_demo.sh           # Marimo 启动脚本
├── run_all_demos.sh             # 批量运行所有示例
├── basic/                       # 基础使用示例
│   ├── 01_simple_logging.py
│   ├── 02_file_logging.py
│   ├── 03_multiple_loggers.py
│   └── 04_log_levels.py
├── advanced/                    # 高级功能示例
│   ├── 01_enhanced_print.py
│   ├── 02_frequency_control.py
│   ├── 03_external_services.py
│   └── 04_web_framework.py
├── performance/                 # 性能测试
│   ├── benchmark_comparison.py
│   └── performance_report.md
└── config_examples/             # 配置文件示例
    ├── nb_log_config_dev.py
    ├── nb_log_config_prod.py
    └── nb_log_config_explanation.py
```

## 快速开始

### 1. 安装 nb_log

```bash
uv add nb-log
# 或
pip install nb-log
```

### 2. 最简单的例子（30秒上手）

```python
from nb_log import get_logger

# 创建日志器
logger = get_logger('my_app')

# 开始记录日志
logger.info('这是我的第一条日志！')
logger.debug('调试信息')
logger.warning('警告信息')
logger.error('错误信息')
```

### 3. 运行示例

#### 🎯 交互式演示（推荐）⭐

使用 marimo 交互式笔记本，实时调整参数查看效果：

```bash
# 方式 1: 使用启动脚本（推荐）
bash run_marimo_demo.sh

# 方式 2: 直接运行 marimo
marimo edit nb_log_marimo_demo.py

# 方式 3: 只读模式
marimo run nb_log_marimo_demo.py
```

**交互式演示功能**:
- ✅ 实时调整日志级别
- ✅ 可视化文件日志配置
- ✅ 内置性能测试对比
- ✅ 一键运行所有示例

#### 📝 标准示例

```bash
# 运行基础示例
cd basic/
uv run python 01_simple_logging.py

# 运行所有示例
cd ..
bash run_all_demos.sh

# 运行性能测试
cd performance/
uv run python benchmark_comparison.py 2>/dev/null
```

## 参考资源

- **GitHub 仓库**: https://github.com/ydf0509/nb_log
- **项目文档**: 已通过 DeepWiki 获取完整文档
- **性能测试报告**: 见 `performance/performance_report.md`

## 主要特性

### 1. 零配置开箱即用
- 自动生成配置文件
- 彩色控制台输出
- 自动文件切割

### 2. 高级功能
- 增强的 print 函数
- 系统输出重定向
- 频率控制防刷屏
- 多进程安全

### 3. 外部服务集成
- MongoDB
- Elasticsearch
- Kafka
- DingTalk
- Email

### 4. 性能优化
- 跨平台优化（Windows 批量写入，Linux 直接写入）
- 多种文件处理器（7 种类型）
- LRU 缓存优化

## 学习路径

1. **基础入门** → `basic/` 文件夹
   - 了解基本的日志记录
   - 学习文件输出
   - 掌握多日志器使用

2. **高级特性** → `advanced/` 文件夹
   - 增强的 print 功能
   - 频率控制
   - 外部服务集成

3. **性能优化** → `performance/` 文件夹
   - 性能对比测试
   - 不同场景下的最佳实践

4. **配置定制** → `config_examples/` 文件夹
   - 开发环境配置
   - 生产环境配置
   - 配置项详解

## 常见使用场景

### 场景 1: Web 应用日志
```python
# 自动捕获 Flask/FastAPI 请求日志
logger = get_logger('werkzeug', log_filename='requests.log')
```

### 场景 2: 定时任务日志
```python
# 带频率控制的日志，避免刷屏
from nb_log.frequency_control_log import FrequencyControlLog
fc_logger = FrequencyControlLog(logger, interval=60)
```

### 场景 3: 多进程应用
```python
# 自动处理多进程文件写入安全
logger = get_logger('worker', log_filename='worker.log', 
                   log_file_handler_type=1)  # 多进程安全
```

## 性能数据

基于实际测试（5000 次迭代，多次运行平均）：

| 日志库               | 简单日志 | 结构化日志 | 总耗时 | 吞吐量        |
| -------------------- | -------- | ---------- | ------ | ------------- |
| **structlog + rich** | 0.044s   | 0.049s     | 0.093s | 107,500 ops/s |
| **nb_log**           | 0.034s   | 0.037s     | 0.071s | 141,000 ops/s |

**nb_log 比 structlog + rich 快约 24-27%**

## 常见问题

### Q: 如何禁用控制台输出？

```python
logger = get_logger('app', log_filename='app.log', 
                   is_add_stream_handler=False)
```

### Q: 日志文件在哪里？

- **Mac/Linux**: `~/pythonlogs/` 或 `/pythonlogs/`
- **Windows**: `C:/pythonlogs/`

### Q: 如何控制日志文件大小？

```python
# log_file_size: 文件大小（MB）
# 备份数量在 nb_log_config.py 中通过 LOG_FILE_BACKUP_COUNT 配置
logger = get_logger('app', 
                   log_filename='app.log',
                   log_file_size=10,  # 10MB
                   log_file_handler_type=1)
```

### Q: 如何在多进程环境中使用？

```python
# 使用 log_file_handler_type=1（推荐）或 6
logger = get_logger('worker', 
                   log_filename='worker.log',
                   log_file_handler_type=1)  # 多进程安全
```

### Q: 性能测试结果准确吗？

是的！经过多次验证：
- 禁用控制台输出（只测试文件写入）
- 多次运行取平均值
- nb_log 比 structlog 快 **24-34%**（平均约 27%）

## 推荐学习顺序

### 🎯 方式 1: 交互式学习（推荐）

```bash
# 一站式交互式体验所有功能
marimo edit nb_log_marimo_demo.py
```

**特点**: 
- ✅ 可视化界面
- ✅ 实时调整参数
- ✅ 即时查看效果
- ✅ 包含性能测试

### 📝 方式 2: 传统示例学习

```
1. basic/01_simple_logging.py      → 了解基础用法
2. basic/02_file_logging.py        → 学习文件日志
3. basic/04_log_levels.py          → 掌握日志级别
4. advanced/01_enhanced_print.py   → 体验增强功能
5. advanced/02_frequency_control.py → 学习频率控制
6. config_examples/                 → 自定义配置
```

## 相关链接

- **GitHub**: https://github.com/ydf0509/nb_log
- **PyPI**: https://pypi.org/project/nb-log/
- **性能报告**: [performance/performance_report.md](performance/performance_report.md)

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**最后更新**: 2025-10-23  
**项目**: daoji-demo
