#!/bin/bash

# nb_log Demo 运行脚本
# 这个脚本会依次运行所有示例程序

set -e  # 遇到错误立即退出

echo "════════════════════════════════════════════════════════════════"
echo "  🚀 nb_log 示例程序运行器"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 检查 nb_log 是否已安装
if ! python -c "import nb_log" 2>/dev/null; then
    echo "❌ nb_log 未安装！"
    echo "请先安装: uv add nb-log"
    exit 1
fi

echo "✅ nb_log 已安装"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 函数：运行示例并暂停
run_demo() {
    local file=$1
    local title=$2
    
    echo "════════════════════════════════════════════════════════════════"
    echo "  📂 $title"
    echo "  📝 文件: $file"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    
    python "$file"
    
    echo ""
    echo "按 Enter 继续下一个示例..."
    read -r
    echo ""
}

# 基础示例
echo "┌──────────────────────────────────────────────────────────────┐"
echo "│  📚 基础示例                                                 │"
echo "└──────────────────────────────────────────────────────────────┘"
echo ""

run_demo "basic/01_simple_logging.py" "01. 简单控制台日志"
run_demo "basic/02_file_logging.py" "02. 文件日志输出"
run_demo "basic/03_multiple_loggers.py" "03. 多日志器管理"
run_demo "basic/04_log_levels.py" "04. 日志级别控制"

# 高级示例
echo "┌──────────────────────────────────────────────────────────────┐"
echo "│  🔥 高级示例                                                 │"
echo "└──────────────────────────────────────────────────────────────┘"
echo ""

run_demo "advanced/01_enhanced_print.py" "01. 增强的 print 函数"
run_demo "advanced/02_frequency_control.py" "02. 频率控制（防刷屏）"

echo "════════════════════════════════════════════════════════════════"
echo "  ℹ️  跳过高级示例 03 和 04（需要外部服务支持）"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 性能测试
echo "┌──────────────────────────────────────────────────────────────┐"
echo "│  ⚡ 性能测试                                                 │"
echo "└──────────────────────────────────────────────────────────────┘"
echo ""

echo "是否运行性能测试？(可能需要 1-2 分钟) [y/N]"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    run_demo "performance/benchmark_comparison.py" "性能对比测试"
else
    echo "跳过性能测试"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ 所有示例运行完成！"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "💡 提示:"
echo "  - 查看生成的日志文件: ~/pythonlogs/ (Linux/Mac)"
echo "  - 阅读配置示例: config_examples/"
echo "  - 查看性能报告: performance/performance_report.md"
echo ""
echo "📚 更多信息:"
echo "  - GitHub: https://github.com/ydf0509/nb_log"
echo "  - 本地文档: README.md"
echo ""

