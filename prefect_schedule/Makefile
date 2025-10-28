.PHONY: help start stop restart logs ps clean deploy init backup

# 默认目标
help:
	@echo "Prefect Docker Compose 管理命令"
	@echo "================================"
	@echo "make start       - 启动所有服务"
	@echo "make stop        - 停止所有服务"
	@echo "make restart     - 重启所有服务"
	@echo "make logs        - 查看所有服务日志"
	@echo "make ps          - 查看服务状态"
	@echo "make init        - 初始化环境（首次使用）"
	@echo "make deploy      - 部署 flow"
	@echo "make backup      - 备份数据库"
	@echo "make clean       - 清理所有数据（危险操作）"
	@echo ""
	@echo "生产环境命令:"
	@echo "make start-prod  - 启动生产环境"
	@echo "make stop-prod   - 停止生产环境"

# 初始化环境
init:
	@echo "📝 初始化 Prefect 环境..."
	@mkdir -p flows data backups ssl
	@if [ ! -f .env ]; then cp env.template .env; echo "✅ .env 文件已创建"; fi
	@echo "✅ 环境初始化完成"

# 启动开发环境
start: init
	@echo "🚀 启动 Prefect 服务..."
	@docker-compose up -d
	@echo "⏳ 等待服务启动..."
	@sleep 10
	@docker-compose ps
	@echo "✅ 服务已启动"
	@echo "📖 访问 UI: http://localhost:4200"

# 停止服务
stop:
	@echo "🛑 停止 Prefect 服务..."
	@docker-compose down
	@echo "✅ 服务已停止"

# 重启服务
restart:
	@echo "🔄 重启 Prefect 服务..."
	@docker-compose restart
	@echo "✅ 服务已重启"

# 查看日志
logs:
	@docker-compose logs -f

# 查看服务状态
ps:
	@docker-compose ps

# 部署 flow
deploy:
	@echo "🚀 部署 Flow..."
	@docker-compose exec -T prefect-server sh -c "cd /flows && prefect deploy --all"
	@echo "✅ Flow 部署完成"

# 备份数据库
backup:
	@echo "💾 备份数据库..."
	@mkdir -p backups
	@docker-compose exec -T postgres pg_dump -U prefect prefect > backups/prefect_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ 备份完成"

# 清理所有数据
clean:
	@echo "⚠️  警告：这将删除所有数据！"
	@read -p "确定要继续吗？(yes/no): " confirm && [ "$$confirm" = "yes" ] || exit 1
	@docker-compose down -v
	@rm -rf data/* backups/*
	@echo "✅ 清理完成"

# 生产环境启动
start-prod: init
	@echo "🚀 启动生产环境..."
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "✅ 生产环境已启动"

# 生产环境停止
stop-prod:
	@echo "🛑 停止生产环境..."
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
	@echo "✅ 生产环境已停止"

# 扩展 worker
scale-workers:
	@read -p "Worker 数量: " count; \
	docker-compose up -d --scale prefect-worker=$$count
	@echo "✅ Worker 已扩展"

# 进入 server 容器
shell-server:
	@docker-compose exec prefect-server bash

# 进入 worker 容器
shell-worker:
	@docker-compose exec prefect-worker bash

# 健康检查
health:
	@echo "🏥 健康检查..."
	@curl -f http://localhost:4200/api/health && echo "✅ Prefect Server 健康" || echo "❌ Prefect Server 异常"
	@docker-compose exec -T postgres pg_isready -U prefect && echo "✅ PostgreSQL 健康" || echo "❌ PostgreSQL 异常"

# 查看 work pools
list-pools:
	@docker-compose exec -T prefect-server prefect work-pool ls

# 查看 deployments
list-deployments:
	@docker-compose exec -T prefect-server prefect deployment ls

# 查看 flow runs
list-runs:
	@docker-compose exec -T prefect-server prefect flow-run ls --limit 10

