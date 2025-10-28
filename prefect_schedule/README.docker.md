# Prefect 私有化部署指南

本文档介绍如何使用 Docker Compose 部署 Prefect。

## 目录结构

```
prefect_schedule/
├── docker-compose.yml          # 开发环境配置
├── docker-compose.prod.yml     # 生产环境配置
├── .env                        # 环境变量配置
├── nginx.conf                  # Nginx 反向代理配置
├── flows/                      # Flow 代码目录
│   └── flow.py
├── data/                       # 数据目录
├── backups/                    # 数据库备份目录
└── ssl/                        # SSL 证书目录（生产环境）
```

## 快速开始

### 1. 准备目录

```bash
# 创建必要的目录
mkdir -p flows data backups ssl

# 复制 flow 文件
cp flow.py flows/
```

### 2. 配置环境变量

编辑 `.env` 文件，修改相关配置：

```bash
# 生产环境请使用强密码
POSTGRES_PASSWORD=your-secure-password

# 生产环境使用实际域名
PREFECT_UI_API_URL=http://localhost:4200/api
```

### 3. 启动服务（开发环境）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看服务状态
docker-compose ps
```

### 4. 初始化配置

```bash
# 进入 server 容器
docker-compose exec prefect-server bash

# 创建 work pool
prefect work-pool create default --type process

# 查看 work pool
prefect work-pool ls

# 退出容器
exit
```

### 5. 部署 Flow

```bash
# 方式 1：使用 prefect.yaml
docker-compose exec prefect-server sh -c "cd /flows && prefect deploy --all"

# 方式 2：使用命令行
docker-compose exec prefect-server sh -c "cd /flows && prefect deploy \
  --name get_repo_info \
  --pool default \
  --cron '0 9 * * *' \
  --timezone 'Asia/Shanghai' \
  flow.py:get_repo_info"
```

### 6. 访问 UI

打开浏览器访问：http://localhost:4200

## 生产环境部署

### 1. 使用生产配置

```bash
# 使用生产环境配置启动
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 2. 配置 SSL 证书

```bash
# 将 SSL 证书放入 ssl 目录
cp your-cert.pem ssl/cert.pem
cp your-key.pem ssl/key.pem

# 修改 nginx.conf，启用 HTTPS 配置
# 取消注释 HTTPS server 块
```

### 3. 修改环境变量

```bash
# .env
POSTGRES_PASSWORD=strong-production-password
PREFECT_UI_API_URL=https://your-domain.com/api
REDIS_PASSWORD=strong-redis-password
```

## 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f [service_name]

# 查看服务状态
docker-compose ps

# 扩展 worker 数量
docker-compose up -d --scale prefect-worker=3
```

### 数据管理

```bash
# 备份数据库
docker-compose exec postgres pg_dump -U prefect prefect > backup.sql

# 恢复数据库
cat backup.sql | docker-compose exec -T postgres psql -U prefect prefect

# 清理旧数据（包括 volumes）
docker-compose down -v
```

### Worker 管理

```bash
# 查看 worker 日志
docker-compose logs -f prefect-worker

# 重启 worker
docker-compose restart prefect-worker

# 进入 worker 容器
docker-compose exec prefect-worker bash
```

### Prefect 操作

```bash
# 进入 server 容器执行 prefect 命令
docker-compose exec prefect-server bash

# 查看 deployments
prefect deployment ls

# 查看 flows
prefect flow ls

# 查看 work pools
prefect work-pool ls

# 手动运行 deployment
prefect deployment run 'get-repo-info/github-repo-info-deployment'

# 查看 flow runs
prefect flow-run ls --limit 10
```

## 监控和维护

### 健康检查

```bash
# 检查服务健康状态
docker-compose ps

# 检查 Prefect Server API
curl http://localhost:4200/api/health

# 检查数据库连接
docker-compose exec postgres pg_isready -U prefect
```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f prefect-server
docker-compose logs -f prefect-worker
docker-compose logs -f postgres

# 查看最近 100 行日志
docker-compose logs --tail=100 prefect-server
```

### 资源监控

```bash
# 查看容器资源使用情况
docker stats

# 查看磁盘使用
docker system df

# 清理未使用的资源
docker system prune -a
```

## 故障排查

### Server 无法启动

```bash
# 检查数据库连接
docker-compose exec prefect-server env | grep PREFECT_API_DATABASE

# 检查 postgres 日志
docker-compose logs postgres

# 重启服务
docker-compose restart prefect-server
```

### Worker 无法连接

```bash
# 检查 API URL 配置
docker-compose exec prefect-worker env | grep PREFECT_API_URL

# 测试网络连接
docker-compose exec prefect-worker curl http://prefect-server:4200/api/health

# 重启 worker
docker-compose restart prefect-worker
```

### Flow 执行失败

```bash
# 查看 worker 日志
docker-compose logs -f prefect-worker

# 查看 flow run 详情（在 UI 中）
# 访问 http://localhost:4200/flow-runs

# 检查 flow 文件是否正确挂载
docker-compose exec prefect-worker ls -la /flows
```

## 性能优化

### 1. Worker 配置

```bash
# 增加 worker 数量处理更多并发任务
docker-compose up -d --scale prefect-worker=5
```

### 2. 数据库优化

修改 `docker-compose.yml`，调整 PostgreSQL 配置：

```yaml
postgres:
  command: >
    postgres
    -c max_connections=200
    -c shared_buffers=256MB
    -c effective_cache_size=1GB
```

### 3. 资源限制

根据实际情况调整 `deploy.resources` 配置。

## 安全建议

1. **修改默认密码**：修改 `.env` 中的所有密码
2. **启用 HTTPS**：生产环境使用 SSL 证书
3. **网络隔离**：使用防火墙限制访问
4. **定期备份**：配置自动备份数据库
5. **监控日志**：定期检查异常日志
6. **更新镜像**：定期更新 Docker 镜像版本

## 备份和恢复

### 手动备份

```bash
# 创建备份目录
mkdir -p backups

# 备份数据库
docker-compose exec postgres pg_dump -U prefect prefect > backups/prefect_$(date +%Y%m%d_%H%M%S).sql

# 备份 flows 目录
tar -czf backups/flows_$(date +%Y%m%d_%H%M%S).tar.gz flows/
```

### 自动备份

生产环境配置中已包含自动备份服务，每天自动备份数据库，保留最近 7 天的备份。

### 恢复数据

```bash
# 恢复数据库
cat backups/prefect_20241028_140000.sql | docker-compose exec -T postgres psql -U prefect prefect

# 恢复 flows
tar -xzf backups/flows_20241028_140000.tar.gz
```

## 升级

### 升级 Prefect 版本

```bash
# 1. 停止服务
docker-compose down

# 2. 备份数据
docker-compose exec postgres pg_dump -U prefect prefect > backup_before_upgrade.sql

# 3. 修改镜像版本（如果需要）
# 编辑 docker-compose.yml，修改 image: prefecthq/prefect:3-latest

# 4. 拉取新镜像
docker-compose pull

# 5. 启动服务
docker-compose up -d

# 6. 检查服务状态
docker-compose ps
docker-compose logs -f
```

## 相关链接

- [Prefect 官方文档](https://docs.prefect.io/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)

## 支持

如有问题，请查看日志或访问 Prefect 社区：
- https://discourse.prefect.io/
- https://github.com/PrefectHQ/prefect

