#!/bin/bash

# nb_log Marimo 交互式演示启动脚本

echo "🚀 启动 nb_log Marimo 交互式演示..."
echo ""

# 检查 marimo 是否安装
if ! command -v marimo &> /dev/null; then
    echo "❌ marimo 未安装！"
    echo "请运行: uv add marimo 或 pip install marimo"
    exit 1
fi

# 获取当前脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$SCRIPT_DIR"

echo "📂 工作目录: $SCRIPT_DIR"
echo ""
echo "🎯 启动 marimo 交互式笔记本..."
echo ""
echo "使用说明："
echo "  - 在浏览器中打开显示的 URL"
echo "  - 使用交互式控件调整参数"
echo "  - 实时查看 nb_log 的各种功能"
echo ""
echo "按 Ctrl+C 退出"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 启动 marimo（编辑模式）
marimo edit nb_log_marimo_demo.py

# 如果你想以只读模式运行，使用：
# marimo run nb_log_marimo_demo.py

