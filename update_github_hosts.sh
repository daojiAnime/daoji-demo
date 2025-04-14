#!/bin/bash

# 定义颜色输出
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m" # 恢复默认颜色

# 检查是否以root权限运行
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}请使用sudo运行此脚本${NC}"
    exit 1
fi

echo -e "${GREEN}开始更新GitHub hosts...${NC}"

# 备份当前hosts文件
cp /etc/hosts /etc/hosts.backup
echo -e "${GREEN}已备份当前hosts文件到 /etc/hosts.backup${NC}"

# 下载GitHub520 hosts
TEMP_FILE=$(mktemp)
if ! curl -s https://raw.hellogithub.com/hosts > "$TEMP_FILE"; then
    echo -e "${RED}下载hosts文件失败${NC}"
    rm -f "$TEMP_FILE"
    exit 1
fi

# 提取GitHub520部分
START_LINE=$(grep -n "# GitHub520 Host Start" "$TEMP_FILE" | cut -d: -f1)
END_LINE=$(grep -n "# GitHub520 Host End" "$TEMP_FILE" | cut -d: -f1)

if [ -z "$START_LINE" ] || [ -z "$END_LINE" ]; then
    echo -e "${RED}未找到GitHub520 hosts信息${NC}"
    rm -f "$TEMP_FILE"
    exit 1
fi

# 从原hosts文件中删除旧的GitHub520部分
if grep -q "# GitHub520 Host Start" /etc/hosts; then
    OLD_START=$(grep -n "# GitHub520 Host Start" /etc/hosts | cut -d: -f1)
    OLD_END=$(grep -n "# GitHub520 Host End" /etc/hosts | cut -d: -f1)
    
    if [ -n "$OLD_START" ] && [ -n "$OLD_END" ]; then
        sed -i.bak -e "${OLD_START},${OLD_END}d" /etc/hosts
        echo -e "${GREEN}已删除旧的GitHub520 hosts条目${NC}"
    fi
fi

# 提取并添加新的GitHub520 hosts到本地hosts文件
sed -n "${START_LINE},${END_LINE}p" "$TEMP_FILE" >> /etc/hosts
echo -e "${GREEN}已添加新的GitHub520 hosts条目${NC}"

# 清理临时文件
rm -f "$TEMP_FILE"

# 刷新DNS缓存 (macOS)
if [ "$(uname)" = "Darwin" ]; then
    dscacheutil -flushcache
    killall -HUP mDNSResponder
    echo -e "${GREEN}已刷新DNS缓存${NC}"
fi

echo -e "${GREEN}GitHub hosts更新完成!${NC}"
echo -e "${GREEN}更新时间: $(date)${NC}" 