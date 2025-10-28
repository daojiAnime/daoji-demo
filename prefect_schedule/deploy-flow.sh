#!/bin/bash

# Prefect Flow 部署脚本

set -e

echo "🚀 部署 Prefect Flow"
echo "================================"
echo ""

# 检查服务是否运行
if ! docker-compose ps | grep -q "prefect-server.*Up"; then
    echo "❌ Prefect Server 未运行，请先执行 ./start.sh"
    exit 1
fi

# 检查 work pool 是否存在
echo "📋 检查 work pool..."
if ! docker-compose exec -T prefect-server prefect work-pool ls 2>/dev/null | grep -q "default"; then
    echo "📝 创建 work pool: default"
    docker-compose exec -T prefect-server prefect work-pool create default --type process
    echo "✅ Work pool 创建成功"
else
    echo "✅ Work pool 已存在"
fi

echo ""
echo "🔨 部署 flow..."

# 复制 prefect.yaml 到 flows 目录（如果需要）
if [ -f prefect.yaml ]; then
    cp prefect.yaml flows/
fi

# 部署 flow
docker-compose exec -T prefect-server sh -c "cd /flows && prefect deploy --all"

echo ""
echo "================================"
echo "✅ Flow 部署完成！"
echo ""
echo "📖 接下来的步骤："
echo "1. 访问 UI 查看部署: http://localhost:4200/deployments"
echo "2. 手动运行 deployment:"
echo "   docker-compose exec prefect-server prefect deployment run 'get-repo-info/github-repo-info-deployment'"
echo ""
echo "3. 查看 flow runs:"
echo "   访问 http://localhost:4200/flow-runs"
echo ""
echo "📋 查看 worker 日志: docker-compose logs -f prefect-worker"
echo "================================"

