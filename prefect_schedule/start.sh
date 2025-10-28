#!/bin/bash

# Prefect Docker Compose 快速启动脚本

set -e

echo "🚀 Prefect 私有化部署启动脚本"
echo "================================"
echo ""

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "📝 创建 .env 文件..."
    cp env.template .env
    echo "✅ .env 文件已创建，使用默认配置"
    echo "⚠️  生产环境请修改 .env 中的密码！"
    echo ""
fi

# 检查必要的目录
echo "📁 检查目录结构..."
mkdir -p flows data backups ssl
echo "✅ 目录结构已就绪"
echo ""

# 启动服务
echo "🐳 启动 Docker Compose 服务..."
docker-compose up -d

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo ""
echo "📊 检查服务状态..."
docker-compose ps

# 健康检查
echo ""
echo "🏥 健康检查..."
sleep 5

if curl -f http://localhost:4200/api/health > /dev/null 2>&1; then
    echo "✅ Prefect Server 健康检查通过"
else
    echo "⚠️  Prefect Server 可能还在启动中，请稍等片刻"
fi

echo ""
echo "================================"
echo "✅ Prefect 部署完成！"
echo ""
echo "📖 接下来的步骤："
echo "1. 访问 UI: http://localhost:4200"
echo "2. 创建 work pool:"
echo "   docker-compose exec prefect-server prefect work-pool create default --type process"
echo ""
echo "3. 部署 flow:"
echo "   docker-compose exec prefect-server sh -c 'cd /flows && prefect deploy --all'"
echo ""
echo "📚 查看完整文档: cat README.docker.md"
echo "📋 查看日志: docker-compose logs -f"
echo "🛑 停止服务: docker-compose down"
echo "================================"

