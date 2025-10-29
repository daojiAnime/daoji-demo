"""
nb_log 交互式演示 - Marimo 笔记本

这个交互式笔记本展示了 nb_log 的各种功能和用法。

运行方式:
    marimo edit nb_log_marimo_demo.py
    或
    marimo run nb_log_marimo_demo.py
"""

import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import logging
    import tempfile
    import time
    from pathlib import Path

    mo.md(
        """
        # 🎯 nb_log 交互式演示

        这是一个使用 marimo 构建的交互式 nb_log 演示笔记本。
        你可以实时调整参数，查看不同配置下的日志输出效果。

        ---
        """
    )
    return Path, logging, mo, tempfile, time


@app.cell
def _(mo):
    mo.md(
        """
    ## 📦 1. 安装和导入

    nb_log 是一个零配置、开箱即用的 Python 日志库。
    """
    )
    return


@app.cell
def _():
    # 导入 nb_log
    from nb_log import get_logger
    return (get_logger,)


@app.cell
def _(mo):
    mo.md(
        """
    ## 🎨 2. 基础日志记录

    选择日志级别，查看不同级别的日志输出效果：
    """
    )
    return


@app.cell
def _(logging, mo):
    # 日志级别选择器
    log_level_selector = mo.ui.dropdown(
        options={
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        },
        value="DEBUG",
        label="选择日志级别",
    )

    # 日志器名称输入
    logger_name_input = mo.ui.text(
        value="marimo_demo",
        label="日志器名称",
    )

    mo.hstack([log_level_selector, logger_name_input], justify="start")
    return log_level_selector, logger_name_input


@app.cell
def _(get_logger, log_level_selector, logger_name_input, mo):
    # 创建日志器
    demo_logger = get_logger(
        logger_name_input.value,
        log_level_int=log_level_selector.value,
        is_add_stream_handler=True,
    )

    # 输出示例日志
    mo.md(
        f"""
        ### 日志输出示例

        当前配置：
        - **日志器名称**: `{logger_name_input.value}`
        - **日志级别**: `{log_level_selector.selected_key}` ({log_level_selector.value})

        下面是不同级别的日志输出：
        """
    )
    return (demo_logger,)


@app.cell
def _(demo_logger):
    # 输出各级别日志
    demo_logger.debug("🟢 这是 DEBUG 级别的日志")
    demo_logger.info("🔵 这是 INFO 级别的日志")
    demo_logger.warning("🟡 这是 WARNING 级别的日志")
    demo_logger.error("🔴 这是 ERROR 级别的日志")
    demo_logger.critical("🔥 这是 CRITICAL 级别的日志")

    "✅ 日志已输出到控制台（查看终端）"
    return


@app.cell
def _(mo):
    mo.md(
        """
    ---

    ## 📁 3. 文件日志配置

    nb_log 支持自动将日志写入文件，并提供多种轮转策略。
    """
    )
    return


@app.cell
def _(mo):
    # 文件日志配置
    enable_file_log = mo.ui.checkbox(value=True, label="启用文件日志")

    file_size_slider = mo.ui.slider(
        start=1,
        stop=50,
        step=1,
        value=10,
        label="文件大小限制 (MB)",
    )

    handler_type_selector = mo.ui.dropdown(
        options={
            "类型1: ConcurrentRotating (推荐)": 1,
            "类型3: FileHandler": 3,
            "类型6: 日期+大小轮转": 6,
        },
        value="类型1: ConcurrentRotating (推荐)",
        label="文件处理器类型",
    )

    mo.vstack([
        enable_file_log,
        file_size_slider,
        handler_type_selector,
    ])
    return enable_file_log, file_size_slider, handler_type_selector


@app.cell
def _(
    Path,
    enable_file_log,
    file_size_slider,
    get_logger,
    handler_type_selector,
    mo,
    tempfile,
):
    if enable_file_log.value:
        # 创建临时目录用于演示
        temp_dir = Path(tempfile.gettempdir()) / "nb_log_marimo_demo"
        temp_dir.mkdir(exist_ok=True)

        file_logger = get_logger(
            "file_demo",
            log_filename="marimo_demo.log",
            log_path=str(temp_dir),
            log_file_size=file_size_slider.value,
            log_file_handler_type=handler_type_selector.value,
            is_add_stream_handler=False,
        )

        # 写入一些测试日志
        for idx in range(10):
            file_logger.info(f"测试日志消息 #{idx+1}")

        log_file_path = temp_dir / "marimo_demo.log"

        mo.md(
            f"""
            ### 文件日志配置完成

            - **日志文件位置**: `{log_file_path}`
            - **文件大小限制**: {file_size_slider.value} MB
            - **处理器类型**: {handler_type_selector.selected_key}
            - **已写入**: 10 条测试日志

            ✅ 日志文件已创建，你可以在终端使用以下命令查看：
            ```bash
            cat {log_file_path}
            ```
            """
        )
    else:
        mo.md("ℹ️ 文件日志已禁用")
    return


@app.cell
def _(mo):
    mo.md(
        """
    ---

    ## 🚀 4. 性能对比测试

    实时对比 nb_log 和 Python 标准 logging 的性能。
    """
    )
    return


