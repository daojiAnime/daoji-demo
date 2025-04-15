#!/bin/bash

# 设置日志目录
LOG_DIR="/root/daoji-demo/logs"
mkdir -p $LOG_DIR

# 记录开始时间
echo "====================================" >> $LOG_DIR/traffic.log
echo "开始运行时间: $(date)" >> $LOG_DIR/traffic.log

# 激活虚拟环境
cd "$(dirname "$0")"
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
  aws-traffic "$@"
else
  echo "错误: 找不到虚拟环境，将尝试使用全局命令" >> $LOG_DIR/traffic.log
  aws-traffic "$@" || echo "错误: 命令执行失败!" >> $LOG_DIR/traffic.log
fi

# 记录结束时间
echo "结束运行时间: $(date)" >> $LOG_DIR/traffic.log
echo "====================================" >> $LOG_DIR/traffic.log 