@app.cell
def _(mo):
    # 性能测试配置
    iterations_slider = mo.ui.slider(
        start=100,
        stop=10000,
        step=100,
        value=1000,
        label="测试迭代次数",
    )

    run_benchmark_button = mo.ui.button(
        value=0,
        label="🚀 运行性能测试",
        kind="success",
    )

    mo.hstack([iterations_slider, run_benchmark_button], justify="start")
    return iterations_slider, run_benchmark_button


@app.cell
def _(
    Path,
    get_logger,
    iterations_slider,
    logging,
    mo,
    run_benchmark_button,
    tempfile,
    time,
):
    if run_benchmark_button.value > 0:
        import io
        import sys

        iterations = iterations_slider.value

        # 测试 nb_log
        temp_dir_bench = Path(tempfile.gettempdir()) / "nb_log_benchmark"
        temp_dir_bench.mkdir(exist_ok=True)

        nb_logger = get_logger(
            "benchmark_nb",
            log_filename="benchmark.log",
            log_path=str(temp_dir_bench),
            is_add_stream_handler=False,
        )

        start_time = time.perf_counter()
        for i in range(iterations):
            nb_logger.info(f"Benchmark message {i}")
        nb_time = time.perf_counter() - start_time

        # 测试标准 logging
        std_logger = logging.getLogger("benchmark_std")
        std_logger.setLevel(logging.INFO)
        std_handler = logging.FileHandler(temp_dir_bench / "benchmark_std.log")
        std_logger.addHandler(std_handler)

        start_time = time.perf_counter()
        for i in range(iterations):
            std_logger.info(f"Benchmark message {i}")
        std_time = time.perf_counter() - start_time

        # 计算结果
        speedup = ((std_time - nb_time) / std_time) * 100 if std_time > 0 else 0

        result_md = f"""
        ### 🏁 性能测试结果

        测试迭代次数: **{iterations:,}** 次

        | 日志库 | 耗时 | 吞吐量 |
        |--------|------|--------|
        | **nb_log** | {nb_time:.4f}s | {iterations/nb_time:,.0f} ops/s |
        | **标准 logging** | {std_time:.4f}s | {iterations/std_time:,.0f} ops/s |

        """

        if speedup > 0:
            result_md += f"✨ **nb_log 比标准 logging 快 {speedup:.1f}%**"
        else:
            result_md += f"⚠️ **标准 logging 比 nb_log 快 {-speedup:.1f}%**"

        mo.md(result_md)
    else:
        mo.md("👆 点击按钮开始性能测试")
    return


@app.cell
def _(mo):
    mo.md(
        """
    ---

    ## 🎨 5. 增强的 print 功能

    nb_log 可以增强 Python 的 `print()` 函数，自动添加时间戳和位置信息。
    """
    )
    return


@app.cell
def _(mo):
    enable_print_demo = mo.ui.checkbox(value=False, label="启用 print 增强演示")
    enable_print_demo
    return (enable_print_demo,)


@app.cell
def _(enable_print_demo, get_logger):
    if enable_print_demo.value:
        # 创建 logger 会自动激活 print 增强
        _print_logger = get_logger("print_enhancer")

        # 使用增强的 print
        print("👋 这是增强后的 print 输出")
        print("📍 它会显示文件名和行号")
        print("⏰ 还会显示时间戳")

        "✅ 增强的 print 已激活（查看终端输出）"
    else:
        "ℹ️ 勾选上面的复选框以启用 print 增强"
    return


@app.cell
def _(mo):
    mo.md(
        """
    ---

    ## 📊 6. nb_log 特性总结

    ### ✨ 主要特性

    | 特性 | 说明 |
    |------|------|
    | 🎯 **零配置** | 开箱即用，无需复杂配置 |
    | 🎨 **彩色输出** | 自动为不同级别添加颜色 |
    | 📁 **自动切割** | 内置日志文件轮转功能 |
    | 🚀 **高性能** | 比标准 logging 快 20-30% |
    | 🔧 **多进程安全** | 支持多进程环境 |
    | ✨ **Print 增强** | 增强 print 函数 |
    | 📨 **外部集成** | 支持 DingTalk、Email、Kafka 等 |

    ### 🎓 学习路径

    1. **基础示例** → `nb_log_demo/basic/`
    2. **高级功能** → `nb_log_demo/advanced/`
    3. **配置定制** → `nb_log_demo/config_examples/`
    4. **性能测试** → `nb_log_demo/performance/`

    ### 🔗 相关链接

    - [GitHub](https://github.com/ydf0509/nb_log)
    - [PyPI](https://pypi.org/project/nb-log/)
    - [项目文档](../README.md)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    ---

    ## 💡 使用提示

    ### 常见问题

    **Q: 日志文件在哪里？**
    - Mac/Linux: `~/pythonlogs/`
    - Windows: `C:/pythonlogs/`

    **Q: 如何禁用控制台输出？**
    ```python
    logger = get_logger('app', is_add_stream_handler=False)
    ```

    **Q: 如何在生产环境使用？**
    - 设置合适的日志级别（INFO 或 WARNING）
    - 配置文件轮转策略
    - 使用多进程安全的处理器（类型1或6）

    ---

    **🎉 探索更多功能，请查看 `nb_log_demo/` 目录中的其他示例！**
    """
    )
    return


if __name__ == "__main__":
    app.run()
